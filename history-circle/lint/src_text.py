"""렌더 소스·화면 문자열 검사: 남은 태그(qa.py 통합) + 금지 기호.

사용: python3 src_text.py 파일·폴더 ...   (.py .json .ass .srt .txt)
 - 남은 태그(실패): '[기록]·[통설]·[해석]·[연출]' 문자열, '(통설)'·'(해석)'·'(연출)', '개념도'
   — 11/04 확정 C5: 화면 태그·칩은 전 포맷에서 삭제. 주석 줄과 tag_rec(·chip( 호출 줄은 qa.py처럼 제외.
 - 금지 기호(실패): 따옴표 안 문자열의 '·', '『', '』', '→' — 글꼴(JUA·BlackHanSans 등)에 없어 □로 렌더.
   .py는 따옴표 안만 본다(주석·독스트링 줄 제외). .json/.ass/.srt는 값 전체.
근거: thresholds.json src_text
"""
import argparse
import os
import re

from common import emit, result, th

CHECK = "src_text"
EXTS = (".py", ".json", ".ass", ".srt", ".txt")
TAG_RE = re.compile(r"""['"]\[(기록|통설|해석|연출)[^'"\]]*\]|\((통설|해석|연출)\)|개념도['"]""")
TAG_RE_TEXT = re.compile(r"\[(기록|통설|해석|연출)[^\]]*\]|\((통설|해석|연출)\)|개념도")
STR_RE = re.compile(r"""'([^'\\\n]*(?:\\.[^'\\\n]*)*)'|"([^"\\\n]*(?:\\.[^"\\\n]*)*)\"""")


def _files(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                for n in sorted(names):
                    if n.endswith(EXTS):
                        yield os.path.join(root, n)
        elif p.endswith(EXTS):
            yield p


def check(paths):
    symbols = th(CHECK, "forbidden_symbols")
    viol, files = [], 0
    for f in _files(paths):
        files += 1
        py = f.endswith(".py")
        in_doc = False
        for n, line in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
            s = line.strip()
            if py:
                if s.count('"""') == 1 or s.count("'''") == 1:
                    in_doc = not in_doc
                    continue
                if in_doc or s.startswith("#") or s.startswith('"""') or s.startswith("'''"):
                    continue
            if (TAG_RE if py else TAG_RE_TEXT).search(line) and "tag_rec(" not in line and "chip(" not in line:
                viol.append({"what": "남은 태그", "file": f, "line": n, "text": s[:120]})
            strings = [a or b for a, b in STR_RE.findall(line)] if py else [line]
            for st in strings:
                bad = [c for c in symbols if c in st]
                if bad:
                    viol.append({"what": "금지 기호", "symbols": bad, "file": f, "line": n, "text": s[:120]})
                    break
    return result(CHECK, not viol, viol, {"files": files}, target=list(paths))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    emit(check(ap.parse_args().paths))
