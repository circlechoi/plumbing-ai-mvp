---
name: "history-map-v4"
description: "역사서클 롱폼·쇼츠의 지도 컷(광역·지역·도식)을 만들 때 사용. 실제 고도·하천 바탕 + 삼국전투기 스타일 산지(v4-S, 기본) 또는 AI 재채색 지형 + 코드 표시. history-longform E-3(지도 v3)보다 우선."
---

# 역사서클 지도 v4 (v4.2 — 2026-10-31: 쇼츠 전체 화면 지도 영상(mapvid.py) 추가 · 10/28 v4-S 삼국전투기 스타일, 롱폼·쇼츠 공통 기본)

함께 읽기: history-channel-concept(라디오 기준·지도 문법), history-battle-shorts 3절(삼국전투기 지도 문법), history-longform(롱폼 전체 규칙), history-shorts-craft(신작 쇼츠 작법). **지도에 관해서는 이 스킬이 history-longform E-3(지도 v3)과 history-shorts L(AI 재채색 지도)보다 우선한다.**

## 0. 원칙 (사용자 확정 10/28)
- **기본 = v4-S(실제 고도 기반 삼국전투기 스타일)** — 사용자: '산맥이랑 포인트들은 삼국전투기 느낌으로 표현', '실제 고도자료 기반을 삼국전투기 스타일 변화', '롱폼에도 이 형태로'. 실제 고도·하천·해안으로 위치를 정확히 잡고, 보이는 모양은 녹색 산지 면 + 먹 테두리 + ^ 획 + 핵심 길·고개 강조.
- **핵심 지형이 안 읽히면 그 부분만 과장**(예: 고개 양옆 산줄기 키우기) + 화면 '개념도'. 그래도 안 읽히면 코드 개념도(손으로 찍은 산지)로 돌아간다(사용자: '여차하면 다시 기존 삼국전투기로'). 기준은 '그 장면의 핵심 지형(예: 탄현)이 어떤지 이해되나'.
- **세 겹 구조는 유지**: ① 정확한 바탕(코드: 실제 고도·하천·해안) → ② 지형 표현(v4-S 코드 양식 = 기본 / AI 재채색 = 선택) → ③ 표시(코드: 나라 마크·화살표·영역색·도시·범례·자막·글자).
- **색감·표시 형태는 지금 것 유지**(사용자: '색감 표시형태 등은 지금을 유지해도 좋아'). 글자·마크·화살표·국경은 AI에 맡기지 않는다.
- 레퍼런스: 삼국전투기(지도 문법), Kings and Generals 지도·Crusader Kings 종이 지도(질감). 화면을 베끼지 않는다.
- 지도 컷을 쓸지·무엇을 보일지는 '지도 설계 프롬프트 v1'(온조 문서 탭 '3단계 · 지도 설계 v1'): 컷마다 '이유' 한 줄, 지명 3~4개, 주 화살표 1~2개, 요소 7개 이하, 라디오 기준, 위치 불확실 = 점선 + '개념도', 선택지를 인장·상자로 나열하지 않음.

## 1. 실패 기록 (반복 금지)
- v1(10/28): 코드만으로 그린 둥근 녹색 산 덩어리 + 큰 ^ 아이콘, 직선에 가까운 관 모양 강, 매끄럽게 뭉갠 해안 → '강·바다·산이 다 어색' / 말갈을 강원 동해안에 둠 → '너무 동쪽'.
- v2: 노이즈 산 경계·가는 강으로 다듬었지만 여전히 아이콘식. 강 좌표를 기억으로 찍으면 굽이가 틀린다.
- 교훈 1: 위치는 실제 자료로 잡는다(기억·손 좌표 금지).
- **실제 고도 음영만(코드 단계 그대로, 10/28 쇼츠 시험)**: 산맥이 뚜렷하지 않고 핵심 지점(탄현)이 어떤 지형인지 이해 불가 → 교훈 2: 보이는 모양은 삼국전투기 문법(v4-S).
- 단순 고도 임계값으로 산지를 잡으면 낮은 산줄기(예: 대전 동쪽)가 사라져 '고개'가 안 보일 수 있다 → 길 띠 + 고개 표시 + 필요하면 국소 과장.
- (10/31 오노성 편) 평야 입구 흙둑(미즈키)이 들판 한가운데 떠 보임 → 고도 단면(트랜섹트)을 찍어 보니 서쪽 구릉이 약 50m → 소지역 지도 임계값을 45m로 낮추자 '두 구릉 사이를 막는 둑'이 읽혔다. 교훈 3: 핵심 시설이 지형에 붙어 보이지 않으면 먼저 고도 단면을 찍고 임계값을 그 지형 높이에 맞춘다.
- (10/31) 규슈 하천 Overpass 질의가 시간 초과 → 하천 없이 진행. 하천이 판단의 근거가 아니면 생략 가능.

## 2. 공통 바탕 (코드)
1. **범위**: `Map(lon0, lon1, clat)`. 롱폼 = bmap16(16:9 레터박스 패널 1920×804, PANEL=(0,138,1920,942), 위도 폭 ≈ 경도 폭 × 0.8 / 2.39, 광역 예 `Map(123.95, 131.05, 37.45)`), 쇼츠 = bmap3(9:16 패널 (24,170)-(1056,1580)). 두 모듈은 Map·W·H·K·PANEL 이름이 같아 terrain.py의 import만 바꾸면 둘 다 쓴다(쇼츠용 terrain3.py). **쇼츠 전체 화면(1080×1920)은 10절**.
2. **고도**(terrain.py `dem`·`sample`, `paint`는 음영 바탕): AWS Terrarium 타일(`s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png`, 고도 = R·256+G+B/256−32768) → 메르카토르→정거원통 분리 보간. 광역 z=7~8, 지역 z=9~10, 소지역(성·둑 수준) z=11. 결과를 npy로 저장해 재사용.
3. **실제 하천**(rivers_osm.py / 쇼츠 mkbase.py): Overpass(`overpass-api.de`, User-Agent 지정) `way["waterway"="river"]["name"~"^(한강|북한강|남한강|임진강|한탄강|안성천)$"](S,W,N,E); out geom;` — 편마다 이름만 바꾼다(660 백제 = 금강|갑천|미호강|논산천). 짙은 테두리(46,74,112) + 물색(96,140,200) + 굵은 강 가운데 밝은 줄. 폭: 본류 7 / 지류 4.5 / 작은 강 3.2(광역), 지역 지도는 ×2~3. **본류는 하구로 갈수록 넓게**(mkbase.py `mouth_lon` 이서 최대 3.2배) → 바다와 한 물. Natural Earth 10m 하천은 쓰지 않는다. 영역색을 칠한 뒤 강을 다시 그려 강이 탁해지지 않게. 해외(일본 등)는 Overpass가 시간 초과가 잦다 → 범위를 좁히거나 생략.
4. 같은 범위의 바탕은 편 안에서 재사용(광역 1장 + 지역 1~2장이면 편 전체 지도 컷을 덮는다). 표시 동작만 장면마다 바꾼다.

## 3. v4-S 삼국전투기 스타일 (기본, 크레딧 0)
1. **땅 마스크**: 고도 > 0.5m → Gaussian(5·K) 단순화 → 작은 섬 제거(면적 0.2% 미만) → `M._lm`에 넣고 `map_base(M)`으로 해안(얕은 바다 띠·먹선) 그리기.
2. **산지 면**: 고도를 Gaussian(sm=5) 평활 → **임계값 약 165m**(지역 지도 기준. 광역은 300m 안팎부터 시험, 소지역은 지형 높이에 맞춰 45m까지 — 1절 교훈 3) → 면적 1.2% 미만 조각 제거 → 가장자리 부드럽게. 임계값은 150/220/300 세 장을 나란히 보고 고른다.
3. **그리기**(mkstyl.py `highland_from_mask`): 녹색 GREEN(98,146,92) 면 + 먹 테두리(MaxFilter 11) + 격자 어긋남 ^ 획(간격 78, 크기 20~38을 고도에 비례, 면 안에 다 들어오는 것만).
4. **실제 하천**(2-3) → **핵심 포인트**(mkstyl.py `pass_marks`): 진군로 = 먹 테두리 밝은 길 띠(ROAD), 고개 = ')(' 호 표시, 필요하면 들 이름. 타당하면 고개 양옆 산지를 키워 과장 + '개념도'.
5. **표시**: 영역색 = 흐린 면(쇼츠 `territory(soft=0.6)`, 롱폼 `soft_tint` α 0.35 안팎) → 강 다시 그리기 → 지명·마크·화살표. 함대 화살표가 실제 해안을 따라 바다로 가는지 확인.
6. 재현: 쇼츠 키트 v8 `python3 mkstyl.py`(DEM 저장) → `python3 mkstyl_run.py`(바탕 out/reg_styl_full.png·reg_lm.png) → scenes13 `TERRAIN_BG`. 롱폼은 같은 함수를 bmap16 import로 쓰고(지도 키트 v2의 terrain·rivers_osm와 합치기), m1v4.py의 `paint`+`draw_rivers` 대신 mkstyl `build`를 부른다. 온조 편은 말갈 길·위례 같은 핵심 포인트를 `pass_marks`로 강조.

## 4. (선택) AI 재채색 — 온조 M1 시안 A 방식
1. 바탕(terrain.py `paint` 음영 + 하천, 표시 없음) 저장 → JPG q85 → media_upload.
2. 재채색(편집장 확인 후): `gpt_image_2_5`, 16:9, quality medium, 2k, role `image_references` = 바탕, **장당 1크레딧**, 시안 2장. 프롬프트(그대로):
```
Repaint reference image 1 as a hand-painted historical war-campaign map illustration. Keep the EXACT same coastline, islands, river courses, mountain positions, framing and black bars at top and bottom, pixel-aligned. Keep the same palette: ochre parchment lowlands, muted green highlands, blue sea, blue rivers. Improve only the terrain rendering: painterly relief shading of ridges and valleys like an illustrated atlas, subtle parchment paper texture, small stippled tree clusters on hills, soft painted sea with lighter shallow water near the coast and faint wave texture, rivers with darker banks. No text, no labels, no symbols, no borders, no roads, no new rivers, no compass, no frame.
```
3. **정렬 검수(필수)**: 1920×1080으로 줄여 땅/바다 마스크 IoU(파랑이 아니면 땅). **0.90 이상만 사용**(10/28 A안 0.931, B안 0.928). 미만이면 재생성. 표시 위치는 확대 크롭으로 확인.
4. 표시 얹기(m1v4.py `base(ai=...)`): AI 그림의 패널 부분만 붙이고 그 위에 bmap16 표시.
- 주의: AI 재채색도 고도 음영 바탕을 따르므로 산맥·고개가 뚜렷해지지는 않는다. 전투 설명 컷은 v4-S를 우선한다.

## 5. 표시 규칙 (bmap16 — 쇼츠 bmap3을 16:9로)
- 레터박스 2.39:1: 위 띠 왼쪽 = 연도 배지(금색 Jua), 아래 띠 = 자막(NotoSansKR Bold 46), 범례 = 패널 왼쪽 아래 크림색 상자, '개념도' = 오른쪽 위. 쇼츠 화면 틀은 history-battle-shorts 2절.
- 나라 마크 = 한글 원형 마크(r 52~58), 이름표 중복 금지(마크 안 글자만). 화살표 = 꼬리 가늘고 머리 굵은 곡선 + 흐르는 점선. 결과 = 효과(빨간 톱니/노란 폭발). 목책·성 = 성벽 기호.
- 나라색(임시, 컨셉 7-1과 맞춰 확정 필요): 백제 황금 (232,184,56) / 신라 주홍 (226,96,52) / 당 먹회색 (70,74,84) / **왜 = 일장기 빨강 (206,32,46)**(사용자 확정 10/29, 보라 금지) / 마한 연보라 (178,120,168) / 말갈 갈색 (118,86,62) / 낙랑 먹회색 (84,88,102).
- 영역: 옛은 면, 경계선 없이 흐리게. 국경선은 그 수의 이유일 때만 굽은 점선.
- **그리는 순서(10/31)**: 화살표·폭발 효과를 먼저, 나라 마크·이름표를 나중에 그린다. 화살표 머리가 나라 마크 글자를 덮으면 안 된다(오노성 편 지도 ①에서 '백제' 글자가 가려져 재렌더). 화살표 끝은 마크 테두리 바로 앞에서 멈춘다. 폭발 효과('열흘' 등)는 이름표와 겹치지 않는 빈 땅에.
- 위치 고증 메모(온조 편): 말갈 = 위례 북쪽 산간(연천·철원 방향) — 원문 13년 '北有靱鞉' [기록], 18년 칠중하 = 임진강 견해 [미확인], 실체·위치 여러 설 → 개념도. 위례(강북) 위치 여러 설 → 작은 영역 + 개념도. 웅천 = 굽은 점선 + 개념도. (660 백제 편) 탄현 위치 여러 설 → 개념도.

## 6. 검수 체크리스트
- 핵심 지형(고개·길목·들)이 한눈에 읽히나 / 산지가 조각나지 않고 큰 덩어리로 읽히나 / 떠 있는 물 조각 없나 / 강 하구가 바다와 한 물인가 / 강 위 도시·마크 위치가 기슭에 맞나 / 함대는 바다로 / 지명 3~4개·화살표 1~2개·요소 7개 이하 / 폰 크기(가로 400px)에서 마크·자막이 읽히나 / 지도 글자가 모두 내레이션에 나오나 / (AI를 썼다면) 해안선 IoU ≥ 0.90, 글자·기호·새 강을 그려 넣지 않았나.
- (전체 화면 쇼츠 지도) 지도 글자가 상단 제목 자리(y 약 200~520)와 자막 띠(y 1130~1610)에 걸리지 않나 / 화살표가 나라 마크 글자를 덮지 않나 / 효과가 이름표를 가리지 않나 — 동작이 끝나는 시점마다 프레임을 뽑아 본다.
- 보고마다: Claude는 움직임을 볼 수 없고 소리를 들을 수 없다 — 정지 프레임으로만 확인했다고 적는다.

## 7. 크레딧·시간
- v4-S는 전부 코드(0크레딧): 고도 타일+바탕 약 1분, 표시 포함 컷당 30~90초(sandbox 표준, 502 오류가 잦으니 background + 짧은 폴링).
- 전체 화면 지도 영상(10절): 6~7초 한 편에 약 1분(15fps).
- AI 재채색(선택): 장당 1크레딧, 편당 바탕 2~3장 × 시안 2 = 4~6크레딧.

## 8. 출처 표기 (설명란)
- '지도 자료 © OpenStreetMap 기여자(ODbL) · 고도 자료 AWS Terrain Tiles · 지도는 개념도이며 경계·위치는 학설에 따라 다릅니다.'

## 9. 자산
| 자산 | 위치 |
|---|---|
| 지도 키트 v2(롱폼: bmap3·bmap16·terrain·rivers_osm·m1v4·onjo_maps·폰트·geo·OSM 하천·M1 AI 바탕 A) | https://d2ol7oe51mr4n9.cloudfront.net/user_3Juf1bLtazzBl3p1xDJV2TokuBm/1f011f9e-6a0a-4d82-948d-ecfffa33b80b.zip |
| 쇼츠 전투 키트 v8(v4-S 코드: terrain3·mkbase·mkstyl·mkstyl_run·osm/geum.json·바탕 PNG·DEM) | https://d2ol7oe51mr4n9.cloudfront.net/user_3Juf1bLtazzBl3p1xDJV2TokuBm/f17675c8-7c38-4d0a-88d8-9ab35d32f509.zip |
| **오노성 편 키트(10/31: kit/*.py 전체 + mapvid.py, r/render.py v7.6·sprite.py·thumb.py·scenes.json·maps, sig/sigs.py, 그림·지도 영상·내레이션)** | https://d2ol7oe51mr4n9.cloudfront.net/user_3Juf1bLtazzBl3p1xDJV2TokuBm/97ecf09f-5fb5-4949-847a-ac55d6f19243.zip |
| v4-S 시안(660 백제 지역 지도, 채택) | https://d2ol7oe51mr4n9.cloudfront.net/user_3Juf1bLtazzBl3p1xDJV2TokuBm/63de47d9-8d21-4d51-a43a-7aa5b09ffd2a.jpg |
| 온조 M1 AI 바탕 A(job 23c8a8c2-0963-4d59-b6fe-0a8e0fad9570) | https://d8j0ntlcm91z4.cloudfront.net/user_3Juf1bLtazzBl3p1xDJV2TokuBm/hf_20261028_064222_23c8a8c2-0963-4d59-b6fe-0a8e0fad9570.png |
| 온조 M1 완성 시안 A(AI 방식, 표시 포함) | https://d2ol7oe51mr4n9.cloudfront.net/user_3Juf1bLtazzBl3p1xDJV2TokuBm/31a24197-55c7-4fa3-a5c8-764611f0a003.jpg |

- 키트 복구: sandbox에서 zip을 curl로 받아 푼다(`python3 m1v4.py out/ai0.png`로 AI 방식 M1 재현). 작업공간(Bash)에서는 cloudfront·higgsfield가 막혀 있으니 sandbox에서만.

## 10. 쇼츠 전체 화면 지도 영상 — mapvid.py (10/31 오노성 편에서 확정)
쓰는 때: 45초 신작·전투 해설 쇼츠에서 지도를 상자 안이 아니라 1080×1920 화면 전체에 깔고, 화살표·봉화·성 표시가 시간에 맞춰 나타나는 6~8초 영상이 필요할 때. 결과 mp4를 render.py scenes.json의 `"video"`로 넣으면 제목·연도 배지·워터마크·자막이 그 위에 얹힌다.

1. **전체 화면 트릭**: 다른 모듈을 import하기 **전에** bmap3의 패널을 화면 전체로 바꾼다.
```python
import bmap3 as B
B.PANEL = (0, 0, 1080, 1920)   # 반드시 from bmap3 import * · terrain3 · mkbase · mkstyl보다 먼저
from bmap3 import *
import terrain3, mkbase
from mkstyl import masks, highland_from_mask
PANEL = B.PANEL
B.NAT.update({'WAE': (206, 32, 46)}); B.MARK.update({'WAE': '왜'})   # 새 나라는 이렇게 등록
FPS = 15
```
   Map은 `Map(lon0, lon1, clat, box=PANEL)`로 만든다(위도 범위는 화면 비율로 자동).
2. **바탕**: `base(M, z, thr, sm=5, rivers=False)` = dem(z) → masks(thr, sm) → map_base → highland_from_mask (+ draw_rivers). 오노성 편 실제 값: 광역(한반도~규슈) `Map(125.6,131.3,34.8)` z7 thr300 하천 포함 / 해협 `Map(128.9,130.9,34.0)` z9 thr250 / 소지역(다자이후 평야) `Map(130.36,130.66,33.45)` z11 thr45 sm3.
3. **프레임 루프**: `render(name, M, bg, draw, dur)` — 매 프레임 `bg.copy()`에 `draw(d, t, im)`로 표시를 그리고 1080×1920으로 줄여 ffmpeg(libx264 crf17 veryfast yuv420p) 파이프로 `out/{name}.mp4`. 표시 함수는 시간 인자로 등장한다: `arrow(..., t0, t1)`(그려지는 구간), `burst(d, xy, r, text, at)`, `pk(t,a,b)`(0→1 진행률), `if t >= 1.9: d.text(...)`.
4. **표시 함수(mapvid.py에 있음)**: `label`(Jua 먹 글자 흰 테두리) · `water`(파란 바다 이름) · `beacon`(봉화, k로 크기 등장) · `fortmark`(빨간 원 성 표시 + 이름 + 부제, k<0.6이면 점만) · `capsule`(방어선 캡슐 띠, p로 그려짐) · `dashed`(점선 진로 + 화살 머리) · `boats`(작은 배) · bmap3의 `emblem`(나라 원형 마크)·`arrow`·`burst`.
5. **배치 규칙**: 상단 제목·배지 자리(y 약 200~520)와 자막 띠(y 1130~1610), 출처 줄(y 약 1508)을 비운다 → 핵심 표시는 y 550~1100에. 화면 중심(clat)을 옮겨 핵심 지점을 그 띠에 넣는다(오노성 편 소지역: clat 33.45로 기이성을 자막 위로 올림). 이름표가 화면 밖으로 잘리면 앵커를 바꾼다(`anchor='lm'`). 그리는 순서는 5절.
6. **검수**: 동작이 끝난 시점마다 `ffmpeg -ss t -frames:v 1`로 뽑아 405×720으로 본다. 고치면 그 지도만 `python3 mapvid.py m3`(함수 이름 인자)로 다시 만들고 전체 렌더.
7. 파일: 오노성 편 키트 zip(9절)의 kit/mapvid.py — m3(660 당 함대 → 하카타 위협), m5a(쓰시마·이키 봉화), m5b(미즈키·오노성·기이성·다자이후)가 예제.