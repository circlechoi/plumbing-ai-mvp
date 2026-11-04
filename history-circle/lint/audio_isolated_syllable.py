"""장면 wav 앞뒤 끝에 남은 '고립 음절' 검사.

사용: python3 audio_isolated_syllable.py scene01.wav [scene02.wav ...]
문단 녹음을 장면별로 자를 때, 앞 장면 끝에 다음 문단 첫 음절(약 0.1초)이 남는 사고를 찾는다.
조건: 파일 끝(또는 시작) 쪽 소리 덩어리가 max_blob_s 미만이고, 본문과 min_gap_s 이상 무음으로 떨어져 있으며,
파일 끝에서 edge_window_s 안에 있다.
근거: history-battle-shorts:133 (4편 '8초에 6…' 사고)
"""
import argparse

import numpy as np

from common import emit, load_audio, result, rms_db_frames, segments, th

CHECK = "audio_isolated_syllable"
MERGE_S = 0.03  # 30ms보다 짧은 끊김은 한 덩어리로 본다


def _blobs(x):
    db, fs = rms_db_frames(x, frame_s=0.01)
    on = db > th(CHECK, "silence_db")
    segs = segments(on, fs)
    merged = []
    for s, e in segs:
        if merged and s - merged[-1][1] < MERGE_S:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    return merged, len(db) * fs


def check_file(path):
    gap_min = th(CHECK, "min_gap_s")
    blob_max = th(CHECK, "max_blob_s")
    edge = th(CHECK, "edge_window_s")
    blobs, dur = _blobs(load_audio(path))
    viol = []
    if len(blobs) >= 2:
        s, e = blobs[-1]
        gap = s - blobs[-2][1]
        if e - s < blob_max and gap >= gap_min and dur - e <= edge:
            viol.append({"file": path, "where": "끝", "blob_start_s": round(s, 2), "blob_len_s": round(e - s, 2),
                         "gap_before_s": round(gap, 2)})
        s, e = blobs[0]
        gap = blobs[1][0] - e
        if e - s < blob_max and gap >= gap_min and s <= edge:
            viol.append({"file": path, "where": "시작", "blob_start_s": round(s, 2), "blob_len_s": round(e - s, 2),
                         "gap_after_s": round(gap, 2)})
    return viol, {"blobs": len(blobs), "duration_s": round(dur, 2)}


def check(paths):
    viol, metrics = [], {}
    for p in paths:
        v, m = check_file(p)
        viol += v
        metrics[p] = m
    return result(CHECK, not viol, viol, metrics, target=paths)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+")
    emit(check(ap.parse_args().paths))
