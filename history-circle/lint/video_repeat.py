"""같은 컷 반복 + 클립 과도 늘림 검사.

사용: python3 video_repeat.py final.mp4 [--cuts cuts.json] [--format shorts|longform]
 - 같은 컷 반복: 컷마다 평균 프레임을 32×18 흑백으로 줄여 비교(평균 절대차 same_cut_diff 미만 = 같은 컷).
   같은 컷 사용 횟수가 warn_uses 이상이면 경고, fail_uses 이상이면 실패.
   흑백 회상(채도 flashback_sat 미만)으로 다시 쓴 컷은 허용(스타일 바이블 '흑백 회상으로 재사용').
   cuts.json에서 kind가 map인 컷은 같은 바탕 지도를 정당하게 다시 쓰므로 비교에서 뺀다.
 - 클립 과도 늘림: 원래 프레임으로 디코드해, 움직이는 컷에서 '앞 프레임과 거의 같은 프레임'(복제) 비율을 잰다.
   2배 늘림 ≈ 0.5, 0.7배속(1.43배) ≈ 0.3. stretch_warn 이상 경고, stretch_fail 이상 실패.
   프레임 보간(minterpolate·AI 보간)으로 늘린 클립은 복제 프레임이 없어 잡지 못한다(한계).
근거: golden G18 '같은 컷 5회 반복'·'5초 클립을 1.1~3.5배 늘린 컷 25개', thresholds.json video_repeat
"""
import argparse

import numpy as np

from common import (band_for, emit, frame_diffs, load_gray_frames, load_json, load_rgb_frames, result, th,
                    video_fps)

CHECK = "video_repeat"


def _cuts(d, n, fps, thr, plan):
    if plan:
        return [(int(round(c["start"] * fps)), int(round(c["end"] * fps)), c.get("kind"), c.get("id")) for c in plan]
    idx = [0] + [i + 1 for i, v in enumerate(d) if v >= thr] + [n]
    return [(idx[k], idx[k + 1], None, None) for k in range(len(idx) - 1)]


def _thumb(frames):
    """(N, H, W) → 32×18 평균 프레임."""
    m = frames.mean(axis=0)
    h, w = m.shape
    ys = np.linspace(0, h, 19).astype(int)
    xs = np.linspace(0, w, 33).astype(int)
    return np.array([[m[ys[i]:ys[i + 1], xs[j]:xs[j + 1]].mean() for j in range(32)] for i in range(18)])


def check(path, cuts_path=None, fmt="shorts"):
    fps = th(CHECK, "sample_fps")
    band = band_for(path, fmt)
    g = load_gray_frames(path, fps, band=band)
    rgb = load_rgb_frames(path, fps, band=band)
    n = min(len(g), len(rgb))
    g, rgb = g[:n], rgb[:n]
    d = frame_diffs(g)
    plan = load_json(cuts_path) if cuts_path else None
    min_len = th(CHECK, "min_cut_s")
    cuts = []
    for a, b, kind, cid in _cuts(d, n, fps, th(CHECK, "cut_diff"), plan):
        a, b = max(0, a), min(n, b)
        if b - a < max(1, int(min_len * fps)) or kind == "map":
            continue
        sat = float((rgb[a:b].max(axis=3) - rgb[a:b].min(axis=3)).mean())
        cuts.append({"start_s": round(a / fps, 2), "end_s": round(b / fps, 2), "thumb": _thumb(g[a:b]),
                     "sat": sat, "id": cid})

    # 같은 컷 묶기
    same = th(CHECK, "same_cut_diff")
    group = list(range(len(cuts)))
    for i in range(len(cuts)):
        for j in range(i):
            if group[j] == j and np.mean(np.abs(cuts[i]["thumb"] - cuts[j]["thumb"])) < same:
                group[i] = j
                break
    viol, warn = [], []
    flash = th(CHECK, "flashback_sat")
    for root in sorted(set(group)):
        members = [c for k, c in enumerate(cuts) if group[k] == root]
        color = [c for c in members if c["sat"] >= flash]
        uses = len(color) if color else len(members)
        item = {"uses": uses, "at_s": [c["start_s"] for c in members],
                "flashback_reuse": len(members) - len(color) if color else 0}
        if uses >= th(CHECK, "fail_uses"):
            viol.append(dict(item, what="같은 컷 반복"))
        elif uses >= th(CHECK, "warn_uses"):
            warn.append(dict(item, what="같은 컷 2회 사용"))

    # 늘림(복제 프레임)
    nat = video_fps(path)
    full = load_gray_frames(path, None, width=96, band=band)
    fd = frame_diffs(full)
    dup_thr, move_thr = th(CHECK, "dup_diff"), th(CHECK, "moving_diff")
    stretch = []
    for c in cuts:
        a, b = int(c["start_s"] * nat) + 1, int(c["end_s"] * nat) - 1
        seg = fd[a:b]
        if len(seg) < nat:  # 1초 미만 컷은 판단하지 않음
            continue
        moving = seg[seg >= dup_thr]
        if len(moving) == 0 or np.median(moving) < move_thr:
            continue  # 정지 컷은 video_static 몫
        ratio = float(np.mean(seg < dup_thr))
        rec = {"start_s": c["start_s"], "end_s": c["end_s"], "dup_ratio": round(ratio, 2),
               "approx_stretch": round(1 / max(1e-6, 1 - ratio), 2)}
        stretch.append(rec)
        if ratio >= th(CHECK, "stretch_fail"):
            viol.append(dict(rec, what="클립 과도 늘림(복제 프레임)"))
        elif ratio >= th(CHECK, "stretch_warn"):
            warn.append(dict(rec, what="클립 늘림 의심(0.7배속 초과)"))
    return result(CHECK, not viol, viol,
                  {"cuts_compared": len(cuts), "groups": len(set(group)), "native_fps": round(nat, 3),
                   "stretch_measured": stretch[:100]},
                  warnings=warn, target=path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--cuts")
    ap.add_argument("--format", default="shorts", choices=["shorts", "longform"])
    a = ap.parse_args()
    emit(check(a.path, a.cuts, a.format))
