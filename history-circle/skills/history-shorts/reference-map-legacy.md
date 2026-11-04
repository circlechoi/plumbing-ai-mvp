# history-shorts — reference-map-legacy.md (현행 규칙 · 필요할 때만 읽음 · 11/04 재구조화)

> history-core → SKILL.md를 먼저 읽는다. 이 파일의 규칙은 현행이다(원장과 다르면 원장 우선).

<!-- 원본 984–986줄 -->
### (대체용) 채색 지도 (v7: 코드 밑그림 + AI 재채색 + 코드 표지)
**원칙**: 지형(해안선·강·산지 위치)은 코드가, 그림체는 AI가, 표지·경로·글자는 다시 코드가 맡는다. AI에게 지도를 처음부터 그리게 하지 않는다(해안선이 틀어짐). **사용자가 승인한 한반도 지도(L-5의 korea_full)의 그림체를 채널 표준으로 고정**하고, 새 지도는 항상 그 지도를 두 번째 참조 이미지로 넣어 그림체를 맞춘다(사용자 결정, 2026-09-28).


<!-- 원본 987–993줄 -->
### L-1. 언제 쓰나
- 전체 조망: 이야기의 무대가 한반도 어디인지(도읍·주요 도시 표시)
- 이동: 인물·집단의 이동, 천도, 원정 경로(점선 화살표)
- 영역: 나라·세력의 대략적 범위와 그 변화(근거 있을 때만)
- 방위 설명: 사료가 동서남북을 말할 때 방향 라벨만 달고 구체 지명은 단정하지 않는다
- 근거: 유적 위치(예: 풍납토성)를 확대해 표시


<!-- 원본 994–1003줄 -->
### L-2. 지도 고증 규칙
- 도시·유적 위치는 비정(比定) 근거가 있는 곳만 찍고 부제에 등급을 단다: `[통설] 서울 풍납토성`, `[추정] 북한산 인수봉 부근`, `[여러 설] 인천 또는 아산`. `[미상]`이거나 `[여러 설]`이 넓게 갈리면 점을 찍지 않고 '?' 라벨·개념 경로만(예: ⑤ 부여).
- **위치 미상인 나라를 그래도 보여 줘야 할 때(v7.6, ⑨ 사용자 결정 — 점선 원이 아니라 '지도에 색칠하듯 영역으로')**: 점·경계선 없이 **번지는 색칠 영역 + `이름 ?` 글자**(`regions`, `alpha` 0.5)로 '이 근처 어딘가'만 전한다. 위치·크기는 화면 배치상의 임의 선택임을 note("○○은 위치 미상(임의 표시)")와 설명란에 밝힌다. 다른 표지·경로·제목과 겹치지 않는 쪽에 둔다(⑨ 황룡국: 졸본 서쪽)
- 확인된 좌표(현대 위치): 풍납토성 127.117E 37.528N / 미추홀(인천 일대, 통설) 126.67E 37.44N / 부아악(추정) 126.99E 37.66N / 졸본=환런 오녀산성(통설, 위키백과 근거라 공식 DB 재확인 필요) 125.417E 41.328N / 석촌동 고분군(근사) 127.104E 37.502N / 국내성=지안 일대(통설, 근사 좌표·재확인 필요) 126.18E 41.12N
- 부여 도읍: 통설은 지린시 동단산·남성자 일대(경향신문 보도 기준)이나, 대소의 부여(동부여 포함) 위치는 [여러 설] → ⑤에서는 점 없이 북쪽 '?'에서 내려오는 개념 경로만
- 영역(regions)은 근거 문헌·교과서·백과사전 지도에서 확인한 범위만. 근거를 못 찾으면 영역을 그리지 않고 도시 점만 쓴다(예외: 바로 위 '위치 미상' 표시 — 반드시 `?`와 임의 표시 고지를 붙인다).
- 현대 국경선은 그리지 않는다(AI 프롬프트에도 금지). 현대 지명은 부제에만('지금의 ○○').
- 해안선·강은 **현대 기준**이고 **산 표현은 과장**이다. note와 설명란에 밝힌다. 개념적인 경로는 '경로는 개념도'.
- 핵심 표지·경로는 줌이 끝난 화면 기준 y 500~1100 안에 오게 center/span_lat/zoom/focus를 잡는다. note는 화면 고정 문구(y 550, 오른쪽 정렬).


<!-- 원본 1004–1019줄 -->
### L-3. spec 형식 (ep/m_이름.json) — anim.py 입력
```json
{"out":"maps/m_korea.png","center":[126.4,38.8],"span_lat":15.2,"zoom":1.5,
 "markers":[{"name":"위례성","sub":"[통설] 서울 풍납토성","lon":127.117,"lat":37.528,"main":true,"side":"r","at":2.4}],
 "routes":[{"pts":[[125.42,41.15],[126.2,39.6],[127.02,37.66]],"label":"남쪽으로","at":0.8,"dur":1.5}],
 "regions":[{"name":"…","poly":[[lon,lat],…],"color":[150,70,40],"label_at":[lon,lat],"size":76,"alpha":0.3,"at":0.2,"dur":1.3}],
 "labels":[{"text":"?","lon":126.75,"lat":39.55,"size":170,"color":[170,38,32]}],
 "note":"위치는 통설 기준 · 경로는 개념도 · 현대 해안선"}
```
- **center/span_lat은 배경으로 쓸 AI 지도의 밑그림(ctl.py spec)과 반드시 같아야** 표지가 제자리에 온다. L-5 라이브러리의 값을 그대로 복사한다.
- center=[경도,위도], span_lat=화면 세로 위도 폭(한반도+요동 약 15.2, 지역 확대 약 3, 도성 주변 약 0.6). side: r/l/u/d. `at`·`dur`: 장면 시작 후 등장 시각·그려지는 시간. route `color` 기본은 붉은색, 개념 경로는 회갈색 [110,100,90].
- ⑤ 예시(korea_full 재사용, 부여→졸본 개념 경로): `{"out":"maps/m_ep5.png","center":[126.4,38.8],"span_lat":15.2,"zoom":1.55,"markers":[{"name":"졸본","sub":"[통설] 환런 오녀산성 일대","lon":125.417,"lat":41.328,"main":true,"side":"r","at":0.2}],"routes":[{"pts":[[126.6,43.7],[126.1,42.6],[125.55,41.55]],"color":[110,100,90],"at":0.5,"dur":1.6}],"labels":[{"text":"?","lon":126.75,"lat":43.95,"size":130,"color":[170,38,32]}],"note":"부여 위치는 여러 설 · 경로는 개념도"}`
- ⑧ 예시(부여→국내성, 나머지는 ⑤와 같음): marker `{"name":"국내성","sub":"[통설] 지안 일대","lon":126.18,"lat":41.12,"main":true,"side":"r","at":0.2}`, route pts `[[126.6,43.7],[126.45,42.5],[126.25,41.35]]`
- ⑨ 예시(국내성·졸본 + 황룡국 영역, 제목에 안 가리게 초점을 북쪽으로): `{"out":"maps/m_ep9.png","center":[126.4,38.8],"span_lat":15.2,"zoom":1.45,"focus":[125.5,42.5],"markers":[{"name":"국내성","sub":"[통설] 지안 일대","lon":126.18,"lat":41.12,"main":true,"side":"r","at":0.2},{"name":"졸본","sub":"[통설] 환런","lon":125.417,"lat":41.328,"side":"d","at":0.9}],"routes":[{"pts":[[126.6,43.7],[126.45,42.5],[126.25,41.35]],"color":[110,100,90],"at":0.5,"dur":1.6}],"regions":[{"name":"황룡국 ?","poly":[[123.9,41.3],[124.2,42.0],[124.8,42.2],[125.15,41.85],[125.1,41.4],[124.7,41.0],[124.2,40.95]],"color":[196,140,20],"label_at":[124.55,41.55],"size":70,"alpha":0.5,"at":1.6,"dur":1.2}],"labels":[{"text":"부여 ?","lon":127.35,"lat":42.9,"size":100,"color":[170,38,32]}],"note":"황룡국은 위치 미상(임의 표시) · 부여는 여러 설 · 경로는 개념도"}`
- 가까운 표지 둘(졸본·국내성)은 글자 방향을 다르게(`side` d / r), 부제는 짧게 — 길면 옆 표지와 겹친다. 줌이 끝난 화면에서 라벨이 제목(y 300~470)·note(y 550) 뒤로 가지 않게 `focus`·`zoom`을 조절하고 PREVIEW로 확인한다


<!-- 원본 1020–1048줄 -->
### L-4. 새 지도 만들기 (라이브러리에 같은 범위가 없을 때)
1. 밑그림: `{"center":[경도,위도],"span_lat":폭,"blur":4}`로 ctl.py 실행 → `ctl_이름.png`(1152x2048, 해안선·강·고지 갈색, 글자 없음) + `ctl_이름_land.png`(검수용). 산이 조각나 보이면 `blur` 10
2. `media_upload`(png) → sandbox에서 PUT → `media_confirm(type:image)`
3. `get_cost`로 비용 확인(high 2k 2.75) 후 `generate_image`/`generate_image_batch`: `model gpt_image_2_5`, `quality high`, `resolution 2k`, `aspect_ratio 9:16`, `medias: [{value: 밑그림 media_id, role: image_references}, {value: 0cf3c69c-be10-429f-be94-719b2d8b5f5a, role: image_references}]`(두 번째 = 표준 그림체)
4. 검수: `python3 qa.py ai.png ctl_land.png overlay.jpg` → 해안선 ±40px 일치율·IoU·최적 이동. 기준: IoU ≥ 0.88이고 최적 이동이 (0,0,1.0) 근처. 참고로 정확한 코드 지도의 IoU도 0.905가 상한(분류기 한계). 바다가 5% 미만인 지도는 수치 무의미 → 사용자 눈 확인
5. 통과하면 겹침본(overlay.jpg)을 업로드해 사용자에게 링크로 보여 주고, L-5 라이브러리에 추가

**좁은 범위(span_lat < 2) 하천 지도(v7.1)**: Natural Earth 1:10m 하천 선은 도시 규모에서 수 km 어긋난다(한강·송파 일대 약 2km). 서울 한강은 `han_mask.py`(통계청 행정동 경계 — 한강 양안 구 경계 = 중심선, 폭 1km)로 하천 면을 만들고 ctl spec에 `"water_mask":"kr/han_mask.png","ne_rivers":false`. 재채색 프롬프트는 "STRICTLY PRESERVE the exact course, position, bends and width of the blue river band … do not widen it" 문구 사용. AI가 강을 옮기거나 넓히므로 **생성 후 반드시 `fix_river.py`로 보정**(마스크 밖 물 → 땅색, 마스크 안 땅 → 물색, 새 강둑 먹선). 표지와 물 사이 거리를 출력해 확인(풍납토성 0.5km 이상, 석촌동 2km). 다른 강은 같은 방식으로 경계 데이터를 찾아 적용(근거 확인 후).
- 행정동 경계 다운로드(약 35MB): `curl -sSfL -o kr/hjd.geojson https://raw.githubusercontent.com/vuski/admdongkor/master/ver20260701/HangJeongDong_ver20260701.geojson`

**재채색 프롬프트(표준)** — 참조 1 = 밑그림, 참조 2 = korea_full:
```
Reference image 1 defines the geography. Reference image 2 defines the painting style; match its palette, brushwork, paper texture and mountain rendering exactly. Do not copy any geography from reference image 2.
Repaint reference image 1 as an elegant hand-painted illustrated map, like a premium museum exhibition map of ancient Korea.
STRICTLY PRESERVE the exact coastline shapes, island positions, river courses and framing of reference image 1. Do not move, add or remove any landmass, island or river. Keep the same image boundaries and scale. Change only the painting style.
Style: traditional Korean mineral-pigment painting meets modern editorial cartography. Soft layered watercolor washes on warm hanji paper, fine confident ink linework along coastlines, rivers as luminous turquoise-blue ribbons, slightly thicker than reality.
Terrain: {지형 문장}
Sea: layered watercolor gradient from deep teal near the coast to pale jade offshore, faint brush-drawn wave patterns, a soft rose-pink watercolor bleed fading at the outer edges of the paper.
Light: gentle light from the upper left, subtle depth, airy and refined, uncluttered.
Composition: vertical 9:16. Keep the top 20% and bottom 30% calmer and lighter with less detail, reserved for titles and subtitles.
Avoid: any text, letters, labels, place names, numbers, compass rose, legend, scale bar, frame, grid lines, modern borders, roads, cities, buildings, people, photorealism, 3D-render look, neon or oversaturated colors.
```
{지형 문장} 선택:
- 넓은 범위(기본, korea_full에 쓴 문장): `dramatically exaggerate the mountain ranges only where reference image 1 shows high ground (brown areas). Layered painted peaks in the Korean jingyeong-sansu manner: sharp granite ridges, sunlit faces in ochre and warm umber, shaded faces in blue-green (cheongnok), forested feet, thin mist drifting in the valleys. Lowlands in pale celadon green and soft wheat tones.`
- 산악 확대: `a dense sea of rugged painted peaks with deep shaded gorges, only where reference image 1 shows high ground (brown areas); … The river winds through the valley as a bright turquoise ribbon catching light.`
- 강 유역·도성: `broad fertile river plain with low rounded hills in soft celadon green and wheat tones, scattered groves of trees … The river is the hero: wide, luminous turquoise, gently reflecting the sky, painted slightly wider than the reference line. No tall mountains.` (Avoid에 `bridges` 추가)
- 분위기 변주: Light 줄을 `warm golden dawn glow from the east, long soft shadows` 또는 `dim stormy dusk, deep indigo shadows, dramatic but still painterly`로
- korea_full 자체를 만들 때(참조 이미지 1장)는 첫 줄 없이 `Repaint reference image 1 as …`로 시작했다


<!-- 원본 1049–1059줄 -->
### L-5. 승인 지도·이미지 라이브러리 (재사용 — 같은 범위면 새로 만들지 않는다)
| 이름 | center | span_lat | 용도 | job_id(참조용) | 검수 |
|---|---|---|---|---|---|
| **korea_full**(표준 그림체) | [126.4, 38.8] | 15.2 | 한반도+요동 전체, 이동 경로 | 0cf3c69c-be10-429f-be94-719b2d8b5f5a | 해안 0.93 / IoU 0.905 / 이동 없음. **사용자 승인 2026-09-28**. ④~⑨ 사용 |
| jolbon | [125.6, 40.9] | 3.2 (blur 10) | 졸본·압록강 중류 확대 | ce1e57c0-ad09-4799-82a5-4ced4993e960 | 바다 2%라 수치 무의미 → 강 위치 사용자 확인 필요 |
| ~~hangang v1~~ | [127.11, 37.53] | 0.6 | (폐기) | 7046cb1c-4060-4ddb-8ef3-5289e9d1971b | Natural Earth 강 선 오차로 풍납토성·석촌동이 강 위에 찍힘 → 사용 금지 |
| **hangang v2** | [127.11, 37.53] | 0.6 | 한강 하류·풍납토성·석촌동 | 306a4f0d-c779-4be6-a4b2-51e0322cdeef → fix_river 보정본 사용 | 보정 후 하천 IoU 0.93, 풍납토성→물 0.53km, 석촌동 2.12km. 밑그림 media ad29611c-3177-4c7e-80cc-d0f07f69ea2d |
- 원본 URL: `https://d8j0ntlcm91z4.cloudfront.net/user_3Juf1bLtazzBl3p1xDJV2TokuBm/` + korea_full `hf_20260928_141112_0cf3c69c-be10-429f-be94-719b2d8b5f5a.png` / jolbon `hf_20260928_142223_ce1e57c0-ad09-4799-82a5-4ced4993e960.png` / hangang v2 원본 `hf_20260929_100822_306a4f0d-c779-4be6-a4b2-51e0322cdeef.png`(fix_river 필요)
- 재사용 가능한 인물·상징 이미지(같은 URL 접두사): 소서노 `hf_20260928_142220_9d22020e-6c0f-43bb-a34d-f18a257aaa5c.png` / 유리 `hf_20260928_142221_88585b52-38af-43d0-83da-f7cb71cc68bb.png` / 대소(왕, 흰옷·모피) `hf_20260929_120717_ca45658a-f413-4e8d-a25b-edf690f21412.png` / 대소(왕자, 궁에서 내려다봄) `hf_20260929_120714_806b8396-9a73-4714-9a56-918333b9cfff.png` / 부러진 칼 `hf_20260929_120715_4804c874-3b9a-49ad-8169-8ee311b494a8.png` / 절벽 위 궁수(주몽) `hf_20260929_120715_26e57762-3b09-41f6-aec6-f8112bed0165.png`, 그 움직이는 컷 `hf_20260929_121307_7e6ab8fb-b9fd-44d8-bda9-66ed2db4b540.mp4` / 능선 위의 소년(무휼 예고) `hf_20261001_140131_69935699-25de-4e19-87cd-c60147fc7391.png` / 눈보라 속 부여 대군 `hf_20261001_140132_d1a4873f-255c-4dd7-92d5-f0a86fdb6633.png` / 눈 마당의 어린 무휼과 부여 사신(⑧ 첫 장면, 새 의상 색) `hf_20261002_231619_880508d2-c0df-479e-81c2-4615f17c867a.png` / 쌓아 올린 알 `hf_20261002_231121_55302458-cdc7-45ad-924b-133edb19cee8.png` / ⑨ 활을 꺾는 해명(첫 장면, job 24424c0a-0713-4803-b6e2-8b5377e25519) `hf_20261003_182946_24424c0a-0713-4803-b6e2-8b5377e25519.png`, 그 움직이는 컷 `hf_20261003_183128_a106fe6f-4838-4af3-b5a6-f3ae21e7961e.mp4` / 눈밭의 칼과 무릎 꿇은 해명 `hf_20261003_182132_8ca81607-732b-4442-bf54-bec03fe6f476.png` / 떠나는 아들을 보는 유리왕 `hf_20261003_181705_f5ce6724-8769-442d-9dde-309e8874569d.png` / 들판의 창과 달려오는 말 `hf_20261003_181706_8d5d150d-b1a1-4474-8098-b69ca0123a99.png` / 성벽의 왕과 주인 없는 말 `hf_20261003_181704_191d7344-c40b-409e-b98e-348dd17cb8fb.png` / 빈 왕좌 `hf_20261003_181704_f141a140-445f-4224-8ab8-08baab606268.png`
- 새 지도를 만들면 이 표에 한 줄 추가한다(이름·범위·job_id·검수 결과·사용자 확인 여부)


<!-- 원본 1060–1295줄 -->
### L-6. 스크립트
ctl.py (밑그림, v7.1 water_mask 지원):
> 〔코드 48줄(원본 1062–1111줄) → `history-circle/kit/map/ctl.py` — 같은 내용이 kit에 그대로 있음(verify_skills.py)〕
qa.py (해안선 검수):
> 〔코드 42줄(원본 1113–1156줄) → `history-circle/kit/map/qa.py` — 같은 내용이 kit에 그대로 있음(verify_skills.py)〕
anim.py (표지·경로·라벨 좌표 계산):
> 〔코드 34줄(원본 1158–1193줄) → `history-circle/kit/map/anim_shorts_map.py` — 같은 내용이 kit에 그대로 있음(verify_skills.py)〕
- 실행: `python3 anim.py ep/m_*.json` → `maps/m_*.anim.json`(및 영역이 있으면 `.layer.png`)

han_mask.py (서울 한강 정밀 하천 마스크, v7.1):
> 〔코드 43줄(원본 1197–1241줄) → `history-circle/kit/map/han_mask.py` — 같은 내용이 kit에 그대로 있음(verify_skills.py)〕
- 실행: `python3 han_mask.py ep/m_hangang.json kr/han_mask.png 1152 2048 1.0` (spec의 markers가 있으면 강까지 거리 출력)

fix_river.py (AI 재채색 결과 하천 보정, v7.1):
> 〔코드 47줄(원본 1245–1293줄) → `history-circle/kit/map/fix_river.py` — 같은 내용이 kit에 그대로 있음(verify_skills.py)〕
- 실행: `python3 fix_river.py ai_hangang.png kr/han_mask.png ai_hangang_fix.png` → 결과를 scenes.json 지도 장면 `image`로
