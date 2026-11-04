#!/usr/bin/env python3
"""AI 재채색 지도 검수: 해안선 일치도(IoU) + 이동·배율 탐색 + 원본 해안선 겹쳐 그린 확인용 이미지.
사용: python3 qa.py ai.png ctl_land.png overlay.png"""
import sys, json
import numpy as np
from PIL import Image, ImageFilter, ImageChops
W, H = 1152, 2048
ai = Image.open(sys.argv[1]).convert('RGB').resize((W, H), Image.LANCZOS)
land = np.asarray(Image.open(sys.argv[2]).convert('L'), np.float32) > 127
a = np.asarray(ai.filter(ImageFilter.GaussianBlur(3)), np.float32)
# 해안에서 먼 확실한 바다/육지 픽셀로 각 4개 색 중심을 학습 → 전체를 가까운 쪽으로 분류(그림체가 바뀌어도 동작)
L8 = Image.fromarray(land.astype(np.uint8) * 255)
deep_land = np.asarray(L8.filter(ImageFilter.MinFilter(61)), np.uint8) > 127
deep_sea = np.asarray(L8.filter(ImageFilter.MaxFilter(61)), np.uint8) < 128
def km(X, k=4, it=12):
    c = X[np.random.default_rng(0).choice(len(X), k, replace=False)]
    for _ in range(it):
        lab = ((X[:, None] - c[None]) ** 2).sum(-1).argmin(1)
        c = np.array([X[lab == j].mean(0) if (lab == j).any() else c[j] for j in range(k)])
    return c
px = a.reshape(-1, 3); rs = np.random.default_rng(1)
cl_ = km(px[rs.choice(np.flatnonzero(deep_land.ravel()), 4000)]); cs_ = km(px[rs.choice(np.flatnonzero(deep_sea.ravel()), 4000)])
dl = ((px[:, None] - cl_[None]) ** 2).sum(-1).min(1); ds = ((px[:, None] - cs_[None]) ** 2).sum(-1).min(1)
sea_ai = (ds < dl).reshape(H, W)
sea_ai = np.asarray(Image.fromarray(sea_ai.astype(np.uint8) * 255).filter(ImageFilter.ModeFilter(9)), np.uint8) > 127
band = np.asarray(L8.filter(ImageFilter.MaxFilter(81)), np.uint8) > 127
band &= np.asarray(L8.filter(ImageFilter.MinFilter(81)), np.uint8) < 128      # 해안선 ±40px 띠
m = np.zeros((H, W), bool); m[int(H * .05):int(H * .95), int(W * .06):int(W * .94)] = True   # 분홍 번짐 가장자리 제외
def iou(dx, dy, s):
    im = Image.fromarray((~sea_ai).astype(np.uint8) * 255)
    im = im.transform((W, H), Image.AFFINE, (1 / s, 0, W / 2 - (W / 2 + dx) / s, 0, 1 / s, H / 2 - (H / 2 + dy) / s), Image.NEAREST)
    x = np.asarray(im) > 127
    i = (x & land & m).sum(); u = ((x | land) & m).sum(); return i / max(u, 1)
base = iou(0, 0, 1.0)
best = max(((iou(dx, dy, s), dx, dy, s) for s in (0.97, 1.0, 1.03) for dx in range(-40, 41, 20) for dy in range(-40, 41, 20)))
# 확인용: AI 그림 위에 실제 해안선(빨강) 겹치기
edge = Image.fromarray(land.astype(np.uint8) * 255).filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))
ov = ai.copy(); ov.paste((220, 30, 30), (0, 0), edge)
ov.save(sys.argv[3], quality=90) if sys.argv[3].endswith('.jpg') else ov.save(sys.argv[3])
coast_acc = float(((~sea_ai) == land)[band & m].mean())
print(json.dumps({'coast_band_accuracy': round(coast_acc, 3), 'iou_as_is': round(float(base), 3), 'best': [round(float(best[0]), 3), best[1], best[2], best[3]],
                  'sea_ratio_ai': round(float((sea_ai & m).mean() / m.mean()), 3), 'sea_ratio_true': round(float((~land & m).mean() / m.mean()), 3)}))
