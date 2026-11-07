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
- **자체 점수는 참고용이다. 관문 통과는 독립 리뷰어 점수로 판정한다.** (11/05 안시성 시험: 자체 9점 vs 리뷰어 평균 6.7점)
- 대본 검사(리뷰어에게 넘기기 전): `lint/script_lint.py script.txt --format battle|shorts|longform|architecture`
  - 훅 문장 수(쇼츠 2문장), 같은 어미 연속, 평서 '~다.' 종결, '것입니다' 과다, 과거형 ㅆ, 연도 첫머리, 쉼표, 새 인물 수, 금지 기호
- 렌더 뒤 자동 검사: `lint/run_all.py <편 폴더> --format shorts|longform --profile explain|battle [--silent] [--asr]`
  - 검사 항목: 음량·True Peak, 효과음 대 내레이션, 고립 음절, 문장 중간 쉼, 소리 빈 구간, 정지·같은 화면·검은 화면, 같은 방향 팬, 컷 반복·클립 늘림, 화면 태그, 지도 겹침
  - qa.py(롱폼 온조 편)의 항목은 run_all에 흡수됐다(11/05). 녹음 전 애니매틱은 `--silent`.
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

## 7. 백업 — 원본은 GitHub 하나 (11/07)
- 원본 = GitHub `circlechoi/plumbing-ai-mvp` 브랜치 `claude/history-circle-quality-variance-txrqut`의 `history-circle/`(공개). sandbox는 작업 공간일 뿐이다.
- 세션 시작: sandbox에 최신본을 받는다 — `curl -sSL https://codeload.github.com/circlechoi/plumbing-ai-mvp/tar.gz/claude/history-circle-quality-variance-txrqut | tar -xz` 후 `history-circle/`을 `~/history-circle/`에 덮어쓴다.
- **세션 끝(또는 사용자에게 결과를 넘길 때)마다 GitHub에 반영한다.** 키트(style/·components/·animatic/·lint/), 원장(curated.yaml → build_ledger → verify), 편 폴더(episodes/<편>/ — 대본·고증·작업 코드는 `work/`)를 빠짐없이.
  - sandbox는 GitHub에 쓸 수 없다. git이 되는 작업 공간(Claude Code)에서 커밋·push하고, 파일은 sandbox에서 묶어 media_upload → 그 주소로 받는다. 받을 수 없으면 텍스트 파일을 옮기고 md5로 대조한다.
  - 편 작업 코드를 `~/ansi/` 같은 저장소 밖 폴더에만 두지 않는다(5편 사례: 112개 파일이 sandbox에만 남음).
- 큰 바이너리(영상·음성·기준 프레임 PNG)는 media_upload로 올리고 주소·md5를 해당 폴더 MANIFEST/README에 기록한다.
- 같은 스크립트를 번호만 바꿔 쌓지 않는다(예: normvo1~12, run2~38). 현행 파일 하나만 두고, 이전 판은 git 이력으로 남긴다.

## 8. Claude의 한계 (매번 밝힌다)
- Claude는 움직임을 볼 수 없고 소리를 들을 수 없다.
- 그래서 정지 프레임·수치·음성 인식 결과로만 확인했다고 보고한다.
- 재생해서 확인할 구간(초)을 짚어 준다.

## 9. 파일 규약 (11/05 안시성 시험에서 추가)
- 편 폴더: `history-circle/episodes/<포맷><번호>_<이름>/` — research.md(고증·원문 대조표) · beats.md · script.txt · reviews.md · selfscore.md · animatic/
- script.txt 형식(script_lint가 읽는다):
  - `제목:` 한 줄, `인물:` 쉼표로 구분(새 인물 수 검사)
  - `# 장면 N — 이름 (약 N초)`로 장면 구분
  - 내레이션 문장은 접두 없이 한 줄씩
  - `화면:` = 제작 메모(기호 검사 안 함, 따옴표 안 문구만 화면 글자로 검사) / `라벨:` = 실제 화면 글자(전체 검사)
- 원문 대조: 이 Claude Code 환경에서 wikisource·encykorea가 막히면 Higgsfield sandbox에서 받아 대조한다(읽기만, 크레딧 없음). 대조표는 research.md에.

## 10. 지도 컴포넌트와 애니매틱 엔진 (11/05)
- 'ㅗ' 블록·요새·줌·레이아웃 내보내기: `history-circle/components/` (규격 원본 `spec.json`)
  - 블록 등급은 원장 unit_grades. **병력이 사료에 없으면** 등급을 임의로 정하지 말고, 쓰려는 등급과 근거(상대 비교 등)를 그 편 research.md에 적고 화면에 숫자를 쓰지 않는다(임시 — 사용자 확인 전).
  - 광역→지역 줌은 최대 3.4배까지 확대 후 크로스페이드(zoom.py max_scale).
  - 범례 띠: 쇼츠 1600~1700, 그 아래도 같은 검은 띠로 채운다.
- 애니매틱 엔진(무음·저해상도, 크레딧 0): `history-circle/animatic/engine.py` — 지도 바탕 v4-S·흙산 단면 등. 엔진의 label·bubble·lord·gauge·arrow·bignum·hud는 11/06부터 스타일 키트(11절)를 거쳐 그린다(크기 인자는 무시·경고).

## 11. 스타일 키트 v1 (11/06 확정) — 새 그림 직접 그리기 금지
- **원칙: 편 코드에서 글씨·색·크기·도형을 직접 정하지 않는다. 필요한 그림은 `style/parts.py`에 부품으로 등록한 뒤 쓴다.** 새 부품의 숫자는 `style/style.json`에 넣는다. 편마다 엔진을 새로 짜지 않는다(5편 an5.py가 1편과 화면이 달라진 원인).
- 단일 원천: `history-circle/style/style.json` — 폰트 파일, 용도별 크기표(type_scale), 색(세력 색은 원장 값 그대로), 화면 틀 좌표(frame), 부품 치수(parts). 'ㅗ' 블록·성은 `components/spec.json`.
- 화면 틀 = 4편 주필산 방식(원장 kit_frame): 상단 검은 띠 0~140(연도 배지·워터마크) / 크림 제목 띠 140~236(NotoSansKR Black 52, 강조어 진빨강 상자) / 자막 y1420(NotoSansKR Black 56, 그라데이션 1270~1570) / 범례 띠 1600~1920.
- 부품 = 1편 백제 멸망전 방식(원장 kit_parts): `place`(지명) · `label` · `bubble` · `card` · `direction` · `inset` · `burst` · `sfx` · `cross` · `bignum` · `arrow` · `focus_box` · `ring` · `unit`('ㅗ') · `fort`(name=) · `figure`(인물: 얼굴 없음, `parts.people`에 고정 색·모자 등록 필수) · `gauge` · `clock`. 마무리는 `parts.finish(cv, year, title, caption, legend, note)`.
- 지도 바탕 = v4-S 유지(원장 kit_map_base).
- 기준 화면: `golden/style_ref/` — F1(4편 40초, 틀) · R1~R4(1편 21·31·46·61초, 부품) · R5('ㅗ' 블록 시안).
- 검사(사용자에게 보이기 전 필수, 실패하면 고친다): `lint/style_check.py tokens` · `code <편 폴더>` · `frame <png>… --caption "자막" --sheet 비교.jpg` · `layout <layout.json>` + `lint/layout_overlap.py`.
- 임시값(첫 사용 편에서 시안 확인): 인물 표식 4명(안시성주·당 태종·의자왕·계백), 시계, 성 표식 크기. 45초 쇼츠·롱폼 틀은 v1 범위 밖(style.json formats).
