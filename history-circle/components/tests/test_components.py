"""컴포넌트 테스트: 등급 크기 고정·면적 단조, 레이아웃 → lint 판정, require_zoom, 줌 프레임, 요새 크기·허용, 금지 글자."""
import json
import os
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "lint"))

import layout_overlap  # noqa: E402
from canvas import Canvas, MissingGlyph, export_layout, resolve_overlap  # noqa: E402
from forts import FH, FW, NotAllowed, draw_fort  # noqa: E402
from units import ORDER, draw_unit, grade_dims, grade_for, unit_bbox  # noqa: E402
from zoom import Win, require_zoom, zoom_frames  # noqa: E402


def drawn_size(fn):
    """빈 판에 하나만 그리고 실제 칠해진 픽셀 범위(w, h)."""
    cv = Canvas("shorts", bg=(255, 255, 255), scene_id="t")
    fn(cv)
    a = np.asarray(cv.im.resize((cv.W, cv.H), Image.NEAREST).convert("RGB")).astype(int)
    m = np.any(np.abs(a - 255) > 30, axis=2)
    ys, xs = np.where(m)
    return xs.max() - xs.min() + 1, ys.max() - ys.min() + 1


class T(unittest.TestCase):
    def test_same_grade_same_pixels(self):
        for g in ORDER:
            sizes = {drawn_size(lambda cv, f=f: draw_unit(cv, "u", (540, 900), 0, g, f, icon=None))
                     for f in ("goguryeo", "tang", "malgal")}
            self.assertEqual(len(sizes), 1, (g, sizes))

    def test_area_monotonic_and_grade_for(self):
        areas = [grade_dims(g)[0] * grade_dims(g)[1] for g in ORDER]
        self.assertEqual(areas, sorted(areas))
        self.assertEqual(len(set(areas)), len(areas))
        seq = [grade_for(t) for t in (100, 4999, 5000, 14999, 15000, 39999, 40000, 300000)]
        self.assertEqual([ORDER.index(g) for g in seq], sorted(ORDER.index(g) for g in seq))

    def test_forts_same_size(self):
        cv = Canvas("shorts")
        els = [draw_fort(cv, k, (200 + i * 300, 700), k) for i, k in enumerate(("sanseong", "pyeongji", "mokchaek"))]
        self.assertEqual(len({tuple(e["bbox"][2:]) for e in els}), 1)
        self.assertEqual(els[0]["bbox"][2], FW + 5)

    def test_fort_longform_blocked(self):
        cv = Canvas("longform")
        with self.assertRaises(NotAllowed):
            draw_fort(cv, "f", (900, 500), "pyeongji")

    def test_missing_glyph(self):
        cv = Canvas("shorts")
        with self.assertRaises(MissingGlyph):
            cv.label("x", "북쪽 산 · 태종", (500, 700))
        cv.label("ok", "북쪽 산 태종", (500, 700))

    def _lint(self, cv):
        p = os.path.join(tempfile.mkdtemp(), "layout.json")
        export_layout([cv], p)
        return layout_overlap.check([p])

    def test_layout_pass(self):
        cv = Canvas("shorts")
        for i, (g, x) in enumerate(zip(ORDER, (150, 330, 530, 750))):
            draw_unit(cv, f"u{i}", (x, 800), 0, g, "goguryeo")
        draw_unit(cv, "u_m2", (200, 1050), 90, "M", "tang")  # 90도 회전도 같은 등급 면적
        draw_unit(cv, "u_rot", (600, 1080), -40, "M", "tang")
        r = self._lint(cv)
        self.assertTrue(r["ok"], r["violations"])
        sc = r["metrics"][next(iter(r["metrics"]))]["size_classes"]
        self.assertEqual(sc["M"]["n"], 2)
        self.assertEqual(sc["M"]["max_dev_pct"], 0.0)

    def test_layout_overlap_fail(self):
        cv = Canvas("shorts")
        draw_unit(cv, "a", (400, 800), 0, "M", "goguryeo")
        draw_unit(cv, "b", (450, 820), 0, "M", "tang")
        r = self._lint(cv)
        self.assertFalse(r["ok"])
        self.assertTrue(any(v["what"] == "요소 겹침" for v in r["violations"]))

    def test_layout_forbidden_fail(self):
        cv = Canvas("shorts")
        draw_unit(cv, "a", (540, 1400), 0, "M", "goguryeo")  # 자막띠
        draw_unit(cv, "b", (980, 700), 0, "M", "tang")  # 오른쪽 x>900
        r = self._lint(cv)
        zones = {v.get("zone") for v in r["violations"] if v["what"] == "금지 영역 침범"}
        self.assertEqual(zones, {"subtitle_band", "right_ui"})

    def test_resolve_overlap(self):
        b = {"a": unit_bbox((400, 800), 0, "M"), "b": unit_bbox((450, 820), 0, "M"), "f": [380, 900, 100, 100]}
        nb, left = resolve_overlap(b, fixed={"f"}, gap=6)
        self.assertEqual(left, 0)
        self.assertEqual(nb["f"], b["f"])

    def test_require_zoom(self):
        wide, reg = (121.6, 124.2, 40.0, 42.0), (122.745, 122.925, 40.69, 40.80)
        bad = [{"id": "s1", "map": "wide", "win": wide}, {"id": "s2", "map": "region", "win": reg, "transition": "cut"}]
        v = require_zoom(bad)
        self.assertTrue(any("줌 없음" in x["what"] for x in v))
        self.assertTrue(any("한 프레임 컷" in x["what"] for x in v))
        good = [{"id": "s1", "map": "wide", "win": wide}, {"id": "s2", "map": "region", "win": reg, "transition": "zoom"},
                {"id": "s3", "map": "region", "win": (122.75, 122.92, 40.69, 40.80), "transition": "cut"}]
        self.assertEqual(require_zoom(good), [])

    def test_zoom_frames(self):
        W, H = 108, 192
        wide = Image.new("RGB", (W, H), (200, 180, 140))
        reg = Image.new("RGB", (W, H), (40, 120, 60))
        ww = Win(121.6, 124.2, 40.0, 42.0)
        rw = Win(122.8, 123.1, 40.6, 41.1)
        for fmt, n in (("shorts", int(.4 * 24) + int(1.15 * 24) + int(.55 * 24)), ("longform", int(.55 * 24) + int(.45 * 24))):
            fr = zoom_frames(wide, ww, reg, rw, fmt=fmt)
            self.assertEqual(len(fr), n)
            self.assertEqual(fr[-1].getpixel((0, 0)), (40, 120, 60))

    def test_zoom_max_scale(self):
        """쇼츠 확대는 max_scale(4편 3.4배)을 넘지 않는다 — 11/05 안시성 편 약 20배 문제."""
        import zoom as Zm
        seen = []
        orig = Zm._crop

        def spy(img, cx, cy, s, out_wh):
            seen.append(s)
            return orig(img, cx, cy, s, out_wh)
        Zm._crop = spy
        try:
            W, H = 108, 192
            wide = Image.new("RGB", (W, H), (200, 180, 140))
            reg = Image.new("RGB", (W, H), (40, 120, 60))
            ww, rw = Win(121.0, 126.0, 38.0, 43.0), Win(122.80, 122.85, 40.70, 40.79)  # 창 배율 100배 안팎
            Zm.zoom_frames(wide, ww, reg, rw, fmt="shorts")
            self.assertAlmostEqual(max(seen), 3.4, places=6)
            seen.clear()
            Zm.zoom_frames(wide, ww, reg, rw, fmt="shorts", max_scale=2.0)
            self.assertAlmostEqual(max(seen), 2.0, places=6)
            seen.clear()
            Zm.zoom_frames(wide, ww, reg, rw, fmt="longform")  # 롱폼은 같은 경위도 창 원칙 — 상한 없음
            self.assertGreater(max(seen), 3.4)
        finally:
            Zm._crop = orig

    def test_legend_band_forbidden(self):
        """맨 아래 검은 띠(1600~1920)에는 블록을 둘 수 없다(범례 배지·라벨만)."""
        cv = Canvas("shorts")
        draw_unit(cv, "a", (400, 1800), 0, "M", "goguryeo")
        r = self._lint(cv)
        zones = {v.get("zone") for v in r["violations"] if v["what"] == "금지 영역 침범"}
        self.assertIn("legend_band", zones)


if __name__ == "__main__":
    unittest.main()
