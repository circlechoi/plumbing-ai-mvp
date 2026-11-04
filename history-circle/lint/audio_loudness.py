"""최종 영상·음성의 통합 라우드니스(LUFS)가 목표 범위 안인지 검사.

사용: python3 audio_loudness.py final.mp4
근거: thresholds.json audio_loudness (목표값은 사용자 확정 대기 — 스킬 간 충돌)
"""
import argparse
import math

from common import emit, integrated_lufs, result, th

CHECK = "audio_loudness"


def check(path):
    target = th(CHECK, "target_lufs")
    tol = th(CHECK, "tolerance_lu")
    lufs = integrated_lufs(path)
    ok = (not math.isinf(lufs)) and abs(lufs - target) <= tol
    v = [] if ok else [{
        "what": "통합 라우드니스 범위 밖",
        "measured_lufs": lufs, "target_lufs": target, "tolerance_lu": tol,
    }]
    return result(CHECK, ok, v, {"integrated_lufs": lufs, "target_lufs": target}, target=path,
                  warnings=["목표 LUFS는 사용자 확정 대기(임시 −15)"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    emit(check(ap.parse_args().path))
