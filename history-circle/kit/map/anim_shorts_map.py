#!/usr/bin/env python3
"""AI 지도 위에 올릴 애니메이션 정보만 계산: spec.json -> <out>.anim.json (+영역 레이어). 배경은 AI 재채색 지도를 쓴다.
spec의 center/span_lat은 그 AI 지도를 만든 밑그림(ctl.py)과 같아야 좌표가 맞는다."""
import json, math, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
W, H = 2160, 3840
for sp in sys.argv[1:]:
    S = json.load(open(sp)); cx, cy = S['center']; span = S['span_lat']
    k = math.cos(math.radians(cy)); ppd = H / span
    P = lambda lon, lat: (W / 2 + (lon - cx) * k * ppd, H / 2 - (lat - cy) * ppd)
    out = S['out']; A = {'regions': [], 'routes': [], 'markers': [], 'note': S.get('note', ''), 'zoom': S.get('zoom', 1.5)}
    if S.get('regions'):
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        for r in S['regions']:
            c = tuple(r.get('color', [150, 60, 40])); pts = [P(*p) for p in r['poly']]
            pm = Image.new('L', (W, H), 0); ImageDraw.Draw(pm).polygon(pts, fill=255); pm = pm.filter(ImageFilter.GaussianBlur(18))
            edge = ImageChops.subtract(pm, pm.filter(ImageFilter.MinFilter(15)))
            a = ImageChops.lighter(pm.point(lambda v, _a=r.get('alpha', .30): int(v * _a)), edge.point(lambda v: min(255, int(v * 1.6))))  # v7.6: 영역 농도 alpha
            layer = Image.alpha_composite(layer, Image.merge('RGBA', [Image.new('L', (W, H), v) for v in c] + [a]))
            lx, ly = P(*r['label_at']) if r.get('label_at') else (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
            A['regions'].append({'name': r['name'], 'xy': [lx, ly], 'color': list(c), 'size': r.get('size', 76), 'at': r.get('at', .2), 'dur': r.get('dur', 1.3)})
        lp = out.replace('.png', '.layer.png'); layer.save(lp); A['layer'] = lp
    t = .5
    for rt in S.get('routes', []):
        at = rt.get('at', t); dur = rt.get('dur', 1.6); t = at + dur + .2
        A['routes'].append({'pts': [list(P(*p)) for p in rt['pts']], 'color': rt.get('color', [178, 34, 30]), 'label': rt.get('label', ''), 'at': at, 'dur': dur})
    ms = sorted(S.get('markers', []), key=lambda m: not m.get('main')); t = t if S.get('routes') else .4
    for i, m in enumerate(ms):
        A['markers'].append({'xy': list(P(m['lon'], m['lat'])), 'name': m['name'], 'sub': m.get('sub', ''), 'side': m.get('side', 'r'),
                             'main': bool(m.get('main')), 'at': m.get('at', t + .3 * i)})
    A['labels'] = [{'xy': list(P(l['lon'], l['lat'])), 'text': l['text'], 'size': l.get('size', 50), 'color': l.get('color', [40, 80, 105])} for l in S.get('labels', [])]
    f = S.get('focus')
    A['focus'] = [v / s for v, s in zip(P(*f) if f else (A['markers'][0]['xy'] if A['markers'] else (W / 2, H / 2)), (W, H))]
    json.dump(A, open(out.replace('.png', '.anim.json'), 'w'), ensure_ascii=False); print('anim', out)
