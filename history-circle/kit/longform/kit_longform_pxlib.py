# 도트 스프라이트 공용: 작은 격자에 앤티앨리어싱 없이 그리고 외곽선을 자동으로 두른다(역사서클 자체 도안)
from PIL import Image, ImageDraw
import numpy as np
K = (22, 18, 16, 255)
def canvas(w, h): im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def outline(im, col=K):  # 가장자리에서 반대편으로 넘어가지 않게 1px 덧대고 이웃을 본다(크기는 1px씩 커짐)
    a = np.pad(np.asarray(im), ((1, 1), (1, 1), (0, 0))).copy(); m = a[..., 3] > 0; p = np.pad(m, 1); o = np.zeros_like(m)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        o |= p[1 + dy:1 + dy + m.shape[0], 1 + dx:1 + dx + m.shape[1]]
    o &= ~m; a[o] = col; return Image.fromarray(a)
def line(d, p, q, c, w=1): d.line([p, q], fill=c, width=w)
def save(im, path, scale=1):
    if scale > 1: im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    im.save(path)
