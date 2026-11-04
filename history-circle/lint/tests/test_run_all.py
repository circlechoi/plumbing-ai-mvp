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
