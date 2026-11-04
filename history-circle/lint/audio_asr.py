"""발음 의심 단어 검사 (qa.py --asr 통합). faster-whisper가 없으면 건너뛴다(통과 + 경고).

사용: python3 audio_asr.py final.mp4 [--model small]
 - 음성 인식 결과에 watch_list의 '잘못 들린 형태'가 나오면 경고(사람이 직접 들어 판단).
   '낙랑'은 인식기가 거의 항상 '낭낭'으로 받아 적는다(longform-craft) → 실패가 아니라 경고.
근거: thresholds.json audio_asr
"""
import argparse
import os
import subprocess
import tempfile

from common import emit, result, th

CHECK = "audio_asr"


def _mmss(t):
    return "%d:%04.1f" % (int(t // 60), t % 60)


def check(path, model="small"):
    try:
        from faster_whisper import WhisperModel
    except Exception:
        return result(CHECK, True, [], {"skipped": True}, warnings=["faster-whisper 없음 — 발음 검사 건너뜀"],
                      target=path)
    watch = th(CHECK, "watch_list")
    fd, wav = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    segs, _ = WhisperModel(model, compute_type="int8").transcribe(wav, language="ko")
    warn = []
    for s in segs:
        flat = s.text.replace(" ", "")
        for heard, meant in watch.items():
            if heard in flat or heard in s.text:
                warn.append({"what": "발음 의심", "at": _mmss(s.start), "heard": heard, "meant": meant})
    os.remove(wav)
    return result(CHECK, True, [], {"skipped": False}, warnings=warn, target=path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    ap.add_argument("--model", default="small")
    a = ap.parse_args()
    emit(check(a.path, a.model))
