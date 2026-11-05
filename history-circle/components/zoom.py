"""광역 → 지역 연속 줌 + 콘티 점검(require_zoom).

원문 방식
- 쇼츠(history-battle-shorts 3절 13, 4편): 광역 지도에 전장 범위 금색 박스 → 1.15초 동안 박스 중심으로 확대 →
  0.55초 크로스페이드로 전장 지도. 확대하는 그림에는 라벨·성 아이콘을 넣지 않는다.
- 롱폼(history-longform-craft): 광역 지도를 지역도와 같은 경위도 창까지 0.55초 지수 확대 + 줌 블러 → 0.45초 섞기.
배율은 두 지도의 경위도 창에서 계산한다(같은 경위도 창 원칙). 단 쇼츠는 max_scale(기본 3.4배, 4편 원문)을
넘지 않는다 — 넘으면 그 배율에서 멈추고 크로스페이드로 지역 지도를 잇는다(11/05 안시성 편 약 20배 → 금색 박스가 화면을 덮음).

입력 지도는 이미 렌더된 바탕 이미지(라벨·아이콘 없는 판)와 그 경위도 창.
경위도 → 픽셀은 창 안에서 선형으로 본다(지역 규모에서 충분, 광역이 넓으면 오차 — 추정).
"""
import math

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from canvas import SPEC

Z = SPEC["zoom"]


class Win:
    """경위도 창: 서·동 경도, 남·북 위도."""

    def __init__(self, lon0, lon1, lat0, lat1):
        self.lon0, self.lon1, self.lat0, self.lat1 = lon0, lon1, lat0, lat1

    def px(self, img_wh, lon, lat):
        W, H = img_wh
        return ((lon - self.lon0) / (self.lon1 - self.lon0) * W, (self.lat1 - lat) / (self.lat1 - self.lat0) * H)

    def rect_in(self, img_wh, other):
        """다른 창(other)이 이 창 이미지 위에서 차지하는 픽셀 사각형 (x0, y0, x1, y1)."""
        x0, y0 = self.px(img_wh, other.lon0, other.lat1)
        x1, y1 = self.px(img_wh, other.lon1, other.lat0)
        return x0, y0, x1, y1

    @property
    def span(self):
        return self.lon1 - self.lon0


def _ease(t):
    return t * t * (3 - 2 * t)


def _crop(img, cx, cy, s, out_wh):
    W, H = img.size
    cw, ch = W / s, H / s
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    return img.transform(out_wh, Image.EXTENT, box, resample=Image.BILINEAR)


def _zoom_blur(img, strength):
    """가벼운 줌 블러: 조금씩 확대한 사본 평균."""
    if strength <= 0:
        return img
    W, H = img.size
    acc = img
    n = 4
    for i in range(1, n + 1):
        s = 1 + strength * i / n
        z = _crop(img, W / 2, H / 2, s, (W, H))
        acc = ImageChops.blend(acc, z, 1 / (i + 1))
    return acc


def zoom_frames(wide_img, wide_win, region_img, region_win, fmt="shorts", fps=24, max_scale=None):
    """광역 → 지역 프레임 목록(PIL RGB). 마지막 프레임 = 지역 지도 그대로.
    max_scale: 쇼츠 확대 상한(None이면 spec zoom.max_scale). 롱폼은 같은 경위도 창 원칙대로 상한 없음."""
    out_wh = region_img.size
    wide = wide_img.convert("RGB").resize(out_wh, Image.LANCZOS) if wide_img.size != out_wh else wide_img.convert("RGB")
    reg = region_img.convert("RGB")
    x0, y0, x1, y1 = wide_win.rect_in(out_wh, region_win)
    tcx, tcy = (x0 + x1) / 2, (y0 + y1) / 2
    s_end = min(out_wh[0] / (x1 - x0), out_wh[1] / (y1 - y0))  # 지역 창이 화면을 채우는 배율
    if fmt == "shorts":
        cap = Z["max_scale"]["value"] if max_scale is None else max_scale
        s_end = min(s_end, cap)
    W, H = out_wh
    frames = []
    p = Z[fmt]

    if fmt == "shorts":
        box = Image.new("RGB", out_wh)
        box.paste(wide)
        ImageDraw.Draw(box).rectangle([x0, y0, x1, y1], outline=tuple(p["box_rgb"]), width=p["box_w"])
        for i in range(int(p["box_lead_s"] * fps)):
            frames.append(box.copy())
        n = int(p["zoom_s"] * fps)
        for i in range(1, n + 1):
            g = _ease(i / n)
            s = 1 + (s_end - 1) * g
            frames.append(_crop(box, W / 2 + (tcx - W / 2) * g, H / 2 + (tcy - H / 2) * g, s, out_wh))
        last = frames[-1]
        m = int(p["xfade_s"] * fps)
        for i in range(1, m + 1):
            frames.append(Image.blend(last, reg, i / m))
    else:  # longform: 지수 확대 + 줌 블러 → 섞기
        n = int(p["zoom_s"] * fps)
        for i in range(1, n + 1):
            k = i / n
            s = s_end ** k
            f = _crop(wide, W / 2 + (tcx - W / 2) * k, H / 2 + (tcy - H / 2) * k, s, out_wh)
            frames.append(_zoom_blur(f, .04 * math.sin(math.pi * k)) if p.get("blur") else f)
        last = frames[-1]
        m = int(p["xfade_s"] * fps)
        for i in range(1, m + 1):
            frames.append(Image.blend(last, reg, i / m))
    frames[-1] = reg.copy()
    return frames


def require_zoom(scenes):
    """콘티 점검: 지도 단계가 바뀌는 장면 전환에 줌이 있는지, 배율이 크게 다른 한 프레임 컷이 없는지.

    scenes: [{"id", "map": "wide"|"region"|"none", "win": Win 또는 (lon0, lon1, lat0, lat1), "transition": "zoom"|"cut"|"xfade"}]
      transition = 이 장면으로 들어올 때의 전환.
    반환: 위반 목록(빈 목록이면 통과). 근거: battle-shorts 3절 13·14, longform-craft '연속 줌으로 잇는다'.
    """
    ratio_max = Z["cut_scale_ratio_max"]["value"]
    viol = []
    prev = None
    for sc in scenes:
        m = sc.get("map", "none")
        if prev is not None and m != "none" and prev.get("map", "none") != "none":
            pm = prev["map"]
            tr = sc.get("transition", "cut")
            if pm != m and tr != "zoom":
                viol.append({"scene": sc["id"], "what": f"{pm}→{m} 전환에 줌 없음({tr})", "rule": "광역 ↔ 지역은 연속 줌"})
            pw, cw = prev.get("win"), sc.get("win")
            if pw is not None and cw is not None and tr == "cut":
                a = pw.span if isinstance(pw, Win) else pw[1] - pw[0]
                b = cw.span if isinstance(cw, Win) else cw[1] - cw[0]
                r = max(a, b) / min(a, b)
                if r > ratio_max:
                    viol.append({"scene": sc["id"], "what": f"배율 {r:.1f}배 차이를 한 프레임 컷으로 넘김",
                                 "rule": "장면 사이 배율이 크게 다르면 한 프레임 컷 금지"})
        prev = sc
    return viol
