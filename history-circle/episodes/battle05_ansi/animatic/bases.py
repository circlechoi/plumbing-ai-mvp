"""5편 지도 바탕 v4-S 두 장(광역·지역). 4편 mkb4/mkb5 값을 따름(광역 z8 thr260 강 0.9, 지역 z12 thr82 sm2)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "animatic"))
import engine as E

C = json.load(open(os.path.join(HERE, "coords.json"), encoding="utf-8"))
LL = {k: tuple(v["ll"]) for k, v in C.items() if not k.startswith("_")}
# 광역: 안시성·건안성·오골성·요동성·신성이 안전 영역(x<900, y 236~1270)에 들어오게
MW = E.Map(122.22, 124.77, 40.765)
# 지역: 안시성을 (540, 780) 근처에
MR = E.Map(122.713, 122.843, 40.7642)
OUT = os.path.join(HERE, ".cache")
os.makedirs(OUT, exist_ok=True)


def bases(kb=2):
    riv = json.load(open(os.path.join(HERE, "rivers_liao.json"), encoding="utf-8"))
    bw = E.base_v4s(MW, 8, 260, rivers=riv, river_scale=0.9, kb=kb, cache=os.path.join(OUT, f"base_w_k{kb}.png"))
    br = E.base_v4s(MR, 12, 82, sm=2, kb=kb, cache=os.path.join(OUT, f"base_r_k{kb}.png"))
    return bw, br


if __name__ == "__main__":
    bw, br = bases(2)
    for n, im in (("w", bw), ("r", br)):
        im.resize((540, 960)).save(os.path.join(OUT, f"prev_{n}.png"))
    for k, v in LL.items():
        print(k, [round(c) for c in MW.P(*v)], [round(c) for c in MR.P(*v)])
