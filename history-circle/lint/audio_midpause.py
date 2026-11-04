"""문장 중간 쉼 검사.

사용: python3 audio_midpause.py scene01.wav [--words scene01.words.json]
-40dB 0.1초 이상 무음을 찾는다.
 - words.json(단어 시각, faster-whisper 형식 [{"word":..,"start":..,"end":..}])이 있으면:
   앞 단어가 쉼표·마침표로 끝나지 않는 쉼 = 실패, 문장부호 뒤 쉼이 punct_max_pause_s 초과 = 실패.
 - 없으면: punct_max_pause_s 초과 쉼만 실패, 나머지는 경고(문장부호 위치를 모르므로).
근거: history-battle-shorts:134 (11/3)
"""
import argparse

import numpy as np

from common import emit, load_audio, load_json, result, rms_db_frames, segments, th

CHECK = "audio_midpause"


def _pauses(x):
    db, fs = rms_db_frames(x, frame_s=0.01)
    on = db > th(CHECK, "silence_db")
    speech = segments(on, fs)
    if len(speech) < 2:
        return []
    first, last = speech[0][0], speech[-1][1]
    sil = segments(~on, fs)
    mn = th(CHECK, "min_pause_s")
    return [(s, e) for s, e in sil if s >= first and e <= last and (e - s) >= mn - 1e-9]


def _word_before(words, t):
    best = None
    for w in words:
        if w["end"] <= t + 0.08:
            if best is None or w["end"] > best["end"]:
                best = w
    return best


def check(path, words_path=None):
    punct = th(CHECK, "punctuation")
    pmax = th(CHECK, "punct_max_pause_s")
    pauses = _pauses(load_audio(path))
    words = None
    if words_path:
        data = load_json(words_path)
        words = data["words"] if isinstance(data, dict) else data
    viol, warn = [], []
    for s, e in pauses:
        d = round(e - s, 2)
        item = {"start_s": round(s, 2), "len_s": d}
        if words is not None:
            w = _word_before(words, s)
            txt = (w or {}).get("word", "").strip()
            item["word_before"] = txt
            is_punct = bool(txt) and txt[-1] in punct
            if not is_punct:
                viol.append(dict(item, what="문장부호 없는 자리의 쉼"))
            elif d > pmax:
                viol.append(dict(item, what="문장부호 뒤 쉼이 너무 김"))
        else:
            if d > pmax:
                viol.append(dict(item, what="쉼이 너무 김(단어 시각 없음)"))
            else:
                warn.append(dict(item, what="미확인 쉼 — words.json을 주면 판정"))
    return result(CHECK, not viol, viol, {"pauses": len(pauses), "words_json": bool(words_path)},
                  warnings=warn, target=path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    ap.add_argument("--words")
    a = ap.parse_args()
    emit(check(a.path, a.words))
