import copy
import json
import os
import tempfile
import unittest

import layout_overlap

BASE = {
    "episode": "test",
    "canvas": {"w": 1080, "h": 1920},
    "forbidden": [
        {"id": "title_band", "bbox": [0, 140, 1080, 96], "allow_kinds": ["title"]},
        {"id": "subtitle_band", "bbox": [0, 1500, 1080, 200], "allow_kinds": ["subtitle"]},
    ],
    "scenes": [
        {"id": "S1", "elements": [
            {"id": "title", "kind": "title", "bbox": [40, 150, 1000, 70]},
            {"id": "sub", "kind": "subtitle", "bbox": [60, 1520, 960, 120]},
            {"id": "gog_main", "kind": "block", "size_class": "L", "bbox": [200, 700, 160, 80]},
            {"id": "tang_main", "kind": "block", "size_class": "L", "bbox": [600, 700, 160, 80]},
            {"id": "gog_label", "kind": "label", "bbox": [200, 790, 160, 40]},
            {"id": "fort", "kind": "icon", "bbox": [450, 500, 64, 64]},
            {"id": "arrow1", "kind": "arrow", "bbox": [350, 720, 260, 40]}
        ]},
        {"id": "S2", "elements": [
            {"id": "gog_main", "kind": "block", "size_class": "L", "bbox": [220, 720, 162, 80]},
            {"id": "gog_sub", "kind": "block", "size_class": "S", "bbox": [500, 900, 80, 40]}
        ]}
    ]
}


class T(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="hclint_l_")

    def run_doc(self, doc):
        p = os.path.join(self.d, "layout.json")
        json.dump(doc, open(p, "w"), ensure_ascii=False)
        return layout_overlap.check([p])

    def test_pass(self):
        r = self.run_doc(BASE)
        self.assertTrue(r["ok"], r["violations"])

    def test_overlap(self):
        d = copy.deepcopy(BASE)
        d["scenes"][0]["elements"][4]["bbox"] = [200, 760, 160, 40]  # 라벨이 블록을 덮음
        r = self.run_doc(d)
        self.assertFalse(r["ok"])
        self.assertEqual(r["violations"][0]["what"], "요소 겹침")
        # 의도한 겹침은 허용
        d["scenes"][0]["elements"][4]["allow_overlap"] = ["gog_main"]
        self.assertTrue(self.run_doc(d)["ok"])

    def test_arrow_overlap_ignored(self):
        # 화살표는 블록과 겹쳐도 이 검사 대상 아님(BASE의 arrow1이 이미 두 블록과 겹침)
        self.assertTrue(self.run_doc(BASE)["ok"])

    def test_forbidden(self):
        d = copy.deepcopy(BASE)
        d["scenes"][1]["elements"][1]["bbox"] = [500, 1480, 80, 40]  # 자막띠 침범
        r = self.run_doc(d)
        self.assertFalse(r["ok"])
        self.assertTrue(any(v["what"] == "금지 영역 침범" and v["zone"] == "subtitle_band" for v in r["violations"]))

    def test_size_variance(self):
        d = copy.deepcopy(BASE)
        d["scenes"][1]["elements"][0]["bbox"] = [220, 720, 200, 90]  # L 등급인데 40% 큼
        r = self.run_doc(d)
        self.assertFalse(r["ok"])
        self.assertTrue(any(v["what"] == "같은 등급 블록 크기 편차" for v in r["violations"]))

    def test_schema_error(self):
        d = copy.deepcopy(BASE)
        del d["scenes"][0]["elements"][2]["kind"]
        r = self.run_doc(d)
        self.assertFalse(r["ok"])
        self.assertEqual(r["violations"][0]["what"], "형식 오류")

    def test_schema_file_is_valid_json(self):
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        s = json.load(open(os.path.join(here, "schema", "layout.schema.json"), encoding="utf-8"))
        self.assertIn("element", s["definitions"])


if __name__ == "__main__":
    unittest.main()
