"""스타일 키트 v1 시험: 장면 2·6·7을 키트(style.json)로 다시 그려 1080×1920 PNG + layout.json.
사용: python3 kit_trial.py [장면 번호 ...]  (기본 2 6 7)"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B  # noqa: E402

E = B.E
out = os.path.join(HERE, "kit_trial")
os.makedirs(out, exist_ok=True)
E.set_K(2)
scenes = [int(a) for a in sys.argv[1:]] or [2, 6, 7]
cvs = []
for n in scenes:
    u = B.KEY[n]()
    img, cv = B.compose(n, u, camera=False)
    cv.scene_id = f"s{n:02d}"
    cvs.append(cv)
    k, _ = E.sentence_at(B.TL[n], u)
    sub = B.TL[n]["sents"][k]
    img.resize((1080, 1920), E.Image.LANCZOS).save(os.path.join(out, f"s{n:02d}.png"))
    open(os.path.join(out, f"s{n:02d}.caption.txt"), "w", encoding="utf-8").write(sub)
    print("ok", n, round(u, 2), sub, flush=True)
E.CV.export_layout(cvs, os.path.join(out, "layout.json"), episode="battle05_ansi")
