"""역사서클 스타일 키트 — style.json만 읽어 화면 틀을 그린다.

숫자는 이 파일에 쓰지 않는다. 모든 크기·좌표·색은 style.json에서 온다.
사용:
    from style.kit import S, font, draw_frame
    im = draw_frame(map_img, year='645년', title=[('당 태종에게 ', 0), ('포위 섬멸', 1), ('당한 15만 고구려 대군', 0)],
                    caption='하지만 당군은 요동성에서', legend=['고구려', '당'], note='개념도   안시성 = 영성자산성설', t=3.0)
"""
import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # history-circle/
S = json.load(open(os.path.join(ROOT, "style", "style.json"), encoding="utf-8"))
_FC = {}


class GlyphError(ValueError):
    pass


def color(name_or_rgb):
    """색 이름(style.json colors 키) 또는 [r,g,b] → tuple."""
    if isinstance(name_or_rgb, str):
        return tuple(S["colors"][name_or_rgb])
    return tuple(name_or_rgb)


def faction(name, kind="unit_faction"):
    return tuple(S["colors"][kind][name])


def font(type_key, scale=1.0, size=None):
    """type_scale 키 → ImageFont. scale은 슈퍼샘플 배율(K)."""
    t = S["type_scale"][type_key]
    f = S["fonts"][t["font"]]
    px = int(round((size or t["size"]) * scale))
    k = (f["file"], px, t.get("weight"))
    if k not in _FC:
        ft = ImageFont.truetype(os.path.join(ROOT, f["file"]), px)
        if t.get("weight"):
            ft.set_variation_by_name(t["weight"])
        _FC[k] = ft
    return _FC[k]


def check_text(s):
    bad = [g for g in S["fonts"]["forbidden_glyphs"]["value"] if g in s]
    if bad:
        raise GlyphError(f"금지 기호 {bad} in {s!r}")
    return s


def _ramp(t, a, b):
    return max(0.0, min(1.0, (t - a) / max(1e-6, b - a)))


def _gradient(h):
    g = S["frame"]["caption"]["gradient"]
    col = np.zeros((h, 1), np.float32)
    span = g["y1"] - g["y0"]
    for y in range(g["y0"], min(h, g["y1"])):
        col[y] = g["peak_alpha"] * math.sin(math.pi * (y - g["y0"]) / span) ** g["power"] / 255
    return col, g["to"]


def wrap_caption(text, d, f):
    c = S["frame"]["caption"]
    if d.textlength(text, font=f) <= c["max_w"]:
        return [text]
    ws = text.split(" ")
    best = None
    for i in range(1, len(ws)):
        a, b = " ".join(ws[:i]), " ".join(ws[i:])
        m = max(d.textlength(a, font=f), d.textlength(b, font=f))
        if best is None or m < best[0]:
            best = (m, [a, b])
    return best[1] if best else [text]


def draw_frame(im, year, title, caption=None, legend=(), note="", t=99.0, caption_age=99.0, first_scene=False):
    """지도 이미지(1080×1920 RGB) 위에 화면 틀을 얹는다.

    title = [(글자, 강조여부), ...], legend = 세력 이름 목록(unit_faction 키), t = 장면 시작 후 초.
    """
    F = S["frame"]
    W, H = F["canvas"]["w"], F["canvas"]["h"]
    if im.size != (W, H):
        raise ValueError(f"캔버스는 {W}×{H}")
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    g, to = _gradient(H)
    a = a * (1 - g[..., None]) + to * g[..., None]
    im = Image.fromarray(a.astype(np.uint8))
    d = ImageDraw.Draw(im, "RGBA")

    tb = F["top_band"]
    d.rectangle(tb["bbox"], fill=color(tb["fill"]) + (tb["alpha"],))
    yb, wm = tb["year_badge"], tb["watermark"]
    d.text(yb["xy"], check_text(year), font=font(yb["type"]), fill=color(yb["color"]), anchor=yb["anchor"])
    d.text(wm["xy"], wm["text"], font=font(wm["type"]), fill=color(wm["color"]), anchor=wm["anchor"])

    ti = F["title_band"]
    intro = ti["intro"]
    if first_scene and t < intro["hidden_until_s"]:
        d.rectangle(ti["bbox"], fill=color(tb["fill"]) + (intro["hidden_alpha"],))
    else:
        al = int(ti["alpha"] * (_ramp(t, intro["hidden_until_s"], intro["hidden_until_s"] + intro["fade_s"]) if first_scene else 1))
        d.rectangle(ti["bbox"], fill=color(ti["fill"]) + (al,))
        f = font(ti["type"])
        em = ti["emphasis"]
        n_em = sum(1 for _, h in title if h)
        total = sum(d.textlength(check_text(p), font=f) for p, _ in title) + 2 * em["gap"] * n_em
        x = W / 2 - total / 2
        y = ti["text_y"]
        for p, h in title:
            w = d.textlength(p, font=f)
            if h:
                x += em["gap"]
                d.rounded_rectangle([x - em["pad_x"], y - em["half_h"], x + w + em["pad_x"], y + em["half_h"]],
                                    radius=em["radius"], fill=color(em["fill"]) + (al,))
                d.text((x, y + em["text_dy"]), p, font=f, fill=color(em["text"]) + (al,), anchor="lm")
                x += w + em["gap"]
            else:
                d.text((x, y), p, font=f, fill=color(ti["color"]) + (al,), anchor="lm")
                x += w

    if caption:
        c = F["caption"]
        f2 = font(c["type"])
        lines = wrap_caption(check_text(caption), d, f2)
        al = int(255 * _ramp(caption_age, 0, c["fade_s"]))
        y0 = c["center_y"] - (len(lines) - 1) * c["line_gap"] / 2
        for n, ln in enumerate(lines):
            d.text((W / 2, y0 + n * c["line_gap"]), ln, font=f2, fill=color(c["color"]) + (al,), anchor="mm",
                   stroke_width=S["type_scale"][c["type"]]["stroke"], stroke_fill=color(c["stroke_color"]) + (al,))

    lb = F["legend_band"]
    d.rectangle(lb["bbox"], fill=color(lb["fill"]) + (lb["alpha"],))
    ch = lb["chip"]
    fl = font("legend")
    x = ch["x0"]
    y = lb["row_y"]
    for name in legend:
        d.rectangle([x, y - ch["size"] / 2, x + ch["size"], y + ch["size"] / 2], fill=faction(name),
                    outline=tuple(ch["outline"]), width=ch["outline_w"])
        d.text((x + ch["text_dx"], y), name, font=fl, fill=color("legend_text"), anchor="lm")
        x += ch["step_pad"] + d.textlength(name, font=fl)
    if note:
        nt = lb["note"]
        d.text(nt["xy"], check_text(note), font=font(nt["type"]), fill=color(nt["color"]), anchor=nt["anchor"])
    return im
