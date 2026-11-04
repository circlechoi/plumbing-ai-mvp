import json
import os
import tempfile
import unittest

import numpy as np

from synth import SR, silence, tone, write_wav, write_video, texture, pan_clip

import audio_isolated_syllable
import audio_loudness
import audio_midpause
import audio_sfx_vs_vo
from common import integrated_lufs


class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="hclint_")

    def p(self, name):
        return os.path.join(self.d, name)

    # ---- loudness ----
    def test_loudness_pass_and_fail(self):
        x = tone(8, -20)
        write_wav(self.p("probe.wav"), x)
        meas = integrated_lufs(self.p("probe.wav"))
        good = x * 10 ** ((-15 - meas) / 20)
        write_wav(self.p("loud_ok.wav"), good)
        self.assertTrue(audio_loudness.check(self.p("loud_ok.wav"))["ok"])
        quiet = x * 10 ** ((-25 - meas) / 20)
        write_wav(self.p("loud_bad.wav"), quiet)
        self.assertFalse(audio_loudness.check(self.p("loud_bad.wav"))["ok"])

    def test_loudness_on_mp4(self):
        x = tone(4, -20)
        write_wav(self.p("probe2.wav"), x)
        meas = integrated_lufs(self.p("probe2.wav"))
        a = x * 10 ** ((-15 - meas) / 20)
        frames = pan_clip(texture(200, 400, 1), 96, 160, 90, 1, 0)
        write_video(self.p("av.mp4"), frames, audio=a)
        r = audio_loudness.check(self.p("av.mp4"))
        self.assertTrue(r["ok"], r)

    # ---- 11/04 확정: 롱폼 −14 / True Peak −1.5 ----
    def test_loudness_longform_and_true_peak(self):
        x = tone(8, -20)
        write_wav(self.p("probe3.wav"), x)
        meas = integrated_lufs(self.p("probe3.wav"))
        lf = x * 10 ** ((-14 - meas) / 20)
        write_wav(self.p("lf.wav"), lf)
        self.assertTrue(audio_loudness.check(self.p("lf.wav"), "longform")["ok"])
        spike = (x * 10 ** ((-15 - meas) / 20)).copy()
        spike[1000] = 0.99  # 순간 피크 ≈ 0 dBTP
        write_wav(self.p("tp_bad.wav"), spike)
        r = audio_loudness.check(self.p("tp_bad.wav"))
        self.assertFalse(r["ok"], r)
        self.assertTrue(any(v["what"] == "True Peak 초과" for v in r["violations"]))

    def test_sfx_climax_exception(self):
        import json
        vo = tone(4, -20)
        write_wav(self.p("vo_c.wav"), vo)
        write_wav(self.p("sfx_c.wav"), tone(4, -20.5))  # 내레이션보다 0.5dB 작음: 기본(−3dB) 실패, 절정(−1dB 예외) 통과
        sec = self.p("sec.json")
        json.dump([{"start": 0, "end": 4, "kind": "climax"}], open(sec, "w"))
        self.assertFalse(audio_sfx_vs_vo.check(self.p("vo_c.wav"), self.p("sfx_c.wav"))["ok"])
        self.assertTrue(audio_sfx_vs_vo.check(self.p("vo_c.wav"), self.p("sfx_c.wav"), sec)["ok"])

    # ---- sfx vs vo ----
    def test_sfx_vs_vo(self):
        vo = np.concatenate([tone(3, -20), silence(1), tone(2, -20)])
        write_wav(self.p("vo.wav"), vo)
        write_wav(self.p("sfx_ok.wav"), np.concatenate([tone(4, -30), tone(2, -30)]))
        sfx_bad = np.concatenate([tone(1, -30), tone(1, -16), tone(4, -30)])  # 1~2초에 내레이션보다 큼
        write_wav(self.p("sfx_bad.wav"), sfx_bad)
        ok = audio_sfx_vs_vo.check(self.p("vo.wav"), self.p("sfx_ok.wav"))
        self.assertTrue(ok["ok"], ok)
        bad = audio_sfx_vs_vo.check(self.p("vo.wav"), self.p("sfx_bad.wav"))
        self.assertFalse(bad["ok"])
        self.assertTrue(all(v["end_s"] > 1.0 and v["start_s"] < 2.0 for v in bad["violations"]), bad["violations"])  # 창이 1~2초 구간과 겹치면 정상
        # 내레이션이 쉬는 3~4초 구간의 효과음은 비교하지 않는다
        loud_in_gap = np.concatenate([tone(3.2, -30), tone(0.4, -10), tone(2.4, -30)])  # 0.4초 창 경계에 맞춤(내레이션 쉼 3~4초 안)
        write_wav(self.p("sfx_gap.wav"), loud_in_gap)
        self.assertTrue(audio_sfx_vs_vo.check(self.p("vo.wav"), self.p("sfx_gap.wav"))["ok"])

    # ---- isolated syllable ----
    def test_isolated_syllable(self):
        clean = np.concatenate([silence(0.1), tone(2, -20), silence(0.2)])
        tail = np.concatenate([silence(0.1), tone(2, -20), silence(0.2), tone(0.1, -22), silence(0.05)])
        head = np.concatenate([silence(0.02), tone(0.1, -22), silence(0.2), tone(2, -20), silence(0.1)])
        long_tail = np.concatenate([silence(0.1), tone(2, -20), silence(0.2), tone(0.6, -22), silence(0.05)])
        for name, x in [("clean", clean), ("tail", tail), ("head", head), ("long_tail", long_tail)]:
            write_wav(self.p(name + ".wav"), x)
        self.assertTrue(audio_isolated_syllable.check([self.p("clean.wav")])["ok"])
        r = audio_isolated_syllable.check([self.p("tail.wav")])
        self.assertFalse(r["ok"])
        self.assertEqual(r["violations"][0]["where"], "끝")
        r = audio_isolated_syllable.check([self.p("head.wav")])
        self.assertFalse(r["ok"])
        self.assertEqual(r["violations"][0]["where"], "시작")
        # 0.6초 덩어리는 정상 단어로 본다
        self.assertTrue(audio_isolated_syllable.check([self.p("long_tail.wav")])["ok"])

    # ---- midpause ----
    def test_midpause(self):
        x = np.concatenate([tone(1.0, -20), silence(0.2), tone(1.0, -20), silence(0.3), tone(1.0, -20)])
        write_wav(self.p("mp.wav"), x)
        # 단어 시각: 첫 쉼(1.0~1.2) 앞 단어엔 문장부호 없음, 둘째 쉼(2.2~2.5) 앞은 쉼표
        bad_words = [{"word": "요동성에서", "start": 0.3, "end": 1.0}, {"word": "군량,", "start": 1.2, "end": 2.2},
                     {"word": "끝.", "start": 2.5, "end": 3.5}]
        good_words = [{"word": "요동성에서,", "start": 0.3, "end": 1.0}, {"word": "군량,", "start": 1.2, "end": 2.2},
                      {"word": "끝.", "start": 2.5, "end": 3.5}]
        json.dump(bad_words, open(self.p("bad.words.json"), "w"), ensure_ascii=False)
        json.dump({"words": good_words}, open(self.p("good.words.json"), "w"), ensure_ascii=False)
        r = audio_midpause.check(self.p("mp.wav"), self.p("bad.words.json"))
        self.assertFalse(r["ok"])
        self.assertEqual(len(r["violations"]), 1)
        self.assertEqual(r["violations"][0]["word_before"], "요동성에서")
        self.assertTrue(audio_midpause.check(self.p("mp.wav"), self.p("good.words.json"))["ok"])
        # 단어 시각 없음: 0.5초 이하 쉼은 경고만
        r = audio_midpause.check(self.p("mp.wav"))
        self.assertTrue(r["ok"])
        self.assertEqual(len(r["warnings"]), 2)
        # 0.7초 쉼은 단어 시각 없이도 실패
        write_wav(self.p("mp_long.wav"), np.concatenate([tone(1, -20), silence(0.7), tone(1, -20)]))
        self.assertFalse(audio_midpause.check(self.p("mp_long.wav"))["ok"])
        # 문장부호 뒤라도 0.5초 초과면 실패
        json.dump([{"word": "끝.", "start": 0.2, "end": 1.0}, {"word": "다음", "start": 1.7, "end": 2.0}],
                  open(self.p("long.words.json"), "w"), ensure_ascii=False)
        r = audio_midpause.check(self.p("mp_long.wav"), self.p("long.words.json"))
        self.assertFalse(r["ok"])
        self.assertIn("너무 김", r["violations"][0]["what"])


if __name__ == "__main__":
    unittest.main()
