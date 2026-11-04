#!/usr/bin/env python3
"""채색 산수 지도 렌더러 v7: spec.json -> 배경 PNG(2160x3840) + 영역 레이어 + 애니메이션 JSON.
v7: 고도(ETOPO1 색 음영도에서 추정) 기반 청록·황토 채색 + 음영 + 과장된 산 그림 + 굵은 물길 + 수채 바다.
영역·경로·표지·note는 render.py가 시간에 맞춰 그린다(원본 좌표계에 그려서 줌해도 글자가 떨리지 않음)."""
import json, math, sys, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

W, H = 2160, 3840
DATA = os.environ.get('MAPDATA', 'mapdata')
RELIEF = os.environ.get('RELIEF', 'relief')          # etopo1.jpg(5400x2700), shadedrelief.jpg(10800x5400) — basemap-data
FB = os.environ.get('FONT_B', 'fonts/B.ttf')
PAPER = (240, 232, 212); INK = (58, 48, 40)
RIVER = (62, 118, 160)
LAND_STOPS = [(0.0, (178, 204, 142)), (0.3, (196, 202, 146)), (0.55, (210, 186, 132)), (0.8, (196, 158, 112)), (1.0, (160, 128, 100))]

def font(p, s): return ImageFont.truetype(p, s)
def load_geo(n): return json.load(open(os.path.join(DATA, n + '.geojson')))
def polys_of(g):
    t, c = g['type'], g['coordinates']
    return [c] if t == 'Polygon' else (c if t == 'MultiPolygon' else [])
def lines_of(g):
    t, c = g['type'], g['coordinates']
    return [c] if t == 'LineString' else (c if t == 'MultiLineString' else [])
def lowfreq(w, h, cells, seed):
    r = np.random.default_rng(seed).random((cells[1], cells[0])).astype(np.float32)
    return np.asarray(Image.fromarray((r * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255

def crop_eq(path, lon0, lon1, lat0, lat1):
    """등장방형 전지구 이미지에서 경위도 범위를 잘라 W x H로(이 지도의 투영은 경위도에 선형이므로 정확히 맞음)."""
    im = Image.open(path).convert('RGB'); iw, ih = im.size
    box = ((lon0 + 180) / 360 * iw, (90 - lat1) / 180 * ih, (lon1 + 180) / 360 * iw, (90 - lat0) / 180 * ih)
    return im.resize((W, H), Image.BICUBIC, box=box)

def elevation(rgb):
    """ETOPO1 색(초록=저지 → 황갈=중간 → 짙은 갈색=고지)에서 0~1 고도 지수 추정."""
    a = np.asarray(rgb, np.float32) / 255; r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1); v = mx; d = mx - mn + 1e-6
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    tan = np.clip((0.86 - v) / 0.5, 0, 1) * 0.75 + 0.25
    green = np.clip((0.62 - v) / 0.5, 0, 0.15)
    return np.where(h < 75, tan, green).astype(np.float32)

def palette(e):
    out = np.zeros(e.shape + (3,), np.float32)
    xs = [s[0] for s in LAND_STOPS]
    for c in range(3): out[..., c] = np.interp(e, xs, [s[1][c] for s in LAND_STOPS])
    return out

def mountain_img(h, rng, lit, shade):
    """수묵 채색 산 한 덩이(RGBA): 부드럽게 들쭉날쭉한 능선, 왼쪽 위 빛, 바위 주름결, 청록 산자락, 먹 능선, 아래는 번지듯 사라짐."""
    w = h * rng.uniform(1.25, 1.8); ww, hh = int(w) + 10, int(h) + 10
    n = int(rng.integers(9, 15)); kx = np.linspace(0, w, n)
    env = np.clip(np.sin(np.pi * kx / w), 0, 1) ** .7
    jag = rng.uniform(.45, 1.0, n); jag[int(rng.integers(n // 3, 2 * n // 3 + 1))] = 1.0
    ky = env * jag * h; ky[0] = ky[-1] = 0
    X = np.arange(ww, dtype=np.float32) - 5
    hp = np.interp(X, kx, ky)
    hp = np.convolve(hp, np.ones(5) / 5, 'same') + (np.random.default_rng(int(rng.integers(1e9))).random(ww) - .5) * h * .015
    hp = np.clip(hp, 0, None)
    Y = np.arange(hh, dtype=np.float32)[:, None]; top = hh - 5 - hp[None, :]
    depth = (Y - top) / max(8., h)                       # 능선 0 → 아래로 증가
    slope = np.gradient(np.convolve(hp, np.ones(9) / 9, 'same'))
    litf = np.tanh(slope * 1.6) * .5 + .5
    g = np.random.default_rng(int(rng.integers(1e9)))
    furrow = np.asarray(Image.fromarray((g.random((max(2, hh // 18), max(2, ww // 4))) * 255).astype(np.uint8)).resize((ww, hh), Image.BICUBIC), np.float32) / 255
    lit_c, sh_c = np.array(lit, np.float32), np.array(shade, np.float32)
    col = sh_c + (lit_c - sh_c) * np.clip(litf[None, :] + (furrow - .5) * .5, 0, 1)[..., None]
    col = col * (1 - .22 * np.clip(depth, 0, 1))[..., None]
    rim = np.exp(-np.clip(depth, 0, None) * h / 4)[..., None] * litf[None, :, None] * .35
    col = col + (255 - col) * rim                          # 빛 받는 능선 가장자리 밝게
    foot = np.clip((depth - .35) / .45, 0, 1)[..., None] * .7
    col = col * (1 - foot) + np.array([92, 142, 110], np.float32) * foot
    alpha = (depth >= 0) * np.clip(1 - (depth - .85) / .3, 0, 1) * 240
    im = Image.fromarray(np.dstack([np.clip(col, 0, 255), alpha[..., None]]).astype(np.uint8), 'RGBA')
    d = ImageDraw.Draw(im, 'RGBA'); ridge = [(float(x) + 5, hh - 5 - float(y)) for x, y in zip(X - 5 + 5, hp)][::3]
    d.line(ridge, fill=INK + (190,), width=max(2, int(h / 45)), joint='curve')
    pk = [j for j in range(1, n - 1) if ky[j] >= ky[j - 1] and ky[j] >= ky[j + 1]]
    for j in pk:
        x0, y0 = kx[j] + 5, hh - 5 - ky[j]
        for q in range(int(1 + h / 55)):
            L = h * rng.uniform(.12, .32) * (ky[j] / h); dx = rng.uniform(.05, .35) * L
            d.line([(x0 + dx * .2, y0 + 3), (x0 + dx * .6, y0 + L * .6), (x0 + dx, y0 + L)], fill=INK + (95,), width=max(1, int(h / 75)))
    return im

def main(spec_path):
    S = json.load(open(spec_path))
    cx, cy = S['center']; span = S.get('span_lat', 9.0); ex = S.get('exaggerate', 1.0)
    k = math.cos(math.radians(cy)); ppd = H / span
    P = lambda lon, lat: (W / 2 + (lon - cx) * k * ppd, H / 2 - (lat - cy) * ppd)
    lh, th = (W / 2) / (k * ppd), span / 2
    inview = lambda pts, m=1.5: any(cx - lh - m < p[0] < cx + lh + m and cy - th - m < p[1] < cy + th + m for p in pts)
    lon0, lon1, lat0, lat1 = cx - lh, cx + lh, cy - th, cy + th

    lm = Image.new('L', (W, H), 0); md = ImageDraw.Draw(lm); rings = []
    for f in load_geo('ne_10m_land')['features']:
        for poly in polys_of(f['geometry']):
            if not inview(poly[0]): continue
            pts = [P(*p[:2]) for p in poly[0]]; md.polygon(pts, fill=255); rings.append(pts)
            for hole in poly[1:]: md.polygon([P(*p[:2]) for p in hole], fill=0)
    land = np.asarray(lm.filter(ImageFilter.GaussianBlur(2)), np.float32)[..., None] / 255

    relief = S.get('relief', span >= 2.0)   # 도성 주변처럼 좁은 범위는 고도 자료(약 7km 격자)가 너무 거칠어 끔
    e = elevation(crop_eq(os.path.join(RELIEF, 'etopo1.jpg'), lon0, lon1, lat0, lat1)) if relief else np.zeros((H, W), np.float32)
    e = np.asarray(Image.fromarray((e * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)), np.float32) / 255
    sh = np.zeros((H, W), np.float32) if not relief else np.asarray(crop_eq(os.path.join(RELIEF, 'shadedrelief.jpg'), lon0, lon1, lat0, lat1).convert('L').filter(ImageFilter.GaussianBlur(4)), np.float32) / 255
    sh = ((sh - sh[land[..., 0] > .5].mean() if (land > .5).any() else sh - .5) * (1.6 * ex)) if relief else sh
    wash = lowfreq(W, H, (14, 24), 3)[..., None]; fine = lowfreq(W, H, (120, 210), 4)[..., None]

    col = palette(e) * (1 + np.clip(sh, -.45, .35)[..., None]) * (0.94 + 0.1 * wash) * (0.97 + 0.06 * fine)
    coast = np.asarray(lm.filter(ImageFilter.GaussianBlur(70)), np.float32)[..., None] / 255
    seaC = np.array([118, 176, 196], np.float32); seaF = np.array([200, 218, 212], np.float32)
    far = np.clip(1 - coast * 2.2, 0, 1)
    sea = seaC * (1 - far) + seaF * far
    sea = sea * (0.93 + 0.12 * wash) + (np.array(PAPER, np.float32) - sea) * np.clip(far - .55, 0, 1) * .6
    img = col * land + sea * (1 - land)
    rose = lowfreq(W, H, (4, 6), 8)[..., None]
    if S.get('rose', True):  # 예시처럼 가장자리 분홍 번짐
        edge = np.clip(np.maximum(np.abs(np.linspace(-1, 1, W))[None, :], np.abs(np.linspace(-1, 1, H))[:, None]) - .72, 0, 1)[..., None] / .28
        img = img * (1 - edge * rose * .55) + np.array([228, 190, 190], np.float32) * edge * rose * .55
    hanji = (lowfreq(W // 2, H // 2, (300, 520), 9) - .5)
    img = img * (1 + np.asarray(Image.fromarray(((hanji + .5) * 255).astype(np.uint8)).resize((W, H)), np.float32)[..., None] / 255 * .08 - .04)
    img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

    d = ImageDraw.Draw(img, 'RGBA')
    ln = Image.new('L', (W, H), 0); ld = ImageDraw.Draw(ln)
    for pts in rings: ld.line(pts + [pts[0]], fill=255, width=5, joint='curve')
    img = Image.composite(Image.new('RGB', (W, H), (70, 98, 108)), img, ln.filter(ImageFilter.GaussianBlur(1.3)).point(lambda v: int(v * .85)))

    # 과장된 산: 고지일수록 크고 촘촘히. 뒤(위)에서 앞(아래) 순서로 겹쳐 그림
    rng = np.random.default_rng(S.get('seed', 11)); step = int(S.get('mountain_step', 54)); mts = []
    thr = S.get('mountain_min', .34)
    for yy in range(step, H, step):
        for xx in range(step // 2, W, step):
            x = xx + rng.uniform(-.45, .45) * step; y = yy + rng.uniform(-.45, .45) * step
            xi, yi = int(min(W - 1, max(0, x))), int(min(H - 1, max(0, y)))
            ev = e[yi, xi]
            if land[yi, xi, 0] < .9 or ev < thr or rng.random() > (ev - thr) / (1 - thr) * S.get('mountain_density', 2.0): continue
            mts.append((y, x, ev))
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for y, x, ev in sorted(mts):
        h = (50 + 170 * ((ev - thr) / (1 - thr)) ** 1.2) * ex * S.get('mountain_scale', 1.0)
        lit = tuple(min(255, int(v * 1.12)) for v in palette(np.array([min(1, ev * .75)]))[0])
        shade = tuple(int(v * .66) for v in palette(np.array([ev]))[0])
        g = mountain_img(h, rng, lit, shade)
        ox, oy = int(x - g.width / 2), int(y - g.height + 6); layer.paste(g, (ox, oy), g)
    img.paste(layer.filter(ImageFilter.GaussianBlur(.8)), (0, 0), layer.filter(ImageFilter.GaussianBlur(.8)))

    d = ImageDraw.Draw(img, 'RGBA')
    rw = S.get('river_width', 15)
    riv = [[P(*p[:2]) for p in l] for f in load_geo('ne_10m_rivers_lake_centerlines')['features'] for l in lines_of(f['geometry']) if inview(l, 0.5)]
    riv += [[P(*p) for p in rv['pts']] for rv in S.get('rivers_extra', [])]
    for l in riv: d.line(l, fill=(236, 242, 236, 170), width=int(rw * 2.1), joint='curve')
    for l in riv: d.line(l, fill=RIVER + (235,), width=rw, joint='curve')
    for lb in S.get('labels', []):
        d.text(P(lb['lon'], lb['lat']), lb['text'], font=font(FB, lb.get('size', 50)), fill=tuple(lb.get('color', [40, 80, 105])) + (235,),
               anchor='mm', stroke_width=5, stroke_fill=PAPER + (210,))
    out = S['out']; img.save(out)

    A = {'regions': [], 'routes': [], 'markers': [], 'note': S.get('note', ''), 'zoom': S.get('zoom', 1.5)}
    lmask = lm
    if S.get('regions'):
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        for r in S['regions']:
            c = tuple(r.get('color', [150, 60, 40])); pts = [P(*p) for p in r['poly']]
            pm = Image.new('L', (W, H), 0); ImageDraw.Draw(pm).polygon(pts, fill=255)
            pm = pm.filter(ImageFilter.GaussianBlur(18))
            edge = ImageChops.multiply(ImageChops.subtract(pm, pm.filter(ImageFilter.MinFilter(15))), lmask)
            a = ImageChops.lighter(ImageChops.multiply(pm, lmask).point(lambda v: int(v * 0.30)), edge.point(lambda v: min(255, int(v * 1.6))))
            layer = Image.alpha_composite(layer, Image.merge('RGBA', [Image.new('L', (W, H), v) for v in c] + [a]))
            lx, ly = P(*r['label_at']) if r.get('label_at') else (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
            A['regions'].append({'name': r['name'], 'xy': [lx, ly], 'color': list(c), 'size': r.get('size', 76),
                                 'at': r.get('at', 0.2), 'dur': r.get('dur', 1.3)})
        lp = out.replace('.png', '.layer.png'); layer.save(lp); A['layer'] = lp
    t = 0.5
    for rt in S.get('routes', []):
        at = rt.get('at', t); dur = rt.get('dur', 1.6); t = at + dur + 0.2
        A['routes'].append({'pts': [list(P(*p)) for p in rt['pts']], 'color': rt.get('color', [178, 34, 30]),
                            'label': rt.get('label', ''), 'at': at, 'dur': dur})
    ms = sorted(S.get('markers', []), key=lambda m: not m.get('main'))
    t = t if S.get('routes') else 0.4
    for i, m in enumerate(ms):
        x, y = P(m['lon'], m['lat'])
        A['markers'].append({'xy': [x, y], 'name': m['name'], 'sub': m.get('sub', ''), 'side': m.get('side', 'r'),
                             'main': bool(m.get('main')), 'at': m.get('at', t + 0.3 * i)})
    f = S.get('focus')
    A['focus'] = [v / s for v, s in zip(P(*f) if f else (A['markers'][0]['xy'] if A['markers'] else (W / 2, H / 2)), (W, H))]
    json.dump(A, open(out.replace('.png', '.anim.json'), 'w'), ensure_ascii=False)
    print('saved', out, 'mountains', len(mts))

if __name__ == '__main__':
    for p in sys.argv[1:]: main(p)
