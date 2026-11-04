#!/usr/bin/env python3
"""행정경계(통계청 행정동, vuski/admdongkor)의 한강 양안 시군구 경계 = 한강 중심선 → 폭을 입혀 하천 마스크.
사용: python3 han_mask.py spec.json out_mask.png [W H] [폭_km]"""
import json, math, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
S = json.load(open(sys.argv[1])); out = sys.argv[2]
W, H = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (1152, 2048)
wkm = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
cx, cy = S['center']; span = S['span_lat']; k = math.cos(math.radians(cy)); ppd = H / span
P = lambda lo, la: (W / 2 + (lo - cx) * k * ppd, H / 2 - (la - cy) * ppd)
NORTH = {'마포구', '용산구', '성동구', '광진구', '구리시', '남양주시', '고양시덕양구'}
SOUTH = {'강서구', '양천구', '영등포구', '동작구', '서초구', '강남구', '송파구', '강동구', '하남시'}
F = json.load(open(S.get('adm', 'kr/hjd.geojson')))['features']
def mask(names):
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    for f in F:
        if f['properties']['sggnm'] not in names: continue
        g = f['geometry']; ps = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
        for p in ps:
            d.polygon([P(*q[:2]) for q in p[0]], fill=255)
    return m
n, s = mask(NORTH), mask(SOUTH)
cl = ImageChops.multiply(n.filter(ImageFilter.MaxFilter(5)), s.filter(ImageFilter.MaxFilter(5)))   # 공유 경계 = 중심선
px = wkm / 111.0 * ppd            # 하폭(픽셀)
r = int(px / 2) | 1
river = cl.filter(ImageFilter.MaxFilter(min(r * 2 + 1, 255))) if r * 2 + 1 <= 255 else cl
river = river.filter(ImageFilter.GaussianBlur(px / 8)).point(lambda v: 255 if v > 100 else 0)
if S.get('east_ne_from'):  # 행정경계로 안 잡히는 동쪽 끝(두물머리 쪽)은 Natural Earth 선으로 이어 붙임
    d = ImageDraw.Draw(river); lo0 = S['east_ne_from']
    for f in json.load(open('mapdata/ne_10m_rivers_lake_centerlines.geojson'))['features']:
        g = f['geometry']; ls = [g['coordinates']] if g['type'] == 'LineString' else g['coordinates']
        for l in ls:
            seg = [q for q in l if q[0] >= lo0 and abs(q[1] - cy) < span]
            if len(seg) > 1: d.line([P(*q[:2]) for q in seg], fill=255, width=int(px), joint='curve')
river.save(out)
for m in S.get('markers', []):
    x, y = P(m['lon'], m['lat'])
    # 가장 가까운 강 픽셀까지 거리
    import numpy as np
    a = np.asarray(river) > 0; yy, xx = np.nonzero(a)
    dmin = np.hypot(xx - x, yy - y).min() / ppd * 111 if len(xx) else -1
    print(m['name'], 'in_river' if a[int(y), int(x)] else 'ok', f'강까지 {dmin:.2f}km')
print('river px width', round(px, 1))
