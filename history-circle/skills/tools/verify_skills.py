"""재구조화한 스킬에서 원문이 빠지지 않았는지 검사. 누락이 하나라도 있으면 exit 1.

(1) 원본 스킬 9개의 비어 있지 않은 모든 줄(코드 블록 줄 포함)이
    새 SKILL.md ∪ reference-*.md ∪ archive.md ∪ kit 파일에 그대로 있거나,
    replacements.json에 원문 → 새 문장으로 등록돼 있어야 한다.
    코드 울타리 줄(```만 있는 줄)은 위치 표시라서 제외한다.
(2) decisions_raw.yaml의 모든 원문(text)이 새 스킬 파일들에 있어야 한다.
(3) 크기 표: 원본 vs 새 SKILL.md · reference · archive, 그리고 작업별로 읽는 양.

사용: python3 tools/verify_skills.py [원본 스킬 폴더 glob]
"""
import glob
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
HC = os.path.dirname(OUT)
SRC_GLOB = sys.argv[1] if len(sys.argv) > 1 else "/root/.claude/skills/synced/*"
NAMES = ["history-architecture-shorts", "history-battle-shorts", "history-channel-concept", "history-longform",
         "history-longform-craft", "history-map-v4", "history-production-standards", "history-shorts",
         "history-shorts-craft"]
FENCE_ONLY = re.compile(r"^\s*```[\w.+-]*\s*$")


def read(p):
    return open(p, encoding="utf-8", errors="replace").read()


def size(p):
    return os.path.getsize(p) if os.path.exists(p) else 0


def main():
    # 새 파일 전체의 줄 집합 + kit 줄 집합
    new_lines, new_text = set(), []
    for p in glob.glob(os.path.join(OUT, "history-*", "*.md")):
        t = read(p)
        new_text.append(t)
        new_lines.update(x.rstrip() for x in t.split("\n"))
    kit_lines = set()
    for p in glob.glob(os.path.join(HC, "kit", "**", "*"), recursive=True):
        if os.path.isfile(p) and not p.endswith(".md"):
            kit_lines.update(x.rstrip() for x in read(p).split("\n"))
    reps = json.load(open(os.path.join(OUT, "replacements.json"), encoding="utf-8"))
    rep_orig = {(r["skill"], r["original"].rstrip()) for r in reps}

    missing, total = [], 0
    rows = []
    for name in NAMES:
        src = glob.glob(os.path.join(SRC_GLOB, name, "SKILL.md"))[0]
        for i, ln in enumerate(read(src).split("\n")):
            x = ln.rstrip()
            if not x.strip() or FENCE_ONLY.match(x):
                continue
            total += 1
            if x in new_lines or x in kit_lines or (name, x) in rep_orig:
                continue
            missing.append(f"{name}:{i + 1}: {x[:100]}")
        d = os.path.join(OUT, name)
        refs = sum(size(p) for p in glob.glob(os.path.join(d, "reference-*.md")))
        rows.append((name, size(src), size(os.path.join(d, "SKILL.md")), refs, size(os.path.join(d, "archive.md"))))

    # (2) 원장 원문
    raw = yaml.safe_load(open(os.path.join(HC, "decisions", "decisions_raw.yaml"), encoding="utf-8"))
    blob = "\n".join(new_text)
    raw_miss = [x["id"] for x in raw["items"] if x["text"].strip() not in blob]
    # 교체로 바뀐 줄의 결정은 archive '교체 원문'에 원문이 있으므로 blob에 포함된다

    print(f"(1) 원본 줄 {total}개 중 누락 {len(missing)}개")
    for m in missing[:40]:
        print("   [누락]", m)
    print(f"(2) 원장 원문 {len(raw['items'])}건 중 누락 {len(raw_miss)}건", raw_miss[:20])

    print("\n(3) 크기(바이트)")
    print("%-30s %9s %9s %9s %9s" % ("스킬", "원본", "SKILL.md", "reference", "archive"))
    for r in rows:
        print("%-30s %9d %9d %9d %9d" % r)
    core = size(os.path.join(OUT, "history-core", "SKILL.md"))
    print("%-30s %9s %9d" % ("history-core (신규)", "-", core))
    S = {r[0]: (r[1], r[2]) for r in rows}
    print("\n작업별로 먼저 읽는 양 (원본: 해당 스킬 + concept + production-standards / 새: core + 해당 SKILL.md)")
    jobs = {
        "롱폼": ["history-longform", "history-longform-craft", "history-map-v4"],
        "45초 신작": ["history-shorts", "history-shorts-craft", "history-map-v4"],
        "전투 쇼츠": ["history-battle-shorts", "history-map-v4"],
        "건축 쇼츠": ["history-architecture-shorts", "history-shorts"],
    }
    for job, sk in jobs.items():
        old = sum(S[s][0] for s in sk) + S["history-channel-concept"][0] + S["history-production-standards"][0]
        new = core + sum(S[s][1] for s in sk)
        print("  %-10s 원본 %7d → 새 %7d  (%d%% 감소)" % (job, old, new, round(100 * (old - new) / old)))
    sys.exit(1 if (missing or raw_miss) else 0)


if __name__ == "__main__":
    main()
