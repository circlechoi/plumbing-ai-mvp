# 역사서클 자동 검사 (lint)

렌더 결과물을 수치로 검사해, 규칙이 실행 단계에서 빠지는 것(겹침·효과음 음량·고립 음절·정지 화면 등)을 막는다.
의존: python3 + numpy + ffmpeg/ffprobe. 크레딧 없음.

## 사용
```sh
python3 run_all.py <편 폴더> [--profile explain|battle] [--json 결과.json]   # 있는 파일만 검사, 하나라도 실패면 exit 1
python3 <검사>.py ...                                                       # 검사 하나만 (JSON 출력, 실패 exit 1)
sh run_tests.sh                                                             # 합성 샘플 시험(19개)
```
편 폴더 규약: `final.mp4`, `vo.wav`+`sfx.wav`, `scenes/*.wav`(+`scenes/<이름>.words.json`), `layout*.json` 또는 `layout/*.json`, 선택 `sections.json`·`cuts.json`.

## 검사와 근거
| 검사 | 무엇을 | 실패 기준 | 근거 |
|---|---|---|---|
| audio_loudness | 최종 통합 LUFS | 목표 ±1 LU 밖 | **목표 미확정**(battle-shorts:151 −15 / longform:23 −13.7 / craft:75 −17) |
| audio_sfx_vs_vo | 효과음 vs 내레이션 RMS(0.5초 구간) | 둘 다 울릴 때 효과음 > 내레이션 −3dB | longform:93 '모든 효과음이 내레이션보다 작게' |
| audio_isolated_syllable | 장면 wav 앞뒤 끝 고립 음절 | 0.12초+ 무음 뒤 0.2초 미만 소리, 끝에서 0.3초 안 | battle-shorts:133 |
| audio_midpause | 문장 중간 쉼 | −40dB 0.1초+ 쉼이 문장부호 없는 자리 / 문장부호 뒤 0.5초 초과 | battle-shorts:134 |
| video_static | 정지 화면 길이, 컷 길이 | 설명 구간 6초·전투 구간 1초 초과 / 사람 컷 3초·원경 5초 초과(cuts.json) | longform:245·185, craft:35-36 |
| video_pan_repeat | 컷별 화면 이동 방향(위상상관) | 같은 방향 팬 2컷 연속 | 사용자 지적(규칙 신규), 컷 감지 craft:124 |
| layout_overlap | 블록·라벨·아이콘 bbox | 겹침 / 자막띠·제목띠 침범 / 같은 등급 블록 면적 ±5% 초과 | battle-shorts:94·98·71, 사용자 지적 |

- 임계값은 `thresholds.json` 한 곳에만 있다. 항목마다 `source`(스킬:줄)와 `status`(확정/임시/사용자확정대기).
- `audio_midpause`는 단어 시각(faster-whisper `[{"word","start","end"}]`)이 없으면 0.5초 초과 쉼만 실패, 나머지는 경고.
- `layout_overlap` 입력 형식은 `schema/layout.schema.json`. 지도 컴포넌트(세션 2)가 장면마다 이 JSON을 내보내야 검사가 돈다. 화살표·효과(arrow·effect)는 겹침 검사 대상이 아니다.
- `video_pan_repeat`의 방향은 **화면 내용이 움직인 방향**(카메라 이동의 반대). 줌·정지 컷은 none으로 보고 연속 판정에서 뺀다.

## 한계
- 소리·움직임의 '느낌'(억양, AI 티, 충돌감)은 판정하지 못한다. 수치로 잡히는 실수만 막는다.
- 실제 편 원본으로 대조하지 않았다(원본 위치 미확인). 합성 샘플 시험만 통과.
