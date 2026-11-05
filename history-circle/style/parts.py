"""역사서클 공용 부품 라이브러리 v1 — 모든 값은 style/style.json(블록·성은 components/spec.json)에서 읽는다.

규칙
- 새 그림을 편 코드에서 직접 그리지 않는다. 필요한 부품은 여기에 등록한 뒤 쓴다.
- 좌표는 출력 픽셀(1080×1920). components Canvas(cv)의 내부 배율 K로 그린다.
- 모든 부품은 cv.add()로 bbox를 등록한다 → lint/layout_overlap.py와 스타일 검사기가 읽는다.

사용:
    import sys; sys.path.insert(0, '<history-circle>')
    from style import parts as P
    cv = P.new_canvas()
    P.place(cv, 'sabi', (380, 860), '사비', side='r')
    P.unit(cv, 'u1', (520, 900), 90, 'M', '백제', icon='inf')
    img = P.finish(cv, year='660년 7월', title=[('백제는 왜 ', 0), ('열흘', 1), (' 만에 무너졌나', 0)],
                   caption='단 열흘 만에 무너졌습니다', legend=['백제', '신라', '당'])
"""
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw

from . import kit
from .kit import S, check_text, color

ROOT = kit.ROOT
sys.path.insert(0, os.path.join(ROOT, "components"))
import canvas as CV  # noqa: E402
import forts as FT  # noqa: E402
import units as UN  # noqa: E402

S_SPEC = CV.SPEC

PT = S["parts"]
TS = S["type_scale"]


def K():
    return CV.K


def new_canvas(bg=None, scene_id="s1"):
    """쇼츠 캔버스. bg = 1080×1920 지도 이미지(RGB) 또는 색 이름/RGB."""
    if isinstance(bg, Image.Image):
        cv = CV.Canvas("shorts", bg=(0, 0, 0), scene_id=scene_id)
        cv.im.paste(bg.convert("RGBA").resize(cv.im.size, Image.LANCZOS), (0, 0))
        cv.d = ImageDraw.Draw(cv.im)
        return cv
    return CV.Canvas("shorts", bg=color(bg or "cream"), scene_id=scene_id)


def _f(type_key, size=None):
    return kit.font(type_key, scale=K(), size=size)


def _stroke(type_key):
    return int(TS[type_key].get("stroke", 0) * K())


def _txt(cv, xy, text, type_key, fill, anchor="mm", stroke_fill=None, size=None, register=None):
    check_text(text)
    k = K()
    f = _f(type_key, size)
    sw = _stroke(type_key) if stroke_fill is not None else 0
    p = (xy[0] * k, xy[1] * k)
    bb = cv.d.textbbox(p, text, font=f, anchor=anchor, stroke_width=sw)
    cv.d.text(p, text, font=f, fill=fill, anchor=anchor, stroke_width=sw, stroke_fill=stroke_fill)
    return [bb[0] / k, bb[1] / k, (bb[2] - bb[0]) / k, (bb[3] - bb[1]) / k]


def _layer(cv):
    ov = Image.new("RGBA", cv.im.size, (0, 0, 0, 0))
    return ov, ImageDraw.Draw(ov)


def _merge(cv, ov, alpha=1.0):
    if alpha < 1:
        ov.putalpha(ov.split()[3].point(lambda v: int(v * max(0.0, alpha))))
    cv.im.alpha_composite(ov)
    cv.d = ImageDraw.Draw(cv.im)


def _union(*bbs):
    x0 = min(b[0] for b in bbs)
    y0 = min(b[1] for b in bbs)
    x1 = max(b[0] + b[2] for b in bbs)
    y1 = max(b[1] + b[3] for b in bbs)
    return [x0, y0, x1 - x0, y1 - y0]


# ---------------- 글자 표식 (1편 bmap3 city·label·water_label) ----------------

def place(cv, id, xy, name, side="r", target=False, sub=None):
    """지명(성·도성): 네모 성 기호 + Jua 58. side = r/l/u/d. target = 공격 목표(빨강)."""
    c = PT["place"]
    k = K()
    x, y = xy
    r = c["square"] / 2
    ri = c["inner"] / 2
    cv.d.rectangle([(x - r) * k, (y - r) * k, (x + r) * k, (y + r) * k], fill=color("place_fill"), outline=color("ink_line"), width=int(c["outline"] * k))
    cv.d.rectangle([(x - ri) * k, (y - ri) * k, (x + ri) * k, (y + ri) * k], outline=color("ink_line"), width=int(c["inner_outline"] * k))
    an = {"r": "lm", "l": "rm", "u": "md", "d": "ma"}[side]
    g = c["gap"]
    off = {"r": (r + g, 0), "l": (-r - g, 0), "u": (0, -r - 10), "d": (0, r + 10)}[side]
    col = color(c["target_color"]) if target else color("ink_line")
    bb = _txt(cv, (x + off[0], y + off[1]), name, "place", col, an, stroke_fill=color(c["text_stroke_color"]))
    bbs = [[x - r, y - r, 2 * r, 2 * r], bb]
    if sub:
        dy = TS["place"]["size"] - 2 if side != "u" else -(TS["place"]["size"] + 8)
        bbs.append(_txt(cv, (x + off[0], y + off[1] + dy), sub, "place_sub", color("ink_line"), an, stroke_fill=color("white")))
    return cv.add(id, "label", _union(*bbs))


def label(cv, id, xy, text, kind="label", col=None):
    """라벨. kind = label(먹 글씨) / water_label(물 이름, 파랑)."""
    fill = color(col) if col else (color("water_text") if kind == "water_label" else color("ink_line"))
    return cv.add(id, "label", _txt(cv, xy, text, kind, fill, "mm", stroke_fill=color("white")))


# ---------------- 말풍선·카드·방향 버튼 (1편 bmap3·scenes13) ----------------

def bubble(cv, id, xy, text, tail=None, age=99.0):
    """말풍선: 흰 둥근 상자 + 먹 테두리 + 꼬리(말하는 블록 쪽). age = 등장 후 초(팝)."""
    c = PT["bubble"]
    pop = min(1.0, age / c["pop_s"]) if c["pop_s"] > 0 else 1.0
    if pop <= 0.02:
        return None
    k = K()
    tail = tail or c["tail_default"]
    x, y = xy
    f = _f("bubble")
    check_text(text)
    w = cv.d.textlength(text, font=f) / k
    ov, d = _layer(cv)
    ol, fill, ink = int(c["outline"] * k), color(c["fill"]), color("ink_line")
    d.polygon([((x - 20) * k, (y + 20) * k), ((x + tail[0]) * k, (y + tail[1]) * k), ((x + 20) * k, (y + 26) * k)], fill=fill, outline=ink, width=ol)
    box = [x - w / 2 - c["pad_x"], y - c["half_h"], x + w / 2 + c["pad_x"], y + c["half_h"]]
    d.rounded_rectangle([v * k for v in box], c["radius"] * k, fill=fill, outline=ink, width=ol)
    d.polygon([((x - 18) * k, (y + 30) * k), ((x + tail[0] + 6) * k, (y + tail[1] - 8) * k), ((x + 16) * k, (y + 30) * k)], fill=fill)
    d.text((x * k, y * k), text, font=f, fill=color(c["text"]), anchor="mm")
    if pop < 1:
        sc = 0.6 + 0.4 * pop
        ov = ov.resize((int(ov.width * sc), int(ov.height * sc)), Image.BICUBIC)
        big = Image.new("RGBA", cv.im.size, (0, 0, 0, 0))
        big.alpha_composite(ov, (int(x * k * (1 - sc)), int(y * k * (1 - sc))))
        ov = big
    _merge(cv, ov)
    # 꼬리는 말하는 블록에 닿아야 하므로 겹침 검사 대상은 상자만
    return cv.add(id, "label", [box[0], box[1], box[2] - box[0], box[3] - box[1]])


def card(cv, id, row, icon, icon_col, text, age=99.0, alpha=1.0):
    """정보 카드(1편 S3b): 크림 둥근 띠 + 원형 아이콘. row = 0,1,2… 위에서부터. age = 등장 후 초(왼쪽에서 밀려 들어옴)."""
    c = PT["card"]
    k = K()
    g = min(1.0, max(0.0, age / c["slide_s"]))
    e = 1 - (1 - g) ** 3
    y = c["row0_y"] + row * c["row_step"]
    x0 = c["x0"] - (1 - e) * c["slide_px"]
    ov, d = _layer(cv)
    ink = color("ink")
    d.rounded_rectangle([x0 * k, (y - c["half_h"]) * k, (x0 + c["w"]) * k, (y + c["half_h"]) * k], c["radius"] * k,
                        fill=color(c["fill"]) + (255,), outline=ink + (255,), width=int(c["outline"] * k))
    ic = c["icon"]
    r = ic["d"] / 2
    cx = x0 + ic["dx"] + r
    d.ellipse([(cx - r) * k, (y - r) * k, (cx + r) * k, (y + r) * k], fill=color(icon_col) + (255,), outline=ink + (255,), width=int(ic["outline"] * k))
    check_text(icon)
    fi = _f("card_icon", TS["card_icon"]["size_2char"] if len(icon) > 1 else None)
    d.text((cx * k, (y + 2) * k), icon, font=fi, fill=color("white") + (255,), anchor="mm", stroke_width=_stroke("card_icon"), stroke_fill=ink + (255,))
    check_text(text)
    d.text(((x0 + c["text_dx"]) * k, (y + 2) * k), text, font=_f("card_text"), fill=color(c["text"]) + (255,), anchor="lm")
    _merge(cv, ov, alpha * min(1.0, g * 3))
    return cv.add(id, "label", [x0, y - c["half_h"], c["w"], 2 * c["half_h"]])


def card_dim(cv, a=1.0):
    """카드 뒤 지도 어둡게(1편 dim 110)."""
    _merge_tint(cv, color("band_black"), int(PT["card"]["dim_alpha"] * a))


def _merge_tint(cv, rgb, a):
    if a <= 0:
        return
    cv.im.alpha_composite(Image.new("RGBA", cv.im.size, tuple(rgb) + (int(a),)))
    cv.d = ImageDraw.Draw(cv.im)


def direction(cv, id, xy, text, side="r"):
    """방향 버튼: 먹색 알약 + 금색 삼각형('사비 ▶'). side = 삼각형 쪽."""
    c = PT["direction"]
    k = K()
    x, y = xy
    f = _f("direction")
    check_text(text)
    w = cv.d.textlength(text, font=f) / k
    box = [x - w / 2 - c["pad_x"], y - c["half_h"], x + w / 2 + c["pad_x"], y + c["half_h"]]
    cv.d.rounded_rectangle([v * k for v in box], c["half_h"] * k, fill=color(c["fill"]))
    tw, th = c["tri_w"], c["tri_h"] / 2
    if side == "l":
        tri = [(x - w / 2 - 14 - tw, y), (x - w / 2 - 14, y - th), (x - w / 2 - 14, y + th)]
    else:
        tri = [(x + w / 2 + 14 + tw, y), (x + w / 2 + 14, y - th), (x + w / 2 + 14, y + th)]
    cv.d.polygon([(a * k, b * k) for a, b in tri], fill=color(c["tri"]))
    cv.d.text(((x + (8 if side == "l" else -8)) * k, y * k), text, font=f, fill=color(c["text"]), anchor="mm")
    return cv.add(id, "label", [box[0], box[1], box[2] - box[0], box[3] - box[1]])


def inset(cv, id, src, box_src, xy, w, title=None):
    """미니맵: src(1080×1920 지도)를 w폭으로 줄여 흰 테두리 창에. box_src = 원본에서 빨간 상자로 짚을 곳."""
    c = PT["inset"]
    k = K()
    s = src.convert("RGB").copy()
    sd = ImageDraw.Draw(s)
    sd.rectangle(box_src, outline=color(c["box_color"]), width=int(c["box_w"] * 2))
    h = int(w * s.height / s.width)
    small = s.resize((int(w * k), int(h * k)), Image.LANCZOS)
    x, y = xy
    p = c["pad"]
    cv.d.rectangle([(x - p) * k, (y - p) * k, (x + w + p) * k, (y + h + p) * k], fill=color("white"), outline=color("ink_line"), width=int(c["outline"] * k))
    cv.im.paste(small, (int(x * k), int(y * k)))
    cv.d = ImageDraw.Draw(cv.im)
    bbs = [[x - p, y - p, w + 2 * p, h + 2 * p]]
    if title:
        bbs.append(_txt(cv, (x + w / 2, y + h + p), title, "inset_title", color("ink_line"), "ma", stroke_fill=color("white")))
    return cv.add(id, "icon", _union(*bbs))


# ---------------- 효과 (1편 burst·sfx, engine cross·bignum) ----------------

def burst(cv, id, xy, r=80, text=None, seed=0, age=99.0):
    """터짐(충돌·함락 지점): 빨간 별꼴 + 먹 테두리. age = 등장 후 초."""
    c = PT["burst"]
    g = min(1.0, max(0.0, age / c["pop_s"]))
    if g <= 0:
        return None
    c1 = 1.70158
    rr = r * max(0.2, 1 + (c1 + 1) * (g - 1) ** 3 + c1 * (g - 1) ** 2)
    k = K()
    rnd = random.Random(seed)
    x, y = xy
    pts = []
    n = c["spikes"] * 2
    for i in range(n):
        a = math.pi * 2 * i / n + rnd.uniform(-.12, .12)
        q = rr * (1 if i % 2 == 0 else rnd.uniform(.45, .6))
        pts.append(((x + math.cos(a) * q) * k, (y + math.sin(a) * q) * k))
    cv.d.polygon(pts, fill=color(c["fill"]), outline=color("ink_line"), width=int(c["outline"] * k))
    if text:
        size = max(2, int(rr * TS["burst_text"]["size_ratio"]))
        _txt(cv, xy, text, "burst_text", color("white"), "mm", stroke_fill=color("ink_line"), size=size)
    return cv.add(id, "effect", [x - rr, y - rr, 2 * rr, 2 * rr])


def sfx(cv, id, xy, text):
    """효과음 글자(BlackHanSans 120, -8도). 지도·도식에서만(원장 sfx_source)."""
    t = TS["sfx"]
    k = K()
    check_text(text)
    f = _f("sfx")
    sw = _stroke("sfx")
    tile = Image.new("RGBA", (int((t["size"] * len(text) * 1.1 + 60) * k), int((t["size"] + 80) * k)), (0, 0, 0, 0))
    ImageDraw.Draw(tile).text((30 * k, 30 * k), text, font=f, fill=color("white"), stroke_width=sw, stroke_fill=color("ink_line"))
    tile = tile.rotate(t["rotate_deg"], expand=True, resample=Image.BICUBIC)
    cv.paste(tile, (xy[0] * k - tile.width / 2, xy[1] * k - tile.height / 2))
    cv.d = ImageDraw.Draw(cv.im)
    return cv.add(id, "effect", [xy[0] - tile.width / k / 2, xy[1] - tile.height / k / 2, tile.width / k, tile.height / k])


def focus_box(cv, id, xy, half, t=0.0):
    """금색 강조 박스(광역에서 전장 범위·성 짚기, 줌 직전). t = 장면 시각(굵기 맥동)."""
    c = PT["focus_box"]
    k = K()
    x, y = xy
    w = c["w"] + c["pulse_w"] * (0.5 + 0.5 * math.sin(t * c["pulse_hz"] * 2 * math.pi))
    cv.d.rectangle([(x - half) * k, (y - half) * k, (x + half) * k, (y + half) * k], outline=tuple(c["color"]), width=int(w * k))
    return cv.add(id, "effect", [x - half - w / 2, y - half - w / 2, 2 * half + w, 2 * half + w])


def ring(cv, id, xy, r, dashed=False, col=None):
    """붉은 원(빈 자리·틈·위치 미상). dashed = 점선(위치 미상)."""
    c = PT["ring"]
    k = K()
    x, y = xy
    rgb = color(col or c["color"])
    w = int(c["w"] * k)
    box = [(x - r) * k, (y - r) * k, (x + r) * k, (y + r) * k]
    if dashed:
        n = max(8, int(2 * math.pi * r / c["dash"]))
        for i in range(0, n, 2):
            cv.d.arc(box, 360 * i / n, 360 * (i + 1) / n, fill=rgb, width=w)
    else:
        cv.d.ellipse(box, outline=rgb, width=w)
    return cv.add(id, "effect", [x - r - c["w"], y - r - c["w"], 2 * r + 2 * c["w"], 2 * r + 2 * c["w"]])


def cross(cv, id, xy):
    """회색 ✕(기각된 수·무너진 성). 글자 대신 선."""
    c = PT["cross"]
    k = K()
    x, y = xy
    r = c["r"]
    for w, col in ((c["w_outer"], color("ink_line")), (c["w_inner"], tuple(c["color"]))):
        cv.d.line([((x - r) * k, (y - r) * k), ((x + r) * k, (y + r) * k)], fill=col, width=int(w * k))
        cv.d.line([((x - r) * k, (y + r) * k), ((x + r) * k, (y - r) * k)], fill=col, width=int(w * k))
    return cv.add(id, "effect", [x - r - c["w_outer"] / 2, y - r - c["w_outer"] / 2, 2 * r + c["w_outer"], 2 * r + c["w_outer"]])


def bignum(cv, id, text, xy, scale=1.0):
    """큰 숫자(병력 대비 등): BlackHanSans + 먹 테두리, 금색."""
    c = PT["bignum"]
    if scale <= 0.02:
        return None
    k = K()
    check_text(text)
    f = kit.font("sfx", scale=k, size=max(2, c["size"] * scale))
    p = (xy[0] * k, xy[1] * k)
    bb = cv.d.textbbox(p, text, font=f, anchor="mm", stroke_width=int(c["stroke"] * k))
    cv.d.text(p, text, font=f, fill=color(c["color"]), anchor="mm", stroke_width=int(c["stroke"] * k), stroke_fill=color("ink_line"))
    return cv.add(id, "badge", [bb[0] / k, bb[1] / k, (bb[2] - bb[0]) / k, (bb[3] - bb[1]) / k])


# ---------------- 화살표 (1편 bmap3 arrow: 끝으로 갈수록 굵어지는 몸통 + 큰 머리 + 흐름 줄무늬) ----------------

def _spline(pts, n=24):
    if len(pts) < 3:
        a, b = pts
        return [(a[0] + (b[0] - a[0]) * t / 40, a[1] + (b[1] - a[1]) * t / 40) for t in range(41)]
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(n):
            t = j / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[q]) + (-p0[q] + p2[q]) * t + (2 * p0[q] - 5 * p1[q] + 4 * p2[q] - p3[q]) * t2
                                    + (-p0[q] + 3 * p1[q] - 3 * p2[q] + p3[q]) * t3) for q in (0, 1)))
    out.append(tuple(pts[-1]))
    return out


def _dense(c, step):
    out = [c[0]]
    for a, b in zip(c[:-1], c[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(L // step))
        for i in range(1, n + 1):
            out.append((a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n))
    return out


def _cum(c):
    L = [0.0]
    for a, b in zip(c[:-1], c[1:]):
        L.append(L[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return L


def _arrow_poly(c, wid, shrink, tail, hlr, hwr):
    L = _cum(c)
    tot = L[-1]
    hl = wid * hlr
    k = max(i for i, l in enumerate(L) if l <= max(tot - hl, 1)) if tot > hl else 1
    body = c[:k + 1]
    B, T = c[k], c[-1]
    ang = math.atan2(T[1] - B[1], T[0] - B[0])
    nx, ny = -math.sin(ang), math.cos(ang)
    left, right = [], []
    for i, p in enumerate(body):
        a2 = math.atan2(body[i + 1][1] - p[1], body[i + 1][0] - p[0]) if i < len(body) - 1 else ang
        mx, my = -math.sin(a2), math.cos(a2)
        t = L[i] / max(L[k], 1)
        w = wid * (tail + (1 - tail) * t ** 0.7) / 2 - shrink
        left.append((p[0] + mx * w, p[1] + my * w))
        right.append((p[0] - mx * w, p[1] - my * w))
    hw = wid * hwr - shrink * 1.5
    tip = (T[0] - math.cos(ang) * shrink * 1.8, T[1] - math.sin(ang) * shrink * 1.8)
    Bb = (B[0] + math.cos(ang) * shrink * 0.6, B[1] + math.sin(ang) * shrink * 0.6)
    return left + [(Bb[0] + nx * hw, Bb[1] + ny * hw), tip, (Bb[0] - nx * hw, Bb[1] - ny * hw)] + right[::-1]


def arrow(cv, id, pts, faction=None, col=None, wid=None, age=99.0, t=0.0, flow=True, dashed=False):
    """진격 화살표. faction = unit_faction 키(블록과 같은 색). age = 그려지기 시작한 뒤 초(grow_s 동안 자람).
    dashed = 퇴각·우회(점선, 머리 없음 대신 몸통만 끊어 그림)."""
    a = PT["arrow"]
    af = PT["arrow_flow"]
    rgb = kit.faction(faction) if faction else color(col or "ink")
    wid = wid or a["wid"]
    ol = a["outline"]
    g = min(1.0, max(0.0, age / af["grow_s"]))
    if g <= 0.03 or len(pts) < 2:
        return None
    e = 1 - (1 - g) ** 3
    k = K()
    c = _dense(_spline(pts), 4)
    if e < 1:
        L = _cum(c)
        c = [p for p, l in zip(c, L) if l <= L[-1] * e] or c[:2]
    if len(c) < 2:
        return None
    ov, d = _layer(cv)
    if dashed:
        # 퇴각·우회: 가는 점선 몸통(먹 테두리) + 끝에만 작은 머리
        dw = wid * PT["dashed"]["width_ratio"]
        L = _cum(c)
        hl = (dw + ol * 2) * af["head_len_ratio"]
        stop = L[-1] - hl * 0.8
        dash = PT["dashed"]["dash"]
        for w_, col_ in ((dw + ol * 2, color("ink_line")), (dw, rgb)):
            s0 = 0.0
            while s0 < stop:
                seg = [p for p, l in zip(c, L) if s0 <= l <= min(stop, s0 + dash)]
                if len(seg) > 1:
                    d.line([(x * k, y * k) for x, y in seg], fill=col_ + (255,), width=int(w_ * k), joint="curve")
                s0 += dash * 2
        tipc = [p for p, l in zip(c, L) if l >= L[-1] - hl * 1.6]
        if len(tipc) >= 2:
            outer = _arrow_poly(tipc, dw + ol * 2, 0, 1.0, af["head_len_ratio"], af["head_w_ratio"])
            inner = _arrow_poly(tipc, dw + ol * 2, ol, 1.0, af["head_len_ratio"], af["head_w_ratio"])
            d.polygon([(x * k, y * k) for x, y in outer], fill=color("ink_line") + (255,))
            d.polygon([(x * k, y * k) for x, y in inner], fill=rgb + (255,))
        outer = [(x, y) for x, y in c]
    else:
        outer = _arrow_poly(c, wid + ol * 2, 0, af["tail"], af["head_len_ratio"], af["head_w_ratio"])
        inner = _arrow_poly(c, wid + ol * 2, ol, af["tail"], af["head_len_ratio"], af["head_w_ratio"])
        d.polygon([(x * k, y * k) for x, y in outer], fill=color("ink_line") + (255,))
        d.polygon([(x * k, y * k) for x, y in inner], fill=rgb + (255,))
    if not dashed and flow and g >= 1 and len(c) > 20:
        L = _cum(c)
        stop = L[-1] - wid * 2.6
        ph = (t * af["speed"]) % af["period"]
        hi = tuple(min(255, v + af["lighten"]) for v in rgb)
        s0 = ph
        while s0 + af["seg"] <= stop:
            seg = [p for p, l in zip(c, L) if s0 <= l <= s0 + af["seg"]]
            if len(seg) > 1:
                d.line([(x * k, y * k) for x, y in seg], fill=hi + (af["alpha"],), width=int(max(af["min_w"], wid * af["width_ratio"]) * k), joint="curve")
            s0 += af["period"]
    _merge(cv, ov)
    xs = [p[0] for p in outer]
    ys = [p[1] for p in outer]
    return cv.add(id, "arrow", [min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)], faction=faction)


# ---------------- 블록·성 (components 규격 그대로) ----------------

def unit(cv, id, xy, ang, grade, faction, icon=None, hidden=False, alpha=255):
    """'ㅗ' 블록 — components/units.py(spec.json unit). faction = 한글 세력 이름."""
    fid = S["colors"]["faction_ids"].get(faction, faction)
    return UN.draw_unit(cv, id, (round(xy[0]), round(xy[1])), ang, grade, fid, icon=icon, hidden=hidden, alpha=alpha)


def fort(cv, id, xy, kind="sanseong", name=None, side="d"):
    """성 표식 — components/forts.py(산성 sanseong·평지성 pyeongji·목책 mokchaek). name = 성 이름(성 아래/위에 지명 글씨)."""
    el = FT.draw_fort(cv, id, (round(xy[0]), round(xy[1])), kind)
    if name:
        half = S_SPEC["fort"]["size"]["h"] / 2
        g = PT["place"]["gap"]
        y = xy[1] + half + g if side == "d" else xy[1] - half - g
        an = "ma" if side == "d" else "md"
        bb = _txt(cv, (xy[0], y), name, "place", color("ink_line"), an, stroke_fill=color("white"))
        cv.add("l_" + id, "label", bb)
    return el


# ---------------- 인물 표식·게이지·시계 ----------------

def figure(cv, id, xy, person, bow=0.0, name=None):
    """얼굴 없는 인물 표식: 크림 원 + 인물 고정 테두리 색 + 고정 모자. person = parts.people 키(등록 필수)."""
    c = PT["figure"]
    if person not in PT["people"]:
        raise KeyError(f"인물 '{person}'은 style.json parts.people에 먼저 등록한다")
    pp = PT["people"][person]
    k = K()
    x, y = xy[0], xy[1] + 10 * bow
    r = c["r"]
    ring = tuple(pp["ring"])
    ink = color("ink_line")
    hat = pp["hat"]
    if hat == "crown":
        pts = [(x - r * .7, y - r * .7), (x - r * .7, y - r * 1.35), (x - r * .35, y - r * 1.0), (x, y - r * 1.5),
               (x + r * .35, y - r * 1.0), (x + r * .7, y - r * 1.35), (x + r * .7, y - r * .7)]
        cv.d.polygon([(a * k, b * k) for a, b in pts], fill=color("gold"), outline=ink, width=int(3 * k))
    elif hat == "helmet":
        cv.d.pieslice([(x - r * .9) * k, (y - r * 1.55) * k, (x + r * .9) * k, (y - r * .25) * k], 180, 360, fill=ring, outline=ink, width=int(3 * k))
        cv.d.line([(x * k, (y - r * 1.55) * k), (x * k, (y - r * 1.85) * k)], fill=ink, width=int(4 * k))
    elif hat == "hood":
        cv.d.chord([(x - r * 1.05) * k, (y - r * 1.3) * k, (x + r * 1.05) * k, (y + r * .3) * k], 180, 360, fill=ink)
    cv.d.ellipse([(x - r) * k, (y - r) * k, (x + r) * k, (y + r) * k], fill=color(c["fill"]), outline=ring, width=int(c["ring"] * k))
    e = c["edge"]
    cv.d.ellipse([(x - r - 4) * k, (y - r - 4) * k, (x + r + 4) * k, (y + r + 4) * k], outline=ink, width=int(e * k))
    bbs = [[x - r - 4, y - r * 1.9, 2 * r + 8, r * 2.9 + 4]]
    if name:
        bbs.append(_txt(cv, (x, y + r + 12), name, "place_sub", ink, "ma", stroke_fill=color("white")))
    return cv.add(id, "icon", _union(*bbs))


def gauge(cv, id, xy, frac, text="군량", blink=False):
    """게이지(군량 등): 25% 아래 빨강·깜빡임."""
    c = PT["gauge"]
    k = K()
    x, y = xy
    w, h, i = c["w"], c["h"], c["inset"]
    cv.d.rounded_rectangle([x * k, y * k, (x + w) * k, (y + h) * k], radius=c["radius"] * k, fill=tuple(c["bg"]), outline=color("ink_line"), width=int(c["outline"] * k))
    f = max(0.0, min(1.0, frac))
    col = tuple(c["low"]) if f < c["low_at"] else tuple(c["ok"])
    if f > 0 and not (blink and f < c["low_at"]):
        cv.d.rounded_rectangle([(x + i) * k, (y + i) * k, (x + i + (w - 2 * i) * f) * k, (y + h - i) * k], radius=(c["radius"] - 4) * k, fill=col)
    bb = _txt(cv, (x + c["label_dx"], y + h / 2), text, "label", color("ink_line"), "mm", stroke_fill=color("white"))
    return cv.add(id, "badge", _union([x, y, w, h], bb))


def clock(cv, id, xy, frac, text=None):
    """시계(시간 경과): 크림 원판 + 먹색 부채꼴(지난 시간) + 빨간 바늘."""
    c = PT["clock"]
    k = K()
    x, y = xy
    r = c["r"]
    ink = color("ink_line")
    cv.d.ellipse([(x - r) * k, (y - r) * k, (x + r) * k, (y + r) * k], fill=color(c["bg"]), outline=ink, width=int(c["outline"] * k))
    f = max(0.0, min(1.0, frac))
    if f > 0:
        ri = r - c["outline"]
        cv.d.pieslice([(x - ri) * k, (y - ri) * k, (x + ri) * k, (y + ri) * k], -90, -90 + 360 * f, fill=color(c["fill"]))
    a = math.radians(-90 + 360 * f)
    cv.d.line([(x * k, y * k), ((x + math.cos(a) * r * .9) * k, (y + math.sin(a) * r * .9) * k)], fill=color(c["hand"]), width=int(6 * k))
    bbs = [[x - r, y - r, 2 * r, 2 * r]]
    if text:
        bbs.append(_txt(cv, (x, y + c["label_dy"]), text, "place_sub", ink, "mm", stroke_fill=color("white")))
    return cv.add(id, "badge", _union(*bbs))


# ---------------- 마무리: 캔버스 → 1080 이미지 + 화면 틀 ----------------

def finish(cv, year, title, caption=None, legend=(), note="", t=99.0, caption_age=99.0, first_scene=False):
    """cv를 1080×1920으로 줄이고 화면 틀(kit.draw_frame)을 얹는다."""
    out = cv.im.resize((cv.W, cv.H), Image.LANCZOS).convert("RGB")
    return kit.draw_frame(out, year=year, title=title, caption=caption, legend=legend, note=note, t=t,
                          caption_age=caption_age, first_scene=first_scene)
