#!/usr/bin/env python3
"""AI 재채색용 밑그림(control map): 정확한 해안선·강·고지(갈색)만, 글자 없음. + 검수용 육지 마스크.
사용: python3 ctl.py spec.json out_prefix   → out_prefix.png(1152x2048), out_prefix_land.png"""
import json, math, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
W, H = 1152, 2048
DATA = os.environ.get('MAPDATA', 'mapdata'); REL = os.environ.get('RELIEF', 'relief')
def geo(n): return json.load(open(os.path.join(DATA, n + '.geojson')))['features']
def polys(g): return [g['coordinates']] if g['type'] == 'Polygon' else (g['coordinates'] if g['type'] == 'MultiPolygon' else [])
def lines(g): return [g['coordinates']] if g['type'] == 'LineString' else (g['coordinates'] if g['type'] == 'MultiLineString' else [])
def crop(path, a, b, c, d):
    im = Image.open(path).convert('RGB'); iw, ih = im.size
    return im.resize((W, H), Image.BICUBIC, box=((a + 180) / 360 * iw, (90 - d) / 180 * ih, (b + 180) / 360 * iw, (90 - c) / 180 * ih))
S = json.load(open(sys.argv[1])); pre = sys.argv[2]
cx, cy = S['center']; span = S['span_lat']; k = math.cos(math.radians(cy)); ppd = H / span
P = lambda lo, la: (W / 2 + (lo - cx) * k * ppd, H / 2 - (la - cy) * ppd)
lh, th = (W / 2) / (k * ppd), span / 2
inv = lambda pts, m=1.5: any(cx - lh - m < p[0] < cx + lh + m and cy - th - m < p[1] < cy + th + m for p in pts)
lm = Image.new('L', (W, H), 0); d = ImageDraw.Draw(lm); rings = []
for f in geo('ne_10m_land'):
    for p in polys(f['geometry']):
        if not inv(p[0]): continue
        pts = [P(*q[:2]) for q in p[0]]; d.polygon(pts, fill=255); rings.append(pts)
        for hole in p[1:]: d.polygon([P(*q[:2]) for q in hole], fill=0)
lm.save(pre + '_land.png')
e = np.asarray(crop(os.path.join(REL, 'etopo1.jpg'), cx - lh, cx + lh, cy - th, cy + th), np.float32) / 255
mx = e.max(-1); gr = (e[..., 1] >= e[..., 0])            # 초록 계열 = 저지
elev = np.where(gr, 0.1, np.clip((0.86 - mx) / 0.5, 0, 1) * .8 + .2)
elev = np.asarray(Image.fromarray((elev * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(S.get('blur', 4))), np.float32) / 255
sh = np.asarray(crop(os.path.join(REL, 'shadedrelief.jpg'), cx - lh, cx + lh, cy - th, cy + th).convert('L').filter(ImageFilter.GaussianBlur(2)), np.float32) / 255
low, high = np.array([150, 190, 120], np.float32), np.array([150, 105, 60], np.float32)
land = low + (high - low) * np.clip((elev - .2) / .7, 0, 1)[..., None]
land = land * (0.8 + 0.5 * (sh - sh.mean()))[..., None]
sea = np.array([96, 150, 196], np.float32)
m = np.asarray(lm, np.float32)[..., None] / 255
img = Image.fromarray(np.clip(land * m + sea * (1 - m), 0, 255).astype(np.uint8))
d = ImageDraw.Draw(img)
for pts in rings: d.line(pts + [pts[0]], fill=(40, 40, 40), width=2)
if S.get('water_mask'):  # v7.1: 정밀 하천 면(han_mask.py 등)을 물로 칠함 — 좁은 범위에서 Natural Earth 선은 수 km 어긋남
    wm = Image.open(S['water_mask']).convert('L').resize((W, H))
    img.paste((30, 110, 220), (0, 0), wm); d = ImageDraw.Draw(img)
    img.paste((20, 60, 120), (0, 0), Image.eval(wm.filter(ImageFilter.FIND_EDGES), lambda v: 255 if v > 60 else 0))
if S.get('ne_rivers', True):
    for f in geo('ne_10m_rivers_lake_centerlines'):
        for l in lines(f['geometry']):
            if inv(l, .5): d.line([P(*q[:2]) for q in l], fill=(30, 110, 220), width=6, joint='curve')
img.save(pre + '.png'); print('saved', pre)
