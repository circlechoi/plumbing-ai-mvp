import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

import numpy as np

from synth import silence, tone, write_wav
from test_layout import BASE

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class T(unittest.TestCase):
    def test_folder(self):
        d = tempfile.mkdtemp(prefix="hclint_r_")
        os.makedirs(os.path.join(d, "scenes"))
        write_wav(os.path.join(d, "vo.wav"), tone(3, -20))
        write_wav(os.path.join(d, "sfx.wav"), tone(3, -32))
        write_wav(os.path.join(d, "scenes", "s01.wav"), np.concatenate([silence(0.1), tone(2, -20), silence(0.2)]))
        json.dump(BASE, open(os.path.join(d, "layout.json"), "w"), ensure_ascii=False)
        p = subprocess.run([sys.executable, os.path.join(HERE, "run_all.py"), d, "--json", os.path.join(d, "o.json")],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        checks = {r["check"] for r in json.load(open(os.path.join(d, "o.json")))}
        self.assertEqual(checks, {"audio_sfx_vs_vo", "audio_isolated_syllable", "audio_midpause", "layout_overlap"})
        # 고립 음절 넣으면 실패
        write_wav(os.path.join(d, "scenes", "s02.wav"),
                  np.concatenate([silence(0.1), tone(2, -20), silence(0.2), tone(0.1, -22), silence(0.05)]))
        p = subprocess.run([sys.executable, os.path.join(HERE, "run_all.py"), d],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(p.returncode, 1, p.stdout)
        self.assertIn("실패", p.stdout)
        shutil.rmtree(d)

    def test_folder_video_script_src(self):
        from synth import pan_clip, texture, write_video
        d = tempfile.mkdtemp(prefix="hclint_r2_")
        frames = np.concatenate([pan_clip(texture(700, 1600, s), 36, 320, 180, dx, dy)
                                 for s, dx, dy in ((1, 2, 0), (2, 0, 2), (3, -2, 0))])  # 컷마다 방향을 바꿈
        x = tone(4.5, -20)
        from common import integrated_lufs
        write_wav(os.path.join(d, "probe.wav"), x)
        x = x * 10 ** ((-15 - integrated_lufs(os.path.join(d, "probe.wav"))) / 20)
        os.remove(os.path.join(d, "probe.wav"))
        write_video(os.path.join(d, "final.mp4"), frames, 24, audio=x)
        open(os.path.join(d, "script.txt"), "w").write("인물: 가\n당군이 다가옵니다.\n")
        os.makedirs(os.path.join(d, "src"))
        open(os.path.join(d, "src", "r.py"), "w").write("label = '북쪽 산'\n")
        out = os.path.join(d, "o.json")
        p = subprocess.run([sys.executable, os.path.join(HERE, "run_all.py"), d, "--json", out],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        res = {r["check"]: r for r in json.load(open(out))}
        self.assertEqual(set(res), {"audio_loudness", "audio_silence", "video_static", "video_pan_repeat",
                                    "video_repeat", "script_lint", "src_text"})
        self.assertEqual(p.returncode, 0, p.stdout + json.dumps({k: v["violations"] for k, v in res.items()},
                                                               ensure_ascii=False))
        open(os.path.join(d, "src", "r.py"), "a").write("tag = '[통설] 남은 태그'\n")
        p = subprocess.run([sys.executable, os.path.join(HERE, "run_all.py"), d],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(p.returncode, 1, p.stdout)
        shutil.rmtree(d)

    def test_cli_exit_code(self):
        d = tempfile.mkdtemp(prefix="hclint_c_")
        write_wav(os.path.join(d, "x.wav"), np.concatenate([tone(1, -20), silence(0.7), tone(1, -20)]))
        p = subprocess.run([sys.executable, os.path.join(HERE, "audio_midpause.py"), os.path.join(d, "x.wav")],
                           stdout=subprocess.PIPE, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertFalse(json.loads(p.stdout)["ok"])
        shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
