#!/usr/bin/env python3
"""기마병(고구려, 붉은 망토 + 짙은 갈색 말, 등자 없음) 2프레임 질주 → spr/rd0~1.png
자체 도안(게임·만화 도안 아님). v1.1(11/02): pxlib 내장, 단독 실행. 원본 32x24 픽셀, 렌더러에서 px: True로 NEAREST 확대.
사용: python3 rider.py [출력폴더=/home/user/r/spr]"""
import sys, os
# ---- 공통 도구(pxlib 내장 — 단독 실행) ----
from PIL import Image, ImageDraw
import numpy as np
K = (22, 18, 16, 255)
def canvas(w, h): im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def outline(im, col=K):  # 투명 칸 중 불투명 칸에 닿은 곳을 외곽선 색으로
    a = np.pad(np.asarray(im), ((1, 1), (1, 1), (0, 0))).copy(); m = a[..., 3] > 0; p = np.pad(m, 1); o = np.zeros_like(m)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): o |= p[1 + dy:1 + dy + m.shape[0], 1 + dx:1 + dx + m.shape[1]]
    o &= ~m; a[o] = col; return Image.fromarray(a)
def line(d, p, q, c, w=1): d.line([p, q], fill=c, width=w)
def save(im, path, scale=1):
    if scale > 1: im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    im.save(path)
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/user/r/spr'; os.makedirs(OUT, exist_ok=True)
HO, HOD, MANE, HOOF, SK, CAP, RED, REDD, JK, WOOD, IRON = (104, 66, 40, 255), (76, 46, 28, 255), (34, 26, 22, 255), (30, 24, 20, 255), (196, 148, 108, 255), (40, 32, 28, 255), (176, 36, 30, 255), (128, 24, 22, 255), (92, 62, 40, 255), (120, 88, 56, 255), (176, 180, 186, 255)
# 다리: (어깨/엉덩이 기준점, 발끝) — 0 = 뻗음, 1 = 모음
LEGS = [[((10, 14), (4, 21)), ((12, 14), (6, 22)), ((22, 14), (29, 20)), ((20, 14), (27, 22))],
        [((10, 14), (11, 22)), ((12, 14), (13, 21)), ((22, 14), (19, 22)), ((20, 14), (18, 21))]]
for f in range(2):
    im, d = canvas(32, 24); b = 0 if f == 0 else 1
    for k, (p, q) in enumerate(LEGS[f]):
        col = HOD if k % 2 == 0 else HO; p = (p[0], p[1] + b); mid = ((p[0] + q[0]) // 2, (p[1] + q[1]) // 2 + (1 if f else 0))
        line(d, p, mid, col, 2); line(d, mid, q, col, 1); d.point(q, HOOF)
    d.ellipse([7, 9 + b, 24, 16 + b], fill=HO); d.rectangle([9, 14 + b, 22, 15 + b], fill=HOD)        # 몸통
    d.polygon([(21, 11 + b), (24, 5 + b), (27, 5 + b), (25, 12 + b)], fill=HO)                           # 목
    d.polygon([(24, 4 + b), (29, 6 + b), (30, 8 + b), (27, 8 + b), (24, 7 + b)], fill=HO); d.point((26, 5 + b), MANE)  # 머리
    line(d, (21, 9 + b), (24, 4 + b), MANE, 1); d.point((25, 3 + b), MANE)                                 # 갈기·귀
    tail = [(7, 11 + b), (3, 13 + b), (1, 16 + b)] if f == 0 else [(7, 11 + b), (3, 11 + b), (1, 13 + b)]
    d.line(tail, fill=MANE, width=2)                                                                       # 꼬리
    d.rectangle([13, 4 + b, 16, 10 + b], fill=JK); line(d, (13, 9 + b), (17, 9 + b), RED, 1)             # 기수 몸통 + 띠
    cape = [(13, 4 + b), (13, 8 + b), (6, 9 + b), (8, 6 + b)] if f == 0 else [(13, 4 + b), (13, 8 + b), (7, 7 + b), (9, 4 + b)]
    d.polygon(cape, fill=RED); line(d, cape[1], cape[2], REDD, 1)                                          # 펄럭이는 붉은 망토
    d.ellipse([14, 0 + b, 17, 3 + b], fill=SK); d.rectangle([14, 0 + b, 16, 1 + b], fill=CAP); d.point((17, 2 + b), (60, 40, 30, 255))  # 머리·모자
    line(d, (16, 11 + b), (14, 13 + b), JK, 1)                                                             # 다리(등자 없음)
    line(d, (12, 7 + b), (28, 1 + b), WOOD, 1); line(d, (29, 1 + b), (31, 0 + b), IRON, 1)               # 앞으로 겨눈 창
    save(outline(im), f'{OUT}/rd{f}.png'); print('saved', f'{OUT}/rd{f}.png')
