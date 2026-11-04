"""같은 방향 팬이 연속되는지 검사.

사용: python3 video_pan_repeat.py final.mp4 [--cuts cuts.json]
 - 컷 경계: 프레임 차이 평균 cut_diff 이상(또는 cuts.json의 start/end).
 - 컷마다 연속 프레임 쌍의 전역 이동을 위상상관(numpy FFT)으로 구해 합산 → 화면 내용이 움직인 방향
   (left/right/up/down, 이동이 작거나 줌이면 none).
 - none이 아닌 같은 방향 컷이 max_same_dir_run을 넘어 연속되면 실패(기본: 2컷 연속이면 실패).
근거: 사용자 지적 '같은 방향 팬'(규칙 부재 → 신규, 임계값 임시), 컷 감지는 history-longform-craft:124
"""
import argparse

import numpy as np

from common import emit, frame_diffs, load_gray_frames, load_json, result, th

CHECK = "video_pan_repeat"


def phase_shift(a, b):
    """b가 a에서 (dx, dy)만큼 움직였을 때 (dx, dy)를 돌려준다(픽셀, 정수+부화소 근사)."""
    h, w = a.shape
    win = np.outer(np.hanning(h), np.hanning(w))
    A = np.fft.fft2((a - a.mean()) * win)
    B = np.fft.fft2((b - b.mean()) * win)
    R = B * np.conj(A)
    R /= np.abs(R) + 1e-9
    r = np.real(np.fft.ifft2(R))
    iy, ix = np.unravel_index(np.argmax(r), r.shape)

    def sub(c, n, get):
        l, m, p = get((c - 1) % n), get(c), get((c + 1) % n)
        den = l - 2 * m + p
        off = 0.0 if abs(den) < 1e-12 else 0.5 * (l - p) / den
        v = c + off
        return v - n if v > n / 2 else v

    dy = sub(iy, h, lambda k: r[k, ix])
    dx = sub(ix, w, lambda k: r[iy, k])
    return dx, dy


def _cuts_from_frames(d, fps, n_frames, thr):
    idx = [0] + [i + 1 for i, v in enumerate(d) if v >= thr] + [n_frames]
    return [(idx[k], idx[k + 1]) for k in range(len(idx) - 1) if idx[k + 1] - idx[k] >= 2]


def direction(dx, dy, min_px, dom):
    ax, ay = abs(dx), abs(dy)
    if max(ax, ay) < min_px:
        return "none"
    if ax >= dom * ay:
        return "right" if dx > 0 else "left"
    if ay >= dom * ax:
        return "down" if dy > 0 else "up"
    return "diagonal"


def check(path, cuts_path=None):
    fps = th(CHECK, "sample_fps")
    frames = load_gray_frames(path, fps)
    d = frame_diffs(frames)
    if cuts_path:
        cuts = [(int(round(c["start"] * fps)), min(len(frames), int(round(c["end"] * fps))))
                for c in load_json(cuts_path)]
    else:
        cuts = _cuts_from_frames(d, fps, len(frames), th(CHECK, "cut_diff"))
    min_px = th(CHECK, "min_pan_px")
    dom = th(CHECK, "dominance")
    max_run = th(CHECK, "max_same_dir_run")
    info = []
    for s, e in cuts:
        tx = ty = 0.0
        for i in range(s, e - 1):
            dx, dy = phase_shift(frames[i], frames[i + 1])
            tx += dx
            ty += dy
        info.append({"start_s": round(s / fps, 2), "end_s": round(e / fps, 2),
                     "dx_px": round(tx, 1), "dy_px": round(ty, 1), "dir": direction(tx, ty, min_px, dom)})
    viol = []
    run = 1
    for k in range(1, len(info)):
        if info[k]["dir"] not in ("none", "diagonal") and info[k]["dir"] == info[k - 1]["dir"]:
            run += 1
            if run > max_run:
                viol.append({"what": "같은 방향 팬 연속", "dir": info[k]["dir"], "cut_index": k,
                             "start_s": info[k]["start_s"], "run": run})
        else:
            run = 1
    return result(CHECK, not viol, viol, {"cuts": info}, target=path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    ap.add_argument("--cuts")
    a = ap.parse_args()
    emit(check(a.path, a.cuts))
