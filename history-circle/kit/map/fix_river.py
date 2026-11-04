#!/usr/bin/env python3
"""AI 재채색 지도 하천 보정(v7.1): 정밀 하천 마스크 기준으로
① 마스크 밖으로 번진 물 → 주변 땅색으로 메움  ② 마스크 안인데 땅으로 칠해진 곳 → 주변 물색으로 메움  ③ 바뀐 강둑에 옅은 먹선.
사용: python3 fix_river.py ai.png river_mask.png out.png [허용폭_px(1152폭 기준, 기본 4)]"""
import sys
import numpy as np
from PIL import Image, ImageFilter
ai = Image.open(sys.argv[1]).convert('RGB'); W, H = ai.size
tol = float(sys.argv[4]) if len(sys.argv) > 4 else 4
rv = Image.open(sys.argv[2]).convert('L').resize((W, H), Image.BILINEAR)
t = int(tol * W / 1152) * 2 + 1
M = lambda x: Image.fromarray(x.astype(np.uint8) * 255)
dil = lambda x, n: np.asarray(M(x).filter(ImageFilter.MaxFilter(n)), np.uint8) > 127
ero = lambda x, n: np.asarray(M(x).filter(ImageFilter.MinFilter(n)), np.uint8) > 127
river = np.asarray(rv, np.uint8) > 127
a = np.asarray(ai, np.float32); sm = np.asarray(ai.filter(ImageFilter.GaussianBlur(3)), np.float32)
r, g, b = sm[..., 0], sm[..., 1], sm[..., 2]
wat = (b > r + 30) & (b > g - 10)
tex = a - np.asarray(ai.filter(ImageFilter.GaussianBlur(4)), np.float32)            # 붓결·종이 결
def fill_from(src):  # 정규화 합성곱: src 픽셀 색으로 가까운 곳부터 채움
    fill = np.zeros_like(a); done = np.zeros((H, W), bool); w = src.astype(np.float32)
    for sig in (6, 14, 30, 60, 120):
        den = np.asarray(Image.fromarray((w * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sig)), np.float32) / 255
        num = np.stack([np.asarray(Image.fromarray(np.clip(a[..., c] * w, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sig)), np.float32) for c in range(3)], -1)
        ok = (den > .12) & ~done
        fill[ok] = (num / np.maximum(den, 1e-3)[..., None])[ok]; done |= ok
    fill[~done] = a[~done]
    return fill
# ① 넘친 물 → 땅
too_wet = wat & ~dil(river, t)
too_wet = dil(too_wet, 7) & ~dil(river, max(3, t - 4))
land_fill = fill_from(~dil(wat, 9)) + np.roll(tex, 80, 1) * .6
# ② 빠진 물 → 물
too_dry = ero(river, 5) & ~wat
too_dry = dil(too_dry, 5) & river
water_fill = fill_from(ero(wat, 5) & river) + np.roll(tex, 40, 0) * .4
feather = lambda x: np.asarray(M(x).filter(ImageFilter.GaussianBlur(2.5)), np.float32)[..., None] / 255
m1, m2 = feather(too_wet), feather(too_dry)
out = a * (1 - m1) + land_fill * m1
out = out * (1 - m2) + water_fill * m2
# ③ 바뀐 곳의 새 강둑에 옅은 먹선
final_w = (wat & ~too_wet) | too_dry
bank = dil(final_w, 3) & ~ero(final_w, 3) & dil(too_wet | too_dry, 9)
e = np.asarray(M(bank).filter(ImageFilter.GaussianBlur(1.2)), np.float32)[..., None] / 255 * .5
out = out * (1 - e) + np.array([50, 80, 90], np.float32) * e
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(sys.argv[3])
print(f'water {int(wat.sum())} px · 넘친 물 제거 {int(too_wet.sum())} · 빠진 물 채움 {int(too_dry.sum())}')
