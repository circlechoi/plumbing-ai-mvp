"""'ㅗ' 블록 컴포넌트 (원장 C6: 포맷 공통).

기존 코드 jupil/unit.py를 따른다: 넓은 직사각형 + 바라보는 쪽 짧은 돌기, 먹 외곽선,
돌기와 몸통 사이 선을 같은 색으로 덮어 한 덩어리로 보이게, 각도 0 = 북(위)·시계 방향,
병종 도트 아이콘은 회전하지 않고 블록 가운데(+2px)에 NEAREST 확대.
새로 정한 것: 등급(S/M/L/XL)별 고정 크기 — spec.json unit.grades(임시값).
"""
import math
import os

from PIL import Image, ImageDraw

from canvas import HERE, INK, K, SPEC, font

U = SPEC["unit"]
BASE = U["base"]
OUTLINE = tuple(SPEC["palette"]["unit_outline"]["rgb"])
GOLD = tuple(SPEC["palette"]["gold_hidden"]["rgb"])
FACTION = {k: tuple(v) for k, v in SPEC["palette"]["unit_faction"].items() if isinstance(v, list)}
ORDER = U["grades"]["order"]


def grade_dims(grade):
    """등급 → (몸통 w, h) 출력 픽셀. 면적 = 기준 × area_factor, 가로세로 비는 기준(150×64) 유지, 짝수로 맞춤."""
    f = U["grades"]["area_factor"][grade]
    s = math.sqrt(f)
    w = int(round(BASE["w"] * s / 2)) * 2
    h = int(round(BASE["h"] * s / 2)) * 2
    return w, h


def grade_for(troops):
    """병력 → 등급(경계는 spec troops_upper, 임시값)."""
    up = U["grades"]["troops_upper"]
    for g in ORDER:
        if up[g] is None or troops < up[g]:
            return g
    return ORDER[-1]


def _outline_poly(w, h, nw, nh):
    """'ㅗ' 외곽 다각형(중심 0,0, 돌기는 위쪽). 출력 픽셀."""
    return [(-w / 2, -h / 2), (-nw / 2, -h / 2), (-nw / 2, -h / 2 - nh), (nw / 2, -h / 2 - nh),
            (nw / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]


def _rot(pts, ang, cx, cy):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def unit_bbox(xy, ang, grade):
    """그리기 전에 bbox 계산(배치 계획·resolve_overlap용). 외곽선 두께 절반 포함."""
    w, h = grade_dims(grade)
    pts = _rot(_outline_poly(w, h, BASE["nub_w"], BASE["nub_h"]), ang, *xy)
    m = BASE["outline_w"] / 2
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return [min(xs) - m, min(ys) - m, max(xs) - min(xs) + 2 * m, max(ys) - min(ys) + 2 * m]


def _dashed(d, pts, col, wid, dash, gap):
    """닫힌 다각형 점선(내부 좌표)."""
    seq = pts + [pts[0]]
    segs, acc = [], 0.0
    for a, b in zip(seq, seq[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        segs.append((a, b, acc, L))
        acc += L

    def at(s):
        for a, b, s0, L in segs:
            if s <= s0 + L or (a, b) == segs[-1][:2]:
                t = 0 if L == 0 else (s - s0) / L
                return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

    s, step = 0.0, max(1.0, wid / 4)
    while s < acc:
        e = min(acc, s + dash)
        pts_ = [at(s + i * step) for i in range(int((e - s) / step) + 1)] + [at(e)]
        d.line(pts_, fill=col, width=wid, joint="curve")
        s += dash + gap


def draw_unit(cv, id, xy, ang, grade, faction, icon=None, hidden=False, alpha=255):
    """cv(Canvas)에 블록을 그리고 layout 요소를 등록한다.

    xy: 몸통 중심(출력 픽셀) / ang: 바라보는 방향(0 = 북, 시계 방향, 도) / grade: S·M·L·XL
    faction: spec palette.unit_faction 키 / icon: spec unit.icons 키(inf·cav·hvy·mal·tcav) 또는 None
    hidden: 숨은 부대(반투명 먹색 + 금색 점선 + '?')
    """
    w, h = grade_dims(grade)
    nw, nh = BASE["nub_w"], BASE["nub_h"]
    S = 300  # 타일 한 변(출력 픽셀) — XL 블록 + 돌기 + 회전 여유
    tile = Image.new("RGBA", (S * K, S * K), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    cx = cy = S / 2
    kk = lambda *v: [x * K for x in v]

    if hidden:
        hd = U["hidden"]
        fill = tuple(hd["fill_rgb"]) + (hd["fill_alpha"],)
        poly = [(cx + x, cy + y) for x, y in _outline_poly(w, h, nw, nh)]
        d.polygon([(x * K, y * K) for x, y in poly], fill=fill)
        _dashed(d, [(x * K, y * K) for x, y in poly], GOLD + (255,), hd["dash_w"] * K, hd["dash"][0] * K, hd["dash"][1] * K)
    else:
        col = FACTION[faction] + (alpha,)
        ol = OUTLINE + (alpha,)
        d.rectangle(kk(cx - nw / 2, cy - h / 2 - nh, cx + nw / 2, cy - h / 2 + 4), fill=col, outline=ol, width=BASE["nub_outline_w"] * K)
        d.rectangle(kk(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=col, outline=ol, width=BASE["outline_w"] * K)
        d.rectangle(kk(cx - nw / 2 + 3, cy - h / 2 - 2, cx + nw / 2 - 3, cy - h / 2 + 8), fill=col)

    tile = tile.rotate(-ang, center=(cx * K, cy * K), resample=Image.BICUBIC)
    cv.paste(tile, ((xy[0] - cx) * K, (xy[1] - cy) * K))

    if hidden:
        f = font("number", 48 * K)
        cv.d.text((xy[0] * K, (xy[1] + 2) * K), U["hidden"]["mark"], font=f, fill=GOLD, anchor="mm",
                  stroke_width=8 * K, stroke_fill=INK)
    elif icon:
        ic = Image.open(os.path.join(HERE, U["icons"][icon])).convert("RGBA")
        # 기존 iscale 2.2를 따르되 블록 높이(외곽선 안쪽)를 넘지 않게 줄인다(S·M에서 아이콘이 삐져나오던 문제)
        sc = min(BASE["icon_scale"], (h - 2 * BASE["outline_w"] - 4) / ic.height) * K
        ic = ic.resize((int(ic.width * sc), int(ic.height * sc)), Image.NEAREST)
        if alpha < 255:
            ic.putalpha(ic.split()[3].point(lambda v: v * alpha // 255))
        cv.paste(ic, (xy[0] * K - ic.width / 2, (xy[1] + 2) * K - ic.height / 2))

    bb = unit_bbox(xy, ang, grade)
    axis = abs(ang) % 90 < 1e-6
    return cv.add(id, "block", bb, faction=None if hidden else faction,
                  # 회전한 블록은 bbox 면적이 각도마다 달라 등급 크기 검사에 넣지 않는다(크기는 grade_dims로 보장)
                  size_class=grade if axis else None,
                  size_class_nominal=grade, nominal_wh=[w, h], angle=ang, hidden=hidden or None)
