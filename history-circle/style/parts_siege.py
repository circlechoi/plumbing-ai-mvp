"""공성 단면 부품(토산·성벽·성 안) — 값은 style.json parts.siege. 5편 안시성에서 등록(11/06, 임시).
사료 기준 그림 규칙: 토산은 끝내 성벽보다 높아지고(山頂去城數丈 下臨城中), 무너질 때 성벽 위로 쏟아져 성벽이 무너진다(山頹壓城 城崩).
"""
import math, random
from PIL import Image, ImageDraw
from . import kit
from .kit import S, color
from . import parts as P

SG = S["parts"]["siege"]
T = lambda k: tuple(SG[k])

def _lerp(a, b, g): return a + (b - a) * g
def _ease(g): g = max(0.0, min(1.0, g)); return 1 - (1 - g) ** 3

def backdrop(cv, night=False, frost=0.0):
    k = P.K(); d = cv.d; by = SG["base_y"]
    top, bot = T("sky_top"), T("sky_bottom")
    for y in range(0, by, 8):
        g = y / by; c = tuple(int(_lerp(a, b, g)) for a, b in zip(top, bot))
        if night: c = tuple(int(v * .3) for v in (90, 110, 170))
        if frost: c = tuple(int(_lerp(v, 236, frost * .5)) for v in c)
        d.rectangle([0, y * k, 1080 * k, (y + 8) * k], fill=c)
    for i, col in enumerate(SG["ridges"]):
        base = by - 330 + i * 60; amp = 60 - i * 6
        col = tuple(col)
        if night: col = tuple(int(v * .35) for v in col)
        if frost: col = tuple(int(_lerp(v, 232, frost * .6)) for v in col)
        pts = [(0, by)] + [(x, base - amp * (0.5 + 0.5 * math.sin(x / (80 + i * 30) + i)) - 18 * math.sin(x / 27 + i)) for x in range(0, 1081, 12)] + [(1080, by)]
        d.polygon([(x * k, y * k) for x, y in pts], fill=col)
    g = T("ground")
    if night: g = (70, 62, 52)
    if frost: g = tuple(int(_lerp(v, 238, frost * .7)) for v in g)
    d.rectangle([0, by * k, 1080 * k, 1920 * k], fill=g)
    d.line([(0, by * k), (1080 * k, by * k)], fill=color("ink_line"), width=int(4 * k))

def soldier(cv, x, y, faction, face=1, s=1.0, spear=True, shield=True, alpha=255, carry=False):
    """작은 병사 실루엣(얼굴 없음). y = 발 위치. faction = '고구려'/'당'."""
    k = P.K(); d = cv.d; h = SG["soldier_h"] * s
    col = kit.faction(faction); ink = color("ink_line"); skin = T("skin")
    # 다리
    d.line([((x - 4 * s) * k, (y - h * .35) * k), ((x - 6 * s) * k, y * k)], fill=ink, width=int(4 * s * k))
    d.line([((x + 4 * s) * k, (y - h * .35) * k), ((x + 6 * s) * k, y * k)], fill=ink, width=int(4 * s * k))
    # 몸통(갑옷)
    d.rounded_rectangle([(x - 9 * s) * k, (y - h * .78) * k, (x + 9 * s) * k, (y - h * .3) * k], int(4 * s * k), fill=col, outline=ink, width=int(3 * k))
    # 머리 + 투구
    r = 7 * s; hy = y - h * .78 - r
    d.ellipse([(x - r) * k, (hy - r) * k, (x + r) * k, (hy + r) * k], fill=skin, outline=ink, width=int(2.5 * k))
    d.pieslice([(x - r - 1) * k, (hy - r - 3) * k, (x + r + 1) * k, (hy + r - 3) * k], 180, 360, fill=col, outline=ink, width=int(2.5 * k))
    if faction == "고구려": d.line([(x * k, (hy - r - 3) * k), ((x - 3 * face) * k, (hy - r - 11) * k)], fill=(220, 60, 40), width=int(3 * k))
    if spear:
        sx = x + 11 * s * face
        d.line([(sx * k, (y - h * .2) * k), (sx * k, (y - h * 1.35) * k)], fill=(110, 80, 50), width=int(3 * k))
        d.polygon([(sx * k, (y - h * 1.5) * k), ((sx - 3.5) * k, (y - h * 1.32) * k), ((sx + 3.5) * k, (y - h * 1.32) * k)], fill=(200, 200, 210), outline=ink)
    if shield:
        d.ellipse([(x + (3 * face - 7) * s) * k, (y - h * .72) * k, (x + (3 * face + 7) * s) * k, (y - h * .38) * k], fill=tuple(int(v * .8) for v in col), outline=ink, width=int(2 * k))
    if carry:
        d.ellipse([(x - 10 * s) * k, (hy - r - 14 * s) * k, (x + 10 * s) * k, (hy - r + 2) * k], fill=T("earth_light"), outline=ink, width=int(2 * k))

def flag(cv, x, y, faction, h=120, wave=0.0):
    k = P.K(); d = cv.d; ink = color("ink_line"); col = kit.faction(faction)
    d.line([(x * k, y * k), (x * k, (y - h) * k)], fill=ink, width=int(6 * k))
    w = 0.12 * math.sin(wave * 6)
    pts = [(x, y - h), (x + 80, y - h + 14 + 10 * w), (x + 64, y - h + 30), (x + 80, y - h + 46 - 10 * w), (x, y - h + 50)]
    d.polygon([(a * k, b * k) for a, b in pts], fill=col, outline=ink, width=int(3 * k))

def _house(cv, x, y, w=90, granary=False):
    k = P.K(); d = cv.d; ink = color("ink_line")
    if granary:
        for px in (x - w * .35, x + w * .35): d.line([(px * k, y * k), (px * k, (y - 34) * k)], fill=ink, width=int(5 * k))
        y = y - 34
    d.rectangle([(x - w / 2) * k, (y - 46) * k, (x + w / 2) * k, y * k], fill=T("house_wall"), outline=ink, width=int(3 * k))
    d.rectangle([(x - 8) * k, (y - 26) * k, (x + 8) * k, y * k], fill=(110, 80, 56), outline=ink, width=int(2 * k))
    roof = [(x - w / 2 - 16, y - 44), (x - w / 2 + 6, y - 72), (x + w / 2 - 6, y - 72), (x + w / 2 + 16, y - 44)]
    d.polygon([(a * k, b * k) for a, b in roof], fill=T("roof"), outline=ink, width=int(3 * k))
    for i in range(5): d.line([((x - w / 2 + 4 + i * w / 4.5) * k, (y - 70) * k), ((x - w / 2 - 8 + i * w / 4) * k, (y - 46) * k)], fill=(70, 66, 70), width=int(2 * k))

def interior(cv, t=0.0, busy=0.0):
    """성 안: 오른쪽으로 오르는 산비탈 + 집·창고(부경)·깃발 + 목재를 나르는 사람."""
    k = P.K(); d = cv.d; by = SG["base_y"]; wx1 = SG["wall_x"][1]; ink = color("ink_line")
    hill = [(wx1, by), (wx1, by - 30), (900, by - 110), (1000, by - 230), (1080, by - 300), (1080, 1920), (wx1, 1920)]
    d.polygon([(a * k, b * k) for a, b in hill], fill=T("inner_hill"), outline=ink, width=int(4 * k))
    _house(cv, 880, by - 80, 80); _house(cv, 1000, by - 210, 80, granary=True); _house(cv, 960, by - 140, 70)
    flag(cv, 1040, by - 290, "고구려", 110, t)
    for i in range(3):
        ph = (t * .25 + i * .33) % 1.0; x = _lerp(1000, 850, ph); y = by - 60 - (1000 - x) * .9 + 40
        soldier(cv, x, min(by - 20, y + 60), "고구려", -1, .8, spear=False, shield=False)
        d.line([((x - 16) * k, (min(by - 20, y + 60) - 34) * k), ((x + 16) * k, (min(by - 20, y + 60) - 40) * k)], fill=T("timber_line"), width=int(6 * k))

def wall(cv, timber=0.0, breach=0.0, defenders=True, t=0.0):
    """성벽 단면: 돌벽 + 높여 쌓은 목책(timber 0~1) + 성 위 수비병. breach = 무너짐(0~1, 위쪽부터)."""
    k = P.K(); d = cv.d; by = SG["base_y"]; x0, x1 = SG["wall_x"]; ink = color("ink_line")
    st = by - SG["wall_stone_h"]; tm = SG["timber_max"] * timber
    top = st - tm
    cut = top + (by - 380 - top + 60) * _ease(breach)   # 무너진 뒤 남은 벽 높이
    # 돌벽
    sy0 = max(st, cut)
    d.polygon([(x0 * k, by * k), ((x0 + 12) * k, sy0 * k), (x1 * k, sy0 * k), (x1 * k, by * k)], fill=T("stone"))
    for r, yy in enumerate(range(int(sy0) + 26, by, 30)):
        d.line([((x0 + 6) * k, yy * k), (x1 * k, yy * k)], fill=T("stone_line"), width=int(3 * k))
        off = 0 if r % 2 else 24
        for xx in range(x0 + 12 + off, x1, 48): d.line([(xx * k, (yy - 30) * k), (xx * k, yy * k)], fill=T("stone_line"), width=int(3 * k))
    d.polygon([(x0 * k, by * k), ((x0 + 12) * k, sy0 * k), (x1 * k, sy0 * k), (x1 * k, by * k)], outline=ink, width=int(6 * k))
    # 목책(높인 성벽)
    if tm > 2 and cut < st:
        y0 = max(top, cut); n = max(1, int((st - y0) / 40))
        d.rectangle([(x0 + 12) * k, y0 * k, x1 * k, st * k], fill=T("timber"), outline=ink, width=int(5 * k))
        for xx in range(x0 + 20, x1, 16): d.line([(xx * k, (y0 + 3) * k), (xx * k, (st - 3) * k)], fill=T("timber_line"), width=int(4 * k))
        for i in range(n): d.line([((x0 + 12) * k, (y0 + (i + 1) * (st - y0) / (n + 1)) * k), (x1 * k, (y0 + (i + 1) * (st - y0) / (n + 1)) * k)], fill=T("timber_line"), width=int(4 * k))
    wt = max(top, cut)
    if breach < 0.05:
        for xx in range(x0 + 12, x1, 26): d.rectangle([xx * k, (wt - 22) * k, (xx + 14) * k, wt * k], fill=T("timber") if tm > 2 else T("stone"), outline=ink, width=int(4 * k))
        if defenders:
            for i, xx in enumerate((738, 768, 798)):
                soldier(cv, xx, wt - 4, "고구려", -1, 1.0, shield=i != 1)
            flag(cv, x1 - 6, wt - 20, "고구려", 130, t)
    return wt

def mound(cv, h, collapse=0.0, layers=True, t=0.0):
    """토산: 왼쪽 비탈 + 통나무 단 + 평평한 꼭대기. collapse 0~1 = 꼭대기가 성벽 위로 쏟아짐. 반환 = (꼭대기 왼x, 오른x, y)."""
    k = P.K(); d = cv.d; by = SG["base_y"]; foot = SG["mound_foot_x"]; x0 = SG["wall_x"][0]; ink = color("ink_line")
    if h < 4: return (foot, foot, by)
    top = by - h; tl = _lerp(foot + 80, 470, min(1, h / 560)); tr = x0 - 18
    c = _ease(collapse)
    if c <= 0:
        poly = [(foot, by), (tl, top), (tr, top), (x0 - 4, by)]
        d.polygon([(a * k, b * k) for a, b in poly], fill=T("earth"))
        n = max(2, int(h / 46))
        for i in range(1, n):
            y = by - h * i / n; xl = foot + (tl - foot) * i / n
            d.rectangle([(xl + 6) * k, (y - 6) * k, (x0 - 10) * k, (y + 6) * k], fill=T("earth_dark"), outline=ink, width=int(2 * k))
            for xx in range(int(xl) + 20, x0 - 16, 34): d.ellipse([(xx - 7) * k, (y - 7) * k, (xx + 7) * k, (y + 7) * k], fill=T("earth_light"), outline=ink, width=int(2 * k))
        d.polygon([(a * k, b * k) for a, b in poly], outline=ink, width=int(6 * k))
        return (tl, tr, top)
    # 무너짐: 꼭대기 흙덩이가 성벽 위로 넘어가 성 안쪽까지 쏟아짐
    top2 = top + h * .16 * c
    spill_x = _lerp(x0, 930, c); spill_y = _lerp(top + 40, by - 120, c)
    poly = [(foot, by), (tl + 20 * c, top2), (tr - 30 * c, top2 + 10 * c), (x0 + 40 * c, top2 + 50 * c + 10),
            (SG["wall_x"][1] + 20 * c, top2 + 90 * c + 20), (spill_x, spill_y), (spill_x - 20, by - 60 * c), (x0 - 4, by)]
    d.polygon([(a * k, b * k) for a, b in poly], fill=T("earth"), outline=ink, width=int(6 * k))
    rnd = random.Random(3)
    for i in range(int(26 * c)):
        x = rnd.uniform(x0 - 30, spill_x); y = rnd.uniform(top2 + 40, by - 40)
        d.ellipse([(x - 12) * k, (y - 9) * k, (x + 12) * k, (y + 9) * k], fill=T("earth_dark"), outline=ink, width=int(2 * k))
    if collapse < 1:
        for i in range(8):
            a = i * .8 + collapse * 5; r = 60 + 140 * collapse
            x = 760 + math.cos(a) * r * .6; y = top2 + 20 - 120 * math.sin(math.pi * collapse) + math.sin(a) * 30
            d.rectangle([(x - 10) * k, (y - 8) * k, (x + 10) * k, (y + 8) * k], fill=T("stone"), outline=ink, width=int(2 * k))
    return (tl + 20 * c, tr - 30 * c, top2)

def workers(cv, h, t, n=7):
    """흙을 지고 오르는 당 일꾼."""
    by = SG["base_y"]; foot = SG["mound_foot_x"]; tl = _lerp(foot + 80, 470, min(1, h / 560))
    for i in range(n):
        ph = (t * .18 + i / n) % 1.0
        x = _lerp(foot + 10, tl, ph); y = by - h * ph
        soldier(cv, x, y + 2, "당", 1, .85, spear=False, shield=False, carry=True)

def catapult(cv, x, t, fire_at=None):
    """당 투석기(炮車)."""
    k = P.K(); d = cv.d; by = SG["base_y"]; ink = color("ink_line")
    d.rectangle([(x - 50) * k, (by - 30) * k, (x + 50) * k, by * k], fill=(120, 84, 50), outline=ink, width=int(4 * k))
    for wx in (x - 32, x + 32): d.ellipse([(wx - 14) * k, (by - 14) * k, (wx + 14) * k, (by + 14) * k], fill=(90, 64, 40), outline=ink, width=int(3 * k))
    d.polygon([((x - 30) * k, (by - 30) * k), (x * k, (by - 110) * k), ((x + 30) * k, (by - 30) * k)], outline=ink, width=int(6 * k))
    ph = (t * .9) % 1.0; ang = -60 + 100 * (1 - min(1, ph * 6)) if ph < .2 else -60 + 100
    a = math.radians(ang)
    d.line([(x * k, (by - 100) * k), ((x - 80 * math.cos(a)) * k, (by - 100 - 80 * math.sin(a)) * k)], fill=(110, 80, 50), width=int(7 * k))

def stone_shot(cv, x0, target, t):
    """날아가는 돌(포물선)."""
    k = P.K(); d = cv.d; by = SG["base_y"]; ink = color("ink_line")
    ph = (t * .9) % 1.0
    sx = _lerp(x0, target[0], ph); sy = _lerp(by - 160, target[1], ph) - 300 * 4 * ph * (1 - ph)
    d.ellipse([(sx - 14) * k, (sy - 14) * k, (sx + 14) * k, (sy + 14) * k], fill=(110, 100, 92), outline=ink, width=int(4 * k))
    return ph

def drape(cv, collapse, mound_top, wall_top):
    """무너진 흙이 부서진 성벽 머리를 덮고 성 안쪽으로 흘러내린 모양(벽 위에 덧그림)."""
    c = _ease(collapse)
    if c <= 0: return
    k = P.K(); d = cv.d; ink = color("ink_line"); x0, x1 = SG["wall_x"]; by = SG["base_y"]
    pts = [(x0 - 40, mound_top + 40), (x0 + 30, wall_top - 30 * c), (x1 - 10, wall_top - 10 * c), (x1 + 50 * c, wall_top + 80 * c),
           (x1 + 110 * c, by - 160), (x1 + 40 * c, by - 120), (x1, wall_top + 60), (x0 + 10, wall_top + 40), (x0 - 40, mound_top + 120)]
    d.polygon([(a * k, b * k) for a, b in pts], fill=T("earth_light"), outline=ink, width=int(5 * k))
    rnd = random.Random(9)
    for i in range(int(14 * c)):
        x = rnd.uniform(x0, x1 + 80 * c); y = rnd.uniform(wall_top, wall_top + 120 * c)
        d.rectangle([(x - 9) * k, (y - 7) * k, (x + 9) * k, (y + 7) * k], fill=T("stone"), outline=ink, width=int(2 * k))
