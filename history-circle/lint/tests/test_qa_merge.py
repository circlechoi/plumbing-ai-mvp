"""qa.py에서 흡수한 항목: 확대 인식 정지, 3초 경고, 같은 화면 경고, 검은 화면, 계획에 없는 컷, 실사 스틸, 무음, 남은 태그·금지 기호, 발음(건너뜀)."""
import json
import os
import tempfile
import unittest

import numpy as np
from PIL import Image

from synth import pan_clip, silence, texture, tone, write_video, write_wav

import audio_asr
import audio_silence
import src_text
import video_static

W, H, FPS = 640, 360, 24


def zoom_clip(tex, sec, rate=0.06 / 8):
    """liven.py처럼 8초에 6% 천천히 확대."""
    im = Image.fromarray(tex)
    out = []
    for i in range(int(sec * FPS)):
        z = 1 + rate * i / FPS
        bw, bh = W / z, H / z
        x0, y0 = (W - bw) / 2, (H - bh) / 2
        out.append(np.asarray(im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + bw, y0 + bh))))
    return np.array(out, np.uint8)


class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="hclint_q_")
        cls.tex = texture(H, W, 5)
        cls.big = texture(700, 1600, 12)

    def p(self, n):
        return os.path.join(self.d, n)

    def still(self, sec, tex=None):
        t = self.tex if tex is None else tex
        return np.repeat(t[None], int(sec * FPS), axis=0)

    def moving(self, sec):
        return pan_clip(self.big, int(sec * FPS), W, H, 2, 0)

    def test_slow_zoom_is_not_static(self):
        write_video(self.p("z.mp4"), zoom_clip(self.tex, 9), FPS)
        self.assertTrue(video_static.check(self.p("z.mp4"), "explain")["ok"])
        r = video_static.check(self.p("z.mp4"), "explain", zoom_aware=False)  # qa.py 방식이면 정지로 잡힘
        self.assertFalse(r["ok"])

    def test_static_warn_3s_and_low_motion(self):
        write_video(self.p("w.mp4"), np.concatenate([self.moving(1), self.still(4), self.moving(1)]), FPS)
        r = video_static.check(self.p("w.mp4"), "explain")
        self.assertTrue(r["ok"], r)
        self.assertTrue(any("3초+" in w["what"] for w in r["warnings"]), r["warnings"])
        write_video(self.p("lm.mp4"), zoom_clip(self.tex, 7.5), FPS)  # 확대는 정지는 아니지만 움직임은 매우 적음
        r = video_static.check(self.p("lm.mp4"), "explain")
        self.assertTrue(r["ok"])
        self.assertTrue(any("움직임 매우 적음" in w["what"] for w in r["warnings"]), r["warnings"])

    def test_black_screen(self):
        black = np.zeros((int(1.5 * FPS), H, W), np.uint8)
        write_video(self.p("b.mp4"), np.concatenate([self.moving(2), black, self.moving(2)]), FPS)
        r = video_static.check(self.p("b.mp4"), "battle")
        self.assertTrue(any(v["what"] == "검은 화면" for v in r["violations"]), r)
        write_video(self.p("b_end.mp4"), np.concatenate([self.moving(3), black[: int(0.9 * FPS)]]), FPS)
        r = video_static.check(self.p("b_end.mp4"), "battle")
        self.assertFalse(any(v["what"] == "검은 화면" for v in r["violations"]))
        self.assertTrue(any("페이드" in w["what"] for w in r["warnings"]))

    def test_unplanned_cut_and_live_still(self):
        a = self.moving(2)
        b = pan_clip(texture(700, 1600, 99), int(2 * FPS), W, H, 2, 0)
        write_video(self.p("c.mp4"), np.concatenate([a, b]), FPS)
        json.dump([{"start": 0, "end": 4}], open(self.p("plan.json"), "w"))
        r = video_static.check(self.p("c.mp4"), "explain", cuts_path=self.p("plan.json"))
        self.assertTrue(any(w["what"] == "계획에 없는 컷/튐" for w in r["warnings"]), r["warnings"])
        json.dump([{"start": 0, "end": 2}, {"start": 2, "end": 4}], open(self.p("plan2.json"), "w"))
        r = video_static.check(self.p("c.mp4"), "explain", cuts_path=self.p("plan2.json"))
        self.assertFalse(any(w["what"] == "계획에 없는 컷/튐" for w in r["warnings"]))
        write_video(self.p("live.mp4"), np.concatenate([self.moving(1), self.still(2.5)]), FPS)
        json.dump([{"start": 0, "end": 3.5, "kind": "live"}], open(self.p("live.json"), "w"))
        r = video_static.check(self.p("live.mp4"), "explain", cuts_path=self.p("live.json"))
        self.assertTrue(any("실사" in v["what"] for v in r["violations"]), r)

    def test_silence(self):
        write_wav(self.p("s_ok.wav"), np.concatenate([tone(2, -20), silence(2.0), tone(2, -20)]))
        self.assertTrue(audio_silence.check(self.p("s_ok.wav"))["ok"])
        write_wav(self.p("s_warn.wav"), np.concatenate([tone(2, -20), silence(2.7), tone(2, -20)]))
        r = audio_silence.check(self.p("s_warn.wav"))
        self.assertTrue(r["ok"])
        self.assertEqual(len(r["warnings"]), 1)
        write_wav(self.p("s_bad.wav"), np.concatenate([tone(2, -20), silence(3.4), tone(2, -20)]))
        self.assertFalse(audio_silence.check(self.p("s_bad.wav"))["ok"])

    def test_src_text(self):
        src = os.path.join(self.d, "src")
        os.makedirs(src, exist_ok=True)
        good = os.path.join(src, "ok.py")
        open(good, "w").write('# [통설] 주석은 괜찮다\n"""독스트링 · 도 괜찮다"""\nlabel = "북쪽 산, 태종"\n')
        self.assertTrue(src_text.check([src])["ok"])
        open(os.path.join(src, "bad.py"), "w").write("chip_txt = '[통설] 기록에 없음'\nlabel = '북쪽 산 · 태종'\n")
        r = src_text.check([src])
        whats = sorted(v["what"] for v in r["violations"])
        self.assertEqual(whats, ["금지 기호", "남은 태그"], r)
        open(os.path.join(src, "caps.json"), "w").write('{"t": "(해석) 이렇게 읽힌다"}')
        r = src_text.check([os.path.join(src, "caps.json")])
        self.assertFalse(r["ok"])

    def test_asr_skips_without_whisper(self):
        try:
            import faster_whisper  # noqa: F401
            self.skipTest("faster-whisper 있음 — 건너뜀 경로 시험 불가")
        except ImportError:
            pass
        write_wav(self.p("a.wav"), tone(1, -20))
        r = audio_asr.check(self.p("a.wav"))
        self.assertTrue(r["ok"])
        self.assertTrue(r["metrics"]["skipped"])


if __name__ == "__main__":
    unittest.main()
