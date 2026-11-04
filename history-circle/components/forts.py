"""성·요새 표식 세트 — 산성 / 평지성 / 목책. 모두 같은 크기(spec fort.size).

근거: history-map-v4 '목책·성 = 성벽 기호', history-longform-craft 'TB.fort(흙 둔덕 + 목책 + 망루)'·
'목책은 흙 둔덕 위 통나무 이중열 + 도랑', 산성(오노성·안시성).
포맷별 허용: spec fort.allowed (롱폼은 11/04 스타일 바이블 '성·부대 아이콘, 핀 금지' — 사용자 확인 필요).
벡터 도형(먹 외곽선 + 단색 면)이라 확대해도 깨지지 않는다.
"""
from PIL import ImageDraw

from canvas import INK, K, SPEC

F = SPEC["fort"]
FW, FH = F["size"]["w"], F["size"]["h"]
WALL = tuple(F["colors"]["wall"])
EARTH = tuple(F["colors"]["earth"])
WOOD = tuple(F["colors"]["wood"])
OL = 5  # 외곽선(출력 px)


class NotAllowed(Exception):
    pass


def _crenel_line(cx, y, x0, x1, n, mh):
    """톱니 성가퀴 윗선 점열."""
    pts = []
    step = (x1 - x0) / (2 * n)
    for i in range(2 * n + 1):
        x = x0 + i * step
        pts.append((x, y - (mh if i % 2 else 0)))
        if i < 2 * n:
            pts.append((x + step, y - (mh if i % 2 else 0)))
    return pts


def _poly(d, pts, fill):
    d.polygon([(x * K, y * K) for x, y in pts], fill=fill, outline=INK, width=OL * K)


def draw_fort(cv, id, xy, kind, force=False):
    """xy = 표식 중심(출력 px). kind: sanseong / pyeongji / mokchaek."""
    if kind not in F["kinds"]:
        raise ValueError("근거 없는 요새 종류: " + kind)
    if not F["allowed"][cv.fmt]["value"] and not force:
        raise NotAllowed(f"{cv.fmt} 지도에는 성 표식 금지 — spec fort.allowed: {F['allowed'][cv.fmt]['note']}")
    d: ImageDraw.ImageDraw = cv.d
    x, y = xy
    L, T, R, B = x - FW / 2, y - FH / 2, x + FW / 2, y + FH / 2

    if kind == "sanseong":
        # 봉우리 + 그 어깨를 두른 성벽 띠(톱니)
        _poly(d, [(L + 4, B - 4), (x - 6, T + 18), (x + 4, T + 26), (x + 14, T + 14), (R - 4, B - 4)], EARTH)
        top = _crenel_line(x, y + 6, L + 14, R - 14, 4, 8)
        _poly(d, top + [(R - 10, y + 22), (L + 10, y + 22)], WALL)
    elif kind == "pyeongji":
        # 네모 성벽 기호: 바깥 벽(톱니 윗선) + 가운데 성문
        top = _crenel_line(x, T + 30, L + 6, R - 6, 4, 10)
        _poly(d, top + [(R - 6, B - 8), (L + 6, B - 8)], WALL)
        gw, gh = 22, 30
        d.rounded_rectangle([(x - gw / 2) * K, (B - 8 - gh) * K, (x + gw / 2) * K, (B - 8) * K],
                            radius=10 * K, fill=INK)
    elif kind == "mokchaek":
        # 흙 둔덕 + 통나무 이중열 + 망루
        _poly(d, [(L + 2, B - 4), (L + 16, B - 24), (R - 16, B - 24), (R - 2, B - 4)], EARTH)
        for row, (y0, hgt) in enumerate(((B - 24, 30), (B - 24, 22))):
            off = 0 if row == 0 else 5
            for i in range(7):
                px = L + 16 + off + i * 10
                if px > R - 18:
                    break
                d.polygon([(px * K, y0 * K), ((px + 7) * K, y0 * K), ((px + 7) * K, (y0 - hgt + 4) * K),
                           ((px + 3.5) * K, (y0 - hgt) * K), (px * K, (y0 - hgt + 4) * K)],
                          fill=WOOD if row == 0 else tuple(int(c * .8) for c in WOOD), outline=INK, width=3 * K)
        # 망루
        tx = R - 26
        _poly(d, [(tx, B - 24), (tx, T + 14), (tx + 20, T + 14), (tx + 20, B - 24)], WOOD)
        _poly(d, [(tx - 4, T + 16), (tx + 10, T + 4), (tx + 24, T + 16)], WALL)

    return cv.add(id, "icon", [L - OL / 2, T - OL / 2, FW + OL, FH + OL], fort=kind)
