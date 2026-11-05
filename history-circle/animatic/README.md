# 애니매틱 엔진 (편 무관) — `engine.py`

전투 해설 쇼츠의 콘티(정지 시안)와 무음 애니매틱을 크레딧 0으로 만든다. 첫 사용처: `episodes/battle05_ansi/animatic/build.py`.

## 기존 코드를 따른 부분(다시 구현)

| 기능 | 원본(Higgsfield sandbox) |
|---|---|
| 고도 타일·샘플링 `dem`, `sample` | `~/salsu/terrain3.py` dem·sample (AWS Terrarium) |
| 땅·산지 마스크 `masks` | `~/salsu/mkstyl.py` masks |
| 바탕 `map_base` | `~/salsu/bmap3.py` map_base |
| 산 기호 `highland2` | `~/salsu/salsu.py` highland2 |
| 강 `draw_rivers` | `~/salsu/mkbase.py` draw_rivers (OSM 단순화 좌표는 편 폴더에) |
| 화면 띠·자막·범례 `hud` | `~/jupil/anim4.py` hud1080 (제목 띠 140~236, 자막 y 1420·760px 넘으면 두 줄, 범례 1600~1700) |
| 카메라 `cam`, `popf`, `ramp`, `ease` | `~/jupil/anim4.py` cam·popf 등 |
| 블록·성·줌·레이아웃 | `components/` units·forts·zoom·canvas 그대로 |

## 새 부품(components에 없던 것)

| 부품 | 함수 | 상태 |
|---|---|---|
| 흙산 단면 도식(높이 경쟁·무너짐·성벽 균열·주인 바뀜) | `mound_section` | 시안 — 높이 막대·눈금 없음 |
| 군량 게이지(25% 아래 깜빡임) | `gauge` | 시안 |
| 얼굴 없는 인물 표식(크림 원 + 금 테두리) | `lord` | 시안 — 스타일 바이블 '지도에 얼굴 금지' |
| 도트 절 스프라이트(12×16) | `dot_bow` | 시안 — 기존 도트 키트 화풍 미확인 |
| 말풍선(꼬리) | `bubble` | 4편 balloon 형태를 흉내 |
| 큰 숫자(튀어나옴, 크기 0 가드) | `bignum` | 4편 bigtxt + 실패 기록의 max(2, …) 가드 |
| 굵은·점선 화살표(먹 테두리, 자라는 길이) | `arrow` | bmap3 arrow 단순판 |
| 기각 ✕ | `cross` | 선으로 그림(Jua에 ✕ 없음) |
| 종이 결 바탕(도식 장면) | `plain` | 평면색이면 카메라가 움직여도 '정지'로 잡혀서 추가 |
| 문장마다 카메라 밀기 | 편 build.py `push` | 정지 화면 상한(전투 1초)용. 엔진으로 옮길 후보 |
| 대본 → 시간표 | `parse_script`, `timeline`, `syl_time` | 음절/6.2초 + 0.35초 추정 |
| ffmpeg 출력 | `Writer` | 무음 mp4 |

## 쓰는 법

- 편 폴더에 `bases.py`(지도 창·바탕), `build.py`(장면 함수 sN(u) → (Canvas, 카메라))를 둔다.
- `python3 build.py storyboard|animatic|all`.
- 고도 타일 캐시는 `HC_TILES`(기본 `animatic/.tiles`, git 제외)에 둔다.

## 알려진 한계

- components `zoom.zoom_frames`는 지역 창을 화면에 꽉 채울 때까지 확대한다. 광역↔지역 배율이 20배쯤이면 금색 박스가 화면을 덮는다.
  - 5편은 스킬 원문('3.4배 확대 → 크로스페이드')대로 3.4배 창을 넘겨 우회했다.
  - zoom.py에 배율 상한(spec)을 넣는 것이 맞다.
- 한자 글꼴이 없다(원문 카드 불가). NotoSansKR이 없어 자막은 Jua, 제목은 BlackHanSans다(4편은 NotoSansKR Black).
