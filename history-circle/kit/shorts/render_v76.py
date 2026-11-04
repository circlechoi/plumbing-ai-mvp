#!/usr/bin/env python3
"""역사 숏폼 렌더러 v7.6: scenes.json -> final.mp4 (1080x1920, 30fps)
카메라(이징·펀치·컷인·포커스·흔들림) + 전환(먹 번짐·휩·플래시·페이드·컷) + 지도 애니메이션
+ 세이프존 자막(팝인·금색 강조) + 톤 통일(한지 질감·그레인·비네트) + 사운드(효과음·앰비언스·BGM 덕킹)."""
import json, math, os, subprocess, sys, urllib.request, wave
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageEnhance

W, H, SW, SH, FPS, SR = 1080, 1920, 2160, 3840, 30, 44100
PAPER = (236, 227, 206); INKC = np.array([40, 34, 28], np.float32); GOLD = (242, 201, 76)
S = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'scenes.json'))
PREVIEW = os.environ.get('PREVIEW')  # "3.2,10.5,..." -> 해당 시각 프레임만 PNG로 저장
T = float(S['total']); SC = S['scenes']; N = len(SC)
FSM, FB, FX = S.get('font_sm', 'fonts/SM.ttf'), S.get('font_b', 'fonts/B.ttf'), S.get('font_x', 'fonts/X.ttf')
FT = S.get('font_title', 'fonts/NSK.ttf')  # v7.6: 상단 제목 = 본고딕 Black(이전: 검은고딕 fonts/BHS.ttf)
TD = {'ink': 0.6, 'whip_l': 0.32, 'whip_r': 0.32, 'flash': 0.4, 'fade': 0.4, 'cut': 0.0}
SFX_OF = {'ink': 'brush', 'whip_l': 'whoosh', 'whip_r': 'whoosh', 'flash': 'boom', 'fade': None, 'cut': 'hit'}
st = [float(s['start']) for s in SC]; en = st[1:] + [T]
tr = [s.get('trans', 'ink' if i else 'cut') for i, s in enumerate(SC)]
td = [TD[x] if i else 0 for i, x in enumerate(tr)]
LAYOUT = dict(badge_y=245, note_y=550, title_y=425, title_s_y=392, wm_y=245, punch_y=900, cap1_y=1276, cap2_y=1380, src_y=1508, maxw=840, band=(1130, 1610))
LAYOUT.update(S.get('layout', {}))
_fc = {}
def font(p, s):
    k = (p, int(s))
    if k not in _fc:
        _fc[k] = ImageFont.truetype(p, max(8, int(s)))
        if 'NSK' in p: _fc[k].set_variation_by_name('Black')  # v7.6: 제목 = 본고딕 Black(가변 서체, 글자별 굵기 균일)
    return _fc[k]
cl = lambda v, a=0., b=1.: max(a, min(b, v))
eio = lambda x: (lambda x: 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2)(cl(x))
eoexp = lambda x: 1 if x >= 1 else 1 - 2 ** (-10 * cl(x))
eoback = lambda x: (lambda x: 1 + 2.7 * (x - 1) ** 3 + 1.7 * (x - 1) ** 2)(cl(x))

# ---------- 원본 준비 (톤 통일) ----------
os.makedirs('img', exist_ok=True)
rng = np.random.default_rng(3)
def lowfreq(w, h, cells, seed):
    r = np.random.default_rng(seed).random((cells[1], cells[0])).astype(np.float32)
    return np.asarray(Image.fromarray((r * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
hanji = Image.fromarray(np.clip(128 + (lowfreq(SW // 2, SH // 2, (180, 320), 1) - .5) * 60 + rng.normal(0, 6, (SH // 2, SW // 2)), 0, 255).astype(np.uint8)).resize((SW, SH))
def grade(im):
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(S.get('saturation', 1.22))).enhance(1.08)
    a = np.asarray(im, np.float32); lum = a.mean(-1, keepdims=True) / 255
    a = a + (np.array([14, 6, -8], np.float32) * lum + np.array([-6, 2, 10], np.float32) * (1 - lum))  # 하이라이트 따뜻, 그림자 청록
    a = a * 0.97 + 6 + (np.asarray(hanji, np.float32)[..., None] - 128) * 0.08  # 한지 결
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
SRC = {}
def sample(src, l, t, w, h):  # 부동소수 박스로 잘라 1080x1920으로(서브픽셀 이동 → 떨림 없음)
    return src.resize((W, H), Image.BICUBIC, box=(l, t, l + w, t + h))
def load_src(u, is_map):
    if u in SRC: return SRC[u]
    p = u
    if u.startswith('http'):
        p = f'img/{len(SRC)}.png'; urllib.request.urlretrieve(u, p)
    im = Image.open(p).convert('RGB')
    if is_map:  # v7: AI 재채색 지도는 밑그림(9:16)을 비율 그대로 늘려 그린 것이라 자르지 않고 정확히 2160x3840으로 맞춤(좌표 일치)
        im = im.resize((SW, SH), Image.LANCZOS)
    else:
        sc = max(SW / im.width, SH / im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
        l, t = (im.width - SW) // 2, (im.height - SH) // 2; im = im.crop((l, t, l + SW, t + SH))
    SRC[u] = im if is_map else grade(im); return SRC[u]

MAPS = {}
def load_map(i):
    if i in MAPS: return MAPS[i]
    A = json.load(open(SC[i]['map'])); M = {'A': A}
    if A.get('layer'):
        L = np.asarray(Image.open(A['layer']).convert('RGBA'), np.float32)
        M['rgb'], M['a'] = L[..., :3], L[..., 3:] / 255
        yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)
        d = np.full((SH, SW), 1e9, np.float32)
        for r in A['regions']: d = np.minimum(d, np.hypot(xx - r['xy'][0], yy - r['xy'][1]))
        M['dist'] = d / d.max() + (lowfreq(SW, SH, (12, 20), 5) - .5) * 0.25
    MAPS[i] = M; return M

# ---------- 카메라 ----------
def camera(i, u):
    s = SC[i]; D = en[i] - st[i] + (td[i + 1] if i + 1 < N else 0); x = u / D
    mv = s.get('move', ['in', 'out', 'pan_r', 'pan_l'][i % 4]); fx, fy = s.get('focus', [.5, .45])
    if s.get('map') and 'focus' not in s: fx, fy = load_map(i)['A']['focus']
    z, cx, cy = 1.0, .5, .5
    if mv == 'in': z = 1 + .16 * eio(x); cx, cy = .5 + (fx - .5) * eio(x), .5 + (fy - .5) * eio(x)
    elif mv == 'out': z = 1.18 - .18 * eio(x)
    elif mv in ('pan_l', 'pan_r'): z = 1.16; o = .36 + .28 * eio(x); cx = o if mv == 'pan_r' else 1 - o
    elif mv == 'punch': z = 1.36 - .28 * eoexp(u / .7) + .05 * x; cx, cy = fx, fy
    elif mv == 'still': z = 1.03 + .03 * x
    elif mv == 'cutin':
        if x < .5: z = 1 + .08 * eio(x * 2)
        else: z = 1.45 + .08 * (x - .5); cx, cy = fx, fy
    elif mv == 'focus':  # 지도: 잠시 전체를 보여준 뒤 표지로 다가감
        zt = s.get('zoom', load_map(i)['A'].get('zoom', 1.5) if s.get('map') else 1.5); e = eio((u - .5) / max(.1, D - 1.2))
        z = 1 + (zt - 1) * e; cx, cy = .5 + (fx - .5) * e, .5 + (fy - .5) * e
    k = 0
    if mv in ('punch',) or (mv == 'cutin' and x >= .5): k = .012 * math.exp(-(u - (0 if mv == 'punch' else D / 2)) * 7) if u >= (0 if mv == 'punch' else D / 2) else 0
    if 'shake' in s.get('fx', []): k += .0035
    cx += k * (math.sin(u * 23.1) + .5 * math.sin(u * 37.7)); cy += k * (math.cos(u * 19.3) + .5 * math.sin(u * 31.9))
    w, h = SW / z, SH / z
    l, t = cl(cx * SW - w / 2, 0, SW - w), cl(cy * SH - h / 2, 0, SH - h)
    return l, t, w, h

# ---------- 지도 애니메이션 (출력 좌표에 그림) ----------
def dash_path(d, pts, p, col, wd):
    seg = [(pts[j], pts[j + 1], math.dist(pts[j], pts[j + 1])) for j in range(len(pts) - 1)]
    L = sum(s[2] for s in seg); lim = L * p; acc = 0; dash = 17 * wd / 5; tip = pts[0]
    for a, b, sl in seg:
        n = max(1, int(sl // dash))
        for q in range(n):
            s0 = acc + sl * q / n
            if s0 > lim: break
            s1 = min(acc + sl * (q + 1) / n, lim); tip = (a[0] + (b[0] - a[0]) * (s1 - acc) / sl, a[1] + (b[1] - a[1]) * (s1 - acc) / sl)
            if q % 2 == 0:
                d.line([(a[0] + (b[0] - a[0]) * (s0 - acc) / sl, a[1] + (b[1] - a[1]) * (s0 - acc) / sl), tip], fill=col, width=int(wd))
        acc += sl
    return tip, seg[-1]

def draw_map(i, im, u):  # v7: 원본(2160x3840) 좌표에 고정 크기로 그림 → 카메라가 통째로 서브픽셀 이동(글자 떨림 없음)
    M = load_map(i); A = M['A']; s = 1.0
    O = lambda x, y: (x, y)
    d = ImageDraw.Draw(im, 'RGBA'); P = PAPER
    for lb in A.get('labels', []):  # v7: AI 지도 위 고정 라벨(강·바다 이름, '?' 등)
        d.text(O(*lb['xy']), lb['text'], font=font(FB, lb['size']), fill=tuple(lb['color']) + (235,), anchor='mm', stroke_width=6, stroke_fill=P + (220,))
    for r in A['regions']:
        a = cl((u - r['at']) / r['dur']) ** .7
        if a > .3:
            x, y = O(*r['xy']); c = tuple(r['color'])
            d.text((x, y), r['name'], font=font(FX, r['size'] * s), fill=c + (int(235 * cl((a - .3) / .7)),), anchor='mm', stroke_width=max(1, int(5 * s)), stroke_fill=P + (220,))
    for rt in A['routes']:
        p = eio((u - rt['at']) / rt['dur'])
        if p <= 0: continue
        col = tuple(rt['color']) + (230,); pts = [O(*q) for q in rt['pts']]
        tip, (a, b, _) = dash_path(d, pts, p, col, 10 * s)
        if p < 1: rr = 11 * s; d.ellipse([tip[0] - rr, tip[1] - rr, tip[0] + rr, tip[1] + rr], fill=col)
        else:
            ang = math.atan2(b[1] - a[1], b[0] - a[0]); z = 46 * s; tp = (b[0] - math.cos(ang) * 30 * s, b[1] - math.sin(ang) * 30 * s)
            d.polygon([tp, (tp[0] - z * math.cos(ang - .45), tp[1] - z * math.sin(ang - .45)), (tp[0] - z * math.cos(ang + .45), tp[1] - z * math.sin(ang + .45))], fill=col)
        if rt['label'] and p > .5:
            mx, my = (pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2
            d.text((mx + 40 * s, my), rt['label'], font=font(FB, 54 * s), fill=col[:3] + (int(230 * cl((p - .5) * 3)),), anchor='lm', stroke_width=max(1, int(4 * s)), stroke_fill=P + (230,))
    for m in A['markers']:
        v = u - m['at']
        if v <= 0: continue
        x, y = O(*m['xy']); R = (26 if m['main'] else 18) * s; k = eoback(v / .35)
        if v < .8:  # 먹 번지는 파문
            rr = R * (1.2 + 2.6 * v / .8); d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=(170, 38, 32, int(160 * (1 - v / .8))), width=max(2, int(6 * s)))
        r2 = R * k
        d.ellipse([x - r2 - 8 * s, y - r2 - 8 * s, x + r2 + 8 * s, y + r2 + 8 * s], fill=P + (200,))
        d.ellipse([x - r2, y - r2, x + r2, y + r2], fill=(170, 38, 32, 240)); d.ellipse([x - r2 * .35, y - r2 * .35, x + r2 * .35, y + r2 * .35], fill=P + (255,))
        la = cl((v - .15) / .3)
        if la <= 0: continue
        side = m['side']; off = R + 26 * s; rise = (1 - la) * 20 * s
        an = {'r': 'lm', 'l': 'rm', 'u': 'md', 'd': 'ma'}[side]
        tx, ty = {'r': (x + off, y), 'l': (x - off, y), 'u': (x, y - off), 'd': (x, y + off)}[side]; ty += rise
        fs = (86 if m['main'] else 64) * s
        d.text((tx, ty), m['name'], font=font(FX, fs), fill=(40, 32, 26, int(255 * la)), anchor=an, stroke_width=max(1, int(9 * s)), stroke_fill=P + (int(245 * la),))
        if m['sub']:
            sy = ty + (fs * .75 if side in 'rl' else (fs + 10 * s if side == 'd' else -fs - 10 * s))
            d.text((tx, sy), m['sub'], font=font(FB, 46 * s), fill=(70, 52, 40, int(255 * la)), anchor=an.replace('m', 'a') if side in 'rl' else an, stroke_width=max(1, int(8 * s)), stroke_fill=P + (int(245 * la),))

def map_base(i, u):
    M = load_map(i); base = SRC[SC[i]['image']]
    if 'rgb' not in M: return base
    a = max([cl((u - r['at']) / r['dur']) for r in M['A']['regions']] or [1])
    if a >= 1 and 'full' in M: return M['full']
    if a <= 0: return base
    rev = np.clip((a * 1.25 - M['dist']) / .08, 0, 1)[..., None] * M['a']
    out = Image.fromarray((np.asarray(base, np.float32) * (1 - rev) + M['rgb'] * rev).astype(np.uint8))
    if a >= 1: M['full'] = out
    return out

# ---------- 장면 프레임 ----------
MIST = lowfreq(W, H * 2, (6, 18), 9)
VID = {}
def load_vid(u):  # v7.3: 움직이는 컷(Kling 등) — 1080x1920 프레임 배열로 미리 풀어 둠, 톤 통일(v7 grade 근사)
    if u in VID: return VID[u]
    p = u
    if u.startswith('http'): p = f'img/v{len(VID)}.mp4'; urllib.request.urlretrieve(u, p)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-an', '-vf', f'fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},eq=saturation=1.15:contrast=1.05,lutrgb=r=val*0.97+6:g=val*0.97+6:b=val*0.97+6',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    VID[u] = a; return a
def scene_frame(i, t):
    s = SC[i]; u = t - st[i]; is_map = bool(s.get('map'))
    if s.get('video'):
        a = load_vid(s['video']); k = int(cl(u, 0, 99) * FPS) + int(s.get('vstart', 0) * FPS)
        return Image.fromarray(a[min(len(a) - 1, k)])
    src = load_src(s['image'], is_map)
    if is_map: src = map_base(i, u).copy(); draw_map(i, src, u)
    cam = camera(i, u); l, tp, w, h = cam
    im = sample(src, l, tp, w, h)
    if 'mist' in s.get('fx', []):
        o = int((u * 38) % H); m = MIST[o:o + H] ** 2 * .42
        a = np.asarray(im, np.float32); im = Image.fromarray((a * (1 - m[..., None]) + np.array(PAPER, np.float32) * m[..., None]).astype(np.uint8))
    return im

INKN = lowfreq(W, H, (9, 16), 11) * .75 + lowfreq(W, H, (40, 70), 12) * .25
def transition(A, B, p, kind):
    if kind in ('fade', 'cut'): return Image.blend(A, B, p)
    a, b = np.asarray(A, np.float32), np.asarray(B, np.float32)
    if kind == 'ink':
        q = eio(p) * 1.35 - .15; v = (q - INKN) / .07; m = np.clip(v, 0, 1)[..., None]
        e = np.exp(-(v - .5) ** 2 * 1.5)[..., None] * .45 * (1 - p)
        o = a * (1 - m) + b * m; o = o * (1 - e) + INKC * e
    elif kind == 'flash':
        pc = np.array([244, 236, 216], np.float32)
        o = a + (pc - a) * cl(p * 2.2) if p < .5 else b + (pc - b) * cl((1 - p) * 2.2)
    else:
        sg = 1 if kind == 'whip_l' else -1; e = eio(p); sp = math.sin(math.pi * p)
        strip = np.concatenate([a, b], 1) if sg > 0 else np.concatenate([b, a], 1)
        off = int(e * W) if sg > 0 else int((1 - e) * W)
        blur = int(sp * 90); acc = np.zeros_like(a); n = 7
        for k in range(n):
            ox = cl(off + int((k / (n - 1) - .5) * blur), 0, W); acc += strip[:, ox:ox + W]
        o = acc / n
    return Image.fromarray(np.clip(o, 0, 255).astype(np.uint8))

# ---------- HUD (세이프존 기준 고정 위치) ----------
NOGLYPH = set('◀▶·『』「」…※')
def text_img(txt, size, color, fp_main, stroke=4, maxw=None, sw=None):
    segs, gold = [], False  # {단어} -> 금색
    for ch in txt:
        if ch == '{': gold = True; continue
        if ch == '}': gold = False; continue
        c = GOLD if gold else ((232, 214, 170) if txt.startswith('[') and ']' in txt and len(segs) <= txt.index(']') else color)
        fp = 'CIRC' if 0x2460 <= ord(ch) <= 0x2473 else (FB if ch in NOGLYPH else fp_main)
        if segs and segs[-1][1] == fp and segs[-1][2] == c: segs[-1][0] += ch
        else: segs.append([ch, fp, c])
    while True:
        wid = sum(len(t) * size * 1.04 if fp == 'CIRC' else font(fp, size).getlength(t) for t, fp, _ in segs)
        if not maxw or wid <= maxw or size < 20: break
        size -= 2
    pad = stroke * 2 + 6; im = Image.new('RGBA', (int(wid) + pad * 2, int(size * 1.45) + pad * 2)); d = ImageDraw.Draw(im); x = pad
    for t, fp, c in segs:
        f = None if fp == 'CIRC' else font(fp, size)
        if fp == 'CIRC':  # ①~⑳: 어떤 서체에도 없어 원+숫자로 직접 그림
            for ch in t:
                n = str(ord(ch) - 0x245F); r = size * .46; cx0, cy0 = x + r + size * .04, pad + size * .72 - size * .36
                d.ellipse([cx0 - r, cy0 - r, cx0 + r, cy0 + r], outline=c, width=max(2, int(size * .07)))
                d.text((cx0, cy0), n, font=font(FB, size * (.62 if len(n) == 1 else .5)), fill=c, anchor='mm'); x += 2 * r + size * .12
            continue
        d.text((x, pad + size * .72), t, font=f, fill=c + (255,) if len(c) == 3 else c, anchor='ls', stroke_width=stroke, stroke_fill=(0, 0, 0, 190)); x += f.getlength(t)
    bb = im.getchannel('A').getbbox()  # v7: 실제 잉크 폭 기준으로 좌우 여백을 같게(『』·[ ] 같은 전각 부호의 빈 공간 때문에 한쪽으로 쏠리던 문제)
    if bb:
        out = Image.new('RGBA', (bb[2] - bb[0] + pad * 2, im.height)); out.paste(im.crop((bb[0], 0, bb[2], im.height)), (pad, 0)); im = out
    return im
def paste(im, t_im, cx, cy, alpha=1., scale=1., anchor='c'):
    if alpha <= 0: return
    if scale != 1: t_im = t_im.resize((max(1, int(t_im.width * scale)), max(1, int(t_im.height * scale))), Image.BICUBIC)
    if alpha < 1: t_im = t_im.copy(); t_im.putalpha(t_im.getchannel('A').point(lambda v: int(v * alpha)))
    x = cx - t_im.width // 2 if anchor == 'c' else (cx if anchor == 'l' else cx - t_im.width)
    im.alpha_composite(t_im, (int(x), int(cy - t_im.height // 2)))
L = LAYOUT; y0, y1 = L['band']
band = np.zeros((H, W), np.float32); yy = np.arange(H)
band[:] = np.interp(yy, [y0, y0 + 110, y1 - 60, y1 + 100], [0, .5, .5, 0])[:, None]
BAND = Image.fromarray(np.zeros((H, W, 3), np.uint8)).convert('RGBA'); BAND.putalpha(Image.fromarray((band * 255).astype(np.uint8)))
VIG = Image.new('L', (W, H), 0); ImageDraw.Draw(VIG).ellipse([-W * .25, -H * .12, W * 1.25, H * 1.12], fill=255)
VIG = np.asarray(VIG.filter(ImageFilter.GaussianBlur(160)), np.float32)[..., None] / 255 * .26 + .74
VIGIMG = Image.fromarray((VIG[..., 0] * 255).astype(np.uint8)).convert('RGB')
GRAIN = [Image.fromarray(np.clip(16 + np.random.default_rng(20 + k).normal(0, 5.5, (H // 2, W // 2)), 0, 255).astype(np.uint8)).resize((W, H)).convert('RGB') for k in range(4)]
def seal_img(sz):  # v7.3: 연대 배지 문양 = 붉은 낙관 '史' (사용자 결정 C안, 2026-09-29)
    im = Image.new('RGBA', (sz, sz)); d = ImageDraw.Draw(im); red, pap = (170, 38, 32), (245, 232, 210)
    d.rounded_rectangle([2, 2, sz - 3, sz - 3], radius=sz // 9, fill=red)
    d.rounded_rectangle([sz * .1, sz * .1, sz * .9, sz * .9], radius=sz // 12, outline=pap, width=max(2, sz // 22))
    fp = S.get('font_seal', 'fonts/SEAL.ttf')
    if os.path.exists(fp):
        f = ImageFont.truetype(fp, int(sz * .62))
        try: f.set_variation_by_name('Black')
        except Exception: pass
        d.text((sz / 2, sz / 2 + 1), '史', font=f, fill=pap, anchor='mm')
    a = np.asarray(im).copy(); n = np.random.default_rng(1).random(a.shape[:2]) < .06; a[n & (a[..., 3] > 0), 3] = 90  # 인주 번짐 결
    return Image.fromarray(a)
def badge_img(txt):  # v7.3: 배경 상자 없음 · ◀▶ 제거 · 낙관 + 금색 글자 + 부드러운 그림자
    txt = txt.replace('◀', '').replace('▶', '').strip()
    t = text_img(txt, 38, GOLD, FB, 4); sz = 46
    im = Image.new('RGBA', (sz + 12 + t.width, max(sz, t.height) + 8))
    im.alpha_composite(seal_img(sz), (0, (im.height - sz) // 2)); im.alpha_composite(t, (sz + 12, (im.height - t.height) // 2))
    sh = Image.new('RGBA', (im.width + 10, im.height + 10)); sa = Image.new('L', sh.size, 0); sa.paste(im.getchannel('A'), (4, 6))
    sh.putalpha(sa.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * .6))); sh.alpha_composite(im, (0, 0))
    return sh
CAPS = []
for i, s in enumerate(SC):
    last = i == N - 1; a, b = s.get('cap', ['', ''])
    CAPS.append((text_img(a, S.get('cap1_size', 60), (255, 255, 255), FSM, 4, L['maxw']) if a else None,  # v7.5: 자막 확대(48/58 -> 60/80)
                 text_img(b, S.get('cap2_size', 80) + (4 if last else 0), GOLD if last else (255, 255, 255), FSM, 5, L['maxw']) if b else None,
                 badge_img(s['year']) if s.get('year') else None))
def title_img(txt):  # v7.2: 첫 장면 상단 제목 — 2줄, 흰색+{금색}, 굵은 테두리+그림자 (사용자 결정 C안, 2026-09-29)
    if '\n' in txt: lines = txt.split('\n')
    elif len(txt.replace('{', '').replace('}', '')) > 12 and ' ' in txt:
        sp = [i for i, c in enumerate(txt) if c == ' ']; k = min(sp, key=lambda i: abs(i - len(txt) / 2)); lines = [txt[:k], txt[k + 1:]]
    else: lines = [txt]
    ims = [text_img(l, S.get('title_size', 92), (255, 255, 255), FT, 9, 960) for l in lines]
    lh = int(S.get('title_size', 92) * 1.12); h = lh * (len(ims) - 1) + ims[-1].height
    im = Image.new('RGBA', (max(i.width for i in ims), h))
    for n, t in enumerate(ims): im.alpha_composite(t, ((im.width - t.width) // 2, n * lh))
    sh = Image.new('RGBA', (im.width + 40, im.height + 50), (0, 0, 0, 0)); sa = Image.new('L', sh.size, 0); sa.paste(im.getchannel('A'), (20, 28))
    sh.putalpha(sa.filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * .7))); sh.alpha_composite(im, (20, 20))
    return sh
TITLE = title_img(S['title'])
TK = S.get('title_keep', .8)  # v7.5: 첫 장면 뒤에도 제목을 작게 줄여 상단에 계속 띄움(0이면 끔)
TITLE_S = TITLE.resize((max(1, int(TITLE.width * TK)), max(1, int(TITLE.height * TK))), Image.LANCZOS) if TK else None
SCRIM = Image.new('RGBA', (W, H), (0, 0, 0, 0)); SCRIM.putalpha(Image.fromarray((np.interp(np.arange(H), [0, 330, 640], [.5, .38, 0])[:, None] * np.ones((1, W)) * 255).astype(np.uint8)))
def wm_img():  # v7.2: 채널 워터마크(로고 원형 + 채널명), 전 구간 반투명
    if not S.get('watermark'): return None
    t = text_img(S['watermark'], 30, (255, 255, 255), FX, 2)
    if not S.get('watermark_logo'): return t
    lg = Image.open(S['watermark_logo']).convert('RGBA').resize((56, 56), Image.LANCZOS)
    im = Image.new('RGBA', (56 + 8 + t.width, max(56, t.height))); im.alpha_composite(lg, (0, (im.height - 56) // 2)); im.alpha_composite(t, (64, (im.height - t.height) // 2))
    return im
WM = wm_img()
SCRIM_S = SCRIM.copy(); SCRIM_S.putalpha(SCRIM.getchannel('A').point(lambda x: int(x * .72)))
PUNCH = {}  # v7.2 하이브리드 자막: 핵심 대목만 화면 중앙에 큰 단어 '펀치' — scene['punch'] = [{"text":"혹 같은 신세!","at":1.0,"dur":0.8}]
for i, s in enumerate(SC):
    for p in s.get('punch', []):
        PUNCH.setdefault(i, []).append((st[i] + p['at'], p.get('dur', .8), text_img(p['text'], p.get('size', 112), (255, 255, 255), FT, 10, 960)))
SER = text_img(S['series'], 34, (255, 255, 255), FB, 2) if S.get('series') else None
SRCT = text_img(S['source'], 28, (255, 255, 255), FB, 2, 840)
NOTES = {i: text_img(json.load(open(s['map'])).get('note', ''), 26, (240, 232, 214), FB, 2, 840) for i, s in enumerate(SC) if s.get('map') and json.load(open(s['map'])).get('note')}

try: from sprite import SPR  # v7.6: 선택 모듈 — sprite.py가 있으면 장면의 "sprite" 설정대로 도트가 지나감
except Exception: SPR = None
def hud(im, t, i):
    im = im.convert('RGBA'); im.alpha_composite(BAND)
    e0 = en[0] + td[1] / 2 if N > 1 else T
    ta = cl((t - .15) / .12) * ((1 - cl((t - e0 + .3) / .3)) if not TK else 1) if t < e0 else 0
    if ta > 0:  # v7.2: 제목 뒤 상단 어둠 그라데이션(배지·자막보다 먼저 깔아 가리지 않음)
        sc = SCRIM
        if ta < 1: sc = SCRIM.copy(); sc.putalpha(SCRIM.getchannel('A').point(lambda x: int(x * ta)))
        im.alpha_composite(sc)
    elif TK: im.alpha_composite(SCRIM_S)
    for j in (i - 1, i):
        if j < 0: continue
        a0 = .15 if j == 0 else st[j] + td[j] / 2; a1 = T if j == N - 1 else st[j + 1] + td[j + 1] / 2
        if not (a0 - .01 <= t < a1): continue
        fo = cl((a1 - t) / .12)  # 다음 자막이 뜨기 전에 사라짐(겹침 방지)
        a0 += .1 if j else 0
        c1, c2, yr = CAPS[j]
        if c1: v = t - a0; paste(im, c1, W // 2, L['cap1_y'], cl(v / .18) * fo, .9 + .1 * eoback(v / .25))
        if c2: v = t - a0 - .12; paste(im, c2, W // 2, L['cap2_y'], cl(v / .18) * fo, .88 + .12 * eoback(v / .28))
        if yr and t < a1:
            paste(im, yr, 54, L['badge_y'], 1, 1, 'l')
        if j in NOTES and t < a1: paste(im, NOTES[j], 960, L['note_y'], .9 * cl((t - a0) / .4), 1, 'r')
    if t < e0:
        v = t - .15; p = eio((t - e0 + .5) / .5) if TK else 0  # v7.5: 첫 장면 끝 0.5초 동안 작아지며 위로 올라가 고정
        paste(im, TITLE, W // 2, L['title_y'] + (L['title_s_y'] - L['title_y']) * p, ta, (1 + .25 * (1 - eoexp(v / .3))) * (1 + (TK - 1) * p if TK else 1))
    elif TK: paste(im, TITLE_S, W // 2, L['title_s_y'], .96)
    if SER: paste(im, SER, 960, L['badge_y'], .9, 1, 'r')
    if WM: paste(im, WM, 960, L['wm_y'], .7, 1, 'r') if not SER else paste(im, WM, W // 2, L['wm_y'], .7)  # v7.3: 시리즈 표시 없으면 워터마크를 오른쪽으로
    for t0, du, pim in PUNCH.get(i, []) + PUNCH.get(i - 1, []):
        v = t - t0
        if 0 <= v < du: paste(im, pim, W // 2, L['punch_y'], cl(v / .06) * (1 - cl((v - du + .15) / .15)), 1.35 - .35 * eoback(v / .22))
    if SPR: SPR(im, t)
    paste(im, SRCT, W // 2, L['src_y'], .8)
    return im.convert('RGB')

def frame(f):
    t = f / FPS; i = max(j for j in range(N) if st[j] <= t + 1e-6)
    im = scene_frame(i, t)
    if i > 0 and td[i] > 0 and t < st[i] + td[i]: im = transition(scene_frame(i - 1, t), im, (t - st[i]) / td[i], tr[i])
    im = ImageChops.add(ImageChops.multiply(im, VIGIMG), GRAIN[f // 2 % 4], 1, -16)
    k = min(cl(t / .4), cl((T - t) / S.get('fade_out', .3)))  # v7.5: 끝 여운 단축
    if k < 1: im = Image.blend(Image.new('RGB', (W, H)), im, k)
    return hud(im, t, i)

# ---------- 사운드 ----------
def bandpass(x, lo, hi):
    X = np.fft.rfft(x); fq = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (lo / np.maximum(fq, 1)) ** 4) / (1 + (fq / hi) ** 4); return np.fft.irfft(X, len(x)).astype(np.float32)
def norm(x, db): return x / (np.abs(x).max() + 1e-9) * 10 ** (db / 20)
def sfx(kind):
    g = np.random.default_rng(sum(map(ord, kind)))
    if kind in ('boom', 'hit'):
        n = int(SR * (1.1 if kind == 'boom' else .5)); t = np.arange(n) / SR
        f = (40 + 30 * np.exp(-t * 6)) if kind == 'boom' else (62 + 50 * np.exp(-t * 14))
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (4.5 if kind == 'boom' else 11))
        y += bandpass(g.normal(0, 1, n), 80, 2500) * np.exp(-t * 60) * .5
        return norm(y, -9 if kind == 'boom' else -12)
    if kind == 'whoosh':
        n = int(SR * .5); t = np.arange(n) / n; y = bandpass(g.normal(0, 1, n), 300, 4000) * np.sin(np.pi * t) ** 2.5
        return norm(y, -15)
    if kind == 'brush':
        n = int(SR * .45); t = np.arange(n) / n; y = bandpass(g.normal(0, 1, n), 1800, 9000) * (np.sin(np.pi * t ** .6) ** 2) * (1 + .6 * np.sin(t * 70))
        return norm(y, -21)
    return np.zeros(1, np.float32)
def ambience(kind, n):
    g = np.random.default_rng(4); w = g.normal(0, 1, n).astype(np.float32); tt = np.arange(n) / SR
    if kind == 'river': y = bandpass(w, 250, 1800) * (1 + .25 * np.sin(2 * np.pi * .23 * tt))
    else: y = bandpass(w, 90, 700) * (.6 + .4 * np.sin(2 * np.pi * .07 * tt + 1) ** 2)
    return norm(y, S.get('amb_db', -36))
def load_audio(src):
    p = src.replace('file://', '')
    if src.startswith('http'): p = 'dl_' + os.path.basename(src.split('?')[0]); urllib.request.urlretrieve(src, p)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()
def build_audio(path='mix.wav'):
    n = int(T * SR); mix = np.zeros(n, np.float32); voice = np.zeros(n, np.float32)
    if S.get('narration'):
        v = load_audio(S['narration']); o = int(S.get('delay', .4) * SR); v = v[:max(0, n - o)]; voice[o:o + len(v)] = v
    if S.get('amb', 'wind') != 'none': mix += ambience(S.get('amb', 'wind'), n)
    ev = [(.15, 'boom')] + [(st[i], SC[i].get('sfx', SFX_OF.get(tr[i]) if SC[i].get('move') != 'punch' else 'hit')) for i in range(1, N)]
    ev += [(st[i] + (en[i] - st[i]) / 2, 'hit') for i in range(N) if SC[i].get('move') == 'cutin']
    ev += [(st[i] + p['at'], p.get('sfx', 'hit')) for i in range(N) for p in SC[i].get('punch', [])]
    for t0, k in ev:
        if not k or k == 'none': continue
        y = sfx(k); o = int(t0 * SR); y = y[:max(0, n - o)]; mix[o:o + len(y)] += y
    if S.get('bgm'):
        b = load_audio(S['bgm']); b = np.tile(b, n // len(b) + 1)[:n]; b = norm(b, S.get('bgm_db', -17))
        env = np.convolve(np.abs(voice), np.ones(int(SR * .06)) / int(SR * .06), 'same'); env = np.clip(env / (env.max() * .25 + 1e-9), 0, 1)
        env = np.convolve(env, np.ones(int(SR * .25)) / int(SR * .25), 'same')
        mix += b * (1 - (1 - 10 ** (-S.get('duck_db', 9) / 20)) * env)
    mix += voice; fo = int(S.get('fade_out', .3) * SR); mix[-fo:] *= np.linspace(1, 0, fo)
    pcm = (np.clip(mix / max(1, np.abs(mix).max()), -1, 1) * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    return path

def lambda_f(f): return frame(f).tobytes()

if __name__ == '__main__':
    if PREVIEW:
        for x in PREVIEW.split(','): frame(int(float(x) * FPS)).save(f'prev_{float(x):05.1f}.png')
        sys.exit()
    aud = build_audio(); NF = int(T * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', aud,
                           '-filter:a', 'loudnorm=I=-15:TP=-1.5', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-maxrate', '12M', '-bufsize', '24M',
                           '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-t', str(T), '-movflags', '+faststart', S.get('out', 'final.mp4')], stdin=subprocess.PIPE)
    for i, s in enumerate(SC):  # 포크 전에 원본·지도를 미리 올려 두면 각 작업자가 공유
        if s.get('video'): load_vid(s['video']); continue
        load_src(s['image'], bool(s.get('map')))
        if s.get('map'): load_map(i)
    import multiprocessing as mp
    with mp.get_context('fork').Pool(min(8, os.cpu_count() or 1)) as pool:
        for f0 in range(0, NF, 48):  # v7.6: 48프레임 묶음으로 넘겨 주 프로세스에 프레임이 쌓이지 않게(OOM 방지)
            for b in pool.map(lambda_f, range(f0, min(NF, f0 + 48)), chunksize=6): ff.stdin.write(b)
            print(f'frame {f0}/{NF}', flush=True)
    ff.stdin.close(); ff.wait(); print('done', S.get('out', 'final.mp4'), 'starts', st)
