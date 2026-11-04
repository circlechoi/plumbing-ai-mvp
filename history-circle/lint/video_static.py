"""정지 화면 길이 + 컷 길이 상한 검사.

사용: python3 video_static.py final.mp4 [--profile explain|battle] [--sections sections.json] [--cuts cuts.json]
 - 프레임 차이(축소 흑백, 평균 절대차)가 static_diff 미만인 구간을 '정지'로 보고, 구간 상한을 넘으면 실패.
   상한: explain(설명·판단·지도) 6초 / battle(전투·탈출) 1초(규칙상 0, 측정 오차 감안 임시).
 - sections.json: [{"start":0,"end":30,"profile":"battle"}, ...] — 구간마다 프로필을 다르게 줄 때.
 - cuts.json: [{"start":..,"end":..,"kind":"person"|"wide"|..}] — 사람 컷 3초·원경 5초 상한 검사.
근거: history-longform:245(E-6 정지 화면 상한), :185, history-longform-craft:35-36
"""
import argparse

import numpy as np

from common import emit, frame_diffs, load_gray_frames, load_json, result, segments, th

CHECK = "video_static"


def _limit(profile):
    return th(CHECK, "max_static_s_battle" if profile == "battle" else "max_static_s_explain")


def _profile_at(t, sections, default):
    for s in sections or []:
        if s["start"] <= t < s["end"]:
            return s.get("profile", default)
    return default


def check(path, profile="explain", sections_path=None, cuts_path=None):
    fps = th(CHECK, "sample_fps")
    thr = th(CHECK, "static_diff")
    frames = load_gray_frames(path, fps)
    d = frame_diffs(frames)
    sections = load_json(sections_path) if sections_path else None
    viol = []
    runs = segments(d < thr, 1.0 / fps)
    longest = 0.0
    for s, e in runs:
        dur = e - s + 1.0 / fps  # 차이 n개 = 프레임 n+1장
        longest = max(longest, dur)
        prof = _profile_at(s, sections, profile)
        lim = _limit(prof)
        if dur > lim:
            viol.append({"what": "정지 화면 상한 초과", "start_s": round(s, 2), "len_s": round(dur, 2),
                         "profile": prof, "limit_s": lim})
    if cuts_path:
        for c in load_json(cuts_path):
            kind = c.get("kind")
            key = {"person": "max_cut_s_person", "wide": "max_cut_s_wide"}.get(kind)
            if not key:
                continue
            lim = th(CHECK, key)
            dur = c["end"] - c["start"]
            if dur > lim + 1e-6:
                viol.append({"what": "컷 길이 상한 초과", "kind": kind, "start_s": c["start"],
                             "len_s": round(dur, 2), "limit_s": lim, "id": c.get("id")})
    return result(CHECK, not viol, viol,
                  {"frames": int(len(frames)), "longest_static_s": round(longest, 2), "profile": profile},
                  target=path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    ap.add_argument("--profile", default="explain", choices=["explain", "battle"])
    ap.add_argument("--sections")
    ap.add_argument("--cuts")
    a = ap.parse_args()
    emit(check(a.path, a.profile, a.sections, a.cuts))
