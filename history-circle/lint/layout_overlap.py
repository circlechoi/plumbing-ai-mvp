"""지도·도식 레이아웃 검사: 요소 겹침, 금지 영역 침범, 같은 등급 블록 크기 편차.

사용: python3 layout_overlap.py layout.json [layout2.json ...]
입력 형식: schema/layout.schema.json (지도 컴포넌트가 장면마다 내보냄)
 - block·label·icon·badge끼리 겹치면 실패(allow_overlap으로 의도한 겹침은 허용)
 - forbidden 영역(자막띠·제목띠)에 들어가면 실패(allow_kinds 제외)
 - 같은 size_class 블록의 면적이 전체 중앙값에서 ±size_class_max_dev를 넘으면 실패(파일 전체·전 장면 기준)
근거: history-battle-shorts:94·98(겹침 금지), :71(자막띠 피하기), 사용자 지적 '박스 크기 불균일'
"""
import argparse
from collections import defaultdict

import numpy as np

from common import emit, load_json, result, th

CHECK = "layout_overlap"
KINDS = {"block", "label", "icon", "badge", "arrow", "effect", "subtitle", "title", "other"}


def validate(doc):
    """jsonschema 없이 필수 항목만 점검."""
    errs = []
    if not isinstance(doc, dict):
        return ["최상위가 객체가 아님"]
    for k in ("canvas", "scenes"):
        if k not in doc:
            errs.append("필수 키 없음: " + k)
    for z in doc.get("forbidden", []):
        if len(z.get("bbox", [])) != 4:
            errs.append("forbidden bbox 형식 오류: %s" % z.get("id"))
    for sc in doc.get("scenes", []):
        for el in sc.get("elements", []):
            if not {"id", "kind", "bbox"} <= set(el):
                errs.append("요소 필수 키 없음: %s/%s" % (sc.get("id"), el.get("id")))
            elif el["kind"] not in KINDS:
                errs.append("알 수 없는 kind: %s/%s=%s" % (sc.get("id"), el["id"], el["kind"]))
            elif len(el["bbox"]) != 4 or el["bbox"][2] <= 0 or el["bbox"][3] <= 0:
                errs.append("bbox 형식 오류: %s/%s" % (sc.get("id"), el["id"]))
    return errs


def inter(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    w = min(ax + aw, bx + bw) - max(ax, bx)
    h = min(ay + ah, by + bh) - max(ay, by)
    return (w, h) if w > 0 and h > 0 else (0, 0)


def check_doc(doc, name):
    tol = th(CHECK, "overlap_tolerance_px")
    dev_max = th(CHECK, "size_class_max_dev")
    kinds = set(th(CHECK, "overlap_kinds"))
    errs = validate(doc)
    if errs:
        return [{"file": name, "what": "형식 오류", "detail": e} for e in errs], {}
    viol = []
    W, H = doc["canvas"]["w"], doc["canvas"]["h"]
    sizes = defaultdict(list)
    for sc in doc["scenes"]:
        els = sc["elements"]
        zones = list(doc.get("forbidden", [])) + list(sc.get("forbidden", []))
        for el in els:
            x, y, w, h = el["bbox"]
            if x < 0 or y < 0 or x + w > W or y + h > H:
                viol.append({"file": name, "scene": sc["id"], "what": "화면 밖", "element": el["id"]})
            for z in zones:
                if el["kind"] in z.get("allow_kinds", []):
                    continue
                iw, ih = inter(el["bbox"], z["bbox"])
                if iw > tol and ih > tol:
                    viol.append({"file": name, "scene": sc["id"], "what": "금지 영역 침범",
                                 "element": el["id"], "zone": z["id"], "px": [round(iw), round(ih)]})
            if el["kind"] == "block" and el.get("size_class"):
                sizes[el["size_class"]].append((sc["id"], el["id"], w * h, w, h))
        cand = [e for e in els if e["kind"] in kinds]
        for i in range(len(cand)):
            for j in range(i + 1, len(cand)):
                a, b = cand[i], cand[j]
                if b["id"] in a.get("allow_overlap", []) or a["id"] in b.get("allow_overlap", []):
                    continue
                iw, ih = inter(a["bbox"], b["bbox"])
                if iw > tol and ih > tol:
                    viol.append({"file": name, "scene": sc["id"], "what": "요소 겹침",
                                 "a": a["id"], "b": b["id"], "px": [round(iw), round(ih)]})
    spread = {}
    for cls, items in sizes.items():
        med = float(np.median([it[2] for it in items]))
        worst = 0.0
        for sc_id, el_id, area, w, h in items:
            dev = abs(area - med) / med if med else 0.0
            worst = max(worst, dev)
            if dev > dev_max + 1e-9:
                viol.append({"file": name, "scene": sc_id, "what": "같은 등급 블록 크기 편차",
                             "element": el_id, "size_class": cls, "wh": [w, h],
                             "dev_pct": round(dev * 100, 1), "limit_pct": dev_max * 100})
        spread[cls] = {"n": len(items), "median_area": med, "max_dev_pct": round(worst * 100, 1)}
    return viol, {"scenes": len(doc["scenes"]), "size_classes": spread}


def check(paths):
    viol, metrics = [], {}
    for p in paths:
        v, m = check_doc(load_json(p), p)
        viol += v
        metrics[p] = m
    return result(CHECK, not viol, viol, metrics, target=paths)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+")
    emit(check(ap.parse_args().paths))
