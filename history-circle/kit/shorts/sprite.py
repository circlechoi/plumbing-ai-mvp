"""도트 기마 무사(자체 제작, 코드로 그림) — scenes.json 장면에 "sprite":{"at":1.0,"dur":3.8,"y":1012,"alpha":0.9} 가 있으면
그 장면에서 화면 아래쪽을 왼→오로 한 번 지나간다. 외부 이미지·게임 자산을 쓰지 않는다."""
import json, sys, math
from PIL import Image, ImageDraw
_S = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'scenes.json'))
K, H1, H2, M, C, C2, O, SK, HR = (38, 28, 26), (122, 80, 50), (160, 112, 72), (58, 40, 30), (196, 42, 42), (150, 28, 34), (200, 156, 84), (238, 200, 164), (36, 28, 26)
def _frame(n):
    im = Image.new('RGBA', (28, 22), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    R = lambda x0, y0, x1, y1, c: d.rectangle((x0, y0, x1, y1), fill=c + (255,))
    b = 1 if n in (1, 2) else 0                      # 몸통 상하 반동
    # 꼬리
    R(3, 11 - b, 5, 11 - b, M); R(2, 12 - b, 4, 13 - b + (n % 2), M)
    # 몸통·목·머리
    R(6, 10 - b, 19, 14 - b, H1); R(7, 14 - b, 18, 14 - b, H2)
    R(18, 7 - b, 20, 11 - b, H1); R(19, 5 - b, 23, 8 - b, H1); R(23, 7 - b, 24, 8 - b, H2)
    R(20, 4 - b, 20, 4 - b, H1); R(22, 6 - b, 22, 6 - b, K)          # 귀·눈
    R(17, 6 - b, 18, 10 - b, M)                                       # 갈기
    # 다리 4프레임(뻗기 → 모으기)
    L = [((17, 15, 19, 16), (20, 16, 22, 17), (7, 15, 8, 16), (4, 16, 6, 17)),
         ((17, 14, 18, 17), (19, 17, 20, 18), (8, 14, 9, 17), (6, 17, 7, 18)),
         ((15, 14, 16, 17), (13, 17, 14, 18), (10, 14, 11, 17), (11, 17, 12, 18)),
         ((16, 14, 17, 16), (17, 16, 19, 17), (8, 14, 9, 16), (6, 16, 8, 17))][n]
    for r in L: R(*r, M if L.index(r) % 2 else H1)
    # 기수: 망토(뒤로 펄럭) · 몸 · 머리 · 상투
    w = (0, 1, 2, 1)[n]
    R(7 - w, 5 - b, 11, 7 - b, C); R(6 - w, 7 - b, 10, 8 - b + (n % 2), C2)
    R(11, 4 - b, 14, 9 - b, O); R(11, 8 - b, 14, 8 - b, C)            # 저고리 + 붉은 띠
    R(14, 6 - b, 17, 6 - b, O); R(17, 6 - b, 17, 7 - b, SK)           # 고삐 쥔 팔
    R(12, 10 - b, 14, 12 - b, O); R(13, 13 - b, 15, 13 - b, K)        # 다리·신
    R(12, 1 - b, 14, 3 - b, SK); R(12, 0 - b, 14, 0 - b, HR); R(11, 1 - b, 11, 2 - b, HR); R(12, -1 - b + 1, 13, 0 - b, HR)
    return im
def _outline(im):
    a = im.getchannel('A'); o = Image.new('RGBA', im.size, (0, 0, 0, 0)); px = a.load(); op = o.load()
    for y in range(im.height):
        for x in range(im.width):
            if px[x, y] == 0 and any(0 <= x + dx < im.width and 0 <= y + dy < im.height and px[x + dx, y + dy] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                op[x, y] = K + (255,)
    o.alpha_composite(im); return o
SCALE = 4
FR = []
for n in range(4):
    f = Image.new('RGBA', (30, 24), (0, 0, 0, 0)); f.alpha_composite(_frame(n), (1, 2)); f = _outline(f)
    FR.append(f.resize((f.width * SCALE, f.height * SCALE), Image.NEAREST))
_sc = _S['scenes']
RUNS = [(float(s['start']) + s['sprite'].get('at', .8), s['sprite'].get('dur', 3.4), s['sprite'].get('y', 1090), s['sprite'].get('alpha', .92)) for s in _sc if s.get('sprite')]
def SPR(im, t):
    for t0, du, y, al in RUNS:
        v = (t - t0) / du
        if not 0 <= v <= 1: continue
        f = FR[int((t - t0) * 9) % 4]
        x = int(-f.width + (1080 + f.width) * v)
        a = min(1, v / .08, (1 - v) / .08) * al
        sh = Image.new('RGBA', (f.width, 10), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((14, 0, f.width - 14, 9), fill=(0, 0, 0, int(70 * a)))
        im.alpha_composite(sh, (max(0, x), y + f.height - 12)) if 0 <= x <= 1080 - f.width else None
        g = f if a >= .999 else Image.merge('RGBA', f.split()[:3] + (f.getchannel('A').point(lambda p: int(p * a)),))
        cx0 = max(0, -x); cx1 = min(f.width, 1080 - x)
        if cx1 > cx0: im.alpha_composite(g.crop((cx0, 0, cx1, f.height)), (x + cx0, y))
if __name__ == '__main__':
    sheet = Image.new('RGBA', (FR[0].width * 4 * 2, FR[0].height * 2), (120, 150, 110, 255))
    for i, f in enumerate(FR): sheet.alpha_composite(f.resize((f.width * 2, f.height * 2), Image.NEAREST), (i * f.width * 2, 0))
    sheet.save('sprite_sheet.png')
