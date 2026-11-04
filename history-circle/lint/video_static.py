"""정지 화면·같은 화면·검은 화면·컷/튐 검사 (qa.py 영상 항목 통합).

사용: python3 video_static.py final.mp4 [--profile explain|battle] [--format shorts|longform]
                             [--sections sections.json] [--cuts cuts.json] [--no-zoom-aware]
 - 정지(실패): 프레임 차이가 static_diff 미만인 구간이 구간 상한을 넘으면 실패.
   상한: explain(설명·판단·지도) 6초 / battle(전투·탈출) 1초(임시). 3초 넘으면 경고(qa.py '3초+ 정지 화면').
 - 천천히 확대(liven.py)·느린 팬은 정지가 아니다(zoom_aware, 기본 켬): 1초 전 프레임과의 차이가
   still_diff_1s 이상이면 화면이 바뀌고 있는 것으로 본다. 끄면 qa.py처럼 매 프레임 차이만 본다.
 - 같은 화면 오래 유지(경고): 1초 이동평균 차이 low_motion_diff 미만이 6초 이상(qa.py).
 - 검은 화면(실패): 평균 밝기 black_luma 미만 0.8초 이상. 시작·끝 black_edge_s 안의 페이드는 제외(임시).
 - 컷/튐: 프레임 차이 cut_diff 이상. cuts.json이 있으면 계획 경계에서 먼 컷을 '계획에 없는 튐' 경고.
 - cuts.json kind: person 3초 / wide 5초 상한, live(실사) 안의 정지는 2초 이상 실패.
 - 롱폼(--format longform, 1920×1080)은 레터박스 그림 띠(138~942)만 본다(자막·상단 띠 제외, qa.py와 같음).
근거: thresholds.json video_static (longform:245·185, longform-craft 사람 3초·원경 5초·스틸 2초·qa.py)
"""
import argparse

import numpy as np

from common import band_for, emit, frame_diffs, load_gray_frames, load_json, result, segments, th

CHECK = "video_static"


def _limit(profile):
    return th(CHECK, "max_static_s_battle" if profile == "battle" else "max_static_s_explain")


def _profile_at(t, sections, default):
    for s in sections or []:
        if s["start"] <= t < s["end"]:
            return s.get("profile", default)
    return default


def static_mask(frames, fps, zoom_aware=True):
    """프레임 차이 배열 d(길이 N-1)와 정지 마스크를 돌려준다."""
    d = frame_diffs(frames)
    mask = d < th(CHECK, "static_diff")
    if zoom_aware and len(frames) > fps:
        k = int(round(fps))
        thr1 = th(CHECK, "still_diff_1s")
        base = mask.copy()
        # d[i]는 frame i → i+1. 1초 동안 매 프레임은 거의 같지만 1초 전(i+1-k)과는 달라졌다면
        # 천천히 확대·이동 중(liven) → 정지에서 뺀다. 1초 창 안에 큰 변화(컷·움직임)가 있으면 이 판정은 쓰지 않는다.
        for i in range(k - 1, len(d)):
            j = i + 1 - k
            if base[j:i + 1].all() and float(np.mean(np.abs(frames[i + 1] - frames[j]))) >= thr1:
                mask[j:i + 1] = False
    return d, mask


def check(path, profile="explain", sections_path=None, cuts_path=None, fmt="shorts", zoom_aware=True):
    fps = th(CHECK, "sample_fps")
    band = band_for(path, fmt)
    frames = load_gray_frames(path, fps, band=band)
    d, mask = static_mask(frames, fps, zoom_aware)
    sections = load_json(sections_path) if sections_path else None
    cuts_plan = load_json(cuts_path) if cuts_path else []
    viol, warn = [], []
    step = 1.0 / fps

    # 1) 정지
    longest = 0.0
    warn_s = th(CHECK, "warn_static_s")
    for s, e in segments(mask, step):
        dur = e - s + step  # 차이 n개 = 프레임 n+1장
        longest = max(longest, dur)
        prof = _profile_at(s, sections, profile)
        lim = _limit(prof)
        if dur > lim:
            viol.append({"what": "정지 화면 상한 초과", "start_s": round(s, 2), "len_s": round(dur, 2),
                         "profile": prof, "limit_s": lim})
        elif dur >= warn_s:
            warn.append({"what": "정지 화면 3초+ (qa.py)", "start_s": round(s, 2), "len_s": round(dur, 2)})
        for c in cuts_plan:
            if c.get("kind") == "live" and c["start"] - 1e-6 <= s and s + dur <= c["end"] + step:
                lim2 = th(CHECK, "max_still_s_live")
                if dur >= lim2:
                    viol.append({"what": "실사 컷 안 움직임 없는 스틸", "start_s": round(s, 2),
                                 "len_s": round(dur, 2), "limit_s": lim2, "id": c.get("id")})

    # 2) 같은 화면 오래 유지(경고)
    k = int(round(fps))
    if len(d) >= k:
        mov = np.convolve(d, np.ones(k) / k, "same")
        for s, e in segments(mov < th(CHECK, "low_motion_diff"), step):
            if e - s >= th(CHECK, "low_motion_s"):
                warn.append({"what": "움직임 매우 적음(같은 화면 오래 유지, qa.py)", "start_s": round(s, 2),
                             "len_s": round(e - s, 2)})

    # 3) 검은 화면
    luma = frames.mean(axis=(1, 2)) if len(frames) else np.zeros(0)
    total = len(frames) * step
    edge = th(CHECK, "black_edge_s")
    for s, e in segments(luma < th(CHECK, "black_luma"), step):
        if e - s < th(CHECK, "black_min_s"):
            continue
        item = {"what": "검은 화면", "start_s": round(s, 2), "len_s": round(e - s, 2)}
        if s <= edge or e >= total - edge:
            warn.append(dict(item, what="검은 화면(시작·끝 페이드로 보고 경고만)"))
        else:
            viol.append(item)

    # 4) 컷/튐
    cut_thr = th(CHECK, "cut_diff")
    cuts = [round((i + 1) * step, 2) for i, x in enumerate(d) if x >= cut_thr and (i == 0 or d[i - 1] < cut_thr)]
    if cuts_plan:
        bounds = sorted({float(c["start"]) for c in cuts_plan} | {float(c["end"]) for c in cuts_plan})
        tol = th(CHECK, "cut_match_s")
        for t in cuts:
            if not any(abs(t - b) <= tol for b in bounds):
                warn.append({"what": "계획에 없는 컷/튐", "at_s": t})

    # 5) 컷 길이 상한
    for c in cuts_plan:
        key = {"person": "max_cut_s_person", "wide": "max_cut_s_wide"}.get(c.get("kind"))
        if not key:
            continue
        lim = th(CHECK, key)
        dur = c["end"] - c["start"]
        if dur > lim + 1e-6:
            viol.append({"what": "컷 길이 상한 초과", "kind": c["kind"], "start_s": c["start"],
                         "len_s": round(dur, 2), "limit_s": lim, "id": c.get("id")})
    return result(CHECK, not viol, viol,
                  {"frames": int(len(frames)), "longest_static_s": round(longest, 2), "profile": profile,
                   "zoom_aware": zoom_aware, "band": band, "cuts_detected": cuts[:200]},
                  warnings=warn, target=path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--profile", default="explain", choices=["explain", "battle"])
    ap.add_argument("--format", default="shorts", choices=["shorts", "longform"])
    ap.add_argument("--sections")
    ap.add_argument("--cuts")
    ap.add_argument("--no-zoom-aware", action="store_true")
    a = ap.parse_args()
    emit(check(a.path, a.profile, a.sections, a.cuts, a.format, not a.no_zoom_aware))
