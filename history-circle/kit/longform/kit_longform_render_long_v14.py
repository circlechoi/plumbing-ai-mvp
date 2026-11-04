#!/usr/bin/env python3
"""역사서클 롱폼 렌더러 v1.4 (2026-10-23 복구: v1.3 영상 위 layers·sprite frames/ffps/px·sfx_cap·seal_uniform·tag bw / v1.4 music 버스+music_duck)
이전 설명: v0.4 (16:9, 1920x1080, 30fps) — 지도·제목 겹(layers, 아핀 고정), 붓 화살표, 큰 자막
사용:
  python3 render_long.py scenes.json part 0 120     # 0~120초 영상만 렌더 → parts/p_000000.mp4 (소리 없음)
  python3 render_long.py scenes.json audio          # 내레이션·BGM·효과음·앰비언스 믹스 → mix.wav
  python3 render_long.py scenes.json final          # parts/*.mp4 이어붙이고 mix.wav 입혀 out 파일 생성
  PREVIEW=3,51.5,62 python3 render_long.py scenes.json   # 해당 시각 프레임만 prev_XXXX.png
9분 영상은 2~3분 단위 part로 나눠 렌더한다(sandbox 15분 임대 안에서 끝나도록)."""
import json, math, os, subprocess, sys, urllib.request, wave, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageChops

S = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'scenes.json'))
MODE = sys.argv[2] if len(sys.argv) > 2 else ''
W, H, FPS, SR = S.get('w', 1920), S.get('h', 1080), S.get('fps', 30), 44100
SW, SH = int(W * 1.5), int(H * 1.5)          # 원본 작업 해상도(카메라 이동 여유)
T = float(S['total']); SC = S['scenes']; N = len(SC)
F_KO, F_KOB, F_EN = S.get('font', 'fonts/NR.ttf'), S.get('font_b', 'fonts/B.ttf'), S.get('font_en', 'fonts/CG.ttf')
TD = {'ink': .8, 'fade': .6, 'dip': 1.0, 'flash': .4, 'cut': 0.}
st = [float(s['start']) for s in SC]; en = st[1:] + [T]
tr = [s.get('trans', 'fade' if i else 'cut') for i, s in enumerate(SC)]
td = [TD[x] if i else 0 for i, x in enumerate(tr)]
LB = int(round(H * S.get('letterbox', 0.0)))  # 위아래 검은 띠 높이(px). 2.39:1이면 0.128
cl = lambda v, a=0., b=1.: max(a, min(b, v))
eio = lambda x: (lambda x: 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2)(cl(x))
_fc = {}
def font(p, s, var=None):
    k = (p, int(s), var)
    if k not in _fc:
        f = ImageFont.truetype(p, max(8, int(s)))
        if var:
            try: f.set_variation_by_name(var)
            except Exception: pass
        _fc[k] = f
    return _fc[k]
def lowfreq(w, h, cells, seed):
    r = np.random.default_rng(seed).random((cells[1], cells[0])).astype(np.float32)
    return np.asarray(Image.fromarray((r * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
def fetch(u, d='img'):
    if not str(u).startswith('http'): return u
    os.makedirs(d, exist_ok=True); p = os.path.join(d, os.path.basename(u.split('?')[0]))
    if not os.path.exists(p): urllib.request.urlretrieve(u, p)
    return p

# ---------- 색 보정 ----------
HANJI = None
def grade(im, kind):
    global HANJI
    if kind == 'none': return im
    if kind == 'dark':  # 지도용 어두운 톤(본편 겨울 실사 톤에 맞춤): 채도↓ 밝기↓, 차가운 그림자. 전역 "dark": [채도, 밝기]
        cs, br = S.get('dark', [.55, .5]); im = ImageEnhance.Contrast(ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(cs)).enhance(br)).enhance(1.12)
        a = np.asarray(im, np.float32) * np.array([.92, .97, 1.08], np.float32) + np.array([0, 2, 8], np.float32)
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if kind == 'paint':  # 청록산수 채색: 채도↑, 따뜻한 하이라이트, 한지 결
        im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.15)).enhance(1.05)
        a = np.asarray(im, np.float32); lum = a.mean(-1, keepdims=True) / 255
        a = a + np.array([12, 5, -6], np.float32) * lum + np.array([-5, 2, 8], np.float32) * (1 - lum)
        if HANJI is None: HANJI = (lowfreq(im.width // 2, im.height // 2, (160, 90), 1) - .5)
        hj = np.asarray(Image.fromarray(((HANJI + .5) * 255).astype(np.uint8)).resize(im.size), np.float32) - 128
        a = a + hj[..., None] * .06
    else:  # film: 실사 — 채도↓, 차가운 그림자, 대비 약간↑ (Fallen Leaves풍 무채색 겨울)
        im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(S.get('film_sat', .82))).enhance(1.06)
        a = np.asarray(im, np.float32); lum = a.mean(-1, keepdims=True) / 255
        a = a + np.array([6, 3, -4], np.float32) * lum + np.array([-6, 0, 9], np.float32) * (1 - lum)
        a = a * .97 + 5
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

SRC = {}
def load_src(i):
    s = SC[i]; k = (s.get('image'), s.get('grade', 'film'))
    if k in SRC: return SRC[k]
    if not s.get('image'): SRC[k] = Image.new('RGB', (SW, SH), tuple(s.get('bg', [8, 8, 10]))); return SRC[k]
    im = Image.open(fetch(s['image'])).convert('RGB')
    sc = max(SW / im.width, SH / im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    l, t = (im.width - SW) // 2, (im.height - SH) // 2; im = im.crop((l, t, l + SW, t + SH))
    SRC[k] = grade(im, k[1]); return SRC[k]

VID = {}
def load_vid(i):  # 영상 컷: 원본 해상도(최대 1920폭) rgb24 raw로 풀어 memmap — 메모리 대신 디스크 사용
    u = SC[i]['video']
    if u in VID: return VID[u]
    p = fetch(u, 'vid'); os.makedirs('raw', exist_ok=True)
    pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip().split(',')
    vw, vh = int(pr[0]), int(pr[1])
    if vw > W: vh = int(vh * W / vw) // 2 * 2; vw = W
    rp = os.path.join('raw', os.path.basename(p) + f'.{vw}x{vh}.rgb')
    if not os.path.exists(rp):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', p, '-an', '-vf', f'fps={FPS},scale={vw}:{vh}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', rp], check=True)
    a = np.memmap(rp, np.uint8, 'r'); a = a.reshape(-1, vh, vw, 3)
    VID[u] = a; return a

# ---------- 카메라 ----------
def camera(i, u):
    s = SC[i]; D = en[i] - st[i] + (td[i + 1] if i + 1 < N else 0); x = u / max(D, .01)
    mv = s.get('move', 'still'); fx, fy = s.get('focus', [.5, .5]); amt = s.get('amt', 1.0)
    z, cx, cy = 1.0, .5, .5
    if mv == 'in': e = eio(x); z = 1 + .12 * amt * e; cx, cy = .5 + (fx - .5) * e, .5 + (fy - .5) * e
    elif mv == 'out': z = 1 + .12 * amt * (1 - eio(x)); cx, cy = fx, fy
    elif mv == 'push': z = 1 + .06 * amt * x; cx, cy = fx, fy      # 아주 느린 직선 푸시인(시네마틱 기본)
    elif mv in ('pan_l', 'pan_r'): z = 1 + .14 * amt; o = .38 + .24 * eio(x); cx = o if mv == 'pan_r' else 1 - o; cy = fy
    elif mv == 'tilt_up': z = 1 + .14 * amt; cy = .62 - .24 * eio(x); cx = fx
    elif mv == 'tilt_down': z = 1 + .14 * amt; cy = .38 + .24 * eio(x); cx = fx
    elif mv == 'punch': e = 1 - (1 - cl(u / .28)) ** 3; z = 1 + .16 * amt * e + .05 * x; cx, cy = fx, fy  # v0.6: 급한 확대
    else: z = 1.0
    k = .007 if 'quake' in s.get('fx', []) else .0025 if 'shake' in s.get('fx', []) else (.0007 if 'handheld' in s.get('fx', []) else 0)
    if k:
        cx += k * (math.sin(u * 7.1) + .6 * math.sin(u * 13.7) + .3 * math.sin(u * 29.3))
        cy += k * (math.cos(u * 6.3) + .6 * math.sin(u * 11.9) + .3 * math.cos(u * 23.1)); z += k * 2
    z *= s.get('zoom', 1.0); w, h = SW / z, SH / z
    return cl(cx * SW - w / 2, 0, SW - w), cl(cy * SH - h / 2, 0, SH - h), w, h

# ---------- 지도·제목 겹(layers, v0.3) ----------
# 장면 "layers": [{"t":"tint|arrow|sprite|tag|dot|disc|vtext", ...}] — 좌표는 원본 이미지 기준 0~1
# 모든 겹은 원본 좌표(SW x SH)의 RGBA 조각으로 만들어 두고 프레임마다 카메라와 같은 아핀 변환으로 붙인다 → 글자·말이 지도에 고정되어 떨리지 않는다
F_TAG = S.get('font_tag', 'fonts/SM.ttf'); KS = SW / W  # 화면 px → 원본 px 배율
def _alpha(img, a):
    if a >= 1: return img
    img = img.copy(); img.putalpha(img.getchannel('A').point(lambda v: int(v * a))); return img
def put(im, patch, px, py, box, a=1., scale=1., rs=Image.BICUBIC):  # patch 왼쪽 위를 원본 좌표 (px, py)에 — 부동소수 위치로 붙임
    if a <= 0: return
    l, tp, w, h = box; sc = W / w; z = sc * scale
    x0, y0 = (px - l) * sc, (py - tp) * sc; x1, y1 = x0 + patch.width * z, y0 + patch.height * z
    bx0, by0, bx1, by1 = max(0, math.floor(x0)), max(0, math.floor(y0)), min(W, math.ceil(x1)), min(H, math.ceil(y1))
    if bx1 <= bx0 or by1 <= by0: return
    out = patch.transform((bx1 - bx0, by1 - by0), Image.AFFINE, (1 / z, 0, (bx0 - x0) / z, 0, 1 / z, (by0 - y0) / z), rs)
    im.alpha_composite(_alpha(out, a), (bx0, by0))
def smooth(pts, n=40, closed=False):  # Catmull-Rom 곡선
    P = ([pts[-1]] + list(pts) + [pts[0], pts[1]]) if closed else ([pts[0]] + list(pts) + [pts[-1]]); out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = (np.array(P[i + k], np.float32) for k in (-1, 0, 1, 2))
        for j in range(n):
            t = j / n; out.append(tuple(.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)))
    return out if closed else out + [tuple(pts[-1])]
SEALU = None
def seal_metrics():  # v1.3: seal_uniform — 모든 '§' 인장을 같은 글자 크기·폭(가장 긴 문구)·높이로
    global SEALU
    if SEALU is None:
        sz = int(S['seal_uniform'] * KS); f = font(F_KOB, int(sz * 1.5)); f2 = font(F_KOB, int(sz * .74)); tw = th = sw_ = s2h = 0; anysub = False
        for sc_ in SC:
            for L in sc_.get('layers', []):
                if L.get('t') == 'tag' and str(L.get('text', '')).startswith('§'):
                    b = f.getbbox(L['text'][1:]); tw = max(tw, b[2] - b[0]); th = max(th, b[3] - b[1])
                    if L.get('sub'): anysub = True; b2 = f2.getbbox(L['sub']); sw_ = max(sw_, b2[2] - b2[0]); s2h = max(s2h, b2[3] - b2[1])
        hb = f.getbbox('가1'); th = max(th, hb[3] - hb[1]); SEALU = dict(size=S['seal_uniform'], tw=tw, th=th, sw=sw_, s2h=s2h, sub=anysub)
    return SEALU
def seal_img(text, sub, size, bw=None):  # v1.0: 붉은 인장 이름표. 글자를 틀의 정중앙에 놓는다
    U = seal_metrics() if S.get('seal_uniform') else None
    if U: size = U['size']
    size = int(size * KS); f = font(F_KOB, int(size * 1.5)); f2 = font(F_KOB, int(size * .74))
    b = f.getbbox(text); tw, th = b[2] - b[0], b[3] - b[1]; b2 = f2.getbbox(sub) if sub else (0, 0, 0, 0); sw_, s2h = b2[2] - b2[0], b2[3] - b2[1]
    pad = int(size * .62); w_ = int(max(tw + pad * 2, sw_ + pad * 1.2)); bh = th + pad * 2; sh_ = int(s2h + size * .62) if sub else 0; m = 8
    if U:
        w_ = int(max(U['tw'] + pad * 2, U['sw'] + pad * 1.2)); bh = U['th'] + pad * 2; sh_ = int(U['s2h'] + size * .62) if (sub and U['sub']) else 0
    if bw: w_ = int(bw * SW) - 2 * m  # E-3: 고정 폭
    im = Image.new('RGBA', (w_ + 2 * m + 16, bh + sh_ + 2 * m + 16)); ImageDraw.Draw(im).rounded_rectangle([m + 8, m + 10, w_ + m + 8, bh + sh_ + m + 10], 6, fill=(0, 0, 0, 150)); im = im.filter(ImageFilter.GaussianBlur(7))
    d = ImageDraw.Draw(im); d.rectangle([m, m, w_ + m, bh + sh_ + m], fill=(18, 16, 16, 245)); d.rectangle([m, m, w_ + m, bh + m], fill=(158, 26, 24, 252))
    g = int(size * .16); d.rectangle([m + g, m + g, w_ + m - g, bh + m - g], outline=(244, 232, 210, 235), width=2)
    d.rectangle([m, m, w_ + m, bh + sh_ + m], outline=(244, 232, 210, 120), width=1)
    d.text((m + (w_ - tw) / 2 - b[0], m + (bh - th) / 2 - b[1]), text, font=f, fill=(250, 244, 232, 255))
    if sub: d.text((m + (w_ - sw_) / 2 - b2[0], m + bh + (sh_ - s2h) / 2 - b2[1]), sub, font=f2, fill=(236, 226, 206, 255))
    return im
def tag_img(text, sub, size, bw=None):
    if text.startswith('§'): return seal_img(text[1:], sub, size, bw)  # 한지 띠 위 먹 글씨 이름표(원본 배율로 그림)
    size = int(size * KS); f = font(F_TAG, size); f2 = font(F_KOB, int(size * .5)); tw = f.getlength(text); sw_ = f2.getlength(sub) if sub else 0
    px, py = int(size * .5), int(size * .26); w_ = int(max(tw, sw_) + px * 2); h_ = int(size * 1.22 + (size * .68 if sub else 0) + py * 2)
    if bw: w_ = int(bw * SW) - 6  # E-3: 연도 상자 고정 폭(bw × SW, 원본 px)
    sh = Image.new('RGBA', (w_ + 24, h_ + 24)); ImageDraw.Draw(sh).rounded_rectangle([13, 15, w_ + 13, h_ + 15], 8, fill=(0, 0, 0, 120)); sh = sh.filter(ImageFilter.GaussianBlur(6))
    d = ImageDraw.Draw(sh); d.rounded_rectangle([6, 6, w_ + 6, h_ + 6], 7, fill=(240, 230, 205, 248), outline=(96, 78, 52, 255), width=3)
    d.text(((w_ - tw) / 2 + 6, py + 5), text, font=f, fill=(28, 24, 20, 255))
    if sub: d.text(((w_ - sw_) / 2 + 6, py + size * 1.22 + 5), sub, font=f2, fill=(92, 74, 52, 255))
    return sh
def vtext_img(text, size, color):  # 세로쓰기 한 줄
    size = int(size * KS); f = font(S.get('font_v', F_KOB), size); cell = size * 1.16; n = sum(.45 if c in ', ' else 1 for c in text)
    im = Image.new('RGBA', (int(size * 1.8), int(cell * n + size)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); y = size * .2
    for c in text:
        if c == ' ': y += cell * .45; continue
        if c == ',': d.text((size * 1.02, y - cell * .62), ',', font=f, fill=color); y += cell * .45; continue
        d.text((size * .4 + (size - f.getlength(c)) / 2, y), c, font=f, fill=color); y += cell
    return im
def mark_img(kind, r, color):  # 도읍 표지(dot) / 세력 원(disc)
    r = int(r * KS); n = r * 2 + 28; c = n // 2; sh = Image.new('RGBA', (n, n)); ImageDraw.Draw(sh).ellipse([c - r + 3, c - r + 6, c + r + 3, c + r + 6], fill=(0, 0, 0, 130)); sh = sh.filter(ImageFilter.GaussianBlur(5)); d = ImageDraw.Draw(sh)
    if kind == 'dot':
        d.ellipse([c - r, c - r, c + r, c + r], fill=(26, 22, 20, 255)); d.ellipse([c - r * .8, c - r * .8, c + r * .8, c + r * .8], fill=(244, 236, 214, 255))
        d.ellipse([c - r * .5, c - r * .5, c + r * .5, c + r * .5], fill=tuple(color) + (255,))
    else:
        d.ellipse([c - r, c - r, c + r, c + r], fill=(238, 230, 210, 255)); d.ellipse([c - r * .86, c - r * .86, c + r * .86, c + r * .86], fill=tuple(color) + (255,))
    return sh
def tint_img(poly, color, alpha, blur, edge):  # 세력 색 번짐 + 먹 테두리(1440x810로 그려 2배로 붙임)
    tw, th = 1440, 810; m = Image.new('L', (tw, th), 0); c = smooth(poly, 24, True); pp = [(x * tw, y * th) for x, y in c]
    ImageDraw.Draw(m).polygon(pp, fill=255); m = m.filter(ImageFilter.GaussianBlur(blur))
    out = Image.new('RGBA', (tw, th), tuple(color) + (0,)); out.putalpha(m.point(lambda v: int(v * alpha)))
    if edge:
        e = Image.new('RGBA', (tw, th), (0, 0, 0, 0)); ImageDraw.Draw(e).line(pp + [pp[0]], fill=tuple(edge) + (215,), width=5, joint='curve'); out.alpha_composite(e.filter(ImageFilter.GaussianBlur(1.1)))
    return out
def brush_arrow(pts, w0, color, seed=3):  # 붓으로 그은 화살표: 여러 가닥(붓털) + 끝이 갈라지는 마른 붓 + 두 획 화살촉. 진행도 지도(PM)로 그려지는 순서를 기억
    P = np.array(smooth(pts, 60), np.float32) * np.array([SW, SH], np.float32); n = len(P); ss = 2; mg = w0 * 5
    x0, y0 = P[:, 0].min() - mg, P[:, 1].min() - mg; bw, bh = int(P[:, 0].max() + mg - x0), int(P[:, 1].max() + mg - y0)
    A = Image.new('L', (bw * ss, bh * ss), 0); PM = Image.new('L', (bw * ss, bh * ss), 0); da, dp = ImageDraw.Draw(A), ImageDraw.Draw(PM)
    T_ = np.gradient(P, axis=0); T_ /= np.maximum(np.linalg.norm(T_, axis=1, keepdims=True), 1e-6); Nn = np.stack([-T_[:, 1], T_[:, 0]], 1)
    sv = np.linspace(0, 1, n); wp = w0 * (.42 + .58 * np.sin(np.pi * np.clip(sv * .82 + .1, 0, 1))); g = np.random.default_rng(seed); NB = 18
    for b in range(NB):
        v = -1 + 2 * (b + .5) / NB + g.uniform(-.03, .03); s1 = 1 - g.uniform(0, .16) * (.3 + abs(v)); s0 = g.uniform(0, .03); op = int(g.uniform(205, 255)); lw = max(2, int(w0 / NB * 2.3 * ss))
        gap = g.uniform(.5, .92) if g.random() < .4 else 9; gl = g.uniform(.02, .06); Q = (P + Nn * (v * wp / 2)[:, None] - np.array([x0, y0], np.float32)) * ss
        for j in range(n - 1):
            s_ = sv[j]
            if s_ < s0 or s_ > s1 or gap < s_ < gap + gl: continue
            seg = [tuple(Q[j]), tuple(Q[j + 1])]; da.line(seg, fill=op, width=lw); dp.line(seg, fill=int(2 + 236 * s_), width=lw)
    tip = P[-1] + T_[-1] * w0 * 1.5
    for sgn in (1, -1):  # 화살촉 두 획
        ang = math.radians(150) * sgn; dv = np.array([T_[-1][0] * math.cos(ang) - T_[-1][1] * math.sin(ang), T_[-1][0] * math.sin(ang) + T_[-1][1] * math.cos(ang)], np.float32)
        e = tip + dv * w0 * 3.6; nv = np.array([-dv[1], dv[0]], np.float32); hw = w0 * .62
        pg = [tuple((q - np.array([x0, y0], np.float32)) * ss) for q in (tip + nv * hw - dv * hw * .6, tip - nv * hw - dv * hw * .6, e)]; da.polygon(pg, fill=245); dp.polygon(pg, fill=250)
    A = A.filter(ImageFilter.GaussianBlur(.8 * ss)).resize((bw, bh), Image.LANCZOS); PM = PM.resize((bw, bh), Image.BILINEAR)
    col = Image.new('RGBA', (bw, bh), tuple(color) + (0,)); col.putalpha(A.point(lambda v: int(v * .94)))
    return col, np.asarray(PM, np.float32), x0, y0
def band_img(pts, w, color, edge):  # v1.1 방어선·전선 캡슐 띠
    ss = 2; P = np.array(smooth(pts, 40), np.float32) * np.array([SW, SH], np.float32); mg = w * 1.5
    x0, y0 = P.min(0) - mg; x1, y1 = P.max(0) + mg; bw, bh = int(x1 - x0) + 1, int(y1 - y0) + 1
    im = Image.new('RGBA', (bw * ss, bh * ss)); d = ImageDraw.Draw(im); Q = [tuple((p - np.array([x0, y0])) * ss) for p in P]
    e = max(3, int(w * .1)); 
    for col, ww in ((tuple(edge) + (245,), int((w + 2 * e) * ss)), (tuple(color) + (215,), int(w * ss))):
        d.line(Q, fill=col, width=ww, joint='curve'); r = ww / 2
        for q in (Q[0], Q[-1]): d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=col)
    im = im.resize((bw, bh), Image.LANCZOS); sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel('A').filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * .5)))
    out = Image.new('RGBA', im.size); out.alpha_composite(sh, (3, 5)); out.alpha_composite(im); return out, x0, y0
def dash_img(pts, w, color, dl):  # v1.1 교역·보급·이동 경로 점선(그려지는 순서 PM 포함)
    ss = 2; P = np.array(smooth(pts, 80), np.float32) * np.array([SW, SH], np.float32); mg = w * 3
    x0, y0 = P.min(0) - mg; x1, y1 = P.max(0) + mg; bw, bh = int(x1 - x0) + 1, int(y1 - y0) + 1
    A = Image.new('L', (bw * ss, bh * ss), 0); PM = Image.new('L', (bw * ss, bh * ss), 0); da, dp = ImageDraw.Draw(A), ImageDraw.Draw(PM)
    seg = np.linalg.norm(np.diff(P, axis=0), axis=1); cum = np.concatenate([[0], np.cumsum(seg)]); tot = max(cum[-1], 1); Q = (P - np.array([x0, y0])) * ss
    for j in range(len(P) - 1):
        if int(cum[j] / dl) % 2: continue
        sg = [tuple(Q[j]), tuple(Q[j + 1])]; da.line(sg, fill=255, width=int(w * ss)); dp.line(sg, fill=int(2 + 236 * cum[j] / tot), width=int(w * ss))
    A = A.resize((bw, bh), Image.LANCZOS); PM = PM.resize((bw, bh), Image.BILINEAR)
    col = Image.new('RGBA', (bw, bh), tuple(color) + (0,)); col.putalpha(A.point(lambda v: int(v * .92)))
    return col, np.asarray(PM, np.float32), x0, y0
def token_img(size, color, icon, text):  # v1.1 군대·수군 사각 토큰
    s = int(size * KS); m = 16; im = Image.new('RGBA', (s + 2 * m, s + 2 * m)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([m + 4, m + 6, m + s + 4, m + s + 6], int(s * .08), fill=(0, 0, 0, 140)); im = im.filter(ImageFilter.GaussianBlur(5)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([m, m, m + s, m + s], int(s * .08), fill=tuple(color) + (250,), outline=(20, 18, 18, 255), width=max(3, s // 22))
    d.rounded_rectangle([m + s * .1, m + s * .1, m + s * .9, m + s * .9], int(s * .05), outline=(240, 230, 210, 200), width=max(2, s // 40))
    if icon:
        ic = Image.open(fetch(icon, 'spr')).convert('RGBA'); k = s * .72 / max(ic.size); ic = ic.resize((max(1, int(ic.width * k)), max(1, int(ic.height * k))), Image.LANCZOS)
        im.alpha_composite(ic, (int(m + (s - ic.width) / 2), int(m + (s - ic.height) / 2)))
    elif text:
        f = font(F_KOB, int(s * .5)); b = f.getbbox(text); d.text((m + (s - (b[2] - b[0])) / 2 - b[0], m + (s - (b[3] - b[1])) / 2 - b[1]), text, font=f, fill=(250, 244, 232, 255))
    return im
def label_img(text, sub, size, color, alpha):  # v1.1 나라 이름(지도 위 큰 반투명 글자)
    size = int(size * KS); f = font(F_KOB, size); tr = int(size * .18); w_ = sum(f.getlength(c) for c in text) + tr * (len(text) - 1)
    f2 = font(F_KO, int(size * .42)); w2 = f2.getlength(sub) if sub else 0; W_ = int(max(w_, w2)) + 40; H_ = int(size * 1.35 + (size * .6 if sub else 0)) + 30
    im = Image.new('RGBA', (W_, H_)); d = ImageDraw.Draw(im); x = (W_ - w_) / 2
    for c in text: d.text((x, 12), c, font=f, fill=tuple(color) + (int(255 * alpha),), stroke_width=max(1, size // 40), stroke_fill=(30, 26, 24, int(160 * alpha))); x += f.getlength(c) + tr
    if sub: d.text(((W_ - w2) / 2, 12 + size * 1.2), sub, font=f2, fill=tuple(color) + (int(255 * alpha),), stroke_width=1, stroke_fill=(30, 26, 24, int(140 * alpha)))
    return im
def prep_layers(i):
    out = []
    for L in SC[i].get('layers', []):
        d = dict(L); k = L['t']
        if k == 'sprite':  # v1.3: frames[여러 PNG] + ffps, px(픽셀 아트 NEAREST·흔들림 없음), 위치 없으면 우측 하단 구석(x .84→.95, 발 y .866)
            rs = Image.NEAREST if L.get('px') else Image.LANCZOS; fr = L.get('frames') or [L['img']]; w_ = max(2, int(L.get('w', .08) * SW)); ims = []
            for fp in fr:
                im = Image.open(fetch(fp, 'spr')).convert('RGBA'); ims.append(im.resize((w_, max(2, int(w_ * im.height / im.width))), rs))
            d['ims'] = ims; d['im'] = ims[0]
            if 'x' not in L and not L.get('path'):
                D_ = max(.5, en[i] - st[i]); d['path'] = [[0, .84, .866], [D_, .95, .866]]; d['lin'] = True; d.setdefault('anchor', 'bc')
            if L.get('shadow', L.get('anchor', 'bc') == 'bc'):
                s_ = Image.new('RGBA', (w_, max(6, w_ // 4)), (0, 0, 0, 0)); ImageDraw.Draw(s_).ellipse([w_ * .12, 1, w_ * .88, s_.height - 2], fill=(20, 16, 12, 100)); d['sh'] = s_.filter(ImageFilter.GaussianBlur(max(1, w_ // 26)))
        elif k == 'tint': d['im'] = tint_img(L['poly'], L['color'], L.get('alpha', .55), L.get('blur', 10), L.get('edge'))
        elif k == 'arrow': d['im'], d['pm'], d['x0'], d['y0'] = brush_arrow(L['pts'], L.get('w', .011) * SW, L.get('color', [150, 30, 25]), L.get('seed', 3))
        elif k in ('dot', 'disc'):
            d['im'] = mark_img(k, L.get('r', 16 if k == 'dot' else 24), L.get('color', [170, 30, 28] if k == 'dot' else [24, 22, 22]))
            if L.get('name'): d['tg'] = tag_img(L['name'], L.get('sub'), L.get('size', 36))
        elif k == 'tag': d['im'] = tag_img(L['text'], L.get('sub'), L.get('size', 36), L.get('bw'))
        elif k == 'band': d['im'], d['x0'], d['y0'] = band_img(L['pts'], L.get('w', .012) * SW, L.get('color', [150, 30, 25]), L.get('edge', [20, 18, 18]))
        elif k == 'dash': d['im'], d['pm'], d['x0'], d['y0'] = dash_img(L['pts'], L.get('w', .0035) * SW, L.get('color', [30, 40, 90]), L.get('dl', .008) * SW)
        elif k == 'token': d['im'] = token_img(L.get('size', 60), L.get('color', [150, 30, 25]), L.get('icon'), L.get('text'))
        elif k == 'label': d['im'] = label_img(L['text'], L.get('sub'), L.get('size', 60), L.get('color', [245, 238, 225]), L.get('alpha', .62))
        elif k == 'vtext': d['im'] = vtext_img(L['text'], L.get('size', 40), tuple(L.get('color', [30, 28, 26])) + (255,))
        out.append(d)
    return out
LAY = {}
def lpos(d, u):  # path: [[t, x, y], ...] 장면 시작 기준 초
    p = d.get('path')
    if not p: return d['x'], d['y'], False
    if u <= p[0][0]: return p[0][1], p[0][2], False
    for a, b in zip(p, p[1:]):
        if u < b[0]:
            e = (u - a[0]) / max(b[0] - a[0], .01); e = e if d.get('lin') else eio(e); return a[1] + (b[1] - a[1]) * e, a[2] + (b[2] - a[2]) * e, True
    return p[-1][1], p[-1][2], False
ANC = {'bc': (.5, 1.), 'c': (.5, .5), 'tl': (0., 0.), 'tc': (.5, 0.)}
def draw_layers(im, i, u, box):
    if i not in LAY: LAY[i] = prep_layers(i)
    im = im.convert('RGBA')
    for d in LAY[i]:
        at = d.get('at', 0)
        if u < at: continue
        a = cl((u - at) / d.get('fade', .5))
        if d.get('out') is not None: a *= cl((d['out'] - u) / d.get('fade', .5))
        if a <= 0: continue
        k = d['t']; p = cl((u - at) / d.get('dur', 1.2)); t_ = d['im']
        if k == 'tint': put(im, t_, 0, 0, box, eio(p) * (a if d.get('out') is not None else 1), SW / t_.width)
        elif k == 'band': put(im, t_, d['x0'], d['y0'], box, a)
        elif k in ('arrow', 'dash'):
            al = np.asarray(t_.getchannel('A'), np.float32) * np.clip((eio(p) * 262 - d['pm']) / 9, 0, 1) * (d['pm'] > 0); sp = t_.copy(); sp.putalpha(Image.fromarray(al.astype(np.uint8)))
            put(im, sp, d['x0'], d['y0'], box, a if d.get('out') is not None else 1)
        elif k == 'sprite':
            if len(d.get('ims', [])) > 1: t_ = d['ims'][int(u * d.get('ffps', 6)) % len(d['ims'])]
            x, y, mv = lpos(d, u); ax, ay = ANC[d.get('anchor', 'bc')]; sp = t_
            if d.get('reveal'):  # 위에서 아래로 써 내려가듯 드러남
                hh = t_.height; soft = hh * .16; thr = eio(cl((u - at) / d.get('dur', 1.6))) * (hh + soft)
                al = np.asarray(t_.getchannel('A'), np.float32) * np.clip((thr - np.arange(hh, dtype=np.float32)) / soft, 0, 1)[:, None]
                sp = t_.copy(); sp.putalpha(Image.fromarray(al.astype(np.uint8))); a = 1 if d.get('out') is None else a
            bob = math.sin(u * 9 + x * 40) * 3.2 if (mv and not d.get('px') and not d.get('frames')) else 0
            if d.get('sh') is not None: put(im, d['sh'], x * SW - t_.width / 2, y * SH - d['sh'].height * .62, box, a)
            put(im, sp, x * SW - t_.width * ax, y * SH - t_.height * ay + bob, box, a, 1., Image.NEAREST if d.get('px') else Image.BICUBIC)
        elif k in ('dot', 'disc'):
            x, y = d['x'] * SW, d['y'] * SH; put(im, t_, x - t_.width / 2, y - t_.height / 2, box, a)
            if d.get('tg') is not None:
                g = d['tg']; gx = t_.width / 2 - 4; sd = d.get('side', 'r')
                tx, ty = {'r': (x + gx, y - g.height / 2), 'l': (x - gx - g.width, y - g.height / 2), 'u': (x - g.width / 2, y - gx - g.height), 'd': (x - g.width / 2, y + gx)}[sd]
                put(im, g, tx, ty, box, a)
        elif k in ('tag', 'vtext', 'token', 'label'):
            ax, ay = (0., 0.) if k == 'vtext' else (.5, .5); put(im, t_, d['x'] * SW - t_.width * ax, d['y'] * SH - t_.height * ay, box, a)
    return im.convert('RGB')

# ---------- 효과(눈·안개) ----------
SNOW = np.random.default_rng(7).random((420, 4)).astype(np.float32)  # x, y, 크기, 속도
MIST = lowfreq(W * 2, H, (16, 6), 9)
VEIL = lowfreq(W * 2, H, (10, 120), 21)
def fx_layer(im, s, u):
    f = s.get('fx', [])
    if 'mist' in f:
        o = int((u * 22) % W); m = (MIST[:, o:o + W] ** 2 * .35)[..., None]
        a = np.asarray(im, np.float32); im = Image.fromarray((a * (1 - m) + 225 * m).astype(np.uint8))
    if 'snow' in f or 'snow_heavy' in f:
        n = 420 if 'snow_heavy' in f else 160; d = ImageDraw.Draw(im, 'RGBA')
        for x0, y0, sz, sp in SNOW[:n]:
            r = .8 + sz * 2.6; v = 40 + sp * 90
            x = (x0 * W + math.sin(u * (.6 + sp) + x0 * 20) * 18 + u * 14) % W; y = (y0 * H + u * v) % H
            d.ellipse([x - r, y - r, x + r, y + r], fill=(245, 245, 250, int(110 + 120 * sz)))
    if 'blizzard' in f:  # v0.6: 옆으로 몰아치는 눈(빠른 줄무늬)
        d = ImageDraw.Draw(im, 'RGBA')
        for x0, y0, sz, sp in SNOW[:300]:
            vx = 900 + sp * 900; vy = 180 + sz * 260; L = 26 + sz * 60
            x = (x0 * W * 1.3 - u * vx) % (W * 1.3) - W * .15; y = (y0 * H + u * vy) % H
            d.line([x, y, x + L, y - L * vy / vx], fill=(245, 246, 250, int(70 + 110 * sz)), width=int(1 + sz * 3))
    for a, b, c, k in s.get('veil', []):  # v0.6: 눈보라 가림 [시작, 정점, 끝, 세기] (장면 기준 초)
        al = k * (cl((u - a) / max(b - a, .01)) if u < b else cl((c - u) / max(c - b, .01)))
        if al > 0:
            o = int((u * 2400) % W); m = np.clip(.55 + VEIL[:, o:o + W] * .9, 0, 1)[..., None] * al
            arr = np.asarray(im, np.float32); im = Image.fromarray((arr * (1 - m) + 232 * m).astype(np.uint8))
    return im

PIM = {}
def pimg(p):
    k = (p['image'], p.get('grade', 'film'))
    if k not in PIM:
        im = Image.open(fetch(p['image'])).convert('RGB'); im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS); PIM[k] = grade(im, k[1])
    return PIM[k]
def panel_frame(s, u):  # v0.5: 분할 화면(만화 칸). panels: [{image, box[x0,y0,x1,y1](띠 안쪽 기준 0~1), at, out, focus, zoom, from l|r|u|d}]
    im = Image.new('RGB', (W, H), (5, 5, 7)); vh = H - 2 * LB; g = 6
    for p in s['panels']:
        a = eio((u - p.get('at', 0)) / .5)
        if a <= 0: continue
        if p.get('out') is not None: a *= cl((p['out'] - u) / .3)
        x0, y0, x1, y1 = p['box']; bx0, by0, bx1, by1 = int(x0 * W) + g, LB + int(y0 * vh) + g, int(x1 * W) - g, LB + int(y1 * vh) - g
        bw, bh = bx1 - bx0, by1 - by0; src = pimg(p); fx, fy = p.get('focus', [.5, .5])
        z = p.get('zoom', 1.0) * (1 + .012 * max(0, u - p.get('at', 0)))
        cw = min(src.width, src.height * bw / bh) / z; ch = cw * bh / bw
        l = cl(fx * src.width - cw / 2, 0, src.width - cw); tp = cl(fy * src.height - ch / 2, 0, src.height - ch)
        pt = src.resize((bw, bh), Image.BICUBIC, box=(l, tp, l + cw, tp + ch))
        if a < 1: pt = Image.blend(Image.new('RGB', pt.size, (5, 5, 7)), pt, a)
        f = p.get('from', ''); dx = {'l': -1, 'r': 1}.get(f, 0) * int((1 - a) * 70); dy = {'u': -1, 'd': 1}.get(f, 0) * int((1 - a) * 50)
        im.paste(pt, (bx0 + dx, by0 + dy))
    return im

def scene_frame(i, t):
    s = SC[i]; u = t - st[i]
    if s.get('panels'): return fx_layer(panel_frame(s, u), s, u)
    if s.get('video'):
        a = load_vid(i); vt = (float(np.interp(cl(u, 0, 999), [p[0] for p in s['vmap']], [p[1] for p in s['vmap']])) if s.get('vmap') else cl(u, 0, 999) + s.get('vstart', 0)); k = min(len(a) - 1, int(vt * FPS))  # v0.8: vmap = 속도 변주 [[장면 초, 원본 초], ...]
        im = Image.fromarray(np.asarray(a[k])).resize((W, H), Image.BICUBIC)
        if s.get('grade', 'none') != 'none': im = grade(im, s['grade'])
        if s.get('layers'): im = draw_layers(im, i, u, (0, 0, SW, SH))  # v1.3: 영상 컷 위에도 겹(도트·글자) — 화면 고정
    else:
        l, tp, w, h = camera(i, u); im = load_src(i).resize((W, H), Image.BICUBIC, box=(l, tp, l + w, tp + h))
        if s.get('dim'): im = ImageEnhance.Brightness(im).enhance(s['dim'])
        if s.get('layers'): im = draw_layers(im, i, u, (l, tp, w, h))
    if s.get('hblur') and u < .4:  # v0.6: 컷 머리의 가로 번짐(휙 지나감)
        kk = 1 + s['hblur'] * (1 - u / .4); im = im.resize((max(8, int(W / kk)), H), Image.BILINEAR).resize((W, H), Image.BILINEAR)
    return fx_layer(im, s, u)

INKN = lowfreq(W, H, (16, 9), 11) * .75 + lowfreq(W, H, (64, 36), 12) * .25
def transition(A, B, p, kind):
    if kind in ('fade', 'cut'): return Image.blend(A, B, eio(p))
    a, b = np.asarray(A, np.float32), np.asarray(B, np.float32)
    if kind == 'ink':
        q = eio(p) * 1.35 - .15; v = (q - INKN) / .07; m = np.clip(v, 0, 1)[..., None]
        e = np.exp(-(v - .5) ** 2 * 1.5)[..., None] * .4 * (1 - p); o = a * (1 - m) + b * m; o = o * (1 - e) + 30 * e
    elif kind == 'dip': o = a * cl(1 - p * 2) if p < .5 else b * cl(p * 2 - 1)
    else:  # flash
        o = a + (240 - a) * cl(p * 2.2) if p < .5 else b + (240 - b) * cl((1 - p) * 2.2)
    return Image.fromarray(np.clip(o, 0, 255).astype(np.uint8))

# ---------- 글자 ----------
def spaced_img(txt, f, track, color, shadow=True):
    wid = sum(f.getlength(c) for c in txt) + track * max(0, len(txt) - 1); asc, desc = f.getmetrics()
    pad = 8; im = Image.new('RGBA', (int(wid) + pad * 2, asc + desc + pad * 2)); d = ImageDraw.Draw(im); x = pad
    for c in txt: d.text((x, pad), c, font=f, fill=color); x += f.getlength(c) + track
    if not shadow: return im
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel('A').filter(ImageFilter.GaussianBlur(3)).point(lambda v: int(v * .55)))
    out = Image.new('RGBA', im.size); out.alpha_composite(sh, (1, 2)); out.alpha_composite(im); return out
def paste(im, t, x, y, alpha=1., anchor='c'):
    if alpha <= 0: return
    if alpha < 1: t = t.copy(); t.putalpha(t.getchannel('A').point(lambda v: int(v * alpha)))
    xx = x - t.width // 2 if anchor == 'c' else x
    im.alpha_composite(t, (int(xx), int(y - t.height // 2)))
F_CAP = S.get('font_cap', 'fonts/X.ttf' if os.path.exists('fonts/X.ttf') else F_KOB); CAPSZ = S.get('cap_size', 56)  # v0.3: 자막·장소 글자를 굵고 크게
CAP = {i: spaced_img(s['cap'], font(F_CAP, CAPSZ), 1, (248, 244, 236, 255)) for i, s in enumerate(SC) if s.get('cap')}
CAPS = {i: [(spaced_img(c[0], font(F_CAP, CAPSZ), 1, (248, 244, 236, 255)), c[1], c[2]) for c in s['caps']] for i, s in enumerate(SC) if s.get('caps')}  # 장면 안 시간별 자막 [text, at, to]
GCAP = [(spaced_img(c[0], font(F_CAP, CAPSZ), 1, (248, 244, 236, 255)), c[1], c[2]) for c in S.get('gcaps', [])]
def place_img(txt):  # 장소·연도: 붉은 세로 막대 + 굵은 글자
    t = spaced_img(txt, font(F_CAP, S.get('place_size', 44)), 3, (250, 246, 238, 255)); im = Image.new('RGBA', (t.width + 26, t.height), (0, 0, 0, 0))
    ImageDraw.Draw(im).rectangle([0, int(t.height * .2), 7, int(t.height * .84)], fill=(190, 36, 32, 255)); im.alpha_composite(t, (22, 0)); return im
PLACE = {i: place_img(s['place']) for i, s in enumerate(SC) if s.get('place')}
def card_imgs(c):  # 타이틀(배경 위 좌상단, 먹색) / 챕터(가운데, 흰색)
    if c['kind'] == 'title':
        col = tuple(c.get('color', [34, 34, 38])) + (255,)
        return [(spaced_img(c['title'], font(F_KO, W * .031 * c.get('scale', 1)), int(W * .009 * c.get('scale', 1)), col, False), 0),
                (spaced_img(c.get('sub', ''), font(F_KO, W * .015), int(W * .006), col, False), int(W * .031 * 1.8)),
                (spaced_img(c.get('en', ''), font(F_EN, W * .013 * c.get('en_scale', 1), 'Medium'), int(W * .0045 * c.get('en_scale', 1)), col, False), int(W * .031 * 1.8 * c.get('scale', 1) + W * .015 * c.get('gap', 1.9)))]
    col = tuple(c.get('color', [236, 230, 218])) + (255,)
    k = c.get('scale', 1); return [(spaced_img(c['text'], font(F_KO, W * .028 * k), int(W * .012 * k), col), 0),
            (spaced_img(c.get('en', ''), font(F_EN, W * .012 * k, 'Medium'), int(W * .005 * k), col), int(W * .028 * 1.9 * k))]
CARDS = {i: card_imgs(s['card']) for i, s in enumerate(SC) if s.get('card')}
GRAIN = [Image.fromarray(np.clip(16 + np.random.default_rng(30 + k).normal(0, 5, (H // 2, W // 2)), 0, 255).astype(np.uint8)).resize((W, H)).convert('RGB') for k in range(4)]
VIG = Image.new('L', (W, H), 0); ImageDraw.Draw(VIG).ellipse([-W * .15, -H * .25, W * 1.15, H * 1.25], fill=255)
VIG = Image.fromarray((np.asarray(VIG.filter(ImageFilter.GaussianBlur(220)), np.float32) / 255 * .28 * 255 + .72 * 255).astype(np.uint8)).convert('RGB')

def hud(im, t, i):
    im = im.convert('RGBA')
    if LB:
        d = ImageDraw.Draw(im); d.rectangle([0, 0, W, LB], fill=(0, 0, 0, 255)); d.rectangle([0, H - LB, W, H], fill=(0, 0, 0, 255))
    s = SC[i]; u = t - st[i]; D = en[i] - st[i]
    fa = lambda a0, a1, fi=.5, fo=.5: cl((u - a0) / fi) * cl((a1 - u) / fo)
    if i in CARDS:
        c = s['card']; a0 = c.get('in', .6); a1 = c.get('out', D - .3)
        for k, (img, dy) in enumerate(CARDS[i]):
            a = fa(a0 + k * .35, a1, 1.0, .8)
            if c['kind'] == 'title': paste(im, img, int(W * c.get('x', .075)), int(H * c.get('y', .30)) + dy + img.height // 2, a, 'l')
            else: paste(im, img, W // 2, H // 2 - int(W * .02) + dy, a)
    if i in PLACE: paste(im, PLACE[i], int(W * .05), LB // 2 if LB >= 60 else 70, fa(.6, D - .4, .6, .5), 'l')  # 레터박스가 있으면 위쪽 검은 띠 안에
    if i in CAP:
        cy = H - LB // 2 if LB >= 90 else H - 95
        paste(im, CAP[i], W // 2, cy, fa(td[i] / 2 + .1, D - .15, .25, .2))
    if i in CAPS:
        cy = H - LB // 2 if LB >= 90 else H - 95
        for img, c0, c1 in CAPS[i]: paste(im, img, W // 2, cy, fa(c0, c1, .25, .2))
    for img, c0, c1 in GCAP:  # v0.5: 장면과 무관한 전역 자막(대사가 컷을 넘어감)
        if c0 - .05 < t < c1 + .05: paste(im, img, W // 2, H - LB // 2 if LB >= 90 else H - 95, cl((t - c0) / .2) * cl((c1 - t) / .15))
    return im.convert('RGB')

def frame(f):
    t = f / FPS; i = max(j for j in range(N) if st[j] <= t + 1e-6)
    im = scene_frame(i, t)
    if i > 0 and td[i] > 0 and t < st[i] + td[i]: im = transition(scene_frame(i - 1, t), im, (t - st[i]) / td[i], tr[i])
    im = ImageChops.add(ImageChops.multiply(im, VIG), GRAIN[f // 2 % 4], 1, -16)
    k = min(cl(t / .6), cl((T - t) / .8))
    if k < 1: im = Image.blend(Image.new('RGB', (W, H)), im, k)
    return hud(im, t, i).tobytes()

# ---------- 소리 ----------
def bandpass(x, lo, hi):
    X = np.fft.rfft(x); fq = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (lo / np.maximum(fq, 1)) ** 4) / (1 + (fq / hi) ** 4); return np.fft.irfft(X, len(x)).astype(np.float32)
def norm(x, db): return x / (np.abs(x).max() + 1e-9) * 10 ** (db / 20)
def sfx(kind):
    g = np.random.default_rng(sum(map(ord, kind)))
    if kind in ('boom', 'hit', 'drum'):
        n = int(SR * (1.6 if kind == 'drum' else 1.1 if kind == 'boom' else .5)); t = np.arange(n) / SR
        f = (48 + 26 * np.exp(-t * 5)) if kind != 'hit' else (62 + 50 * np.exp(-t * 14))
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (3 if kind == 'drum' else 4.5 if kind == 'boom' else 11))
        y += bandpass(g.normal(0, 1, n), 80, 2500) * np.exp(-t * 60) * .4
        return norm(y, {'drum': -10, 'boom': -9, 'hit': -12}[kind])
    if kind == 'whoosh':
        n = int(SR * .6); t = np.arange(n) / n; return norm(bandpass(g.normal(0, 1, n), 300, 4000) * np.sin(np.pi * t) ** 2.5, -16)
    return np.zeros(1, np.float32)
def load_audio(src):
    p = fetch(src, 'aud')
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()
def place(buf, y, t0):
    o = int(t0 * SR)
    if o >= len(buf): return
    y = y[:len(buf) - o]; buf[o:o + len(y)] += y
def _rmsdb(x, hop):  # 0.1초 창 RMS(dB)
    k = len(x) // hop; y = x[:k * hop].reshape(k, hop); return 10 * np.log10((y.astype(np.float64) ** 2).mean(1) + 1e-12)
def sfx_cap(bus, voice, a, b, win=.1):  # v1.3: 효과음·배경 버스를 내레이션 중 (중앙값−a)dB, 없을 때 (중앙값−b)dB 이하로 자동 감쇠
    hop = int(SR * win); vd = _rmsdb(voice, hop); bd = _rmsdb(bus, hop); act = vd > -45
    if not act.any(): return bus
    med = float(np.median(vd[act])); act = act & (vd > med - 20)
    act = np.convolve(act.astype(float), np.ones(5), 'same') > 0  # 앞뒤 0.2초 여유
    lim = np.where(act, med - a, med - b); g = np.minimum(0, lim - bd)
    g = np.minimum.reduce([g, np.r_[g[1:], g[-1]], np.r_[g[0], g[:-1]]])  # 이웃 창 중 더 센 감쇠
    gl = np.repeat(10 ** (g / 20), hop); gl = np.r_[gl, np.full(max(0, len(bus) - len(gl)), gl[-1] if len(gl) else 1.)][:len(bus)]
    k = int(SR * .01); gs = np.convolve(gl, np.ones(k) / k, 'same').astype(np.float32)  # 창 단위 계단 + 10ms 램프(이웃 최소값이라 상한 유지)
    print(f'sfx_cap: 내레이션 중앙값 {med:.1f}dB, 상한 {med - a:.1f}/{med - b:.1f}dB, 감쇠 창 {(g < -.5).sum()}개')
    return bus * gs
def music_bus(n, voice):  # v1.4: music [{file, at, to, skip, db(RMS), fin, fout}] — 효과음 상한 뒤에 더하고 내레이션 엔벨로프로 덕킹(music_duck, 기본 12dB)
    out = np.zeros(n, np.float32)
    if not S.get('music'): return out
    env = np.convolve(np.abs(voice), np.ones(int(SR * .06)) / int(SR * .06), 'same'); env = np.clip(env / (env.max() * .25 + 1e-9), 0, 1)
    env = np.convolve(env, np.ones(int(SR * .4)) / int(SR * .4), 'same'); duck = 1 - (1 - 10 ** (-S.get('music_duck', 12) / 20)) * np.clip(env * 1.5, 0, 1)
    for m in S['music']:
        y = load_audio(m['file'])[int(m.get('skip', 0) * SR):]; a0 = m.get('at', 0); a1 = min(m.get('to', T), T); L = int((a1 - a0) * SR)
        if L <= 0: continue
        if len(y) < L: y = np.concatenate([y, np.zeros(L - len(y), np.float32)])
        y = y[:L]; r = np.sqrt((y ** 2).mean()) + 1e-9; y = np.tanh(y / r * 10 ** (m.get('db', -24) / 20) / .7) * .7
        fi, fo = int(m.get('fin', 1.5) * SR), int(m.get('fout', 2) * SR)
        if fi: y[:fi] *= np.linspace(0, 1, min(fi, L))[:len(y[:fi])]
        if fo: y[-fo:] *= np.linspace(1, 0, min(fo, L))[-len(y[-fo:]):]
        o = int(a0 * SR); y = y[:n - o]; out[o:o + len(y)] += y
    return out * duck
def build_audio(path='mix.wav'):
    n = int(T * SR); mix = np.zeros(n, np.float32); voice = np.zeros(n, np.float32); tt = np.arange(n) / SR
    for v in S.get('vo', []): place(voice, load_audio(v['file']) * 10 ** (v.get('db', 0) / 20), v['at'])
    if S.get('amb', 'wind') != 'none':
        w = np.random.default_rng(4).normal(0, 1, n).astype(np.float32)
        mix += norm(bandpass(w, 90, 700) * (.6 + .4 * np.sin(2 * np.pi * .05 * tt + 1) ** 2), S.get('amb_db', -34))
    for i, s in enumerate(SC):
        k = s.get('sfx', 'drum' if s.get('card') else None)
        if k and k != 'none': place(mix, sfx(k), st[i])
        for e in s.get('sfx_at', []): place(mix, sfx(e['kind']), st[i] + e['at'])
        if s.get('audio'): place(mix, load_audio(s['audio']) * 10 ** (s.get('audio_db', -6) / 20), st[i] + s.get('audio_at', 0))
    env = np.convolve(np.abs(voice), np.ones(int(SR * .06)) / int(SR * .06), 'same'); env = np.clip(env / (env.max() * .25 + 1e-9), 0, 1)
    env = np.convolve(env, np.ones(int(SR * .3)) / int(SR * .3), 'same'); duck = 1 - (1 - 10 ** (-S.get('duck_db', 8) / 20)) * env
    for b in S.get('bgm', []):
        y = load_audio(b['file'])[int(b.get('skip', 0) * SR):]; a0, a1 = b.get('at', 0), b.get('to', T); L = int((a1 - a0) * SR)  # v0.9: skip = 음원 시작 위치(초)
        y = np.tile(y, L // max(1, len(y)) + 1)[:L]; y = (np.tanh(y / (np.sqrt((y ** 2).mean()) + 1e-9) * 10 ** (b['db'] / 20) / .6) * .6) if b.get('rms') else norm(y, b.get('db', -18)); fd = int(b.get('fade', 2) * SR)  # v1.2: rms = 평균 음량 기준 + 부드러운 제한
        y[:fd] *= np.linspace(0, 1, min(fd, L)); y[-fd:] *= np.linspace(1, 0, min(fd, L))
        o = int(a0 * SR); y = y[:n - o]; mix[o:o + len(y)] += y * duck[o:o + len(y)]
    if S.get('sfx_cap'): mix = sfx_cap(mix, voice, *S['sfx_cap'])
    mus = music_bus(n, voice); bus = mix.copy(); mix += mus
    mix += voice; fo = int(.8 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
    pk = max(1, np.abs(mix).max()); pcm = (np.clip(mix / pk, -1, 1) * 32767).astype(np.int16)
    if os.environ.get('STEMS'): np.savez_compressed('stems.npz', voice=voice / pk, bus=bus / pk, music=mus / pk, mix=mix / pk)
    with wave.open(path, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print('audio', path, round(T, 2), 's')

def render_part(t0, t1):
    f0, f1 = int(round(t0 * FPS)), min(int(round(t1 * FPS)), int(T * FPS))
    need = [i for i in range(N) if st[i] < f1 / FPS and en[i] + (td[i + 1] if i + 1 < N else 0) > f0 / FPS]
    for i in need:  # 포크 전에 이 part에 필요한 원본만 올림(메모리 절약)
        if SC[i].get('video'): load_vid(i)
        else: load_src(i)
        if SC[i].get('layers'): LAY[i] = prep_layers(i)
    os.makedirs('parts', exist_ok=True); out = f'parts/p_{f0:06d}.mp4'
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', S.get('preset', 'medium'), '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS), out], stdin=subprocess.PIPE)
    import multiprocessing as mp
    with mp.get_context('fork').Pool(os.cpu_count() or 1) as pool:
        for k, b in enumerate(pool.imap(frame, range(f0, f1), chunksize=4)):
            ff.stdin.write(b)
            if k % 300 == 0: print(f'frame {f0 + k}/{f1}', flush=True)
    ff.stdin.close(); ff.wait(); print('part', out, f0, f1)

def final():
    parts = sorted(glob.glob('parts/p_*.mp4'))
    with open('parts/list.txt', 'w') as f: f.writelines(f"file '{os.path.basename(p)}'\n" for p in parts)
    out = S.get('out', 'final.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', 'parts/list.txt', '-i', 'mix.wav', '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-filter:a', 'loudnorm=I=-14:TP=-1.5', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-t', str(T), '-movflags', '+faststart', out], check=True)
    print('done', out)

if __name__ == '__main__':
    if os.environ.get('PREVIEW'):
        for x in os.environ['PREVIEW'].split(','):
            f = int(float(x) * FPS); Image.frombytes('RGB', (W, H), frame(f)).save(f'prev_{float(x):07.2f}.png')
    elif MODE == 'part': render_part(float(sys.argv[3]), float(sys.argv[4]))
    elif MODE == 'audio': build_audio()
    elif MODE == 'final': final()
    else: print(__doc__)
