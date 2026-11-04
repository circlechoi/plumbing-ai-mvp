#!/usr/bin/env python3
"""curated.yaml(사람이 정리) + decisions_raw.yaml(기계 추출) → decisions.yaml

- curated 항목의 sources·superseded id를 날짜와 함께 펼친다.
- curated 어디에도 연결되지 않은 raw 항목은 버리지 않고 주제별 '원문_보존'에 원문 그대로 넣는다
  (주제는 키워드로 고르고, 애매하면 '기타').
- curated가 raw에 없는 id를 가리키면 실패한다(스킬 줄 번호가 바뀌었다는 뜻 → extract 다시 실행 후 curated 갱신).
"""
import os
import sys

import yaml

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = os.path.join(D, "decisions_raw.yaml")
CUR = os.path.join(D, "curated.yaml")
OUT = os.path.join(D, "decisions.yaml")

# 남은 원문을 주제로 보낼 때 쓰는 키워드(앞에 있을수록 우선)
TOPIC_KW = [
    ("건축 시리즈", ["건축", "도시의 일생", "그 시절", "온돌", "쪽구들", "졸본", "수도"]),
    ("지도", ["지도", "국경", "라벨", "DEM", "korea_full", "map", "배치"]),
    ("음량·효과음", ["LUFS", "효과음", "음악", "BGM", "Suno", "음량", "현장음"]),
    ("내레이션·TTS", ["Harrison", "TTS", "내레이션", "목소리", "녹음", "배속", "atempo", "낭독"]),
    ("자막·서체", ["자막", "서체", "제목", "배지", "워터마크", "px"]),
    ("영상 생성·크레딧", ["Kling", "Seedance", "크레딧", "job", "시트", "생성"]),
    ("관문·검수", ["관문", "리뷰어", "검수", "점검"]),
    ("화면·색", ["색", "청록", "수묵", "시그니처", "컷", "화면", "피 "]),
    ("대본·오프닝", ["대본", "오프닝", "훅", "질문", "판단", "기록", "해석", "선택지", "편 구성", "정체성"]),
    ("운영·백업", ["설명란", "백업", "2주", "패키징", "썸네일", "시청자", "편당", "숏츠", "쇼츠", "기획"]),
]


def topic_for(text):
    for name, kws in TOPIC_KW:
        if any(k in text for k in kws):
            return name
    return "기타"


def main():
    raw = yaml.safe_load(open(RAW, encoding="utf-8"))
    cur = yaml.safe_load(open(CUR, encoding="utf-8"))
    by_id = {x["id"]: x for x in raw["items"]}

    missing, linked = [], set()

    def expand(ids):
        out = []
        for i in ids or []:
            if i not in by_id:
                missing.append(i)
                continue
            linked.add(i)
            out.append(f"{i} ({by_id[i]['date']})")
        return out

    meta = dict(cur["meta"])
    meta["principle_sources"] = expand(meta["principle_sources"])
    meta["user_over_review_sources"] = expand(meta["user_over_review_sources"])

    topics = []
    for t in cur["topics"]:
        items = []
        for it in t["items"]:
            it = dict(it)
            it["sources"] = expand(it.get("sources"))
            if it.get("superseded"):
                it["superseded"] = expand(it["superseded"])
            items.append(it)
        topics.append({"name": t["name"], "items": items})

    if missing:
        sys.exit("curated.yaml이 raw에 없는 id를 가리킴(스킬 줄 번호 변경?): " + ", ".join(missing))

    # 연결 안 된 raw 항목 → 주제별 원문_보존
    names = [t["name"] for t in topics]
    rest = {}
    for x in raw["items"]:
        if x["id"] in linked:
            continue
        tp = topic_for(x["text"])
        rest.setdefault(tp, []).append({"id": x["id"], "date": x["date"], "status_hint": x["status"], "text": x["text"]})
    for t in topics:
        if t["name"] in rest:
            t["원문_보존"] = rest.pop(t["name"])
    for tp, lst in rest.items():  # '기타' 등 새 주제
        topics.append({"name": tp, "items": [], "원문_보존": lst})

    counts = {
        "raw_total": len(raw["items"]),
        "curated_items": sum(len(t["items"]) for t in topics),
        "linked_by_curation": len(linked),
        "kept_verbatim": sum(len(t.get("원문_보존", [])) for t in topics),
        "pending_user": sum(1 for t in topics for i in t["items"] if i.get("status") == "사용자확정대기"),
    }
    doc = {
        "about": "역사서클 결정 원장 — 생성 파일. 고칠 때는 curated.yaml을 고치고 tools/build_ledger.py를 다시 돌린다. 원문은 decisions_raw.yaml.",
        "source_skills": raw["sources"],
        "counts": counts,
        "meta": meta,
        "topics": topics,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        yaml.safe_dump(doc, fh, allow_unicode=True, sort_keys=False, width=10**6)
    print(counts)


if __name__ == "__main__":
    main()
