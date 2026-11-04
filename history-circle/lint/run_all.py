"""폴더 하나를 받아 있는 파일에 해당하는 검사만 돌리고 요약표를 찍는다.

사용: python3 run_all.py <편 폴더> [--profile explain|battle] [--json out.json]

폴더 규약(있는 것만 검사):
  final.mp4 (또는 *.mp4 중 하나)  → audio_loudness, video_static, video_pan_repeat
  vo.wav + sfx.wav                → audio_sfx_vs_vo
  scenes/*.wav                    → audio_isolated_syllable, audio_midpause
  scenes/<이름>.words.json        → audio_midpause 단어 시각(있으면)
  layout*.json, layout/*.json     → layout_overlap
  sections.json, cuts.json        → video_static·video_pan_repeat 보조 입력
하나라도 실패하면 exit 1.
"""
import argparse
import glob
import json
import os
import sys

import audio_isolated_syllable
import audio_loudness
import audio_midpause
import audio_sfx_vs_vo
import layout_overlap
import video_pan_repeat
import video_static


def _opt(folder, name):
    p = os.path.join(folder, name)
    return p if os.path.exists(p) else None


def run(folder, profile="explain", fmt="shorts"):
    results = []

    def safe(name, fn, *a):
        try:
            results.append(fn(*a))
        except Exception as e:  # 검사 하나가 깨져도 나머지는 돈다
            results.append({"check": name, "ok": False, "target": a[0] if a else None,
                            "violations": [{"what": "검사 실행 오류", "detail": str(e)[:500]}],
                            "warnings": [], "metrics": {}})

    video = _opt(folder, "final.mp4") or next(iter(sorted(glob.glob(os.path.join(folder, "*.mp4")))), None)
    sections, cuts = _opt(folder, "sections.json"), _opt(folder, "cuts.json")
    if video:
        safe("audio_loudness", audio_loudness.check, video, fmt)
        safe("video_static", video_static.check, video, profile, sections, cuts)
        safe("video_pan_repeat", video_pan_repeat.check, video, cuts)
    vo, sfx = _opt(folder, "vo.wav"), _opt(folder, "sfx.wav")
    if vo and sfx:
        safe("audio_sfx_vs_vo", audio_sfx_vs_vo.check, vo, sfx, sections)
    scenes = sorted(glob.glob(os.path.join(folder, "scenes", "*.wav")))
    if scenes:
        safe("audio_isolated_syllable", audio_isolated_syllable.check, scenes)
        for w in scenes:
            words = w[:-4] + ".words.json"
            safe("audio_midpause", audio_midpause.check, w, words if os.path.exists(words) else None)
    layouts = sorted(glob.glob(os.path.join(folder, "layout*.json")) + glob.glob(os.path.join(folder, "layout", "*.json")))
    if layouts:
        safe("layout_overlap", layout_overlap.check, layouts)
    return results


def table(results):
    rows = ["%-24s %-6s %4s %4s  %s" % ("검사", "결과", "위반", "경고", "대상")]
    for r in results:
        tgt = r.get("target")
        if isinstance(tgt, list):
            tgt = "%d개 파일" % len(tgt)
        rows.append("%-24s %-6s %4d %4d  %s" % (r["check"], "통과" if r["ok"] else "실패",
                                               len(r["violations"]), len(r.get("warnings", [])),
                                               os.path.basename(str(tgt))))
    return "\n".join(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--profile", default="explain", choices=["explain", "battle"])
    ap.add_argument("--format", default="shorts", choices=["shorts", "longform"])
    ap.add_argument("--json")
    a = ap.parse_args()
    res = run(a.folder, a.profile, a.format)
    if not res:
        print("검사할 파일이 없음 — 폴더 규약은 --help 참고")
        sys.exit(1)
    print(table(res))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
    sys.exit(0 if all(r["ok"] for r in res) else 1)
