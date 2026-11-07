import os
exec(open(os.path.expanduser('~/ansi/k/scenes9.py')).read())
exec(open(os.path.expanduser('~/ansi/k10/maps10.py')).read())
exec(open(os.path.expanduser('~/ansi/k10/siege10.py')).read())
_unit0 = P.unit
def _unit(cv, id, xy, ang, grade, faction, icon=None, **kw):
    if faction == '당' and icon == 'inf': icon = 'tinf'
    return _unit0(cv, id, xy, ang, grade, faction, icon=icon, **kw)
P.unit = _unit
def S4_both(u, D):
    t3 = chunk_times('S4')[3][0]
    return S4_map(u, D) if u < t3 - .1 else S4(u, D)
TITLE = [('당 태종도 ', 0), ('넘지 못한', 1), (' 안시성', 0)]
SF = {'S1': S1, 'S2': S2, 'S3': S3, 'S4': S4_both, 'S5': S5, 'S6': S6, 'S7': S7, 'S8': S8, 'S9': S9}
def cam(cv, zoom=1.0, cx=540, cy=960, dx=0.0, dy=0.0, top=236, bot=1600):
    """카메라: 화면 틀 아래 본문 영역만 (cx,cy) 중심 확대 + 흔들림."""
    if zoom <= 1.001 and abs(dx) < .5 and abs(dy) < .5: return
    k = KK; W, Hh0 = cv.im.size; T = top * k; Hh = bot * k; ch = Hh - T
    w = W / zoom; h = ch / zoom
    x0 = min(max(cx * k - w / 2, 0), W - w) - dx * k; y0 = min(max(cy * k - h / 2, T), Hh - h) - dy * k
    x0 = min(max(x0, 0), W - w); y0 = min(max(y0, T), Hh - h)
    part = cv.im.transform((W, ch), Image.EXTENT, (x0, y0, x0 + w, y0 + h), resample=Image.BILINEAR)
    cv.im.paste(part, (0, T)); cv.d = ImageDraw.Draw(cv.im)
def camera(s, u, cv):
    D = DUR[s]
    if s == 'S6':
        th = CT('S6', 7); tup = CT('S6', 4) + 1.0; z = 1 + .14 * ease(ramp(u, tup, th - .3)) * (1 - ease(ramp(u, th - .3, th + .5))); cam(cv, z, 520, 900)
    elif s == 'S7':
        tc = CT('S7', 1); tout = CT('S7', 5); t3 = CT('S7', 8)
        sh = max(0.0, 1 - (u - tc) / .9) if u >= tc else 0.0
        z0 = 1.04 if sh > 0 else 1.0
        dx = 12 * sh * math.sin(u * 61); dy = 9 * sh * math.cos(u * 47)
        zin = ease(ramp(u, tout + .4, tout + 1.2)); zout = ease(ramp(u, t3 - 1.0, t3))
        z = max(z0, 1 + .3 * zin * (1 - zout)); cam(cv, z, 480, 640, dx, dy)
    else:   # 기본 카메라: 장면 내내 아주 느린 확대
        cam(cv, 1 + .04 * ease(min(1.0, u / max(D, .1))), 540, 900)
LIVE = os.path.expanduser('~/ansi/k10/live/')
def live(name, tc):
    import glob
    n = len(glob.glob(LIVE + name + '_*.jpg'))
    i = max(1, min(n, int(tc * 15) + 1))
    return Image.open(LIVE + '%s_%03d.jpg' % (name, i)).convert('RGBA')
def live_plan(s, u):
    """(클립, 클립 시각, 불투명도) 또는 None. C1 = 훅 첫 3.3초, C2 = S7 '산은 끝내 고구려 차지' 구간."""
    if s == 'S1':
        a, b = 0.0, chunk_times('S1')[3][0] - .05
        if u < b: return ('c1', u + .3, 1.0 if u < b - .3 else (b - u) / .3)
    if s == 'S7':
        ct = chunk_times('S7'); a, b = ct[9][0] - .15, ct[11][0] - .05
        if a <= u < b: return ('c2', 1.0 + (u - a), min(1.0, (u - a) / .25, (b - u) / .3))
    return None
def frame(t):
    HUD.clear(); s, u = at(t); u = min(u, DUR[s]); cv = SF[s](u, DUR[s]); camera(s, u, cv)
    for f in HUD: f(cv)
    HUD.clear(); cv.d = ImageDraw.Draw(cv.im)
    lp = live_plan(s, u)
    if lp:
        lim = live(lp[0], lp[1]); a_ = max(0.0, min(1.0, lp[2]))
        k_ = KK; box = (0, 236 * k_, lim.width, 1600 * k_)
        reg = cv.im.crop(box).convert('RGBA'); lreg = lim.crop(box)
        cv.im.paste(Image.blend(reg, lreg, a_) if a_ < 1 else lreg, (0, 236 * k_)); cv.d = ImageDraw.Draw(cv.im)
    ct = chunk_times(s); cur = [i for i, (t0, c) in enumerate(ct) if t0 <= u]
    cap = None; age = 99
    if cur:
        i = cur[-1]; st = i - (i % 2); cap = '\n'.join(ct[j][1] for j in range(st, min(st + 2, len(ct))) if ct[j][0] <= u); age = u - ct[i][0]
    note = '재현 이미지   개념도' if lp else '출처: 자치통감 권197~198' if (s == 'S9' and u > DUR['S9'] - 5.0) else '개념도   안시성 = 영성자산성설'
    im = P.finish(cv, year='645년', title=TITLE, caption=cap, legend=LEG, note=note, t=u, caption_age=age, first_scene=(s == 'S1'))
    if s == 'S7':
        tc = ev('S7', '무너져', 2)
        if tc + .3 < u < tc + .5: im = Image.blend(im, Image.new('RGB', im.size, (255, 255, 255)), .5)
    return im
