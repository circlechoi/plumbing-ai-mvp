"""5편 안시성 전투 — 콘티(정지 시안 10장) + 무음 애니매틱.

사용:
  python3 build.py storyboard   → storyboard/sNN.png(540×960) + contact.png + layout.json
  python3 build.py animatic     → animatic.mp4(540×960, 12fps, 무음) + sections.json + cuts.json + timing.json
대본: ../script.txt(v3). 문장 길이 = 음절/6.2초 + 0.35초(추정 — 녹음 뒤 실제 길이로 바꾼다).
크레딧 0: 생성·TTS 없음. 지도 = v4-S(bases.py), 블록·성·줌·레이아웃 = components.
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bases as BS  # noqa: E402
import engine as E  # noqa: E402

SCRIPT = os.path.join(HERE, "..", "script.txt")
SC = E.parse_script(SCRIPT)
TL, TOTAL = E.timeline(SC)
FPS = 12
LL = BS.LL
MW, MR = BS.MW, BS.MR
GOG, TANG = "goguryeo", "tang"
TITLE = [("당 태종을 석 달 묶은 한 수, ", False), ("버티기", True)]
LEGEND = [(E.UNIT["goguryeo"], "고구려"), (E.UNIT["tang"], "당")]
NOTE = "개념도   안시성 = 영성자산성설"
NOTE_SRC = "출처: 삼국사기, 자치통감 권198"
# 장면별 지도 단계(require_zoom) — 3장면은 오골성 우회로를 보여야 해 광역 유지, 광역→지역 줌은 4장면 시작
MAPS = {1: "wide", 2: "wide", 3: "wide", 4: "region", 5: "region", 6: "none", 7: "none", 8: "region", 9: "region", 10: "none"}
TRANS = {4: "zoom"}
ZOOM_S = 0.4 + 1.15 + 0.55

_B = {}


def base(kind):
    k = E.K()
    key = (kind, k)
    if key not in _B:
        bw, br = BS.bases(2)
        im = bw if kind == "wide" else br
        _B[key] = im if k == 2 else im.resize((E.W * k, E.H * k), Image.LANCZOS)
    return _B[key]


def W_(name):
    return MW.P(*LL[name])


def R_(name):
    return MR.P(*LL[name])


def st(n, i):
    return TL[n]["starts"][i]


# ---------------- 장면 ----------------

WIDE_TANG = [((420, 720), 270), ((580, 840), 270), ((440, 1000), 270)]


def s1(u):
    cv = E.world(base("wide"), "s1")
    an = W_("안시성")
    E.fort(cv, "f_ansi", an)
    E.label(cv, "l_ansi", "안시성", (an[0], an[1] + 78), size=44)
    ends = WIDE_TANG
    starts = [(640, 480), (780, 640), (700, 820)]
    g = E.ease(E.ramp(u, 0.0, 3.0))
    for i, ((ex, ey), a), (sx, sy) in zip(range(3), ends, starts):
        E.unit(cv, f"u_tang{i}", (E.lerp(sx, ex, g), E.lerp(sy, ey, g)), a, "XL", TANG, icon="cav")
    age = u - 1.6
    if age > 0:
        E.bignum(cv, "n_3m", "석 달", (640, 1150), size=110, scale=E.popf(age))
    if u >= st(1, 1):
        E.lord(cv, "lord", (an[0], an[1] - 88))
        E.bignum(cv, "q", "?", (an[0] + 64, an[1] - 110), size=70, scale=E.popf(u - st(1, 1)))
    return cv, dict(z=E.lerp(1.0, 1.05, u / TL[1]["dur"]), cx=420, cy=850)


def s2(u):
    cv = E.world(base("wide"), "s2")
    an = W_("안시성")
    # 주필산 15만 잔상(흐려지며 사라짐) — 실제 좌표 주필산에서 남동쪽으로 블록 몸통만 비켜 놓음
    zp = W_("주필산")
    fade = 1 - E.ramp(u, 1.0, st(2, 1))
    if fade > 0:
        E.unit(cv, "u_gog_ghost", (zp[0] + 150, zp[1] + 140), 315, "XL", GOG, icon="inf", alpha=int(60 + 150 * fade))
        E.label(cv, "l_zp", "주필산 15만", (zp[0] + 150, zp[1] + 240), size=38)
    E.fort(cv, "f_ansi", an)
    E.label(cv, "l_ansi", "안시성", (an[0], an[1] + 78), size=44)
    for i, ((x, y), a) in enumerate(WIDE_TANG):
        E.unit(cv, f"u_tang{i}", (x, y), a, "XL", TANG, icon="cav")
    if u >= st(2, 1):
        g = E.ease(E.ramp(u, st(2, 1), st(2, 1) + 1.2))
        E.arrow(cv, "a_pyong", [(an[0] + 60, an[1] + 60), (560, 1110), (850, 1200)], E.GOLD, wid=22, upto=g, dashed=True)
        if g > .9:
            E.label(cv, "l_py", "평양 방향", (700, 1150), size=36)
        pulse = .5 + .5 * math.sin(u * 6)
        k = E.K()
        cv.d.rectangle([(an[0] - 70) * k, (an[1] - 70) * k, (an[0] + 70) * k, (an[1] + 70) * k], outline=(255, 214, 90), width=int((6 + 4 * pulse) * k))
        cv.add("box_ansi", "effect", [an[0] - 74, an[1] - 74, 148, 148])
    return cv, dict(z=E.lerp(1.05, 1.0, u / TL[2]["dur"]), cx=500, cy=880)


def s3(u):
    cv = E.world(base("wide"), "s3")
    an, og, ga, sx = W_("안시성"), W_("오골성"), W_("건안성"), W_("신성")
    for nm, xy, kind, lxy in (("ansi", an, "sanseong", (an[0], an[1] + 78)), ("ogol", og, "sanseong", (og[0] - 10, og[1] - 80)),
                              ("gunan", ga, "sanseong", (ga[0] + 20, ga[1] + 78)), ("sin", sx, "sanseong", (sx[0], sx[1] + 78))):
        E.fort(cv, "f_" + nm, xy, kind)
    E.label(cv, "l_ansi", "안시성", (an[0], an[1] + 78), size=44)
    E.label(cv, "l_ogol", "오골성", (og[0] - 10, og[1] - 80), size=40)
    E.label(cv, "l_gunan", "건안성", (ga[0], ga[1] - 74), size=36)
    E.label(cv, "l_sin", "신성", (sx[0], sx[1] + 78), size=40)
    b1, b2 = WIDE_TANG[0][0], WIDE_TANG[1][0]
    E.unit(cv, "u_tang0", b1, 270, "XL", TANG, icon="cav")
    E.unit(cv, "u_tang1", b2, 270, "XL", TANG, icon="cav")
    # 빠른 길(금 점선): 안시성 → 오골성 → 평양 쪽
    g = E.ease(E.ramp(u, st(3, 1), st(3, 1) + 1.4))
    route = [(b2[0] + 70, b2[1] + 60), (640, 1060), (og[0] - 50, og[1] - 10), (860, 1205)]
    E.arrow(cv, "a_fast", route, E.GOLD, wid=22, upto=g, dashed=True)
    if g > .5:
        E.label(cv, "l_fast", "빠른 길", (600, 1010), size=36)
    if u < st(3, 2):
        E.bubble(cv, "b_go", b1, "늙은 장수부터 치시지요", dx=140, dy=-150)
    else:
        E.bubble(cv, "b_jang", b1, "천자는 요행을 바라지 않습니다", dx=140, dy=-150)
        if u > st(3, 2) + .6:
            E.cross(cv, "x_fast", (700, 1100))
        E.label(cv, "l_safe", "안전한 길", (an[0] + 10, an[1] - 96), size=36)
    if u >= st(3, 4):
        a = E.ease(E.ramp(u, st(3, 4), st(3, 4) + .6))
        E.unit(cv, "u_gog_sin", (sx[0] - 168, sx[1] + 70), 180, "L", GOG, icon="inf", alpha=int(255 * a))
        E.unit(cv, "u_gog_gunan", (ga[0] + 153, ga[1] + 46), 0, "L", GOG, icon="inf", alpha=int(255 * a))
        h = E.ease(E.ramp(u, st(3, 4) + .5, st(3, 4) + 1.6))
        E.arrow(cv, "a_sin", [(sx[0] - 100, sx[1] + 130), (720, 760), (680, 1030)], E.UNIT["goguryeo"], wid=18, upto=h, dashed=True)
        E.arrow(cv, "a_gunan", [(ga[0] + 250, ga[1] + 40), (420, 1150), (560, 1110)], E.UNIT["goguryeo"], wid=18, upto=h, dashed=True)
        E.bignum(cv, "n_10", "10만", (300, 480), size=90, scale=E.popf(u - st(3, 4) - .3))
    return cv, dict(z=E.lerp(1.0, 1.04, u / TL[3]["dur"]), cx=E.lerp(500, 560, u / TL[3]["dur"]), cy=900)


SIEGE = [((330, 800), 90), ((560, 450), 180), ((770, 820), 270)]


def siege_blocks(cv, face=None, shift=0.0, alpha=255):
    for i, ((x, y), a) in enumerate(SIEGE):
        E.unit(cv, f"u_tang{i}", (x + shift, y), face if face is not None else a, "L", TANG, icon="cav", alpha=alpha)


def ansi_region(cv, lab=True):
    an = R_("안시성")
    E.fort(cv, "f_ansi", an)
    if lab:
        E.label(cv, "l_ansi", "안시성", (an[0], an[1] + 84), size=44)
    return an


def s4(u):
    cv = E.world(base("region"), "s4")
    an = ansi_region(cv)
    g = E.ease(E.ramp(u, ZOOM_S, ZOOM_S + 1.0))
    for i, ((x, y), a) in enumerate(SIEGE):
        dx, dy = (x - an[0]) * .6 * (1 - g), (y - an[1]) * .6 * (1 - g)
        E.unit(cv, f"u_tang{i}", (x + dx, y + dy), a, "L", TANG, icon="cav")
    if u >= st(4, 1):
        E.label(cv, "l_cost", "안전한 길의 값", (540, 1060), size=40)
    if u >= st(4, 2):
        E.bignum(cv, "n_time", "시간", (540, 1160), size=96, scale=E.popf(u - st(4, 2)))
    return cv, dict(z=E.lerp(1.0, 1.03, E.ramp(u, ZOOM_S, TL[4]["dur"])), cx=540, cy=820)


def s5(u):
    cv = E.world(base("region"), "s5")
    an = ansi_region(cv)
    # 낮·밤 바뀜(되풀이)
    E.tint(cv, (20, 30, 70), 70 * (.5 - .5 * math.cos(u * 2 * math.pi / 3.0)))
    siege_blocks(cv)
    # 화살이 성벽에 닿고 튕김(3초 주기)
    ph = (u % 3.0) / 3.0
    for i, ((x, y), _) in enumerate(SIEGE):
        tx, ty = an[0] + (x - an[0]) * .45, an[1] + (y - an[1]) * .45
        if ph < .45:
            E.arrow(cv, f"a_hit{i}", [(x + (an[0] - x) * .25, y + (an[1] - y) * .25), (tx, ty)], (200, 200, 205), wid=12, upto=ph / .45, register=False)
        elif ph < .7:
            bx, by = tx + (x - an[0]) * .12, ty + (y - an[1]) * .12
            E.arrow(cv, f"a_bnc{i}", [(tx, ty), (bx + 14, by - 14)], (200, 200, 205), wid=10, upto=1, head=False, register=False)
    E.lord(cv, "lord", (an[0], an[1] - 96))
    if st(5, 2) <= u < st(5, 3) + .4:
        E.bubble(cv, "b_threat", SIEGE[0][0], "성을 빼앗으면 남자는 모두 묻겠다", dx=170, dy=-210, size=34)
        g = E.ramp(u, st(5, 2) + 1.2, st(5, 2) + 1.8)
        if g > 0:
            k = E.K()
            r = 76 + 6 * math.sin(u * 8)
            cv.d.ellipse([(an[0] - r) * k, (an[1] - r) * k, (an[0] + r) * k, (an[1] + r) * k], outline=E.GOLD, width=int(12 * g * k) + 1)
            cv.add("ring", "effect", [an[0] - r - 6, an[1] - r - 6, 2 * r + 12, 2 * r + 12])
    if u >= st(5, 3):
        w = ["하루", "열흘", "한 달"][min(2, int((u - st(5, 3)) / 1.6))]
        E.bignum(cv, "n_day", w, (540, 1150), size=96)
    return cv, dict(z=E.lerp(1.03, 1.0, u / TL[5]["dur"]), cx=540, cy=820)


def section_state(n, u):
    """6·7장면 흙산 단면 상태."""
    if n == 6:
        gm = E.ramp(u, st(6, 2), TL[6]["dur"])
        gw = E.ramp(u, st(6, 3), TL[6]["dur"])
        return dict(mound_h=E.lerp(40, 360, gm), wall_h=E.lerp(260, 330, gw), collapse=0, crack=0, owner=None)
    c = E.ease(E.ramp(u, 0.2, 1.0))
    cr = E.ramp(u, st(7, 1), st(7, 1) + .8)
    own = E.ramp(u, st(7, 8), st(7, 8) + 1.0)
    col = tuple(int(a + (b - a) * own) for a, b in zip((150, 112, 70), (150, 146, 136)))
    return dict(mound_h=360, wall_h=330, collapse=c, crack=cr, owner=col if own > 0 else None)


def s6(u):
    cv = E.plain("s6")
    s = section_state(6, u)
    (px, py), (wx0, wx1, wt) = E.mound_section(cv, "sec", **s)
    E.label(cv, "l_title", "안시성 동남쪽 (개념도)", (540, 330), size=40)
    E.label(cv, "l_mound", "흙산", (300, 1190), size=44)
    E.label(cv, "l_wall", "성벽", (710, 1190), size=44)
    if u < st(6, 1):
        ph = (u % 1.2) / 1.2
        E.arrow(cv, "a_try", [(240, 760), (E.lerp(240, wx0 - 6, ph), E.lerp(760, wt + 60, ph))], (200, 200, 205), wid=12, upto=1, register=False)
    if u >= st(6, 2):
        days = int(60 * E.ramp(u, st(6, 2), TL[6]["dur"] - .5))
        E.bignum(cv, "n_60", f"{days}일", (300, 520), size=96)
    return cv, dict(z=E.lerp(1.0, 1.05, u / TL[6]["dur"]), cx=540, cy=900)


def s7(u):
    cv = E.plain("s7")
    s = section_state(7, u)
    (px, py), (wx0, wx1, wt) = E.mound_section(cv, "sec", **s)
    E.label(cv, "l_title", "안시성 동남쪽 (개념도)", (540, 330), size=40)
    fx = {}
    if u < 1.0:
        fx["flash"] = .45 * (1 - E.ramp(u, 0.25, 0.45)) if u > .25 else 0
        fx["shake"] = E.ramp(u, .2, .3) * (1 - E.ramp(u, .6, 1.0))
    if st(7, 2) <= u < st(7, 4):
        k = E.K()
        r = 44 + 6 * math.sin(u * 9)
        cv.d.ellipse([(wx0 + 30 - r) * k, (wt + 30 - r) * k, (wx0 + 30 + r) * k, (wt + 30 + r) * k], outline=(222, 40, 34), width=8 * k)
        cv.add("gap", "effect", [wx0 + 30 - r, wt + 30 - r, 2 * r, 2 * r])
    if st(7, 3) <= u < st(7, 5) + 1.0:
        k = E.K()
        on = int(u * 3) % 2 == 0
        if on:
            cv.d.ellipse([(px - 50) * k, (py - 120) * k, (px + 50) * k, (py - 20) * k], outline=(222, 40, 34), width=8 * k)
        E.label(cv, "l_empty", "빈 자리", (px - 150, py - 110), size=40, fill=(172, 34, 28))
    if st(7, 4) <= u:
        E.lord(cv, "lord", (wx1 - 30, wt - 64))
    if st(7, 5) <= u:
        for i in range(3):
            g = E.ease(E.ramp(u, st(7, 5) + .25 * i, st(7, 5) + .25 * i + 1.2))
            sx_, sy_ = wx0 + 20, wt + 120
            tx, ty = px - 200 + i * 135, py - 34
            E.unit(cv, f"u_gog{i}", (E.lerp(sx_, tx, g), E.lerp(sy_, ty, g)), 0, "S", GOG, icon="inf")
    if st(7, 7) <= u:
        E.unit(cv, "u_tang", (150, 1040), 90, "M", TANG, icon="cav")
        ph = ((u - st(7, 7)) % 1.0)
        E.arrow(cv, "a_up", [(220, 1000), (E.lerp(220, px - 120, ph), E.lerp(1000, py + 60, ph))], E.UNIT["tang"], wid=16, upto=1, register=False)
        n = min(3, 1 + int((u - st(7, 7)) / 1.0))
        E.bignum(cv, "n_3d", ["하루", "이틀", "사흘"][n - 1], (720, 560), size=96)
        if u < st(7, 8) + .5:
            E.bubble(cv, "b_sol", (150, 990), "저 산을 다시 올라가라고?", dx=150, dy=-350, size=36)
    if st(7, 8) <= u:
        E.label(cv, "l_own", "고구려의 성벽", (px, py - 170), size=44, fill=(120, 30, 24))
    return cv, dict(z=E.lerp(1.05, 1.0, u / TL[7]["dur"]), cx=540, cy=900, **fx)


def s8(u):
    cv = E.world(base("region"), "s8")
    ansi_region(cv)
    frost = E.ramp(u, st(8, 1), st(8, 1) + 2.0)
    E.tint(cv, (236, 242, 250), 90 * frost)
    turn = E.ease(E.ramp(u, st(8, 2), st(8, 2) + 1.2))
    for i, ((x, y), a) in enumerate(SIEGE):
        E.unit(cv, f"u_tang{i}", (x, y), a + (270 - a) * turn if a != 270 else 270, "L", TANG, icon="cav")
    if u >= st(8, 1):
        f = 0.30 - 0.25 * E.ramp(u, st(8, 1), st(8, 1) + 2.0)
        E.gauge(cv, "g_food", (290, 1100), f, "군량", blink=int(u * 3) % 2 == 0)
        if f < .1:
            E.bignum(cv, "n_bot", "바닥", (720, 1120), size=80)
    return cv, dict(z=E.lerp(1.0, 1.04, u / TL[8]["dur"]), cx=540, cy=820)


RETREAT = [[(330, 800), (80, 800)], [(560, 470), (240, 420)], [(770, 820), (770, 560), (420, 300)]]


def s9(u):
    cv = E.world(base("region"), "s9")
    E.tint(cv, (236, 242, 250), 90)
    an = ansi_region(cv)
    g = E.ease(E.ramp(u, 0.0, TL[9]["dur"]))
    for i, path in enumerate(RETREAT):
        p = E._arrow_pts(path, g)[-1]
        E.unit(cv, f"u_tang{i}", p, 270 if i != 2 or g > .6 else 0, "L", TANG, icon="cav", alpha=int(255 * (1 - .4 * g)))
    E.arrow(cv, "a_back", [(an[0] - 120, an[1] + 160), (300, 1000), (40, 1000)], (130, 134, 144), wid=20, upto=E.ramp(u, 0, 2.0), dashed=True)
    bow = E.ramp(u, st(9, 0) + 1.2, st(9, 0) + 1.6) * (1 - E.ramp(u, st(9, 0) + 3.2, st(9, 0) + 3.6))
    E.lord(cv, "lord", (an[0], an[1] - 100), bow=bow)
    if st(9, 0) + .6 <= u < st(9, 0) + 4.0:
        E.dot_bow(cv, "dot_bow", (400, 770), bow)
    if u >= st(9, 1):
        E.bignum(cv, "n_silk", "비단 100필", (540, 1150), size=84, scale=E.popf(u - st(9, 1)))
    return cv, dict(z=E.lerp(1.04, 1.0, u / TL[9]["dur"]), cx=540, cy=820)


def s10(u):
    cv = E.plain("s10")
    k = E.K()
    if u < st(10, 1):
        E.label(cv, "l_noname", "이름은 기록에 없음", (540, 560), size=52)
        if u > .8:
            E.label(cv, "l_yang", "양만춘 = 후대에 전해진 이름", (540, 700), size=44, fill=(90, 84, 70))
    else:
        # 4편 상책 카드 회상(흑백) → '버티기' 금 도장
        cv.d.rounded_rectangle([200 * k, 420 * k, 880 * k, 900 * k], radius=24 * k, fill=(210, 206, 198), outline=E.INK, width=6 * k)
        E.label(cv, "l_card", "4편  15만이 두지 못한 상책", (540, 500), size=40, fill=(70, 66, 60))
        E.bignum(cv, "n_hold", "버티기", (540, 700), size=130, scale=E.popf(u - st(10, 1) - .3))
        if u >= st(10, 2):
            E.fort(cv, "f_ansi", (430, 1080))
            E.label(cv, "l_ansi", "안시성", (580, 1080), size=48)
    return cv, dict(z=E.lerp(1.0, 1.04, u / TL[10]["dur"]), cx=540, cy=880)


SCENES = {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9, 10: s10}


def note_at(n, u):
    return NOTE_SRC if (n == 10 and u > TL[10]["dur"] - 3.6) else NOTE


def compose(n, u, camera=True):
    """장면 n의 시각 u → (최종 그림 1080×1920 RGB, 레이아웃 Canvas)."""
    info = TL[n]
    k, _ = E.sentence_at(info, u)
    if n == 4 and u < ZOOM_S and camera:
        fr = zoom_frames()
        img = fr[min(len(fr) - 1, int(u * FPS))]
        cv = E.world(img, "s4z")
    else:
        w, p = SCENES[n](u)
        img = w.im.convert("RGB")
        if camera:
            z, cx = push(n, u, p.get("z", 1.0), p.get("cx", 540))
            img = E.cam(img, z, cx, p.get("cy", 960))
            img = E.shake(img, p.get("shake", 0), int(u * 60))
            img = E.flash(img, p.get("flash", 0))
            cv = E.world(img, f"s{n}")
        else:
            cv = w
    sub = info["sents"][k]
    a = E.ramp(u - info["starts"][k], 0, .12)
    E.hud(cv, TITLE, "645년", sub, sub_alpha=a, legend=LEGEND, note=note_at(n, u))
    return cv.im.convert("RGB"), cv


def push(n, u, z, cx):
    """문장마다 카메라 밀기(4편 '정지 화면 상한' 대응): 문장 길이 동안 8% 확대, 문장마다 방향(안/밖·좌/우)을 바꾼다."""
    info = TL[n]
    k, du = E.sentence_at(info, u)
    end = info["starts"][k + 1] if k + 1 < len(info["starts"]) else info["dur"]
    g = E.cl(du / max(.5, end - info["starts"][k]))
    sgn = 1 if (k + n) % 2 == 0 else -1
    zz = z * (1 + .08 * (g if sgn > 0 else 1 - g))
    return zz, cx + 30 * sgn * (g - .5)


_Z = {}


def zoom_frames():
    """3→4장면: 광역(라벨·성 없이) → 금색 박스 → 확대 → 지역. components zoom.py."""
    k = E.K()
    if k not in _Z:
        wide = base("wide").resize((E.W * k, E.H * k), Image.LANCZOS) if base("wide").size != (E.W * k, E.H * k) else base("wide")
        reg = base("region")
        # 광역↔지역 배율이 약 20배라 끝까지 확대하면 금색 박스가 화면을 덮는다 → 스킬 3절 13 '박스 중심으로 3.4배 확대 →
        # 0.55초 크로스페이드'대로 3.4배 창(안시성 중심)까지만 확대하고 지역 지도로 섞는다
        ww = MW.win()
        lon_c, lat_c = LL["안시성"]
        sp, hs = (ww.lon1 - ww.lon0) / 3.4, (ww.lat1 - ww.lat0) / 3.4
        mid = E.ZM.Win(lon_c - sp / 2, lon_c + sp / 2, lat_c - hs / 2, lat_c + hs / 2)
        _Z[k] = E.ZM.zoom_frames(wide, ww, reg, mid, fmt="shorts", fps=FPS)
    return _Z[k]


KEY = {1: lambda: TL[1]["dur"] - .2, 2: lambda: TL[2]["dur"] - .2, 3: lambda: st(3, 4) + 2.2, 4: lambda: TL[4]["dur"] - .2,
       5: lambda: st(5, 2) + 2.0, 6: lambda: TL[6]["dur"] - .2, 7: lambda: st(7, 7) + 1.2, 8: lambda: TL[8]["dur"] - .2,
       9: lambda: st(9, 0) + 1.8, 10: lambda: TL[10]["dur"] - .4}


def storyboard():
    E.set_K(2)
    out = os.path.join(HERE, "storyboard")
    os.makedirs(out, exist_ok=True)
    cvs, thumbs = [], []
    for n in sorted(SCENES):
        img, cv = compose(n, KEY[n](), camera=False)
        cv.scene_id = f"s{n:02d}"
        cvs.append(cv)
        small = img.resize((540, 960), Image.LANCZOS)
        small.save(os.path.join(out, f"s{n:02d}.png"), optimize=True)
        thumbs.append(small)
        print("storyboard", n, flush=True)
    E.CV.export_layout(cvs, os.path.join(HERE, "layout.json"), episode="battle05_ansi")
    tw, th = 270, 480
    sheet = Image.new("RGB", (tw * 5 + 6 * 8, th * 2 + 3 * 8 + 40), (24, 22, 20))
    d = ImageDraw.Draw(sheet)
    for i, t in enumerate(thumbs):
        x, y = 8 + (i % 5) * (tw + 8), 8 + (i // 5) * (th + 28)
        sheet.paste(t.resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x + 6, y + th + 4), f"장면 {i + 1}", fill=(240, 230, 210), font=E.CV.font("label", 22))
    sheet.save(os.path.join(HERE, "contact.png"), optimize=True)


def animatic():
    E.set_K(1)
    path = os.path.join(HERE, "animatic.mp4")
    wr = E.Writer(path, (540, 960), FPS, crf=27)
    n_frames = int(round(TOTAL * FPS))
    order = sorted(SCENES)
    XF = .25
    prev_last = None
    for f in range(n_frames):
        t = f / FPS
        n = max(m for m in order if TL[m]["t0"] <= t + 1e-9)
        u = t - TL[n]["t0"]
        img, _ = compose(n, u)
        if n > 1 and u < XF and not (n == 4):
            pimg, _ = compose(n - 1, TL[n - 1]["dur"] - 1 / FPS)
            img = Image.blend(pimg, img, u / XF)
        wr.add(img)
        if f % 120 == 0:
            print(f"frame {f}/{n_frames}", flush=True)
    wr.close()
    # 검사 보조 파일
    secs, cuts = [], []
    kind = {1: "wide", 2: "wide", 3: "wide", 4: "map", 5: "map", 6: "diagram", 7: "diagram", 8: "map", 9: "map", 10: "card"}
    for n in order:
        a, b = TL[n]["t0"], TL[n]["t0"] + TL[n]["dur"]
        secs.append({"start": round(a, 3), "end": round(b, 3), "profile": "battle" if n in (5, 6, 7, 8) else "explain", "scene": n})
        cuts.append({"start": round(a, 3), "end": round(b, 3), "kind": "map" if MAPS[n] != "none" else "diagram", "scene": n})
    json.dump(secs, open(os.path.join(HERE, "sections.json"), "w"), ensure_ascii=False, indent=1)
    json.dump(cuts, open(os.path.join(HERE, "cuts.json"), "w"), ensure_ascii=False, indent=1)
    json.dump({"total_s": round(TOTAL, 2), "fps": FPS, "rate": "음절/6.2초 + 0.35초(추정)",
               "scenes": {n: {"t0": round(TL[n]["t0"], 2), "dur": round(TL[n]["dur"], 2), "starts": [round(x, 2) for x in TL[n]["starts"]],
                              "sents": TL[n]["sents"]} for n in order}},
              open(os.path.join(HERE, "timing.json"), "w"), ensure_ascii=False, indent=1)
    print("done", path, round(TOTAL, 1), "s")


def check_zoom():
    sc = []
    for n in sorted(SCENES):
        win = MW.win() if MAPS[n] == "wide" else (MR.win() if MAPS[n] == "region" else None)
        sc.append({"id": f"s{n}", "map": MAPS[n], "win": win, "transition": TRANS.get(n, "xfade")})
    return E.ZM.require_zoom(sc)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "storyboard"
    v = check_zoom()
    print("require_zoom:", v or "통과")
    if v:
        sys.exit(1)
    if what in ("storyboard", "all"):
        storyboard()
    if what in ("animatic", "all"):
        animatic()
