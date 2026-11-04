---
name: "history-core"
description: "역사서클 모든 작업의 첫 스킬 — 채널 정체성 요약, 현행 값 원장(11/04 확정), 충돌 규칙, 관문·채점표, 크레딧 전 최종 확인, 사용자 결정 우선, 백업 규칙. 롱폼·쇼츠·전투·건축 작업을 시작할 때 다른 history-* 스킬보다 먼저 읽는다."
---

# 역사서클 핵심 (history-core v0.1 · 2026-11-04 · 생성 파일 — `history-circle/skills/tools/build_skills.py`)

## 0. 읽는 순서
1. **이 스킬**(현행 값·규칙)
2. 포맷 스킬 1~2개만
   - 롱폼: history-longform + history-longform-craft
   - 45초 신작: history-shorts + history-shorts-craft
   - 전투 해설: history-battle-shorts
   - 건축: history-architecture-shorts
   - 지도 컷이 있으면 history-map-v4를 더한다
3. 필요할 때만 읽는 것
   - history-channel-concept: 기획·주제 선정
   - history-production-standards: 자원·백업
   - 각 스킬의 `archive.md`: 폐기·이력 원문 (규칙으로 따르지 않는다)

## 1. 정체성 (history-channel-concept 1절 원문 인용)
{{IDENTITY}}

## 2. 충돌 규칙 (11/04 개편)
- **현행 값은 원장(아래 3절 = `decisions/decisions.yaml`) 하나뿐이다.** 스킬 본문과 원장이 다르면 원장을 따르고, 사용자에게 고칠 곳을 알린다.
- 원장에 없는 항목끼리 부딪히면 기존 원칙을 따른다(10/23 확정 원문):
{{PRINCIPLE}}
- 결정이 새로 나오면 다음 순서로 반영한다.
  1. `curated.yaml`에 항목을 추가한다.
  2. `build_ledger.py`로 원장을 다시 만든다.
  3. `verify_ledger.py`로 검증한다.
  4. `build_skills.py`로 이 스킬을 다시 만든다.
- 스킬 줄 번호가 밀렸으면 `remap_ids.py`를 먼저 돌린다.

## 3. 원장 — 현행 값 ({{COUNTS}}) · ★11/04 = 사용자 확정(충돌 C1~C8) · 출처는 decisions.yaml
{{LEDGER}}

## 4. 관문과 채점표
- 롱폼 관문은 3단계다: ① 비트시트 → ② 대본 → ③ 스토리보드. 리뷰어 구성은 history-longform B-0을 따른다.
- 크레딧을 쓰기 전에 **애니매틱(정지 프레임 + 내레이션 + 지도)** 으로 장면마다 등급을 매긴다.
  - S·A: 생성
  - B: 지도·도식으로 대체
  - C: 삭제 또는 병합
- 채점은 `golden/rubric.md`(0/1/2점)로 한다. **0점 항목이 하나라도 있으면 다음 관문으로 가지 않는다.**
  - 근거 사례는 `golden/segments.yaml` 26구간(G01~G26)이다.
- 리뷰어 입력에는 이 원장 표와 채점표, 관련 골든 구간을 고정으로 넣는다.
- 시안을 낼 때는 자체 점수와 '편집장이라면 무엇을 지적할지' 목록을 함께 낸다(G25).
- 렌더 뒤 자동 검사: `lint/run_all.py <편 폴더> --format shorts|longform`
  - 검사 항목: 음량, 효과음 대 내레이션, 고립 음절, 문장 중간 쉼, 정지 구간, 같은 방향 팬, 지도 겹침
  - 실패하면 사용자에게 보이기 전에 고친다.

## 5. 사용자 결정 > 검수 의견 (history-production-standards 원문)
{{USER_OVER_REVIEW}}

## 6. 크레딧 전 최종 확인
- 생성·업스케일 등 크레딧이 드는 호출 전에는 다음 세 가지를 보여 주고 사용자 확인을 받는다.
  - 바뀐 대본·장면
  - 생성할 컷 목록
  - 예상 크레딧 (get_cost 또는 quote)
- 검수 뒤에 바뀐 것도 다시 보여 준다(production-standards 0-1, 10/25).
- Kling은 `sound: "off"`를 문자열로 넣는다. `false`로 넣으면 소리가 켜져 12.5 크레딧이 나간다(longform F, 10/16 사고).

## 7. 백업
- 렌더·빌드 코드는 git(`history-circle/kit/`)이 원본이다.
- sandbox에서 새로 만들거나 고친 스크립트는 세션이 끝날 때마다 묶어서 백업한다.
  - 방법: media_upload 일반 파일로 올리고, 위치·md5를 `kit/MANIFEST.md`에 기록한다.
- 같은 스크립트를 번호만 바꿔 쌓지 않는다(예: normvo1~12, run2~38). 현행 파일 하나만 두고, 이전 판은 git 이력으로 남긴다.

## 8. Claude의 한계 (매번 밝힌다)
- Claude는 움직임을 볼 수 없고 소리를 들을 수 없다.
- 그래서 정지 프레임·수치·음성 인식 결과로만 확인했다고 보고한다.
- 재생해서 확인할 구간(초)을 짚어 준다.
