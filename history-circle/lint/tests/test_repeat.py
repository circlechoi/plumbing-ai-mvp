import json
import os
import tempfile
import unittest

import numpy as np

from synth import pan_clip, texture, write_video

import video_repeat

W, H, FPS = 640, 360, 24


class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="hclint_rep_")
        cls.t = [texture(700, 1600, s) for s in (41, 42, 43, 44, 45)]

    def p(self, n):
        return os.path.join(self.d, n)

    def clip(self, k, sec=1.5):
        return pan_clip(self.t[k], int(sec * FPS), W, H, 2, 0)

    def test_same_cut_repeat(self):
        A = self.clip(0)
        seq = [A, self.clip(1), A, self.clip(2), A, self.clip(3)]
        write_video(self.p("rep.mp4"), np.concatenate(seq), FPS)
        r = video_repeat.check(self.p("rep.mp4"))
        self.assertFalse(r["ok"], r["metrics"])
        v = [x for x in r["violations"] if x["what"] == "같은 컷 반복"]
        self.assertEqual(len(v), 1)
        self.assertEqual(v[0]["uses"], 3)
        write_video(self.p("norep.mp4"), np.concatenate([self.clip(k) for k in range(5)]), FPS)
        r = video_repeat.check(self.p("norep.mp4"))
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["warnings"], [])

    def test_map_cuts_excluded(self):
        A = self.clip(0)
        seq = [A, self.clip(1), A, self.clip(2), A]
        write_video(self.p("map.mp4"), np.concatenate(seq), FPS)
        plan = [{"start": i * 1.5, "end": (i + 1) * 1.5, "kind": "map" if i % 2 == 0 else "live"} for i in range(5)]
        json.dump(plan, open(self.p("cuts.json"), "w"))
        self.assertTrue(video_repeat.check(self.p("map.mp4"), self.p("cuts.json"))["ok"])

    def test_stretch(self):
        base = pan_clip(self.t[4], int(2 * FPS), W, H, 3, 0)
        write_video(self.p("st0.mp4"), base, FPS)
        r = video_repeat.check(self.p("st0.mp4"))
        self.assertTrue(r["ok"], r)
        x3 = np.repeat(base[: int(len(base) / 3) + 1], 3, axis=0)  # 3배 늘림(프레임 복제)
        write_video(self.p("st3.mp4"), x3, FPS)
        r = video_repeat.check(self.p("st3.mp4"))
        self.assertTrue(any("늘림" in v["what"] for v in r["violations"]), r)
        idx = (np.arange(int(len(base) * 1.4)) / 1.4).astype(int)  # 0.7배속(≈1.43배) — 허용
        write_video(self.p("st07.mp4"), base[idx], FPS)
        r = video_repeat.check(self.p("st07.mp4"))
        self.assertTrue(r["ok"], r)


if __name__ == "__main__":
    unittest.main()
