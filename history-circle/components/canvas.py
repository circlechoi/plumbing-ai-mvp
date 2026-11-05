"""그리기 판 + 레이아웃 내보내기.

- 내부는 spec.json supersample(K=2)배로 그리고 save()에서 줄인다(bmap3.py 방식).
- 그리는 모든 요소의 bbox(출력 해상도 픽셀, [x, y, w, h])를 모아
  lint/schema/layout.schema.json 형식으로 내보낸다 → lint/layout_overlap.py로 검사.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = json.load(open(os.path.join(HERE, "spec.json"), encoding="utf-8"))
K = SPEC["supersample"]["value"]


def rgb(name):
    return tuple(SPEC["palette"][name]["rgb"])


INK = rgb("ink")
CREAM = rgb("cream")
WHITE = (255, 255, 255)

_fonts = {}


# 스킬 2절: 'JUA 폰트에 없는 기호(『』, ·, →)는 쓰지 않는다 — 렌더 전 금지 기호 검사'. fontTools가 없을 때의 최소 목록.
BANNED_FALLBACK = set("『』·→×")
_cmaps = {}


class MissingGlyph(ValueError):
    pass


def missing_glyphs(kind, text):
    """폰트에 없는 글자 목록(□로 렌더될 글자). fontTools가 있으면 cmap으로, 없으면 스킬 금지 기호 목록으로."""
    try:
        from fontTools.ttLib import TTFont
        if kind not in _cmaps:
            _cmaps[kind] = set(TTFont(os.path.join(HERE, SPEC["font"][kind])).getBestCmap())
        return sorted({ch for ch in text if not ch.isspace() and ord(ch) not in _cmaps[kind]})
    except ImportError:
        return sorted({ch for ch in text if ch in BANNED_FALLBACK})


def check_text(kind, text):
    miss = missing_glyphs(kind, text)
    if miss:
        raise MissingGlyph(f"{SPEC['font'][kind]}에 없는 글자 {miss} — □로 렌더됨: {text!r}")


def font(kind, size):
    key = (kind, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(os.path.join(HERE, SPEC["font"][kind]), size)
    return _fonts[key]


class Canvas:
    def __init__(self, fmt="shorts", bg=CREAM, scene_id="s1"):
        c = SPEC["canvas"][fmt]
        self.fmt, self.W, self.H, self.scene_id = fmt, c["w"], c["h"], scene_id
        self.im = Image.new("RGBA", (self.W * K, self.H * K), tuple(bg) + (255,))
        self.d = ImageDraw.Draw(self.im)
        self.elements = []
        self.forbidden = [{k: z[k] for k in ("id", "bbox", "allow_kinds")} for z in SPEC["forbidden"][fmt]]

    # 좌표 변환: 출력 픽셀 → 내부(K배)
    @staticmethod
    def k(v):
        return v * K

    def add(self, id, kind, bbox, **extra):
        el = {"id": id, "kind": kind, "bbox": [round(float(v), 1) for v in bbox]}
        el.update({k: v for k, v in extra.items() if v is not None})
        self.elements.append(el)
        return el

    def paste(self, tile, xy):
        """tile(내부 해상도 RGBA)을 내부 좌표 xy(왼쪽 위)에 합성."""
        self.im.alpha_composite(tile, (int(round(xy[0])), int(round(xy[1]))))

    def label(self, id, text, xy, size=36, fill=INK, stroke=WHITE, sw=6):
        """기존 lab() 방식: Jua + 흰 테두리. xy = 가운데(출력 픽셀)."""
        check_text("label", text)
        f = font("label", size * K)
        x, y = xy[0] * K, xy[1] * K
        bb = self.d.textbbox((x, y), text, font=f, anchor="mm", stroke_width=sw * K)
        self.d.text((x, y), text, font=f, fill=fill, anchor="mm", stroke_width=sw * K, stroke_fill=stroke)
        return self.add(id, "label", [bb[0] / K, bb[1] / K, (bb[2] - bb[0]) / K, (bb[3] - bb[1]) / K])

    def subtitle(self, text, y=None, size=None):
        """폐지(11/05 스타일 키트 v1): 자막은 style.kit.draw_frame(style.parts.finish)만 그린다."""
        raise RuntimeError("Canvas.subtitle 폐지 — style.parts.finish(cv, caption=...)를 쓴다")

    def save(self, path, **kw):
        out = self.im.resize((self.W, self.H), Image.LANCZOS).convert("RGB")
        if path.endswith(".png"):
            out = out.quantize(colors=kw.pop("colors", 256), method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
            out.save(path, optimize=True)
        else:
            out.save(path, quality=kw.get("quality", 90))
        return path

    def scene(self):
        return {"id": self.scene_id, "elements": list(self.elements)}


def layout_doc(canvases, episode=None):
    """여러 Canvas(장면) → layout.schema.json 문서."""
    c0 = canvases[0]
    doc = {"canvas": {"w": c0.W, "h": c0.H}, "forbidden": c0.forbidden, "scenes": [c.scene() for c in canvases]}
    if episode:
        doc["episode"] = episode
    return doc


def export_layout(canvases, path, episode=None):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(layout_doc(canvases, episode), f, ensure_ascii=False, indent=1)
    return path


# ---------- 자동 배치 보조 ----------

def _inter(a, b):
    w = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
    h = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
    return w, h


def resolve_overlap(boxes, fixed=(), zones=(), gap=8, iters=200, canvas_wh=None):
    """겹치는 bbox를 최소 이동으로 밀어낸다(그리기 전 배치 계획용).

    boxes: {id: [x, y, w, h]}  fixed: 움직이지 않을 id  zones: [[x, y, w, h], ...] 들어가면 안 되는 영역
    매 반복마다 겹친 쌍에서 '덜 겹친 축' 방향으로 겹친 만큼 + gap 민다. 움직일 수 있는 쪽만 민다.
    반환: (새 boxes, 남은 겹침 수). 남으면 사람이 배치를 다시 정해야 한다(자동으로 지우지 않음).
    """
    B = {k: list(v) for k, v in boxes.items()}
    ids = list(B)
    W, H = canvas_wh or (10 ** 9, 10 ** 9)

    def clamp(k):
        B[k][0] = min(max(B[k][0], 0), W - B[k][2])
        B[k][1] = min(max(B[k][1], 0), H - B[k][3])

    def sep(a, b_box, share):
        """a를 b_box에서 떼어 낼 이동량(덜 겹친 축) × share. 반환 (dx, dy) 또는 None."""
        iw, ih = _inter(B[a], b_box)
        if iw <= 0 or ih <= 0:
            return None
        cx = B[a][0] + B[a][2] / 2 - (b_box[0] + b_box[2] / 2)
        cy = B[a][1] + B[a][3] / 2 - (b_box[1] + b_box[3] / 2)
        if iw <= ih:
            return ((iw + gap) * share * (1 if cx >= 0 else -1), 0)
        return (0, (ih + gap) * share * (1 if cy >= 0 else -1))

    for _ in range(iters):
        moved = False
        for i in range(len(ids)):
            a = ids[i]
            if a not in fixed:
                for z in zones:
                    m = sep(a, z, 1.0)
                    if m:
                        B[a][0] += m[0]; B[a][1] += m[1]; clamp(a); moved = True
            for j in range(i + 1, len(ids)):
                b = ids[j]
                fa, fb = a in fixed, b in fixed
                if fa and fb:
                    continue
                # 둘 다 움직일 수 있으면 반씩, 하나가 고정이면 다른 쪽이 전부
                share_a = 0.0 if fa else (1.0 if fb else 0.5)
                m = sep(a, B[b], 1.0)
                if not m:
                    continue
                if share_a:
                    B[a][0] += m[0] * share_a; B[a][1] += m[1] * share_a; clamp(a)
                if 1 - share_a:
                    B[b][0] -= m[0] * (1 - share_a); B[b][1] -= m[1] * (1 - share_a); clamp(b)
                moved = True
        if not moved:
            break
    left = 0
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            iw, ih = _inter(B[ids[i]], B[ids[j]])
            left += iw > 0 and ih > 0
        for z in zones:
            if ids[i] not in fixed:
                iw, ih = _inter(B[ids[i]], z)
                left += iw > 0 and ih > 0
    return B, left
