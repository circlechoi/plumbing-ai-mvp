"""segments.yaml의 anchor 문구가 스킬 원문에 그대로 있는지 검사. 없으면 exit 1.

스킬은 줄 번호가 자주 밀리므로(11/04 longform-craft v2.3) 줄 번호 대신 원문 문구로 연결한다.
"""
import glob
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.environ.get("HISTORY_SKILLS", "/root/.claude/skills/synced/*")

segs = yaml.safe_load(open(os.path.join(HERE, "..", "segments.yaml"), encoding="utf-8"))["segments"]
miss = []
for s in segs:
    paths = glob.glob(os.path.join(SKILLS, s["skill"], "SKILL.md"))
    if not paths:
        miss.append((s["id"], "스킬 없음: " + s["skill"]))
        continue
    if s["anchor"] not in open(paths[0], encoding="utf-8").read():
        miss.append((s["id"], s["anchor"]))
print(f"구간 {len(segs)}개 / 원문 확인 {len(segs) - len(miss)}개")
for m in miss:
    print("[원문에 없음]", *m)
sys.exit(1 if miss else 0)
