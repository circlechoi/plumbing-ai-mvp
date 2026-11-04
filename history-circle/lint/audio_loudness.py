"""최종 영상·음성의 통합 라우드니스(LUFS)와 True Peak 검사.

사용: python3 audio_loudness.py final.mp4 [--format shorts|longform]
근거: thresholds.json audio_loudness (11/04 사용자 확정 C3: 롱폼 −14 / 쇼츠·전투·건축 −15 LUFS, TP −1.5)
"""
import argparse
import math

from common import emit, integrated_lufs, result, th, true_peak_db

CHECK = "audio_loudness"


def check(path, fmt="shorts"):
    target = th(CHECK, "target_lufs_longform" if fmt == "longform" else "target_lufs")
    tol = th(CHECK, "tolerance_lu")
    tp_max = th(CHECK, "max_true_peak_db")
    lufs = integrated_lufs(path)
    tp = true_peak_db(path)
    v = []
    if math.isinf(lufs) or abs(lufs - target) > tol:
        v.append({"what": "통합 라우드니스 범위 밖", "measured_lufs": lufs, "target_lufs": target, "tolerance_lu": tol})
    if tp > tp_max:
        v.append({"what": "True Peak 초과", "measured_dbtp": tp, "max_dbtp": tp_max})
    return result(CHECK, not v, v, {"format": fmt, "integrated_lufs": lufs, "target_lufs": target, "true_peak_db": tp},
                  target=path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    ap.add_argument("--format", default="shorts", choices=["shorts", "longform"])
    a = ap.parse_args()
    emit(check(a.path, a.format))
