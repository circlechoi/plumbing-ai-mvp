#!/usr/bin/env python3
"""history-* 스킬 9개에서 날짜가 붙은 결정을 기계적으로 뽑아 decisions_raw.yaml로 저장한다.

뽑는 대상
- 변경 이력 표 행: | 10/23 | ... |
- [확정 MM/DD], [MM/DD] 표기
- (MM/DD ... 사용자 결정), 'MM/DD 사용자' 등 날짜 + 결정 표현이 있는 줄

원문은 자르지 않는다. status는 키워드로 1차 판정만 한다(최종 판단은 decisions.yaml).
사용: python3 extract_decisions.py [스킬 루트] [출력 경로]
"""
import glob
import hashlib
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = "/root/.claude/skills/synced/*"
DEFAULT_OUT = os.path.join(HERE, "..", "decisions_raw.yaml")

DATE = r"(?:\d{4}-)?(1[0-2]|0?[1-9])[/-](3[01]|[12]\d|0?[1-9])"
RE_TABLE = re.compile(r"^\|\s*(?:\*\*)?(" + r"(?<![\d.])(?:1[0-2]|0?[1-9])/(?:3[01]|[12]\d|0?[1-9])(?![\d])" + r")(?:\*\*)?\s*\|")
RE_CONFIRM = re.compile(r"\[(?:확정|결정)\s*(" + r"(?<![\d.])(?:1[0-2]|0?[1-9])/(?:3[01]|[12]\d|0?[1-9])(?![\d])" + r")")
RE_BRACKET = re.compile(r"\[(" + r"(?<![\d.])(?:1[0-2]|0?[1-9])/(?:3[01]|[12]\d|0?[1-9])(?![\d])" + r")\]")
RE_DECIDE = re.compile(r"((?<![\d.])(?:1[0-2]|0?[1-9])/(?:3[01]|[12]\d|0?[1-9])(?!\d))[^\n]{0,40}?(사용자|확정|결정)|(사용자 결정|사용자 답|사용자 선택|확정)[^\n]{0,40}?((?<![\d.])(?:1[0-2]|0?[1-9])/(?:3[01]|[12]\d|0?[1-9])(?!\d))")
RE_ISO = re.compile(r"(20\d\d)-(\d\d)-(\d\d)")

KW_DEPRECATED = ["폐기", "폐지", "중단", "대체",  "(이전", "이전(폐기)", "더 이상 쓰지", "쓰지 않는다(이전"]
KW_HOLD = ["보류", "[제안]", "미구현", "[미확인]"]


def status_of(text):
    if any(k in text for k in KW_DEPRECATED):
        return "폐기후보"
    if any(k in text for k in KW_HOLD):
        return "보류후보"
    return "현행후보"


def norm_date(m, d):
    return f"{int(m):02d}/{int(d):02d}"


def find_date(line):
    for rx in (RE_TABLE, RE_CONFIRM, RE_BRACKET):
        m = rx.search(line)
        if m:
            mm, dd = m.group(1).split("/")
            return norm_date(mm, dd), rx is RE_TABLE and "변경이력표" or "확정표기"
    m = RE_DECIDE.search(line)
    if m:
        ds = m.group(1) or m.group(4)
        mm, dd = ds.split("/")
        return norm_date(mm, dd), "날짜+결정어"
    m = RE_ISO.search(line)
    if m and ("사용자" in line or "결정" in line or "확정" in line):
        return norm_date(m.group(2), m.group(3)), "날짜+결정어"
    return None, None


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ROOT
    out = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUT
    files = sorted(glob.glob(os.path.join(root, "history-*", "SKILL.md")))
    if not files:
        sys.exit(f"스킬 파일 없음: {root}")
    items, src = [], {}
    for f in files:
        skill = os.path.basename(os.path.dirname(f))
        raw = open(f, encoding="utf-8").read()
        src[skill] = {"lines": raw.count("\n") + 1, "md5": hashlib.md5(raw.encode()).hexdigest()}
        in_code = False
        for i, line in enumerate(raw.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code or i <= 4:  # 코드 블록과 frontmatter 제외
                continue
            date, kind = find_date(line)
            if not date:
                continue
            text = line.strip()
            if kind == "변경이력표" and re.match(r"^\|\s*-", text):
                continue
            iid = f"{skill.replace('history-', '')}:{i}"
            items.append({
                "id": iid,
                "date": date,
                "skill": skill,
                "line": i,
                "kind": kind,
                "status": status_of(text),
                "text": text,
            })
    doc = {
        "generated_by": "tools/extract_decisions.py",
        "sources": src,
        "count": len(items),
        "count_by_status": {s: sum(1 for x in items if x["status"] == s) for s in ("현행후보", "폐기후보", "보류후보")},
        "items": items,
    }
    with open(out, "w", encoding="utf-8") as fh:
        yaml.safe_dump(doc, fh, allow_unicode=True, sort_keys=False, width=10**6)
    print(f"{len(files)}개 스킬, {len(items)}건 추출 → {out}")
    print(doc["count_by_status"])


if __name__ == "__main__":
    main()
