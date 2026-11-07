"""세력 영역 칠하기(빈틈 없는 방식). style.json rules.map_territory.
territories(im, M, regs, K=2): regs=[(poly_lonlat, rgb, alpha)], M=engine.Map. im=K배 RGBA 지도.
- 경계는 이웃끼리 같은 꼭짓점 리스트를 공유(정·역순)
- 해안 쪽 꼭짓점은 바다로 넉넉히 → 바다 마스크(파랑>빨강+25)로 잘라냄
- ModeFilter로 꼭짓점 각을 둥글게, 국경선은 세력이 맞닿는 육지 위에만"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
def sea_mask(im):
    a = np.asarray(im.convert('RGB')).astype(int); return a[..., 2] > a[..., 0] + 25
def territories(im, M, regs, K=2, smooth=21, border=(60, 40, 32)):
    sea = sea_mask(im); W, H = im.size; lab = Image.new('L', (W, H), 0); dl = ImageDraw.Draw(lab)
    for i, (poly, rgb, al) in enumerate(regs): dl.polygon([(M.P(*p)[0] * K, M.P(*p)[1] * K) for p in poly], fill=i + 1)
    lab = lab.filter(ImageFilter.ModeFilter(smooth)); L = np.asarray(lab).copy(); L[sea] = 0
    a = np.asarray(im.convert('RGBA')).astype(np.float32); lum = a[..., :3].mean(2, keepdims=True) / 200
    for i, (poly, rgb, al) in enumerate(regs):
        m = (L == i + 1)[..., None]; tint = np.array(rgb, np.float32) * np.clip(lum, .55, 1.15)
        a[..., :3] = np.where(m, a[..., :3] * (1 - al) + tint * al, a[..., :3])
    out = Image.fromarray(a.astype(np.uint8)); Lc = L.astype(np.int16); bd = np.zeros(L.shape, bool)
    for sh in ((0, 3), (3, 0)): bd |= Lc != np.roll(Lc, sh, (0, 1))
    for sh in ((3, 0), (0, 3), (-3, 0), (0, -3)): bd &= ~np.roll(sea, sh, (0, 1))
    bd &= ~sea; bd[:, :4] = False; bd[:, -4:] = False; bd[:4, :] = False; bd[-4:, :] = False  # roll 래핑 잔선 방지
    out.paste(Image.new('RGBA', (W, H), border + (255,)), (0, 0), Image.fromarray((bd * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7)))
    return out
