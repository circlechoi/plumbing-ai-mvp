# 역사서클 스킬 재구조화 제안본 (11/04)

- 원본 스킬 9개는 손대지 않았습니다. 이 폴더는 제안본이며, 아래 「적용 방법」을 거쳐야 실제로 반영됩니다.
- 원칙: 사용자가 합의한 결정은 **삭제하지 않고 옮기기만** 합니다. 지금 구조(9개 스킬)도 그대로 유지합니다.

## 무엇이 바뀌나

| 파일 | 역할 | 읽는 때 |
|---|---|---|
| `history-core/SKILL.md` (신규) | 정체성 요약, **원장 현행 값 58항목**, 충돌 규칙, 관문·채점표, 크레딧 전 확인, 백업 | 항상 처음 |
| `<스킬>/SKILL.md` | 현행 작업 지침 | 해당 포맷 작업 때 |
| `<스킬>/reference-*.md` | 현행 규칙 중 특정 작업에서만 쓰는 것 (재편집, 업로드 메타, 기획 사슬, 지도 구판 파이프라인, 건축 기획) | 그 작업 때만 |
| `<스킬>/archive.md` | 폐기·보류·편별 이력·변경 이력 표·교체 전 원문 | 규칙으로 따르지 않음 (근거 확인용) |

- **충돌 규칙 개편**
  - 이전: "날짜가 붙은 최신 결정 우선". 매번 모델이 여러 파일을 대조해 해석해야 했습니다.
  - 이후: "현행 값은 원장 하나뿐, 원장과 다르면 원장 우선". 원장에 없는 항목끼리 부딪힐 때만 기존 원칙을 그대로 씁니다. 기존 원칙의 원문은 archive에 남겼습니다.
- **코드 본문 대체**: render.py v7.6, sprite.py, build_short v8.0, ctl·qa·han_mask·fix_river·anim(지도) 등 코드 블록 11개를 `history-circle/kit/` 경로 참조로 바꿨습니다. 같은 내용이 kit에 줄 그대로 있는지 검증했습니다.

## 크기 (바이트, `tools/verify_skills.py` 출력)

| 스킬 | 원본 | SKILL.md | reference | archive |
|---|---|---|---|---|
| history-shorts | 192,213 | 73,485 | 38,484 | 32,881 |
| history-longform | 72,635 | 56,651 | 2,021 | 17,259 |
| history-channel-concept | 65,926 | 40,298 | 15,275 | 15,113 |
| history-battle-shorts | 45,305 | 39,178 | 2,417 | 5,147 |
| history-architecture-shorts | 23,157 | 18,362 | 2,953 | 4,073 |
| history-longform-craft | 19,106 | 16,268 | 0 | 3,834 |
| history-production-standards | 18,406 | 17,534 | 0 | 2,337 |
| history-map-v4 | 16,727 | 16,776 | 0 | 253 |
| history-shorts-craft | 6,953 | 6,686 | 0 | 968 |
| history-core (신규) | — | 17,597 | — | — |

**작업마다 먼저 읽는 양**

| 작업 | 원본 (해당 스킬 + concept + production-standards) | 새 구조 (core + 해당 SKILL.md) | 감소 |
|---|---|---|---|
| 롱폼 | 192,800 | 107,292 | 44% |
| 45초 신작 | 300,225 | 114,544 | 62% |
| 전투 쇼츠 | 146,364 | 73,551 | 50% |
| 건축 쇼츠 | 299,702 | 109,444 | 63% |

- 기존 우선순위 규칙은 concept을 먼저 읽게 돼 있었습니다. 새 구조에서는 그 핵심(정체성·원장)이 core에 들어가므로 concept은 기획할 때만 읽습니다.
- history-core는 17.6KB로 목표(15KB)를 넘습니다. 원장 현행 값 원문(약 9.6KB)을 줄이지 않았기 때문입니다. 줄이면 결정이 희석됩니다.

## 바뀐 표기 (14줄)

원문은 각 스킬의 `archive.md` 「교체 원문」에 줄 그대로 있습니다. 목록은 `replacements.json`에 있습니다.

- 충돌 규칙 포인터(5줄): architecture·concept·longform·production-standards·shorts의 「우선순위(10/23 확정)」 문단
- **C1 지도 v3 → v4-S (7줄)**
  - shorts 제목줄·원칙 4번
  - architecture 지도 항목
  - concept 7-1 세력 색 줄·쇼츠 지도 줄
  - longform E-3 제목
  - production-standards 2절
- **C4 낙랑 = 먹회색 (84,88,102)**: concept 7-1 세력 색 줄 (C1과 같은 줄)
- **C5 화면 태그 부제 삭제**: architecture 지도 표지 줄
- **C6 부대 표시 = 'ㅗ' 블록 공통, 도트는 장식**: longform E-3 도트 기마병 줄
- C2(배속)·C3(음량)·C7(롱폼 자막)·C8(배역 목소리)은 본문에 현행으로 남은 상충 문장이 없어 교체하지 않았습니다.
  - 해당 원문은 결정 로그나 편별 이력이라 archive로 옮겼습니다.
  - 현행 값은 core 원장 표에 있습니다.

## 검증 (`python3 tools/verify_skills.py`)

- 원본 9개 스킬의 비어 있지 않은 줄 3,058개가 모두 새 파일이나 kit에 그대로 있습니다. 바뀐 줄은 교체 기록에 있습니다. **누락 0**입니다.
- 원장 원문 277건이 모두 새 파일에 있습니다. **누락 0**입니다.
- 검증 도구가 실제로 누락을 잡는지 시험했습니다. archive에서 한 줄을 지우자 누락 1건으로 exit 1이 났습니다.
- 한계: 검사는 줄 단위로 "어딘가에 있는지"만 봅니다. 표 구분선처럼 흔한 줄은 다른 곳에 있어도 통과합니다. 순서나 문맥은 검사하지 않습니다.

## 다시 만들기

```
python3 tools/build_skills.py      # 원본 스킬 + patches/ + decisions.yaml + kit → 이 폴더
python3 tools/verify_skills.py     # 누락 0이 아니면 exit 1
```

- 고칠 곳
  - 이동할 절: `tools/patches/plan.yaml`
  - 표기 교체: `tools/patches/replacements.yaml`
  - core 틀: `tools/patches/core_template.md`
- 원장(`decisions.yaml`)이 바뀌면 core도 다시 만들어야 합니다.

## 적용 방법 (사용자가 직접)

이 Claude Code 환경에서는 claude.ai 스킬을 직접 올리거나 고칠 수 없습니다.

1. 이 폴더의 `history-*` 10개 폴더를 각각 zip으로 묶습니다. 묶을 파일은 `SKILL.md`, `reference-*.md`, `archive.md`입니다.
2. claude.ai 설정의 스킬 화면에서 기존 9개를 교체하고 history-core를 새로 추가합니다. 화면 이름과 위치는 확인하지 못했습니다(추정).
3. 처음 한 편은 기존 스킬을 비활성화만 하고 지우지 않은 채 새 구조로 만들어 봅니다.
4. 문제가 없으면 기존 스킬을 정리합니다.
5. kit 경로(`history-circle/kit/...`)는 GitHub 저장소 기준입니다. Higgsfield sandbox에서 쓰려면 해당 파일을 sandbox로 가져와야 합니다. 기존 Drive 백업 경로도 production-standards 4절에 그대로 남아 있습니다.
