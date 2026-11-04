#!/usr/bin/env python3
"""결정 원장 검증 — 스킬의 날짜 결정이 원장에서 하나도 빠지지 않았는지 확인한다.

검사
1. raw의 모든 항목(현행·폐기·보류 후보 전부)이 decisions.yaml의 sources / superseded / 원문_보존 중 한 곳에 연결됐는가
2. decisions.yaml이 raw에 없는 id를 가리키지 않는가
3. (선택) 스킬 원문이 추출 이후 바뀌었는가 — md5 비교. 바뀌었으면 extract → build를 다시 돌려야 한다
4. status: 사용자확정대기 항목 목록 출력(실패는 아님)

미연결이 하나라도 있으면 exit 1.
사용: python3 verify_ledger.py [스킬 루트]
"""
import glob
import hashlib
import os
import re
import sys

import yaml

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ID_RE = re.compile(r"^([a-z0-9-]+:\d+)")


def ids_in(doc):
    found = set()
    for t in doc["topics"]:
        for it in t["items"]:
            for k in ("sources", "superseded"):
                for s in it.get(k) or []:
                    found.add(ID_RE.match(s).group(1))
        for x in t.get("원문_보존", []):
            found.add(x["id"])
    for k in ("principle_sources", "user_over_review_sources"):
        for s in doc["meta"].get(k, []):
            found.add(ID_RE.match(s).group(1))
    return found


def main():
    raw = yaml.safe_load(open(os.path.join(D, "decisions_raw.yaml"), encoding="utf-8"))
    led = yaml.safe_load(open(os.path.join(D, "decisions.yaml"), encoding="utf-8"))
    raw_ids = {x["id"] for x in raw["items"]}
    led_ids = ids_in(led)

    unlinked = sorted(raw_ids - led_ids)
    dangling = sorted(led_ids - raw_ids)
    ok = True

    print(f"raw {len(raw_ids)}건 / 원장 연결 {len(raw_ids & led_ids)}건")
    if unlinked:
        ok = False
        print(f"[실패] 미연결 {len(unlinked)}건:")
        by = {x["id"]: x for x in raw["items"]}
        for i in unlinked:
            print(f"  - {i} ({by[i]['date']}) {by[i]['text'][:120]}")
    else:
        print("[통과] 미연결 0건")
    if dangling:
        ok = False
        print(f"[실패] raw에 없는 id {len(dangling)}건: {', '.join(dangling)}")

    root = sys.argv[1] if len(sys.argv) > 1 else "/root/.claude/skills/synced/*"
    for f in sorted(glob.glob(os.path.join(root, "history-*", "SKILL.md"))):
        sk = os.path.basename(os.path.dirname(f))
        md5 = hashlib.md5(open(f, encoding="utf-8").read().encode()).hexdigest()
        want = raw["sources"].get(sk, {}).get("md5")
        if want is None:
            print(f"[경고] 원장에 없는 스킬: {sk}")
        elif md5 != want:
            print(f"[경고] {sk} 원문이 추출 이후 바뀜 → extract_decisions.py · build_ledger.py 다시 실행")

    pend = [(t["name"], i["key"], i.get("conflict", "")) for t in led["topics"] for i in t["items"] if i.get("status") == "사용자확정대기"]
    print(f"사용자확정대기 {len(pend)}건:")
    for p in pend:
        print(f"  - [{p[2]}] {p[0]} / {p[1]}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
