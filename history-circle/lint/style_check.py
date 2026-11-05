#!/usr/bin/env python3
"""스타일 검사기 v1 — 렌더 프레임과 코드가 style/style.json(스타일 키트)에서 벗어났는지 자동 검출한다.

검사
1. tokens : style.json 세력 색 = 원장(decisions.yaml faction_colors·unit_faction_colors) = components/spec.json
2. code   : 편 코드가 폰트·색·크기를 직접 쓰는지(ImageFont.truetype, RGB 리터럴, engine size= 인자, 새 그리기 함수)
3. frame  : 렌더 PNG의 화면 틀 — 상단 띠·제목 띠·범례 띠 색, 띠 경계 위치, 자막 글자 중심 y·높이, 오른쪽 x>900 표식
            (+ 기준 프레임 F1과 띠 영역 픽셀 비교)
4. layout : cv.elements(layout json)의 글자 최소 크기·금지 영역 — 기존 lint/layout_overlap.py에 맡기고 여기서는 x>900만
5. sheet  : 렌더 프레임을 기준 세트(golden/style_ref)와 나란히 놓은 비교 시트(--sheet out.jpg)

사용
  python3 style_check.py tokens
  python3 style_check.py code <파일 또는 폴더>...
  python3 style_check.py frame <png>... [--caption "자막 문장"] [--sheet out.jpg] [--json out.json]
하나라도 실패하면 exit 1. 실패하면 사용자에게 보이기 전에 고친다(원장 gates).
"""
import argparse
import glob
import json
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from style import kit  # noqa: E402

S = kit.S
REF = os.path.join(ROOT, "golden", "style_ref")
TH = {"band_color_tol": 14, "band_ref_diff_pct": 2.0, "caption_cy_tol": 14, "caption_h_tol": 0.15, "edge_tol": 3}


def _rgb_list(text):
    out = {}
    for name, r, g, b in re.findall(r"([가-힣]+)(?:\s[가-힣]+)?\s*\((\d+),\s*(\d+),\s*(\d+)\)", text):
        out.setdefault(name, [int(r), int(g), int(b)])
    return out


# ---------------- 1. 토큰 ----------------

def check_tokens():
    import yaml
    led = yaml.safe_load(open(os.path.join(ROOT, "decisions", "decisions.yaml"), encoding="utf-8"))
    items = {i["key"]: i for t in led["topics"] for i in t["items"]}
    res = []
    for key, sect in (("faction_colors", "faction"), ("unit_faction_colors", "unit_faction")):
        want = _rgb_list(items[key]["current"].split("낙랑과 당이")[0])
        have = {k: v for k, v in S["colors"][sect].items() if not k.startswith("_")}
        for name, rgb in want.items():
            ok = have.get(name) == rgb
            res.append({"check": f"tokens.{sect}.{name}", "ok": ok, "want": rgb, "have": have.get(name)})
    spec = json.load(open(os.path.join(ROOT, "components", "spec.json"), encoding="utf-8"))
    ids = S["colors"]["faction_ids"]
    for name, fid in ids.items():
        if name.startswith("_"):
            continue
        ok = spec["palette"]["unit_faction"].get(fid) == S["colors"]["unit_faction"].get(name)
        res.append({"check": f"tokens.spec.{fid}", "ok": ok, "want": S["colors"]["unit_faction"].get(name),
                    "have": spec["palette"]["unit_faction"].get(fid)})
    for key in ("jua", "nsk", "bhs"):
        p = os.path.join(ROOT, S["fonts"][key]["file"])
        res.append({"check": f"tokens.font.{key}", "ok": os.path.exists(p), "have": S["fonts"][key]["file"]})
    return res


# ---------------- 2. 코드 ----------------

CODE_RULES = [
    ("font_direct", re.compile(r"ImageFont\.truetype\("), "폰트를 직접 연다 → style.kit.font(type_scale 키)"),
    ("rgb_literal", re.compile(r"\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*(,\s*\d{1,3}\s*)?\)"), "RGB 숫자를 직접 쓴다 → style.json colors 이름"),
    ("size_arg", re.compile(r"\bE\.(label|bubble|lord|gauge)\([^)]*\b(size|r|w)\s*=\s*\d"), "엔진 부품에 크기를 직접 준다(무시됨) → 인자 삭제"),
    ("raw_draw", re.compile(r"\.(rounded_rectangle|ellipse|polygon|text)\("), "편 코드에서 새 그림을 직접 그린다 → style/parts.py에 부품으로 등록 후 사용"),
]
CODE_ALLOW = ("style/", "components/", "animatic/engine.py", "lint/", "decisions/", "skills/")


def check_code(paths):
    files = []
    for p in paths:
        files += sorted(glob.glob(os.path.join(p, "**", "*.py"), recursive=True)) if os.path.isdir(p) else [p]
    res = []
    seen = set()
    for f in files:
        real = os.path.realpath(f)
        if real in seen:
            continue
        seen.add(real)
        rel = os.path.relpath(real, ROOT).replace(os.sep, "/")
        if rel.startswith(CODE_ALLOW):
            continue
        for n, line in enumerate(open(f, encoding="utf-8"), 1):
            s = line.split("#")[0]
            for rid, rx, msg in CODE_RULES:
                if rx.search(s):
                    res.append({"check": f"code.{rid}", "ok": False, "where": f"{rel}:{n}", "msg": msg, "line": line.strip()[:120]})
    if not res:
        res.append({"check": "code", "ok": True, "files": len(files)})
    return res


# ---------------- 3. 프레임 ----------------

def _band_color(a, box, avoid_text=True):
    x0, y0, x1, y1 = box
    reg = a[y0:y1, x0:x1].reshape(-1, 3).astype(int)
    if avoid_text:
        # 가장 흔한 색(배경) — 글자 픽셀 제외
        q = (reg // 4) * 4
        vals, cnt = np.unique(q, axis=0, return_counts=True)
        return vals[cnt.argmax()].tolist()
    return reg.mean(axis=0).round().astype(int).tolist()


def _expect(fill, alpha, under=None):
    c = np.array(kit.color(fill), float)
    if under is None:
        return c.round().astype(int).tolist()
    return (c * alpha / 255 + np.array(under, float) * (1 - alpha / 255)).round().astype(int).tolist()


def _edge(a, x, y0, y1):
    """세로선 x에서 y0~y1 사이 밝기 급변 지점."""
    col = a[y0:y1, x].astype(float).mean(axis=1)
    return int(y0 + np.argmax(np.abs(np.diff(col))) + 1)


def check_frame(png, caption=None, ref=None):
    F = S["frame"]
    im = Image.open(png).convert("RGB")
    a = np.asarray(im)
    res = []
    name = os.path.basename(png)
    if im.size != (F["canvas"]["w"], F["canvas"]["h"]):
        return [{"check": f"frame.size[{name}]", "ok": False, "have": im.size}]

    # 띠 색(배경 최빈색) — 반투명 띠는 아래 지도에 따라 조금 달라지므로 허용 오차 band_color_tol
    tb, ti, lb = F["top_band"], F["title_band"], F["legend_band"]
    for key, box, fill, al, sub in (("top_band", (300, 10, 780, 130), tb["fill"], tb["alpha"], None),
                                    ("title_band", (0, 146, 1080, 230), ti["fill"], ti["alpha"], None),
                                    ("legend_band", (420, 1710, 1080, 1900), lb["fill"], lb["alpha"], None)):
        have = _band_color(a, box)
        want = _expect(fill, al, sub)
        # 반투명 띠: 아래 지도가 (255-alpha)/255만큼 비친다 → 허용 범위 [want-tol, want+(255-alpha)+tol] (밝은 띠는 반대 방향)
        under = 255 - al
        dark = sum(want) < 384
        ok = all((w - TH["band_color_tol"] <= h <= w + under + TH["band_color_tol"]) if dark else (w - under - TH["band_color_tol"] <= h <= w + TH["band_color_tol"]) for h, w in zip(have, want))
        res.append({"check": f"frame.{key}.color[{name}]", "ok": ok, "want": want, "have": have})

    # 띠 경계 위치(제목 띠 위·아래, 범례 띠 위)
    for key, x, y0, y1, want in (("title_top", 8, 120, 160, ti["bbox"][1]), ("title_bottom", 8, 216, 256, ti["bbox"][3]),
                                 ("legend_top", 8, 1580, 1620, lb["bbox"][1])):
        e = _edge(a, x, y0, y1)
        res.append({"check": f"frame.{key}.y[{name}]", "ok": abs(e - want) <= TH["edge_tol"], "want": want, "have": e})

    # 자막: 흰 글자(>235) 행 범위 → 중심 y·글자 높이
    c = F["caption"]
    band = a[1270:1580, 60:1020]
    white = (band.min(axis=2) > 235)
    rr = np.where(white.sum(axis=1) > 6)[0]
    # 흰 글자 행을 덩어리로 나눠 자막 중심(1420) 근처 덩어리만 자막으로 본다
    groups, cur = [], []
    for y in rr:
        if cur and y - cur[-1] > 10:
            groups.append(cur); cur = []
        cur.append(y)
    if cur:
        groups.append(cur)
    near = [g for g in groups if abs(1270 + (g[0] + g[-1]) / 2 - c["center_y"]) <= c["line_gap"] * 1.2]
    rows = np.array([y for g in near for y in g])
    others = [g for g in groups if g not in near]
    if others:
        res.append({"check": f"frame.caption.band_clear[{name}]", "ok": False, "msg": "자막 띠(1270~1580)에 자막 외 흰 글자", "rows": [[1270 + g[0], 1270 + g[-1]] for g in others]})
    if caption is not None:
        if len(rows) == 0:
            res.append({"check": f"frame.caption.present[{name}]", "ok": False})
        else:
            lines = 1 if (rows[-1] - rows[0]) < c["line_gap"] * 0.9 else 2
            cy = 1270 + (rows[0] + rows[-1]) / 2
            res.append({"check": f"frame.caption.center_y[{name}]", "ok": abs(cy - c["center_y"]) <= TH["caption_cy_tol"], "want": c["center_y"], "have": round(cy, 1), "lines": lines})
            if lines == 1:
                f = kit.font(c["type"])
                l, t_, r_, b_ = ImageDraw.Draw(Image.new("L", (10, 10))).textbbox((0, 0), caption, font=f, anchor="mm")
                want_h = b_ - t_
                have_h = rows[-1] - rows[0] + 1
                res.append({"check": f"frame.caption.glyph_h[{name}]", "ok": abs(have_h - want_h) / want_h <= TH["caption_h_tol"], "want": want_h, "have": int(have_h)})

    # 기준 프레임 F1과 띠 영역 비교(글자 위치까지)
    if ref:
        r = np.asarray(Image.open(ref).convert("RGB")).astype(int)
        for key, box in (("top", (0, 0, 1080, 140)), ("legend_chips", (0, 1600, 300, 1700))):
            x0, y0, x1, y1 = box
            diff = np.abs(r[y0:y1, x0:x1] - a[y0:y1, x0:x1].astype(int)).max(axis=2)
            # 1px 안티에일리어싱 차이는 무시: 3×3 최솟값 필터 뒤에도 남는 차이만 센다
            from PIL import ImageFilter
            dm = np.asarray(Image.fromarray((diff > 40).astype(np.uint8) * 255).filter(ImageFilter.MinFilter(3))) > 0
            pct = float(dm.mean() * 100)
            res.append({"check": f"frame.ref.{key}[{name}]", "ok": pct <= TH["band_ref_diff_pct"], "have_pct": round(pct, 2)})
    return res


# ---------------- 4. 레이아웃 ----------------

def check_layout(path):
    doc = json.load(open(path, encoding="utf-8"))
    x_max = S["frame"]["safe"]["right_ui_x"]
    res = []
    for sc in doc.get("scenes", []):
        for el in sc.get("elements", []):
            if el.get("kind") in ("label", "block", "icon", "badge"):
                x, y, w, h = el["bbox"]
                if x + w > x_max + 1 and 236 < y < 1270:
                    res.append({"check": f"layout.right_ui[{sc['id']}:{el['id']}]", "ok": False, "have": round(x + w), "want": f"<= {x_max}"})
    if not res:
        res.append({"check": f"layout.right_ui[{os.path.basename(path)}]", "ok": True})
    return res


# ---------------- 5. 비교 시트 ----------------

def sheet(pngs, out, labels=None, width=360):
    refs = [("F1 틀 (4편)", "f1_ep4_40s.png"), ("R1 지도 (1편)", "ep1_21s.png"), ("R3 말풍선 (1편)", "ep1_46s.png"), ("R4 도식 (1편)", "ep1_61s.png")]
    items = [(l, os.path.join(REF, f)) for l, f in refs if os.path.exists(os.path.join(REF, f))]
    items += [(labels[i] if labels else os.path.basename(p), p) for i, p in enumerate(pngs)]
    h = int(width * 1920 / 1080)
    W = len(items) * (width + 10)
    sh = Image.new("RGB", (W, h + 50), (20, 20, 20))
    d = ImageDraw.Draw(sh)
    f = kit.font("legend_note", size=30)
    for i, (lab, p) in enumerate(items):
        sh.paste(Image.open(p).convert("RGB").resize((width, h)), (i * (width + 10), 50))
        d.text((i * (width + 10) + 6, 8), lab, font=f, fill=(240, 220, 150) if i < len(refs) else (255, 255, 255))
    sh.save(out, quality=82)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["tokens", "code", "frame", "layout"])
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--caption", action="append", help="frame 순서대로 자막 문장(없으면 자막 검사 생략)")
    ap.add_argument("--ref", default=os.path.join(REF, "f1_ep4_40s.png"))
    ap.add_argument("--sheet")
    ap.add_argument("--labels", nargs="*")
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.mode == "tokens":
        res = check_tokens()
    elif a.mode == "code":
        res = check_code(a.paths)
    elif a.mode == "layout":
        res = [r for p in a.paths for r in check_layout(p)]
    else:
        res = []
        for i, p in enumerate(a.paths):
            cap = a.caption[i] if a.caption and i < len(a.caption) else None
            res += check_frame(p, caption=cap, ref=a.ref if os.path.exists(a.ref) else None)
        if a.sheet:
            sheet(a.paths, a.sheet, a.labels)
    bad = [r for r in res if not r["ok"]]
    if a.mode == "code" and len(bad) > 30:
        from collections import Counter
        cnt = Counter((r["where"].split(":")[0], r["check"]) for r in bad)
        for (f, ck), n in sorted(cnt.items()):
            print(f"실패 {ck}  {f} {n}건")
        print(f"--- {len(bad)}건 실패 (상세는 --json)")
        if a.json:
            json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=int)
        sys.exit(1)
    for r in res:
        print(("통과 " if r["ok"] else "실패 ") + r["check"] + ("" if r["ok"] else "  " + json.dumps({k: v for k, v in r.items() if k not in ("check", "ok")}, ensure_ascii=False, default=int)))
    print(f"--- {len(res) - len(bad)}/{len(res)} 통과")
    if a.json:
        json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=int)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
