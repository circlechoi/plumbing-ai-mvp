import json
import os
import tempfile
import unittest

import numpy as np

from synth import pan_clip, texture, write_video

import video_pan_repeat
import video_static

W, H, FPS = 640, 360, 24


class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="hclint_v_")
        cls.texA = texture(700, 1600, 11)
        cls.texB = texture(700, 1600, 22)
        cls.texC = texture(700, 1600, 33)

    def p(self, n):
        return os.path.join(self.d, n)

    def _still(self, tex, sec):
        f = pan_clip(tex, 1, W, H, 0, 0)
        return np.repeat(f, int(sec * FPS), axis=0)

    # ---- static ----
    def test_static_explain(self):
        moving = pan_clip(self.texA, 2 * FPS, W, H, 2, 0)
        write_video(self.p("st_bad.mp4"), np.concatenate([moving, self._still(self.texB, 8), moving]), FPS)
        write_video(self.p("st_ok.mp4"), np.concatenate([moving, self._still(self.texB, 4), moving]), FPS)
        r = video_static.check(self.p("st_bad.mp4"), "explain")
        self.assertFalse(r["ok"], r["metrics"])
        self.assertAlmostEqual(r["violations"][0]["len_s"], 8, delta=0.4)
        r = video_static.check(self.p("st_ok.mp4"), "explain")
        self.assertTrue(r["ok"], r)
        # 전투 구간 프로필이면 4초 정지도 실패
        self.assertFalse(video_static.check(self.p("st_ok.mp4"), "battle")["ok"])
        # sections로 정지 구간만 전투로 지정해도 실패
        json.dump([{"start": 1.5, "end": 7, "profile": "battle"}], open(self.p("sec.json"), "w"))
        self.assertFalse(video_static.check(self.p("st_ok.mp4"), "explain", self.p("sec.json"))["ok"])

    def test_cut_length(self):
        moving = pan_clip(self.texA, 2 * FPS, W, H, 2, 0)
        write_video(self.p("cl.mp4"), moving, FPS)
        json.dump([{"id": "c1", "start": 0, "end": 4.0, "kind": "person"},
                   {"id": "c2", "start": 4.0, "end": 9.0, "kind": "wide"}], open(self.p("cuts_bad.json"), "w"))
        r = video_static.check(self.p("cl.mp4"), cuts_path=self.p("cuts_bad.json"))
        self.assertFalse(r["ok"])
        self.assertEqual([v["id"] for v in r["violations"]], ["c1"])

    # ---- pan direction ----
    def test_phase_shift_sign(self):
        a = texture(90, 160, 5).astype(np.float32)
        b = np.roll(a, 4, axis=1)  # 내용이 오른쪽으로 4px
        dx, dy = video_pan_repeat.phase_shift(a, b)
        self.assertAlmostEqual(dx, 4, delta=0.3)
        self.assertAlmostEqual(dy, 0, delta=0.3)

    def test_pan_repeat(self):
        n = 2 * FPS
        c1 = pan_clip(self.texA, n, W, H, 3, 0)    # 창이 오른쪽 → 내용은 왼쪽
        c2_same = pan_clip(self.texB, n, W, H, 3, 0)
        c2_opp = pan_clip(self.texB, n, W, H, -3, 0)
        c3_up = pan_clip(self.texC, n, W, H, 0, 3)
        write_video(self.p("pan_bad.mp4"), np.concatenate([c1, c2_same]), FPS)
        write_video(self.p("pan_ok.mp4"), np.concatenate([c1, c2_opp, c3_up]), FPS)
        r = video_pan_repeat.check(self.p("pan_bad.mp4"))
        dirs = [c["dir"] for c in r["metrics"]["cuts"]]
        self.assertEqual(dirs, ["left", "left"], r["metrics"])
        self.assertFalse(r["ok"])
        r = video_pan_repeat.check(self.p("pan_ok.mp4"))
        dirs = [c["dir"] for c in r["metrics"]["cuts"]]
        self.assertEqual(dirs, ["left", "right", "up"], r["metrics"])
        self.assertTrue(r["ok"])

    def test_still_cuts_are_none(self):
        write_video(self.p("pan_still.mp4"), np.concatenate([self._still(self.texA, 2), self._still(self.texB, 2)]), FPS)
        r = video_pan_repeat.check(self.p("pan_still.mp4"))
        self.assertTrue(r["ok"])
        self.assertEqual([c["dir"] for c in r["metrics"]["cuts"]], ["none", "none"])


if __name__ == "__main__":
    unittest.main()
