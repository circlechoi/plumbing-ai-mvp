"""역사서클 스킬 재구조화 — 원본 스킬 9개를 core + (현행 SKILL.md / archive.md)로 나눈다.

원본은 읽기만 한다. 줄을 지우지 않고 옮기기만 한다(검증: verify_skills.py).
입력: patches/plan.yaml(이동할 절·줄), patches/replacements.yaml(원장과 다른 표기 교체),
      patches/core_template.md, ../../decisions/decisions.yaml, ../../kit/**
출력: ../<스킬>/SKILL.md, ../<스킬>/archive.md, ../history-core/SKILL.md, ../replacements.json, ../moves.json

사용: python3 tools/build_skills.py [원본 스킬 폴더 glob]
"""
import glob
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)  # history-circle/skills
HC = os.path.dirname(OUT)    # history-circle
SRC_GLOB = sys.argv[1] if len(sys.argv) > 1 else "/root/.claude/skills/synced/*"
FENCE = re.compile(r"^\s*```")
HEAD = re.compile(r"^(#{1,6}) (.*)$")
MIN_CODE_LINES = 8

POINTER = ("> **history-core를 먼저 읽는다.** 현행 값은 원장(decisions.yaml) 하나뿐 — 이 본문과 다르면 원장 우선. "
           "폐기·보류·편별 이력·변경 이력 원문은 같은 폴더 `archive.md`(규칙으로 따르지 않음).")


def load(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def kit_index():
    idx = {}
    for p in glob.glob(os.path.join(HC, "kit", "**", "*"), recursive=True):
        if os.path.isfile(p) and not p.endswith(".md"):
            rel = os.path.relpath(p, HC)
            for ln in open(p, encoding="utf-8", errors="replace").read().splitlines():
                idx.setdefault(ln.rstrip(), set()).add(rel)
    return idx


def find_src(name):
    ps = glob.glob(os.path.join(SRC_GLOB, name, "SKILL.md"))
    if not ps:
        sys.exit("원본 스킬 없음: " + name)
    return ps[0]


def structure(lines):
    """코드 밖 제목 목록과 각 줄의 코드 여부."""
    heads, in_code, code = [], False, []
    for i, ln in enumerate(lines):
        if FENCE.match(ln):
            code.append(True)
            in_code = not in_code
            continue
        code.append(in_code)
        m = HEAD.match(ln)
        if m and not in_code:
            heads.append((i, len(m.group(1)), m.group(2)))
    return heads, code


def section_span(heads, i_head, n, children=True):
    start, lvl, _ = heads[i_head]
    for j in range(i_head + 1, len(heads)):
        if heads[j][1] <= lvl or not children:
            return start, heads[j][0]
    return start, n


def transform(seg, off, name, reps, prec_re, prec_new, kidx, rep_log, arch_reps, moves):
    """유지되는 줄 묶음: 코드 블록은 kit 참조로, 원장과 다른 표기는 교체(원문은 archive)."""
    out, i, n = [], 0, len(seg)
    while i < n:
        ln = seg[i]
        if FENCE.match(ln):
            j = i + 1
            while j < n and not FENCE.match(seg[j]):
                j += 1
            inner = [x.rstrip() for x in seg[i + 1:j] if x.strip()]
            if len(inner) >= MIN_CODE_LINES and all(x in kidx for x in inner):
                cnt = {}
                for x in inner:
                    for f in kidx[x]:
                        cnt[f] = cnt.get(f, 0) + 1
                best = max(cnt, key=cnt.get)
                out.append(f"> 〔코드 {len(inner)}줄(원본 {off + i + 1}–{off + j + 1}줄) → `history-circle/{best}` — 같은 내용이 kit에 그대로 있음(verify_skills.py)〕")
                moves.append({"skill": name, "kind": "code→kit", "lines": [off + i + 1, off + j + 1], "kit": best})
                i = j + 1
                continue
            out.extend(seg[i:j + 1])
            i = j + 1
            continue
        new = ln
        if re.search(prec_re, ln):
            new = prec_new
        for r in reps:
            if r["skill"] == name and r["line_has"] in new and r["old"] in new:
                new = new.replace(r["old"], r["new"])
        if new != ln:
            rep_log.append({"skill": name, "line": off + i + 1, "original": ln, "new": new})
            arch_reps.append((off + i + 1, ln))
        out.append(new)
        i += 1
    return out


def build_one(name, plan, reps, prec_re, prec_new, kidx):
    src = find_src(name)
    lines = open(src, encoding="utf-8").read().split("\n")
    n = len(lines)
    heads, _ = structure(lines)
    # frontmatter
    fm_end = 0
    if lines and lines[0].strip() == "---":
        fm_end = lines.index("---", 1) + 1 if "---" in lines[1:] else 0
    action = [None] * n  # None=유지, ('sec', k) 이동, ('line', reason)
    moves, sec_stub = [], {}
    for k, ms in enumerate(plan.get("move_sections") or []):
        hits = [i for i, h in enumerate(heads) if h[2].startswith(ms["heading"])]
        if len(hits) != 1:
            sys.exit(f"{name}: 제목 '{ms['heading']}' 일치 {len(hits)}개")
        a, b = section_span(heads, hits[0], n, ms.get("children", True))
        if any(action[i] is not None for i in range(a, b)):
            sys.exit(f"{name}: 절 '{ms['heading']}'이 다른 이동과 겹침 — children:false 또는 순서 조정")
        for i in range(a, b):
            if action[i] is None:
                action[i] = ("sec", k)
        sec_stub[a] = (k, ms, a, b)
        moves.append({"skill": name, "kind": "section", "to": ms.get("to", "archive.md"), "heading": heads[hits[0]][2], "lines": [a + 1, b], "reason": ms["reason"]})
    # 줄 이동(코드 밖)
    _, code = structure(lines)
    for ml in plan.get("move_lines") or []:
        rx = re.compile(ml["regex"])
        for i in range(fm_end, n):
            if action[i] is None and not code[i] and rx.search(lines[i]):
                action[i] = ("line", ml["reason"])
                moves.append({"skill": name, "kind": "line", "line": i + 1, "reason": ml["reason"]})

    skill_out, arch_out, rep_log, arch_moved_lines, arch_reps = [], [], [], [], []
    refs = {}  # 파일명 → 줄 목록(현행 규칙, 필요할 때만 읽음)
    skill_out.extend(lines[:fm_end])
    skill_out.append("")
    skill_out.append(POINTER)
    i = fm_end
    first_line_stub_done = False
    while i < n:
        act = action[i]
        if act and act[0] == "sec":
            k, ms, a, b = sec_stub[i]
            title = lines[a].lstrip("#").strip()
            if ms.get("to"):
                ref = refs.setdefault(ms["to"], [])
                skill_out.append(f"> 〔현행 규칙 — `{ms['to']}`에 있음: '{title}'. {ms['reason']} 때만 읽는다〕")
                seg = transform(lines[a:b], a, name, reps, prec_re, prec_new, kidx, rep_log, arch_reps, moves)
                ref += [f"<!-- 원본 {a + 1}–{b}줄 -->"] + seg + [""]
                i = b
                continue
            skill_out.append(f"> 〔archive.md로 이동: '{title}' — {ms['reason']}〕")
            arch_out.append(f"## 〔원래 위치: 원본 {a + 1}–{b}줄〕 {title}")
            arch_out.append(f"> 이동 이유: {ms['reason']}")
            arch_out.append("")
            arch_out.extend(lines[a:b])
            arch_out.append("")
            i = b
            continue
        if act and act[0] == "line":
            arch_moved_lines.append((i + 1, lines[i], act[1]))
            if not first_line_stub_done:
                skill_out.append(f"> 〔{act[1]} — archive.md '머리말에서 옮긴 줄'〕")
                first_line_stub_done = True
            i += 1
            continue
        # 연속된 '유지' 구간을 한 번에 변환
        j = i
        while j < n and action[j] is None:
            j += 1
        skill_out += transform(lines[i:j], i, name, reps, prec_re, prec_new, kidx, rep_log, arch_reps, moves)
        i = j

    # archive 머리
    head = [f"# {name} — archive (원문 보관 · 11/04 재구조화)", "",
            "> 이 파일은 **규칙으로 따르지 않는다.** 폐기·보류·편별 이력·변경 이력·교체 전 원문을 줄 그대로 보관한다. 현행 값은 원장(history-core).", ""]
    if arch_reps:
        head += ["## 교체 원문 (원장 반영으로 SKILL.md에서 바뀐 줄)", ""]
        for ln_no, t in arch_reps:
            head += [f"- 원본 {ln_no}줄:", "", t, ""]
    if arch_moved_lines:
        head += ["## 머리말에서 옮긴 줄", ""]
        for ln_no, t, why in arch_moved_lines:
            head += [f"<!-- 원본 {ln_no}줄 · {why} -->", t, ""]
    archive = head + arch_out
    os.makedirs(os.path.join(OUT, name), exist_ok=True)
    with open(os.path.join(OUT, name, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(skill_out).rstrip("\n") + "\n")
    for fn, body in refs.items():
        with open(os.path.join(OUT, name, fn), "w", encoding="utf-8") as f:
            f.write("\n".join([f"# {name} — {fn} (현행 규칙 · 필요할 때만 읽음 · 11/04 재구조화)", "",
                                "> history-core → SKILL.md를 먼저 읽는다. 이 파일의 규칙은 현행이다(원장과 다르면 원장 우선).", ""] + body).rstrip("\n") + "\n")
    with open(os.path.join(OUT, name, "archive.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(archive).rstrip("\n") + "\n")
    used = {r["old"] for r in reps if r["skill"] == name} - {r["old"] for r in reps if r["skill"] == name and any(r["old"] in x["original"] for x in rep_log)}
    if used:
        sys.exit(f"{name}: 적용 안 된 교체 {used}")
    return rep_log, moves


def build_core():
    led = load(os.path.join(HC, "decisions", "decisions.yaml"))
    tpl = open(os.path.join(HERE, "patches", "core_template.md"), encoding="utf-8").read()
    concept = open(find_src("history-channel-concept"), encoding="utf-8").read().split("\n")
    a = concept.index("## 1. 정체성") + 1
    b = next(i for i in range(a, len(concept)) if concept[i].startswith("## "))
    keep = ("- [확정] 한 문장", "- [확정] 장르", "- [확정 10/7] **내용의 구성과 영상미", "- [확정] **듣기만 해도",
            "- [확정 10/9] **상대를 바보로", "- [확정 10/10] **기록이 한 줄이어도", "- 무엇이 아닌가")
    ident = "\n".join(x for x in concept[a:b] if x.startswith(keep))
    ident += "\n- (나머지 정체성 항목: history-channel-concept 1절)"
    rows = []
    for tp in led["topics"]:
        if not tp["items"]:
            continue
        rows.append(f"\n**{tp['name']}**\n")
        rows.append("| 항목 | 현행 값 |")
        rows.append("|---|---|")
        for it in tp["items"]:
            cur = str(it["current"]).replace("|", "\\|").replace("\n", " ")
            st = it.get("status", "현행")
            cf = str(it.get("confirmed") or "")
            mark = (" ★" + (cf[:5] if cf[:2].isdigit() else "11/04")) if cf else ("" if st == "현행" else f" ({st})")
            rows.append(f"| {it['key']}{mark} | {cur} |")
    c = led["counts"]
    meta = led["meta"]
    out = (tpl.replace("{{IDENTITY}}", ident)
           .replace("{{PRINCIPLE}}", "  > " + str(meta["principle"]).strip().replace("\n", " "))
           .replace("{{USER_OVER_REVIEW}}", "- " + str(meta["user_over_review"]).strip().replace("\n", " "))
           .replace("{{COUNTS}}", f"{c['curated_items']}항목 · 원문 {c['raw_total']}건 연결 · 확정 대기 {c['pending_user']}")
           .replace("{{LEDGER}}", "\n".join(rows)))
    os.makedirs(os.path.join(OUT, "history-core"), exist_ok=True)
    with open(os.path.join(OUT, "history-core", "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(out)


def main():
    plan = load(os.path.join(HERE, "patches", "plan.yaml"))
    reps = load(os.path.join(HERE, "patches", "replacements.yaml"))
    kidx = kit_index()
    all_reps, all_moves = [], []
    for name, p in plan["skills"].items():
        r, m = build_one(name, p or {}, reps, plan["precedence_regex"], plan["precedence_new"], kidx)
        all_reps += r
        all_moves += m
    build_core()
    json.dump(all_reps, open(os.path.join(OUT, "replacements.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(all_moves, open(os.path.join(OUT, "moves.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"교체 {len(all_reps)}줄 · 이동 {len(all_moves)}건")


if __name__ == "__main__":
    main()
