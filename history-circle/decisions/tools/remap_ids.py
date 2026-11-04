"""스킬이 고쳐져 줄 번호가 밀렸을 때 curated.yaml의 출처 id를 원문 텍스트 기준으로 다시 맞춘다.

사용(스킬 갱신 후):
  cp decisions_raw.yaml /tmp/raw_old.yaml
  python3 tools/extract_decisions.py
  python3 tools/remap_ids.py /tmp/raw_old.yaml
  python3 tools/build_ledger.py && python3 tools/verify_ledger.py
줄 번호만 보고 연결하면, 밀린 id가 우연히 존재하는 다른 줄을 가리켜도 검증이 통과한다(11/04 실제 발생 — 10건).
유사도 0.9 미만은 자동으로 바꾸지 않고 목록만 출력하고 exit 1.
"""
import difflib
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main(old_path):
    old = yaml.safe_load(open(old_path, encoding="utf-8"))
    new = yaml.safe_load(open(os.path.join(ROOT, "decisions_raw.yaml"), encoding="utf-8"))
    ot = {x["id"]: x["text"] for x in old["items"]}
    by_skill = {}
    for x in new["items"]:
        by_skill.setdefault(x["id"].split(":")[0], []).append((x["id"], x["text"]))
    nt = {x["id"]: x["text"] for x in new["items"]}
    path = os.path.join(ROOT, "curated.yaml")
    s = open(path, encoding="utf-8").read()
    mp, weak = {}, []
    for oid in sorted(set(re.findall(r"[a-z-]+:\d+", s))):
        if oid not in ot:
            continue
        if nt.get(oid) == ot[oid]:
            continue
        cands = by_skill.get(oid.split(":")[0], [])
        if not cands:
            weak.append((oid, None, 0.0))
            continue
        best = max(cands, key=lambda t: difflib.SequenceMatcher(None, ot[oid], t[1]).ratio())
        r = difflib.SequenceMatcher(None, ot[oid], best[1]).ratio()
        if r >= 0.9:
            mp[oid] = best[0]
        else:
            weak.append((oid, best[0], round(r, 2)))
    s = re.sub(r"[a-z-]+:\d+", lambda m: "\0" + mp.get(m.group(0), m.group(0)), s).replace("\0", "")
    open(path, "w", encoding="utf-8").write(s)
    for a, b in mp.items():
        print(f"{a} -> {b}")
    for w in weak:
        print("[확인 필요]", w)
    sys.exit(1 if weak else 0)


if __name__ == "__main__":
    main(sys.argv[1])
