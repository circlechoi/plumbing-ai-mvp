import os
import tempfile
import unittest

import script_lint

GOOD = """인물: 고연수, 당 태종

# 1
645년 여름, 고구려 15만 대군이 주필산 아래에 진을 칩니다.
당 태종은 군사를 셋으로 나눕니다.

# 2
고연수는 화친 제안을 당군이 지쳤다는 신호로 읽습니다.
그 판단에는 이유가 있습니다.

화면: 북쪽 산, 태종
"""

BAD = """인물: 가, 나, 다, 라, 마, 바

# 1
옛날 옛적, 요동에 큰 성이 있었답니다.
645년, 당 태종이 쳐들어왔습니다.
여기, 보시는 것처럼 강이 흐릅니다.
고구려는, 버티고, 또 버텼습니다.

이것이 첫 번째 것입니다.

두 번째 것입니다.

세 번째 것입니다.

네 번째 것입니다.

화면: 북쪽 산 · 태종
"""


class T(unittest.TestCase):
    def w(self, text):
        fd, p = tempfile.mkstemp(suffix=".txt")
        os.write(fd, text.encode("utf-8"))
        os.close(fd)
        return p

    def test_good_battle(self):
        r = script_lint.check(self.w(GOOD), "battle")
        rules = {v["rule"] for v in r["violations"]}
        # '645년 여름'으로 시작하는 문장은 연도 첫머리 → 전투 쇼츠에서는 실패
        self.assertEqual(rules, {"year_start"}, r["violations"])
        self.assertEqual(r["metrics"]["people"], 2)
        self.assertEqual(r["metrics"]["scenes"], 2)

    def test_bad_battle(self):
        r = script_lint.check(self.w(BAD), "battle")
        rules = {v["rule"] for v in r["violations"]}
        for need in ("geot_endings", "past_ss", "year_start", "commas", "people", "radio_banned",
                     "fairytale_opening", "forbidden_symbols"):
            self.assertIn(need, rules, need)
        self.assertTrue(any(w["rule"] == "fairytale_suspect" for w in r["warnings"]))

    def test_longform_allows_past(self):
        r = script_lint.check(self.w("부여는 그 길을 막았습니다.\n그것이 패착이었습니다.\n"), "longform")
        self.assertTrue(r["ok"], r)
        self.assertFalse(any(v["rule"] == "past_ss" for v in r["violations"] + r["warnings"]))
        r = script_lint.check(self.w("부여는 그 길을 막았습니다.\n"), "shorts")
        self.assertTrue(r["ok"])
        self.assertTrue(any(w["rule"] == "past_ss" for w in r["warnings"]))

    def test_present_not_past(self):
        r = script_lint.check(self.w("인물: 가\n군량이 남아 있습니다.\n곧 결전을 치르겠습니다.\n"), "battle")
        self.assertTrue(r["ok"], r)

    def test_no_people_line_warns(self):
        r = script_lint.check(self.w("당군이 다가옵니다.\n"), "battle")
        self.assertTrue(r["ok"])
        self.assertTrue(any(w["rule"] == "people" for w in r["warnings"]))


if __name__ == "__main__":
    unittest.main()
