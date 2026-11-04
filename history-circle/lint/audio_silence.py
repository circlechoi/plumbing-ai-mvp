"""소리 빈 구간 검사 (qa.py '2.5초+ 소리 빈 구간' 통합).

사용: python3 audio_silence.py final.mp4
 - silencedetect(noise_db)로 무음 구간을 찾는다.
 - fail_s 이상이면 실패(스타일 바이블 '무음 3초 금지(제목·시그니처 포함)'), warn_s 이상이면 경고(qa.py 2.5초).
 - 의도한 정적은 '결정적 대사 앞 1~2초만'이라 경고 기준보다 짧다.
근거: thresholds.json audio_silence
"""
import argparse

from common import emit, media_duration, result, silence_runs, th

CHECK = "audio_silence"


def check(path):
    warn_s = th(CHECK, "warn_s")
    fail_s = th(CHECK, "fail_s")
    runs = silence_runs(path, th(CHECK, "noise_db"), min(warn_s, fail_s))
    viol, warn = [], []
    for a, b in runs:
        item = {"start_s": round(a, 2), "end_s": round(b, 2), "len_s": round(b - a, 2)}
        if b - a >= fail_s:
            viol.append(dict(item, what="무음 %g초 이상" % fail_s))
        elif b - a >= warn_s:
            warn.append(dict(item, what="무음 %g초 이상(qa.py)" % warn_s))
    return result(CHECK, not viol, viol, {"duration_s": round(media_duration(path), 2), "silences": len(runs)},
                  warnings=warn, target=path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    emit(check(ap.parse_args().path))
