#!/usr/bin/env python3
"""몰래 빠지는 병사(고구려, 황갈 삼베옷 + 붉은 띠, 창을 낮게 든 웅크린 걸음) 4프레임 → spr/sn0~3.png
자체 도안(게임·만화 도안 아님). v1.1(11/02): pxlib 내장, 단독 실행. 원본 24x24 픽셀, 렌더러에서 px: True로 NEAREST 확대.
사용: python3 sneak.py [출력폴더=/home/user/r/spr]"""
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
SK, CAP, OC, OCD, RED, LEG, LEGD, BOOT, WOOD, IRON = (196, 148, 108, 255), (40, 32, 28, 255), (150, 108, 58, 255), (112, 78, 42, 255), (172, 34, 30, 255), (96, 76, 54, 255), (70, 54, 38, 255), (46, 36, 28, 255), (120, 88, 56, 255), (176, 180, 186, 255)
# 발 위치(뒤 다리, 앞 다리) — 웅크린 걸음 주기
FEET = [((5, 21), (15, 21)), ((8, 21), (12, 20)), ((14, 21), (6, 21)), ((11, 20), (9, 21))]
BOB = [0, -1, 0, -1]
for f in range(4):
    im, d = canvas(24, 24); b = BOB[f]; hip = (10, 14 + b)
    far, near = FEET[f] if f < 2 else (FEET[f][1], FEET[f][0])
    for foot, col in ((far, LEGD), (near, LEG)):  # 먼 다리를 먼저(어둡게)
        knee = ((hip[0] + foot[0]) // 2 + 2, (hip[1] + foot[1]) // 2 - 1)
        line(d, hip, knee, col, 2); line(d, knee, foot, col, 2); line(d, (foot[0], foot[1]), (foot[0] + 2, foot[1]), BOOT, 1); d.point((foot[0], foot[1] - 1), BOOT)
    d.polygon([(7, 14 + b), (12, 14 + b), (16, 8 + b), (11, 7 + b)], fill=OC)       # 앞으로 숙인 몸통
    d.polygon([(7, 14 + b), (9, 14 + b), (12, 8 + b), (11, 7 + b)], fill=OCD)       # 등 그늘
    line(d, (8, 13 + b), (13, 12 + b), RED, 1)                                       # 붉은 띠
    d.rectangle([7, 15 + b, 12, 15 + b], fill=OC)                                     # 저고리 자락
    d.ellipse([15, 3 + b, 19, 7 + b], fill=SK); d.rectangle([15, 3 + b, 18, 4 + b], fill=CAP); d.point((14, 4 + b), CAP)  # 머리 + 상투 모자
    d.point((18, 5 + b), (60, 40, 30, 255))                                           # 눈(앞을 살핌)
    line(d, (2, 13 + b), (19, 10 + b), WOOD, 1); line(d, (20, 10 + b), (22, 9 + b), IRON, 1); d.point((19, 10 + b), (150, 30, 26, 255))  # 낮게 든 창 + 붉은 술
    line(d, (14, 9 + b), (16, 11 + b), OCD, 2); d.point((17, 11 + b), SK)             # 팔과 손
    save(outline(im), f'{OUT}/sn{f}.png'); print('saved', f'{OUT}/sn{f}.png')
