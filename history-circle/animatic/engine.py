"""역사서클 전투 쇼츠 애니매틱 엔진 (편 무관).

- 지도 바탕 v4-S: 4편 키트(salsu terrain3.dem·sample, mkstyl.masks, bmap3.map_base, salsu.highland2,
  mkbase.draw_rivers)를 이 환경에서 다시 구현. 고도 = AWS Terrarium 타일.
- 블록·성·줌·레이아웃은 components/(units, forts, zoom, canvas)를 그대로 쓴다.
- 화면 구성은 4편 anim4.py hud1080·cam을 따른다: 위 검은 띠 0~140(연도·채널명), 크림 제목 띠 140~236(강조어 진빨강 상자),
  자막 y≈1420(그라데이션 1270~1570, 760px 넘으면 두 줄), 범례 띠 1600~1700, 카메라 중심 y=800.
- 새로 만든 도식(흙산 단면·군량 게이지·얼굴 없는 인물 표식·도트 절 스프라이트·말풍선·큰 숫자)은 아래 '새 부품'.
"""
import json
import math
import os
import random
import subprocess
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "components"))
import canvas as CV  # noqa: E402
import forts as FT  # noqa: E402
import units as UN  # noqa: E402
import zoom as ZM  # noqa: E402

sys.path.insert(0, ROOT)
from style import kit as SK  # noqa: E402  스타일 키트 v1: 글자·말풍선·인물·게이지·화면 틀은 style.json 경유
from style import parts as SP  # noqa: E402
import warnings  # noqa: E402


def _warn_size(fn, size):
    if size is not None:
        warnings.warn(f"engine.{fn}(size={size}) 무시 — 크기는 style.json type_scale", stacklevel=3)

W, H = 1080, 1920
TILES = os.environ.get("HC_TILES", os.path.join(HERE, ".tiles"))

INK = (30, 26, 24)
WHITE = (255, 255, 255)
TAN = (214, 190, 150)
WATER = (118, 150, 214)
HILL = (168, 170, 140)
GOLD = (240, 196, 80)
HOT = (172, 34, 28)
CREAM = (250, 244, 228)
UNIT = CV.SPEC["palette"]["unit_faction"]


def set_K(k):
    """components의 내부 배율을 바꾼다(스토리보드 2, 애니매틱 1)."""
    CV.K = UN.K = FT.K = k


def K():
    return CV.K


def font(kind, size):
    return CV.font(kind, int(size * K()))


# ---------------- 지도 바탕 v4-S ----------------

class Map:
    """bmap3.Map과 같은 정거원통 투영. box = 화면 전체(battle-shorts 3절 'PANEL(0,0,1080,1920)')."""

    def __init__(self, lon0, lon1, clat, box=(0, 0, W, H)):
        self.lon0, self.lon1, self.box, self.clat = lon0, lon1, box, clat
        self.k = math.cos(math.radians(clat))
        self.sc = (box[2] - box[0]) / ((lon1 - lon0) * self.k)
        self.cy = (box[1] + box[3]) / 2

    def P(self, lon, lat):
        return (self.box[0] + (lon - self.lon0) * self.k * self.sc, self.cy - (lat - self.clat) * self.sc)

    def win(self):
        half = (self.box[3] - self.box[1]) / 2 / self.sc
        return ZM.Win(self.lon0, self.lon1, self.clat - half, self.clat + half)


def _txy(lon, lat, z):
    n = 2 ** z
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n


def dem(lon0, lon1, lat0, lat1, z):
    """terrain3.dem과 같음: Terrarium 타일 → 고도(m) 배열."""
    import urllib.request
    os.makedirs(TILES, exist_ok=True)
    x0, y0 = _txy(lon0, lat1, z)
    x1, y1 = _txy(lon1, lat0, z)
    rows = []
    for ty in range(int(y0), int(y1) + 1):
        row = []
        for tx in range(int(x0), int(x1) + 1):
            p = os.path.join(TILES, f"{z}_{tx}_{ty}.png")
            if not os.path.exists(p):
                urllib.request.urlretrieve(f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{tx}/{ty}.png", p)
            a = np.asarray(Image.open(p).convert("RGB"), np.float32)
            row.append(a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768)
        rows.append(np.concatenate(row, 1))
    return np.concatenate(rows, 0), int(x0), int(y0), z


def sample(M, E, tx0, ty0, z, kb):
    """terrain3.sample: 지도 픽셀마다 메르카토르 타일 좌표로 보간."""
    Wk, Hk = W * kb, H * kb
    xs = (np.arange(Wk) / kb - M.box[0]) / (M.k * M.sc) + M.lon0
    ys = M.clat - (np.arange(Hk) / kb - M.cy) / M.sc
    n = 2 ** z
    sx = ((xs + 180) / 360 * n - tx0) * 256
    sy = ((1 - np.arcsinh(np.tan(np.radians(np.clip(ys, -80, 80)))) / np.pi) / 2 * n - ty0) * 256
    cols, rows = np.arange(E.shape[1]), np.arange(E.shape[0])
    T = np.stack([np.interp(sx, cols, E[r]) for r in range(E.shape[0])])
    return np.stack([np.interp(sy, rows, T[:, c]) for c in range(Wk)], 1).astype(np.float32)


def masks(e, thr, sm, minarea, kb):
    """mkstyl.masks: 땅 마스크 → Gaussian(sm) 평활 고도 > thr = 산지 면(작은 조각 제거)."""
    from scipy import ndimage
    land = e > 0.5
    lmI = Image.fromarray((land * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5 * kb)).point(lambda v: 255 if v > 128 else 0)
    land = np.asarray(lmI) > 128
    lab, n = ndimage.label(land)
    if n:
        sizes = ndimage.sum(land, lab, range(1, n + 1))
        land = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > minarea * land.size])
    es = ndimage.gaussian_filter(np.where(land, e, 0), sm * kb)
    hm = (es > thr) & land
    lab, n = ndimage.label(hm)
    if n:
        sizes = ndimage.sum(hm, lab, range(1, n + 1))
        hm = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 0.012 * hm.size])
    hmI = Image.fromarray((hm * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4 * kb)).point(lambda v: 255 if v > 128 else 0)
    return Image.fromarray((land * 255).astype(np.uint8)), hmI, es


def map_base(lm, kb, seed=7):
    """bmap3.map_base: 바다 + 얕은 바다 띠 + 물결 + 땅(TAN) + 해안 안쪽 밝은 띠 + 먹 해안선."""
    Wk, Hk = W * kb, H * kb
    im = Image.new("RGB", (Wk, Hk), WATER)
    sh = lm.filter(ImageFilter.GaussianBlur(13 * kb)).point(lambda v: 255 if v > 14 else 0)
    sh = ImageChops.subtract(sh, lm)
    im.paste(Image.new("RGB", (Wk, Hk), (146, 178, 228)), (0, 0), sh)
    rnd = random.Random(seed)
    d = ImageDraw.Draw(im)
    for _ in range(170):
        x, y = rnd.uniform(30, W - 40), rnd.uniform(30, H - 30)
        px = lambda X, Y: (min(Wk - 1, int(X * kb)), min(Hk - 1, int(Y * kb)))
        if lm.getpixel(px(x, y)) or sh.getpixel(px(x, y)) or lm.getpixel(px(x + 30, y)):
            continue
        d.arc([(x - 14) * kb, (y - 6) * kb, x * kb, (y + 6) * kb], 200, 340, fill=(92, 124, 194), width=3 * kb)
        d.arc([x * kb, (y - 6) * kb, (x + 14) * kb, (y + 6) * kb], 200, 340, fill=(92, 124, 194), width=3 * kb)
    im.paste(Image.new("RGB", (Wk, Hk), TAN), (0, 0), lm)
    inner = ImageChops.subtract(lm, lm.filter(ImageFilter.MinFilter(11)))
    im.paste(Image.new("RGB", (Wk, Hk), (238, 222, 188)), (0, 0), inner)
    edge = ImageChops.subtract(lm.filter(ImageFilter.MaxFilter(13)), lm)
    im.paste(Image.new("RGB", (Wk, Hk), INK), (0, 0), edge)
    return im


def highland2(im, m, es, kb, step=112, seed=3):
    """salsu.highland2: 산지 면 HILL + 테두리 + 고도 따라 크기가 바뀌는 '^' 산 기호."""
    Wk, Hk = im.size
    rnd = random.Random(seed)
    im.paste(Image.new("RGB", (Wk, Hk), HILL), (0, 0), m)
    edge = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(7)), m)
    im.paste(Image.new("RGB", (Wk, Hk), (90, 84, 70)), (0, 0), edge)
    d = ImageDraw.Draw(im)
    a = np.asarray(m) > 128
    ok = lambda X, Y: 0 <= X < W and 0 <= Y < H and a[int(Y * kb), int(X * kb)]
    row = 0
    for y in range(30, 1910, int(step * .8)):
        for x in range(16 + (row % 2) * step // 2, 1070, step):
            jx, jy = x + rnd.uniform(-14, 14), y + rnd.uniform(-10, 10)
            if not (0 <= jx < W and 0 <= jy < H):
                continue
            el = es[int(jy * kb), int(jx * kb)]
            sz = (18 + min(1.0, max(0.0, (el - 160) / 450)) * 14) * rnd.uniform(.9, 1.1)
            if ok(jx, jy) and ok(jx - sz - 10, jy + sz * .7 + 8) and ok(jx + sz + 10, jy + sz * .7 + 8) and ok(jx, jy - sz * .6 - 10):
                d.line([((jx - sz) * kb, (jy + sz * .7) * kb), (jx * kb, (jy - sz * .5) * kb), ((jx + sz) * kb, (jy + sz * .7) * kb)],
                       fill=(90, 84, 70), width=5 * kb, joint="curve")
        row += 1


def draw_rivers(im, M, lm, rivers, kb, scale=1.0, wid=None):
    """mkbase.draw_rivers: 짙은 테두리 + 물색 + 굵은 강은 가운데 밝은 줄."""
    wid = wid or {"辽河": 13, "大辽河": 13, "太子河": 7, "浑河": 7}
    Wk, Hk = im.size
    body, core = Image.new("L", (Wk, Hk), 0), Image.new("L", (Wk, Hk), 0)
    bd, cd = ImageDraw.Draw(body), ImageDraw.Draw(core)
    for nm, parts in rivers.items():
        if nm.startswith("_"):
            continue
        w = wid.get(nm, 5) * scale
        for pts in parts:
            P = [tuple(v * kb for v in M.P(lo, la)) for lo, la in pts]
            for p1, p2 in zip(P, P[1:]):
                r = w * kb / 2
                bd.line([p1, p2], fill=255, width=max(2, int(w * kb)))
                bd.ellipse([p2[0] - r, p2[1] - r, p2[0] + r, p2[1] + r], fill=255)
                if w > 12:
                    cd.line([p1, p2], fill=255, width=max(1, int(w * kb * .28)))
    outer = body.filter(ImageFilter.MaxFilter(7))
    im.paste(Image.new("RGB", (Wk, Hk), (46, 74, 112)), (0, 0), ImageChops.multiply(outer, lm))
    im.paste(Image.new("RGB", (Wk, Hk), (96, 140, 200)), (0, 0), body)
    im.paste(Image.new("RGB", (Wk, Hk), (150, 190, 236)), (0, 0), core.filter(ImageFilter.GaussianBlur(kb)))


def base_v4s(M, z, thr, sm=5, minarea=0.0002, rivers=None, river_scale=0.55, kb=2, cache=None):
    """salsu.base와 같은 순서: dem → masks → map_base → highland2 → rivers. kb배 크기 RGB."""
    if cache and os.path.exists(cache):
        return Image.open(cache).convert("RGB")
    half = H / 2 / M.sc
    E, tx0, ty0, zz = dem(M.lon0 - .1, M.lon1 + .1, M.clat - half - .1, M.clat + half + .1, z)
    e = sample(M, E, tx0, ty0, zz, kb)
    lm, hm, es = masks(e, thr, sm, minarea, kb)
    im = map_base(lm, kb)
    highland2(im, hm, es, kb)
    if rivers:
        draw_rivers(im, M, lm, rivers, kb, scale=river_scale)
    if cache:
        im.save(cache)
    return im


# ---------------- 판(Canvas) ----------------

def world(base_img, scene_id):
    """바탕 그림 위에 components Canvas를 연다(K = 현재 배율)."""
    cv = CV.Canvas("shorts", scene_id=scene_id)
    k = K()
    b = base_img if base_img.size == (W * k, H * k) else base_img.resize((W * k, H * k), Image.LANCZOS)
    cv.im = b.convert("RGBA")
    cv.d = ImageDraw.Draw(cv.im)
    return cv


_PAPER = {}


def plain(scene_id, bg=(232, 220, 196)):
    """지도 없는 도식 판(종이색 + 종이 결). 결이 있어야 카메라 움직임이 화면에 보인다(평면색은 확대해도 그대로)."""
    cv = CV.Canvas("shorts", bg=bg, scene_id=scene_id)
    k = K()
    key = (bg, k)
    if key not in _PAPER:
        rng = np.random.default_rng(5)
        g1 = np.asarray(Image.fromarray((rng.random((H // 12, W // 12)) * 255).astype(np.uint8)).resize((W * k, H * k), Image.BICUBIC), np.float32) / 255 - .5
        g2 = rng.random((H * k, W * k)).astype(np.float32) - .5
        a = np.clip(np.array(bg, np.float32)[None, None, :] + (g1 * 26 + g2 * 8)[..., None], 0, 255).astype(np.uint8)
        _PAPER[key] = Image.fromarray(a).convert("RGBA")
    cv.im = _PAPER[key].copy()
    cv.d = ImageDraw.Draw(cv.im)
    return cv


def overlay(cv, fn):
    """반투명 그리기: fn(d)로 RGBA 층에 그린 뒤 합성."""
    ov = Image.new("RGBA", cv.im.size, (0, 0, 0, 0))
    fn(ImageDraw.Draw(ov))
    cv.im.alpha_composite(ov)
    cv.d = ImageDraw.Draw(cv.im)


def tint(cv, rgb, a):
    if a <= 0:
        return
    cv.im.alpha_composite(Image.new("RGBA", cv.im.size, tuple(rgb) + (int(a),)))
    cv.d = ImageDraw.Draw(cv.im)


# ---------------- 표식·도식 ----------------

def unit(cv, id, xy, ang, grade, faction, icon=None, hidden=False, alpha=255):
    return UN.draw_unit(cv, id, (round(xy[0]), round(xy[1])), ang, grade, faction, icon=icon, hidden=hidden, alpha=alpha)


def fort(cv, id, xy, kind="sanseong"):
    return FT.draw_fort(cv, id, (round(xy[0]), round(xy[1])), kind)


def label(cv, id, text, xy, size=None, fill=None, register=True, kind="label"):
    """라벨 = style.parts.label(크기는 style.json type_scale.label). size 인자는 무시(경고)."""
    _warn_size("label", size)
    el = SP.label(cv, id, xy, text, kind=kind, col=fill)
    if not register:
        cv.elements.remove(el)
    return el


def bignum(cv, id, text, xy, size=None, fill=None, scale=1.0):
    """큰 숫자 = style.parts.bignum. size < small_below면 작은 판(size_small), 아니면 기본 크기."""
    b = SK.S["parts"]["bignum"]
    small = size is not None and size < b["small_below"]
    return SP.bignum(cv, id, text, xy, scale=scale * (b["size_small"] / b["size"] if small else 1.0))

def _arrow_pts(pts, upto):
    L = [0.0]
    for a, b in zip(pts, pts[1:]):
        L.append(L[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    tot = L[-1] * max(0.0, min(1.0, upto))
    out = [pts[0]]
    for i in range(1, len(pts)):
        if L[i] <= tot:
            out.append(pts[i])
        else:
            a, b = pts[i - 1], pts[i]
            g = (tot - L[i - 1]) / max(1e-6, L[i] - L[i - 1])
            out.append((a[0] + (b[0] - a[0]) * g, a[1] + (b[1] - a[1]) * g))
            break
    return out


def arrow(cv, id, pts, col, wid=None, upto=1.0, dashed=False, head=True, register=True, alpha=255, t=0.0):
    """화살표 = style.parts.arrow(1편 방식). col = RGB 또는 style 색 이름. upto(0~1) = 자라난 정도. wid 인자는 무시(경고)."""
    _warn_size("arrow", wid)
    if upto <= 0.01 or len(pts) < 2:
        return None
    el = SP.arrow(cv, id, pts, col=col, age=upto * SK.S["parts"]["arrow_flow"]["grow_s"], t=t, dashed=dashed)
    if el is not None and not register:
        cv.elements.remove(el)
    return el

def cross(cv, id, xy, r=34, col=(150, 150, 150)):
    """회색 ✕ 표시(기각된 수). 글자 대신 선으로 그린다(JUA에 ✕ 없음)."""
    k = K()
    x, y = xy
    for w, c in ((22, INK), (12, col)):
        cv.d.line([((x - r) * k, (y - r) * k), ((x + r) * k, (y + r) * k)], fill=c, width=w * k)
        cv.d.line([((x - r) * k, (y + r) * k), ((x + r) * k, (y - r) * k)], fill=c, width=w * k)
    return cv.add(id, "effect", [x - r - 11, y - r - 11, 2 * r + 22, 2 * r + 22])


def bubble(cv, id, anchor, text, dx=0, dy=-120, size=None, fill=None, age=99.0):
    """말풍선 = style.parts.bubble(1편 방식). 꼬리는 anchor(말하는 블록)를 향한다."""
    _warn_size("bubble", size)
    cx, cy = anchor[0] + dx, anchor[1] + dy
    return SP.bubble(cv, id, (cx, cy), text, tail=(anchor[0] - cx, anchor[1] - cy - (8 if dy < 0 else -8)), age=age)


def lord(cv, id, xy, r=None, bow=0.0, person="안시성주", name=None):
    """얼굴 없는 인물 표식 = style.parts.figure(인물별 고정 색·모자, style.json parts.people)."""
    _warn_size("lord", r)
    return SP.figure(cv, id, xy, person, bow=bow, name=name)


def dot_bow(cv, id, xy, phase, px=7):
    """도트 그림(원장 dot_sprite: 매 편 1곳): 성벽 위 성주의 절. phase 0 = 선 자세, 1 = 숙임."""
    k = K()
    fr = _BOW[1 if phase > .5 else 0]
    col = {"1": INK, "2": GOLD, "3": (200, 70, 52)}
    x0, y0 = xy[0] - 6 * px, xy[1] - 16 * px
    for j, row in enumerate(fr):
        for i, c in enumerate(row):
            if c in col:
                cv.d.rectangle([(x0 + i * px) * k, (y0 + j * px) * k, (x0 + (i + 1) * px) * k - 1, (y0 + (j + 1) * px) * k - 1], fill=col[c])
    return cv.add(id, "icon", [x0, y0, 12 * px, 16 * px])


def gauge(cv, id, xy, frac, text="군량", w=None, h=None, blink=False):
    """게이지 = style.parts.gauge."""
    _warn_size("gauge", w)
    return SP.gauge(cv, id, xy, frac, text=text, blink=blink)


def mound_section(cv, id, mound_h, wall_h, collapse=0.0, owner=None, crack=0.0, base_y=1120):
    """흙산 단면 도식(전술 도식, 지도 버림): 왼쪽 흙산 / 오른쪽 성벽 높이 경쟁, 무너짐·성벽 균열.

    mound_h·wall_h: 출력 px 높이 / collapse: 0~1 무너짐(꼭대기가 성벽 쪽으로 쏟아짐) / owner: 흙산 위 주인 색.
    """
    k = K()
    d = cv.d
    # 땅
    d.rectangle([0, base_y * k, W * k, (base_y + 150) * k], fill=(196, 168, 120))
    d.line([(0, base_y * k), (W * k, base_y * k)], fill=INK, width=6 * k)
    # 성벽(오른쪽): 돌 벽 + 성가퀴
    wx0, wx1 = 640, 780
    wt = base_y - wall_h
    stone = (150, 146, 136)
    d.rectangle([wx0 * k, wt * k, wx1 * k, base_y * k], fill=stone, outline=INK, width=6 * k)
    for i in range(4):
        cx_ = wx0 + 10 + i * 34
        d.rectangle([cx_ * k, (wt - 22) * k, (cx_ + 20) * k, wt * k], fill=stone, outline=INK, width=5 * k)
    for j in range(int(wall_h // 40)):
        yy = base_y - 40 * (j + 1)
        d.line([(wx0 + 4) * k, yy * k, (wx1 - 4) * k, yy * k], fill=(120, 116, 108), width=3 * k)
    if crack > 0:
        pts = [(wx0 + 10, wt + 30), (wx0 + 50, wt + 70), (wx0 + 30, wt + 120), (wx0 + 70, wt + 170)]
        pts = _arrow_pts(pts, crack)
        d.line([(x * k, y * k) for x, y in pts], fill=INK, width=8 * k)
        if crack >= 1:
            d.polygon([(wx0 * k, (wt - 22) * k), ((wx0 + 60) * k, (wt - 22) * k), ((wx0 + 30) * k, (wt + 60) * k), (wx0 * k, (wt + 90) * k)],
                      fill=(232, 220, 196))
    # 흙산(왼쪽): 꼭대기가 무너질수록 성벽 쪽으로 기울고 낮아짐
    peak_x = 430 + 190 * collapse
    peak_y = base_y - mound_h * (1 - .25 * collapse)
    poly = [(110, base_y), (peak_x - 70, peak_y + 18), (peak_x, peak_y), (peak_x + 60 + 40 * collapse, peak_y + 30 * (1 - collapse)),
            (wx0 + 40 * collapse, base_y - (wall_h * .55) * collapse), (wx0, base_y)]
    earth = (150, 112, 70) if owner is None else tuple(int(a * .55 + b * .45) for a, b in zip((150, 112, 70), owner))
    d.polygon([(x * k, y * k) for x, y in poly], fill=earth, outline=INK, width=6 * k)
    for j in range(5):
        yy = base_y - (j + 1) * mound_h / 6
        if yy > peak_y + 10:
            d.line([((130 + j * 40) * k, yy * k), ((wx0 - 10 - j * 30) * k, yy * k)], fill=(120, 88, 56), width=3 * k)
    cv.add(id + "_wall", "other", [wx0, wt - 22, wx1 - wx0, base_y - wt + 22])
    cv.add(id + "_mound", "other", [110, peak_y, wx0 - 110, base_y - peak_y])
    return (peak_x, peak_y), (wx0, wx1, wt)


# ---------------- HUD (4편 hud1080) ----------------

def hud(cv, title_parts, year, subtitle, sub_alpha=1.0, legend=None, note=None, t=99.0, first_scene=False):
    """화면 틀 = style.kit.draw_frame(4편 hud1080 방식, style.json frame). legend = 세력 이름(한글) 목록."""
    names = []
    for it in legend or []:
        names.append(it[1] if isinstance(it, (tuple, list)) else it)
    age = 99.0 if sub_alpha >= 1 else sub_alpha * SK.S["frame"]["caption"]["fade_s"]
    out = SK.draw_frame(cv.im, year=year, title=title_parts, caption=subtitle, legend=names, note=note or "",
                        t=t, caption_age=age, first_scene=first_scene, scale=K())
    cv.im = out.convert("RGBA")
    cv.d = ImageDraw.Draw(cv.im)
    return cv


def cam(img, z=1.0, cx=540, cy=960):
    """anim4.cam: 확대 z, 중심(cx, cy) 출력 좌표. 화면 밖으로 나가지 않게 고정."""
    Wi, Hi = img.size
    s = Wi / W
    w, h = Wi / z, Hi / z
    x0 = max(0, min(Wi - w, cx * s - w / 2))
    y0 = max(0, min(Hi - h, cy * s - h / 2))
    return img.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((Wi, Hi), Image.BILINEAR)


def flash(img, a, col=(255, 255, 255)):
    return Image.blend(img, Image.new(img.mode, img.size, col), max(0.0, min(1.0, a))) if a > 0 else img


def shake(img, amt, seed):
    if amt <= 0:
        return img
    r = random.Random(seed)
    dx, dy = int(r.uniform(-1, 1) * 14 * amt), int(r.uniform(-1, 1) * 14 * amt)
    return ImageChops.offset(img, dx, dy)


def cl(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def ramp(u, a, b):
    return cl((u - a) / max(1e-6, b - a))


def ease(g):
    return 1 - (1 - g) ** 3


def lerp(a, b, g):
    return a + (b - a) * g


def popf(age, d=.22):
    """anim4.popf: 튀어나오며 커짐."""
    if age < 0:
        return 0
    g = cl(age / d)
    return g * (1 + .25 * math.sin(math.pi * g))


class Writer:
    """ffmpeg로 프레임(PIL RGB)을 mp4로. 무음."""

    def __init__(self, path, size=(540, 960), fps=12, crf=26):
        self.size = size
        self.p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                   "-s", f"{size[0]}x{size[1]}", "-r", str(fps), "-i", "-", "-c:v", "libx264",
                                   "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart", path],
                                  stdin=subprocess.PIPE)

    def add(self, img):
        im = img.convert("RGB")
        if im.size != self.size:
            im = im.resize(self.size, Image.LANCZOS)
        self.p.stdin.write(im.tobytes())

    def close(self):
        self.p.stdin.close()
        self.p.wait()


# ---------------- 대본 → 시간표 ----------------

def parse_script(path):
    """script.txt(# 장면 N 머리, 내레이션 줄, '화면:'·'라벨:' 제작 줄) → {장면: [문장]}."""
    import re
    scenes, cur = {}, None
    for line in open(path, encoding="utf-8"):
        s = line.strip()
        m = re.match(r"# 장면 (\d+)", s)
        if m:
            cur = int(m.group(1))
            scenes[cur] = []
            continue
        if s.startswith("# "):
            cur = None
            continue
        if cur is None or not s or re.match(r"(화면|라벨|제목|인물):", s):
            continue
        scenes[cur].append(s)
    return scenes


def syl_time(s, rate=6.2, pad=0.35):
    """문장 길이 추정: 음절/6.2초 + 0.35초(5편 대본 추정과 같은 식). 숫자는 읽는 음절로."""
    import re
    t = s.replace("15만", "십오만").replace("10만", "십만").replace("60일", "육십일").replace("100필", "백필")
    return len(re.findall(r"[가-힣]", t)) / rate + pad


def timeline(scenes):
    """장면별 문장 시작 시각·길이."""
    out, t = {}, 0.0
    for n in sorted(scenes):
        starts, u = [], 0.0
        for s in scenes[n]:
            starts.append(u)
            u += syl_time(s)
        out[n] = {"t0": t, "dur": u, "starts": starts, "sents": scenes[n]}
        t += u
    return out, t


def sentence_at(info, u):
    k = max(i for i, s in enumerate(info["starts"]) if s <= u + 1e-6)
    return k, u - info["starts"][k]
