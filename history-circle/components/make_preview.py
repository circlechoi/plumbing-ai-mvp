"""시안 PNG 3장 + 샘플 전장 layout JSON 생성.

사용: python3 make_preview.py   → preview/a_units.png, b_forts.png, c_battle.png, c_battle.layout.json
바탕 지도(v4-S)는 이 컴포넌트 몫이 아니라 단색 바탕을 쓴다.
"""
import os

from PIL import ImageDraw

from canvas import CREAM, INK, K, Canvas, export_layout, resolve_overlap
from forts import draw_fort
from units import ORDER, draw_unit, grade_dims, unit_bbox

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "preview")
GROUND = (214, 196, 156)  # 황토(3절 16 '황토·녹색 산지·파란 물') — 시안용 단색


def a_units():
    cv = Canvas("shorts", bg=CREAM, scene_id="a_units")
    cv.label("t", "'ㅗ' 블록 등급 규격 (S, M, L, XL)", (540, 300), 48)
    facs = [("goguryeo", "고구려", "inf"), ("tang", "당", "cav"), ("malgal", "말갈", "mal")]
    for j, (fk, fn, ic) in enumerate(facs):
        cv.label(f"h{j}", fn, (250 + j * 280, 420), 40)
        for i, g in enumerate(ORDER):
            draw_unit(cv, f"{fk}_{g}", (250 + j * 280, 560 + i * 200), 0, g, fk, icon=ic)
    for i, g in enumerate(ORDER):
        w, h = grade_dims(g)
        cv.label(f"g{g}", f"{g} {w}x{h}", (90, 560 + i * 200), 30)
    draw_unit(cv, "hidden_M", (390, 1400 - 40), 0, "M", "tang", hidden=True)
    cv.label("hl", "숨은 부대", (650, 1360), 36)
    return cv


def b_forts():
    cv = Canvas("shorts", bg=CREAM, scene_id="b_forts")
    cv.label("t", "성과 요새 표식 (같은 크기 96x96)", (540, 400), 48)
    for i, (k, n) in enumerate([("sanseong", "산성"), ("pyeongji", "평지성"), ("mokchaek", "목책")]):
        x = 220 + i * 300
        draw_fort(cv, k, (x, 700), k)
        cv.label(f"n{k}", n, (x, 820), 40)
    # 실제 크기 비교: 블록 M 옆
    draw_unit(cv, "cmp_M", (380, 1080), 0, "M", "goguryeo", icon="inf")
    draw_fort(cv, "cmp_fort", (640, 1080), "sanseong")
    cv.label("cmp", "블록 M과 같은 화면에서", (540, 1200), 34)
    return cv


def c_battle():
    cv = Canvas("shorts", bg=GROUND, scene_id="c_battle")
    d = ImageDraw.Draw(cv.im)
    # 제목 띠(2절): 검은 띠 + 크림 띠 140~236
    d.rectangle([0, 0, 1080 * K, 140 * K], fill=(20, 18, 16))
    d.rectangle([0, 140 * K, 1080 * K, 236 * K], fill=CREAM)
    from canvas import font
    d.text((540 * K, 188 * K), "안시성 앞 고구려 진", font=font("label", 52 * K), fill=INK, anchor="mm")
    cv.add("title", "title", [0, 140, 1080, 96])
    # 계획: 블록 6개(지형 따라 휘고 엇갈리게, 3절 9) + 성 1개 → 겹침 자동 해소
    plan = {
        "g1": ((260, 820), -60, "M", "goguryeo", "cav"),
        "g2": ((380, 760), -50, "M", "goguryeo", "inf"),
        "g3": ((500, 730), -40, "M", "goguryeo", "inf"),
        "g4": ((610, 760), -30, "M", "goguryeo", "inf"),
        "g5": ((700, 820), -20, "M", "goguryeo", "cav"),
        "g6": ((760, 920), -10, "L", "malgal", "mal"),
    }
    fort_xy = (330, 1110)
    boxes = {k: unit_bbox(*v[:3]) for k, v in plan.items()}
    boxes["fort"] = [fort_xy[0] - 50, fort_xy[1] - 50, 100, 100]
    zones = [z["bbox"] for z in cv.forbidden]
    fixed_boxes, left = resolve_overlap(boxes, fixed={"fort"}, zones=zones, gap=10, canvas_wh=(1080, 1920))
    assert left == 0, "자동 배치로 겹침이 안 풀림"
    for k, (xy, ang, g, fk, ic) in plan.items():
        b0, b1 = boxes[k], fixed_boxes[k]
        nxy = (xy[0] + b1[0] - b0[0], xy[1] + b1[1] - b0[1])
        draw_unit(cv, k, nxy, ang, g, fk, icon=ic)
    draw_fort(cv, "ansi", fort_xy, "sanseong")
    cv.label("ansi_l", "안시성", (fort_xy[0] + 130, fort_xy[1]), 40)
    # 자막은 style.parts.finish가 그린다(Canvas.subtitle 폐지)
    return cv


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("a_units", a_units), ("b_forts", b_forts), ("c_battle", c_battle)):
        cv = fn()
        p = cv.save(os.path.join(OUT, name + ".png"))
        print(p, os.path.getsize(p))
        if name == "c_battle":
            print(export_layout([cv], os.path.join(OUT, "c_battle.layout.json"), episode="preview"))


if __name__ == "__main__":
    main()
