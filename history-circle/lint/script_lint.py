"""대본 텍스트 검사.

사용: python3 script_lint.py script.txt [--format battle|shorts|longform|architecture]
대본 형식:
 - 문단 = 빈 줄로 구분. 장면 = '#'로 시작하는 줄, '---', '[장면 …]' 줄로 구분(없으면 전체가 한 장면).
 - '인물: 가, 나, 다' 줄이 있으면 새 인물 수를 센다(없으면 경고만).
 - '화면:', '라벨:', '자막:', '제목:', '[화면]'으로 시작하는 줄은 화면 문자열 → 금지 기호 검사. 내레이션 검사에서는 뺀다.
검사(실패 / 경고는 thresholds.json script_lint의 포맷별 설정):
 - '~것입니다'로 맺는 문단 편당 3회 초과(롱폼 원문 규칙).
 - 과거형 ㅆ 어미, 연도로 시작하는 문장, 문장당 쉼표 2개 이상, 새 인물 5명 초과(battle-shorts 대본 점검).
 - 라디오 기준 금지어('여기', '이쪽', '보시는 것처럼'), 동화식 도입('옛날 옛적' 등).
 - 화면 문자열 금지 기호(·, 『, 』, →).
 - 동화적 표현 의심어(임시 목록, 경고만).
근거: thresholds.json script_lint
"""
import argparse
import re

from common import emit, result, th

CHECK = "script_lint"
SCREEN_PREFIX = ("화면:", "라벨:", "자막:", "제목:", "[화면]")
SCENE_RE = re.compile(r"^\s*(#|---|\[장면)")
SENT_RE = re.compile(r"[^.?!…\n]+[.?!…]*")
YEAR_START_RE = re.compile(r"^\s*[\"'“‘(]?\s*((기원전|서기|BC|AD)\s*)?[0-9０-９一二三四五六七八九十百千]+\s*년")


def _has_ss(ch):
    """한글 음절의 받침이 ㅆ인가."""
    o = ord(ch) - 0xAC00
    return 0 <= o < 11172 and o % 28 == 20


def _past_ss(sentence):
    """'~었습니다/았습니다/했다/였다'처럼 ㅆ 받침 어미로 끝나는 문장."""
    s = re.sub(r"[\s\"'”’)\].?!…,]+$", "", sentence)
    m = re.search(r"([가-힣]+)$", s)
    if not m:
        return False
    w = m.group(1)
    for tail in ("습니다", "습니까", "다", "지요", "죠", "어요", "어", "고"):
        if w.endswith(tail) and len(w) > len(tail):
            ch = w[-len(tail) - 1]
            if _has_ss(ch) and ch not in ("있", "겠"):  # 있습니다(현재)·하겠습니다(미래)는 과거형 아님
                return True
    return False


def parse(text):
    scenes, paras, people, screen = [[]], [], None, []
    cur = []
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if line.startswith("인물:"):
            people = [p.strip() for p in re.split(r"[,，、/]", line[3:]) if p.strip()]
            continue
        if line.startswith(SCREEN_PREFIX):
            screen.append((n, line))
            continue
        if SCENE_RE.match(raw):
            if cur:
                paras.append(cur)
                scenes[-1].append(cur)
                cur = []
            scenes.append([])
            continue
        if not line:
            if cur:
                paras.append(cur)
                scenes[-1].append(cur)
                cur = []
            continue
        cur.append((n, line))
    if cur:
        paras.append(cur)
        scenes[-1].append(cur)
    return [s for s in scenes if s], paras, people, screen


def _cfg(fmt):
    c = th(CHECK, "format_rules")
    return c.get(fmt, c["shorts"])


def check(path, fmt="shorts"):
    text = open(path, encoding="utf-8").read()
    scenes, paras, people, screen = parse(text)
    rules = _cfg(fmt)
    viol, warn = [], []

    def put(rule, item):
        lvl = rules.get(rule, "warn")
        if lvl == "fail":
            viol.append(dict(item, rule=rule))
        elif lvl == "warn":
            warn.append(dict(item, rule=rule))

    # 1) '것입니다' 문단 맺음
    endings = []
    for p in paras:
        last = re.sub(r"[\s\"'”’)\]]+$", "", p[-1][1])
        if re.search(r"것입니다[.!?…]*$", last):
            endings.append(p[-1][0])
    total_geot = len(re.findall(r"것입니다", text))
    if len(endings) > th(CHECK, "max_geot_endings"):
        put("geot_endings", {"what": "'~것입니다'로 맺는 문단 %d회(편당 %d회 이하)" % (len(endings), th(CHECK, "max_geot_endings")),
                             "lines": endings})

    # 문장 단위
    sents = []
    for p in paras:
        for n, line in p:
            for m in SENT_RE.finditer(line):
                s = m.group(0).strip()
                if s:
                    sents.append((n, s))
    past = [(n, s) for n, s in sents if _past_ss(s)]
    for n, s in past:
        put("past_ss", {"what": "과거형 ㅆ 어미", "line": n, "text": s[:80]})
    for n, s in sents:
        if YEAR_START_RE.match(s):
            put("year_start", {"what": "연도로 시작하는 문장", "line": n, "text": s[:80]})
        if s.count(",") + s.count("，") > th(CHECK, "max_commas_per_sentence"):
            put("commas", {"what": "문장당 쉼표 %d개 초과" % th(CHECK, "max_commas_per_sentence"), "line": n,
                           "text": s[:80]})
        for w in th(CHECK, "radio_banned"):
            if re.search(r"(?<![가-힣])" + re.escape(w), s):
                put("radio_banned", {"what": "라디오 기준 금지어 '%s'" % w, "line": n, "text": s[:80]})
        for w in th(CHECK, "fairytale_openings"):
            if w in s:
                put("fairytale_opening", {"what": "동화식 도입 '%s'" % w, "line": n, "text": s[:80]})
        for w in th(CHECK, "fairytale_suspects"):
            if re.search(w, s):
                put("fairytale_suspect", {"what": "동화적 표현 의심(임시 목록) '%s'" % w, "line": n, "text": s[:80]})

    # 훅 문장 수 (원장 opening_hook: 쇼츠 2문장)
    if scenes:
        hook = [m.group(0).strip() for p in scenes[0] for _, line in p for m in SENT_RE.finditer(line) if m.group(0).strip()]
        if len(hook) > th(CHECK, "max_hook_sentences"):
            put("hook_sentences", {"what": "훅(장면 1) %d문장(%d문장 이하)" % (len(hook), th(CHECK, "max_hook_sentences")),
                                   "text": " / ".join(h[:30] for h in hook)})

    # 같은 어미 연속·평서 '~다.' (원장 narration_style)
    tail = th(CHECK, "same_ending_tail")
    prev = None
    for n, s in sents:
        h = re.sub(r"[^가-힣]", "", s)
        e = h[-tail:] if len(h) >= tail else None
        if e and e == prev:
            put("same_ending", {"what": "같은 어미 연속 '%s'" % e, "line": n, "text": s[:80]})
        if h.endswith("다") and not h.endswith("니다") and re.search(r"다[.!…]*\s*$", s):
            put("plain_da", {"what": "평서 '~다.' 종결", "line": n, "text": s[:80]})
        prev = e

    # 새 인물 수
    if people is None:
        warn.append({"what": "'인물:' 줄 없음 — 새 인물 수 검사 건너뜀", "rule": "people"})
    elif len(people) > th(CHECK, "max_new_people"):
        put("people", {"what": "새 인물 %d명(%d명 이하)" % (len(people), th(CHECK, "max_new_people")),
                       "people": people})

    # 화면 문자열 금지 기호
    for n, line in screen:
        bad = [c for c in th(CHECK, "forbidden_symbols") if c in line]
        if bad:
            put("forbidden_symbols", {"what": "화면 문자열 금지 기호", "symbols": bad, "line": n, "text": line[:80]})

    return result(CHECK, not viol, viol,
                  {"format": fmt, "scenes": len(scenes), "paragraphs": len(paras), "sentences": len(sents),
                   "geot_total": total_geot, "geot_endings": len(endings),
                   "past_ss_ratio": round(len(past) / max(1, len(sents)), 2),
                   "people": None if people is None else len(people)},
                  warnings=warn, target=path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--format", default="shorts", choices=["battle", "shorts", "longform", "architecture"])
    a = ap.parse_args()
    emit(check(a.path, a.format))
