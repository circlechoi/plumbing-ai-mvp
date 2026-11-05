"""스킬 10개(history-core + 9개)를 claude.ai에 한 번에 올릴 스킬 1개(history-circle)로 묶는다.

- SKILL.md = history-core 본문(읽는 순서만 guides 경로로 바꿈)
- guides/<스킬>.md = 각 스킬 SKILL.md 본문(앞머리 제외, 내용 그대로)
- guides/<스킬>/reference-*.md, archive/<스킬>.md = 그대로
내용은 바꾸지 않는다. 검사: 각 원천 파일 본문이 묶음 안에 그대로 있는지 확인.
사용: python3 tools/bundle_single.py  → dist/history-circle.zip
"""
import glob
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.dirname(HERE)
OUT = os.path.join(SK, "dist_single", "history-circle")

DESC = ("역사서클 채널(정체성 '그 판단은 왜 그랬을까?' — 역사/전략 시네마틱 해설)의 모든 제작 작업에 사용: "
        "롱폼(8~12분), 45초 신작·재편집 쇼츠, 전투 해설 쇼츠(70~140초, 삼국전투기식 지도·도식), 건축 '그 시절' 쇼츠, "
        "지도 컷(v4-S), 기획·주제 선정·고증·대본·콘티·Higgsfield 생성·렌더·업로드. 현행 값 원장·채점표·크레딧 전 확인 규칙 포함. "
        "'롱폼', '숏츠 만들어줘', '전투 해설', '○○ 전투 만들어줘', '그 시절 ○○', '다음 편', '/history-circle'.")


def body(path):
    t = open(path, encoding="utf-8").read()
    m = re.match(r"---\n.*?\n---\n", t, re.S)
    return t[m.end():] if m else t


def main():
    if os.path.exists(os.path.dirname(OUT)):
        shutil.rmtree(os.path.dirname(OUT))
    os.makedirs(os.path.join(OUT, "guides"))
    os.makedirs(os.path.join(OUT, "archive"))
    names = sorted(d for d in os.listdir(SK) if d.startswith("history-") and d != "history-core")
    core = body(os.path.join(SK, "history-core", "SKILL.md"))
    core = re.sub(r"(?m)^# 역사서클 핵심 \(history-core", "# 역사서클 (history-circle 단일 스킬 · 원천 history-core", core, count=1)
    note = ("\n> **단일 스킬 묶음 안내**: 이 문서에서 `history-<이름>` 스킬이라고 한 것은 이 스킬 안의 `guides/history-<이름>.md`다. "
            "그 스킬의 `reference-*.md`는 `guides/history-<이름>/`, `archive.md`는 `archive/history-<이름>.md`에 있다. "
            "포맷 작업 때는 이 문서 다음에 해당 guides 파일 1~2개만 읽는다.\n")
    core = core.replace("\n## 0. 읽는 순서", note + "\n## 0. 읽는 순서", 1)
    with open(os.path.join(OUT, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write('---\nname: "history-circle"\ndescription: "%s"\n---\n' % DESC.replace('"', "'") + core)
    for n in names:
        src = os.path.join(SK, n)
        with open(os.path.join(OUT, "guides", n + ".md"), "w", encoding="utf-8") as f:
            f.write(body(os.path.join(src, "SKILL.md")))
        refs = glob.glob(os.path.join(src, "reference-*.md"))
        if refs:
            os.makedirs(os.path.join(OUT, "guides", n))
            for r in refs:
                shutil.copy(r, os.path.join(OUT, "guides", n, os.path.basename(r)))
        a = os.path.join(src, "archive.md")
        if os.path.exists(a):
            shutil.copy(a, os.path.join(OUT, "archive", n + ".md"))
    # 검사: 원천 본문이 그대로 있는지
    miss = []
    for n in names:
        if open(os.path.join(OUT, "guides", n + ".md"), encoding="utf-8").read() != body(os.path.join(SK, n, "SKILL.md")):
            miss.append(n)
    if len(DESC) > 1024:
        miss.append("description 1024자 초과")
    zp = os.path.join(SK, "dist", "history-circle.zip")
    if os.path.exists(zp):
        os.remove(zp)
    subprocess.run(["zip", "-qr", zp, "history-circle"], cwd=os.path.dirname(OUT), check=True)
    print("묶음:", len(names) + 1, "개 스킬 → history-circle.zip", os.path.getsize(zp), "바이트, description", len(DESC), "자")
    print("SKILL.md", os.path.getsize(os.path.join(OUT, "SKILL.md")), "바이트")
    if miss:
        print("[실패]", miss)
        sys.exit(1)
    print("[통과] 원천 본문 9개 그대로")


if __name__ == "__main__":
    main()
