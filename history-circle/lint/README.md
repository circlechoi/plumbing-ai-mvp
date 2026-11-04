# 역사서클 자동 검사 (lint)

렌더 결과물과 대본을 수치로 검사해, 규칙이 실행 단계에서 빠지는 것(겹침·효과음 음량·고립 음절·정지 화면·남은 태그 등)을 막는다.
온조 편 `qa.py`(longform-craft 11절)의 영상·소리·태그·발음 항목을 흡수했다 — 앞으로는 qa.py 대신 `run_all.py`를 돌린다.
의존: python3 + numpy + Pillow + ffmpeg/ffprobe. 발음 검사만 faster-whisper(없으면 건너뜀). 크레딧 없음.

## 사용
```sh
python3 run_all.py <편 폴더> [--profile explain|battle] [--format shorts|longform]
                   [--script-format battle|shorts|longform|architecture] [--asr] [--json 결과.json]
python3 <검사>.py ...     # 검사 하나만 (JSON 출력, 실패 exit 1)
sh run_tests.sh           # 합성 샘플 시험(37개)
```

편 폴더 규약(있는 것만 검사, 하나라도 실패면 exit 1):

| 파일 | 검사 |
|---|---|
| `final.mp4` (또는 `*.mp4` 하나) | audio_loudness, audio_silence, video_static, video_pan_repeat, video_repeat (+ `--asr`이면 audio_asr) |
| `vo.wav` + `sfx.wav` | audio_sfx_vs_vo |
| `scenes/*.wav` (+ `scenes/<이름>.words.json`) | audio_isolated_syllable, audio_midpause |
| `layout*.json`, `layout/*.json` | layout_overlap |
| `script.txt` 또는 `script.md` | script_lint |
| `src/` (렌더 소스 .py·자막 .ass/.srt·라벨 .json) | src_text |
| `sections.json`, `cuts.json` | 보조 입력(구간 프로필·절정 구간 / 계획 컷·kind) |

- `--format longform`이고 1920×1080이면 영상 검사는 레터박스 그림 띠(138~942)만 본다(qa.py와 같음).
- 대본 형식: 빈 줄 = 문단, `#`·`---`·`[장면` 줄 = 장면 구분, `인물: 가, 나` = 새 인물 목록, `화면:`·`라벨:`·`자막:`·`제목:`·`[화면]` 줄 = 화면 문자열.
- `cuts.json` kind: `person`(3초 상한) · `wide`(5초) · `live`(실사, 안의 스틸 2초 금지) · `map`(같은 컷 반복 비교에서 제외).

## 검사와 근거
| 검사 | 무엇을 | 실패 / 경고 | 근거 |
|---|---|---|---|
| audio_loudness | 통합 LUFS·True Peak | 쇼츠 −15 / 롱폼 −14 ±1 LU 밖, TP > −1.5 | 11/04 확정 C3 |
| audio_silence | 소리 빈 구간 (qa.py) | 3초+ 실패 / 2.5초+ 경고 | 스타일 바이블 '무음 3초 금지' · qa.py |
| audio_sfx_vs_vo | 효과음 vs 내레이션 RMS(0.4초 창) | 효과음 > 내레이션 −3dB (절정 구간 −1dB) | longform '모든 효과음이 내레이션보다 작게' · C3 |
| audio_isolated_syllable | 장면 wav 앞뒤 끝 고립 음절 | 0.12초+ 무음 뒤 0.2초 미만 소리 | battle-shorts 고립 음절 검사 |
| audio_midpause | 문장 중간 쉼 | −40dB 0.1초+ (문장부호 없는 자리) | battle-shorts 문장 중간 쉼 자동 점검 |
| audio_asr | 발음 의심 단어 (qa.py) | 경고만, faster-whisper 없으면 건너뜀 | qa.py WATCH 목록 |
| video_static | 정지·같은 화면·검은 화면·컷/튐 (qa.py 통합) | 정지: 설명 6초·전투 1초 초과 실패, 3초+ 경고 / 같은 화면 6초+ 경고 / 검은 화면 0.8초+ 실패(시작·끝 페이드는 경고) / 계획에 없는 컷 경고 / 사람 컷 3초·원경 5초·실사 스틸 2초 | longform E-6 · longform-craft · qa.py |
| video_pan_repeat | 컷별 화면 이동 방향 | 같은 방향 팬 2컷 연속 | 사용자 지적(규칙 신규) |
| video_repeat | 같은 컷 반복 · 클립 늘림 | 같은 컷 3회+ 실패, 2회 경고(흑백 회상·map 컷 제외) / 복제 프레임 0.45+ 실패, 0.34+ 경고 | golden G18 · 스타일 바이블 회수 규칙 · 0.7배속 허용 |
| layout_overlap | 블록·라벨·아이콘 bbox | 겹침 / 자막띠·제목띠 침범 / 같은 등급 면적 ±5% | battle-shorts 겹침 금지 배치 |
| script_lint | 대본 | '것입니다' 문단 맺음 3회 초과 · 라디오 금지어 · 동화식 도입 · 화면 금지 기호는 전 포맷 실패 / 과거형 ㅆ·연도 첫머리·쉼표 2개+·새 인물 6명+는 전투 쇼츠만 실패(그 외 경고, 롱폼은 과거형 검사 끔) / 동화적 표현 의심어는 경고(임시 목록) | longform 풀이 종결 · battle-shorts 대본 원칙 · shorts 라디오 기준·첫 장면 |
| src_text | 렌더 소스·자막·라벨 | 남은 태그([기록]/[통설]/[해석]/[연출], 개념도) · 금지 기호(·『』→) | qa.py 태그 grep · C5 · battle-shorts 금지 기호 |

- 임계값은 `thresholds.json` 한 곳에만 있다. 항목마다 `source`(스킬 원문 문구)와 `status`(확정/임시).
- **정지 판정과 liven.py**: 천천히 확대한 구간은 매 프레임 차이가 작아 qa.py에서는 '정지'로 잡혔다(longform-craft 주의사항). video_static은 1초 전 프레임과 비교해 화면이 바뀌는 중이면 정지에서 뺀다(`--no-zoom-aware`로 끄면 qa.py와 같은 판정). 대신 같은 화면 6초+ 경고는 남는다.
- `video_pan_repeat`의 방향은 **화면 내용이 움직인 방향**(카메라 이동의 반대). 줌·정지 컷은 none.

## 한계
- 소리·움직임의 '느낌'(억양, AI 티, 충돌감)은 판정하지 못한다. 수치로 잡히는 실수만 막는다.
- 클립 늘림은 복제 프레임으로만 잡는다. 프레임 보간(minterpolate·AI 보간)으로 늘린 클립은 못 잡는다.
- 같은 컷 반복은 평균 프레임 비교라, 같은 바탕 지도에 표식만 바꾼 컷은 같은 컷으로 잡힐 수 있다 → `cuts.json`에 kind `map`.
- script_lint의 받침 충돌·동음 혼동(battle-shorts)은 검사하지 않는다(사전 필요). 새 인물 수는 `인물:` 줄이 있어야 센다.
- 실제 편 원본으로 대조하지 않았다. 합성 샘플 시험만 통과.
