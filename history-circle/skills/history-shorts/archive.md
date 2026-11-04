# history-shorts — archive (원문 보관 · 11/04 재구조화)

> 이 파일은 **규칙으로 따르지 않는다.** 폐기·보류·편별 이력·변경 이력·교체 전 원문을 줄 그대로 보관한다. 현행 값은 원장(history-core).

## 교체 원문 (원장 반영으로 SKILL.md에서 바뀐 줄)

- 원본 6줄:

# 역사 숏폼 제작 파이프라인 (채널 표준 v8.1 · 2026-10-23 스킬 정비 · 두 형식: 롱폼 재편집 + 45초 신작 · 지도 v3 · 시그니처 3초 · 도트 필수)

- 원본 8줄:

> **우선순위(10/23 확정)**: 스킬끼리 충돌하면 **날짜가 붙은 최신 사용자 결정**을 따른다. 날짜가 같거나 없으면 history-channel-concept > history-longform · history-architecture-shorts > history-shorts. 작업 중 낡은 문장을 발견하면 그 문장을 따르지 말고, 사용자에게 알리며 고칠 곳을 제안한다.

- 원본 36줄:

4. **지도를 자주 쓴다.** 시청자가 도시 위치·나라 영역·이동 경로를 파악할 수 있도록 매 편 지도 장면을 넣는다(섹션 L, v8.0 표준은 지도 v3 — L-0).

## 머리말에서 옮긴 줄

<!-- 원본 10줄 · 머리말의 버전별 변경 이력(v6~v8.1) -->
v8.1 변경(2026-10-23, 스킬 정비 — 사용자 답): ① 충돌은 최신 날짜 결정 우선(위 문단) ② **도트 매 편 1곳 필수**(concept 7-3, 10/17 — 아래 v7.6⑤·v7.7① 폐지) ③ 내레이션 기본 = '합니다'체 + '~죠/~요' 대화체, 평서 '~다.' 0회(D-2) ④ 설명란 = 10/19 사용자 양식으로 쇼츠 전체 통일, 깨알 정보 줄 삭제(J) ⑤ 재편집 화면의 제목·연도 배지·워터마크를 신작 표준과 통일, 자막은 1줄 방식 유지(M-4) ⑥ Kling `sound: "off"` 문자열(F-4) ⑦ A '이야기 사슬'은 곁가지 후보 발굴 도구(채널 구조는 concept 8-1) ⑧ 진행 상황 갱신(A-4) ⑨ 지도 핵심 표지 = 붉은 원 markers, 인장은 이름표에만(L-0) ⑩ 태그 = concept 5-1 마스터 표(C-2)

<!-- 원본 15줄 · 머리말의 버전별 변경 이력(v6~v8.1) -->
v8.0 변경(2026-10-12, 사용자 결정 — 롱폼 스킬 v2.0과 채널 컨셉 v0.6에서 쇼츠에 쓸 내용을 옮김): ① **두 형식 병행** — 롱폼마다 재편집 하이라이트 3~5편(M, 10/7 대무신왕 1부 5편 방식) + 롱폼에 없는 곁가지는 45초 신작(B~L) ② **채널 컨셉 우선** — 기획·대본 전에 `history-channel-concept`을 먼저 읽는다: '그 판단은 왜 그랬을까?', 상대를 바보로 그리지 않기, 라디오 기준, 신이한 기사의 현대식 재해석, 역사적 상상력(A-0) ③ **신작 그림체는 청록산수 유지**(사용자 선택). 의상 색·피아 색 구분·진창·진영 규모는 롱폼 기준(E) ④ **시그니처 3초 축약판** — 신작 첫 장면 = 수묵 스틸 → 먹 번짐 → 같은 구도의 움직이는 실사 컷, 제목은 처음부터(D-1, F-5) ⑤ **지도 v3로 통일** — 지형 음영 + 지형(분수령) 국경 + 진한 저채도 세력 색, 1세기 초 고구려는 동해에 닿지 않음(L-0). AI 재채색 지도(korea_full)는 도시 위치·이동 경로만 보일 때의 대체용 ⑥ **내레이션 작법** — 롱폼 D-1의 '설명하듯 잇기'를 45초에 맞게(D-2) ⑦ **음향** — 효과음 mirelo 생성 가능, 음량은 RMS 기준, BGM은 사용자 Suno 곡(F-6) ⑧ **작업 규칙** — 매 보고에 '움직임을 볼 수 없고 소리를 들을 수 없음' 명시(A-0), 롱폼에서 겪은 sandbox 규칙(G), 한글 고유어 오타 확인(H) ⑨ 고증 태그를 롱폼과 맞춤([상상]·[연출] 추가, C-2).

<!-- 원본 17줄 · 머리말의 버전별 변경 이력(v6~v8.1) -->
v7.7 변경(2026-10-04, 사용자 결정 — 렌더러는 v7.6 그대로): ① **도트·깨알 요소는 선택 사항**(v8.1에서 폐지 — 도트 필수) — 기본은 넣지 않는다. 편의 분위기에 맞고 넣을 이유가 분명할 때만 구성 확인 단계에서 선택지로 제안하고, 사용자가 승인한 편에만 넣는다(D-1). 설명란 '깨알 정보' 줄도 해당 사항이 있을 때만(J) ② **편성 순서 변경** — 숏폼 ⑩ 이후는 롱폼과 내용이 겹치므로 **롱폼 3부작을 먼저 만들고, 숏폼은 완성된 롱폼 내용으로 이어간다**(A-4, A-5).

<!-- 원본 19줄 · 머리말의 버전별 변경 이력(v6~v8.1) -->
v7.6 변경(2026-10-04, ⑨ 제작 중 사용자 결정): ① **제목 서체 = 본고딕 Black**(검은고딕은 획 많은 글자가 가늘게 보임, D-3) ② **설명란 표준 양식 + '깨알 정보' 한 줄**(J, 깨알 정보는 선택) ③ **[해석] 태그** — 사료에 없는 의미 부여는 '~듯/~로 읽힌다'로만(C-2) ④ **위치 미상인 나라는 점 대신 색칠 영역 + '?'**(L-2) ⑤ **깨알 도트(선택 사항 — 기본은 넣지 않음, v7.7 · v8.1에서 폐지 — 도트 필수)** — 자체 제작 도트 스프라이트가 한 장면을 지나감(sprite.py, G-4) ⑥ **첫 장면 = 전경 액션 클로즈업, 구도가 다른 후보 2~3장을 비교해 고름**(E, F) ⑦ **끝맺음 대안: 시청자에게 묻는 질문**(D-1) ⑧ 대본은 사용자가 직접 고쳐 쓰는 일이 많다 → 사용자 문장을 살리고 고증·비문만 고친다(B) ⑨ 렌더 메모리 초과 방지(48프레임 묶음)와 업로드 전 파일 검증(G).

<!-- 원본 21줄 · 머리말의 버전별 변경 이력(v6~v8.1) -->
v7.5 변경(2026-10-03, ⑥·⑦ 공개 후 사용자 피드백): ① **자막 확대** 1줄 60 / 2줄 80(마지막 84) ② **제목을 영상 내내 표시** — 첫 장면 뒤 80%로 줄어 상단(y 392)에 고정 ③ **템포를 늦춤** — 8~9장면, 장면당 4.5초 이상, 같은 그림 재확대 컷 금지 ④ **끝 여운 단축** — "다음 이야기에서"를 읽지 않고 자막으로만, 마지막 단어 뒤 0.6초에 종료 ⑤ **'~다, ~다' 반복 금지** 문체 규칙(D-2) ⑥ 주제 '뻔함 필터'(A-2)와 조회 지표 기록(H) ⑦ **롱폼과 같은 의상 색 포인트**(고구려 붉은색 / 부여 흰색+검은색)와 **밝고 강한 첫 장면**(E).

<!-- 원본 23줄 · 머리말의 버전별 변경 이력(v6~v8.1) -->
v7 변경(2026-09-28, 사용자 요청): ① 지도 = 코드 밑그림(ctl.py) → gpt_image_2_5가 그림체만 다시 칠함 → 해안선 자동 검수(qa.py) → 표지·경로·글자는 코드(anim.py + render.py). **사용자가 승인한 한반도 지도의 그림체를 채널 표준으로 고정**(L-5 라이브러리) ② 이미지 STYLE을 무채색 → 청록산수 채색으로, 해상도 1k → 2k ③ 지도 라벨을 원본 좌표계에 그려 줌 중 글자 떨림 제거 ④ 자막을 실제 잉크 폭 기준으로 중앙 정렬(『』·[ ] 쏠림 해결) ⑤ 내레이션을 흥나는 이야기꾼 문체로(D-2) ⑥ 렌더 그레이딩: 채도↑·대비↑·따뜻한 하이라이트/청록 그림자.

<!-- 원본 24줄 · 머리말의 버전별 변경 이력(v6~v8.1) -->
v7.4 변경(2026-09-29, ⑤ 제작 후 사용자 결정): ① 내레이션 **Harrison 다큐체 확정**(D-2, F-2) ② 연도 배지 = **붉은 낙관 '史' + 금색 글자, 배경 상자 없음, ◀▶ 없음**(D-3) ③ **영상 화면의 시리즈 표시 제거**, 워터마크는 우상단 '역사서클' 글자만 ④ 움직이는 컷 `video` 필드·효과음 없는 컷 구현(F-4, G-2) ⑤ 업로드 제목은 시리즈명·편 번호 유지(J, 화면 표시만 제거).

<!-- 원본 26줄 · 머리말의 버전별 변경 이력(v6~v8.1) -->
v7.3 변경(2026-09-29, 사용자 요청): ① **서사 설계 강화** — 장기 아크(A-5)와 대본 서사 점검표(D-0: 핵심 메시지 한 문장, 문장 간 인과, 시대 소급 금지) ② 첫 장면 규칙 — 상단 제목(검은고딕, 흰색+금색, 첫 장면만) + 지도 대신 강렬한 장면 + 첫 문장이 곧 질문 ③ 하이브리드 자막(2줄 유지 + 핵심 대목 중앙 '펀치' 3~4회) ④ 채널 워터마크(로고 + '역사서클') ⑤ 컷 템포 약 2~2.5초(효과음 없는 확대 컷) ⑥ 움직이는 컷(Kling v3.0) 편당 1~2개, 생성 전 사용자 검수 ⑦ 좁은 범위 하천 정밀화(han_mask.py·fix_river.py, v7.1) ⑧ 내레이션을 Kings and Generals식 다큐 내레이터로 전환 검토(D-2).

<!-- 원본 27줄 · 머리말의 버전별 변경 이력(v6~v8.1) -->
v7.1(2026-09-29): 한강 지도에서 풍납토성·석촌동이 강 위에 찍히던 오류 수정 — Natural Earth 1:10m 하천 선이 송파 일대에서 약 2km 어긋남 → 행정경계 기반 하천 + AI 결과 보정.

<!-- 원본 28줄 · 머리말의 버전별 변경 이력(v6~v8.1) -->
v6 변경: 세이프존 레이아웃, 지도 애니메이션, 장면별 카메라·전환, 효과음 합성, render.py(8코어 병렬).

## 〔원래 위치: 원본 75–91줄〕 A-4. 사슬 진행 상황 (2026-10-12 기준)
> 이동 이유: 10/12 기준 진행 현황(편별 이력)

### A-4. 사슬 진행 상황 (2026-10-12 기준)
- (10/23) **지표는 history-production-standards 8절 '성과 장부'에 기록한다.** 아래 편별 지표 서술은 10/4까지의 기록이며 더 늘리지 않는다
- 백제 ① 온조, 한강에 백제를 세우다 — 20초판만 있음, 45초 재제작 대기(건국 연대 BC 18은 '기록상 연도', 3세기 후반 건국설 있음)
- 백제 ② 왜 하필 한강이었을까? — 완료(43초)
- 백제 ③ (사용자 제작 완료, 제목은 사용자 확인 필요)
- 백제 ④ 온조는 왜 고구려를 떠났을까? — **v7.1 완료**(44초, 한강 지도 수정본). 결말에서 '주몽은 왜 유리를 골랐을까?' 예고
- ⑤ 고구려, 주몽 혼자 세웠을까? — **완료**(45.4초, 2026-09-29, 첫 다큐체·Harrison 음성·첫 움직이는 컷). 핵심: 부여를 등진 주몽 무리 + 졸본 세력의 결합, 대소와의 대립 시작. 연도 배지 BC 6(대소의 인질 요구, 유리왕 14년)은 사료 DB 재확인 필요. 이 편까지는 화면에 시리즈 표시·◀▶ 배지(v7.3 양식)
- ⑥ 주몽은 왜 유리를 택했을까? — **완료**(43.2초, 2026-09-30, v7.4 양식 첫 적용). 기록상 이유는 '큰아들 증표(부러진 칼)'뿐, 친아들 아님 견해는 한 문장 + 설명란. **성과 부진**: 게시 24시간 유효 조회 210, 계속 시청 43.5% / 이탈 56.5%, 평균 시청 1:09(본 사람은 반복 시청) → 내용이 아니라 주제·첫 화면에서 넘겨짐
- ⑦ 부여는 왜 고구려를 바로 없애지 못했을까? — **완료**(45.6초, 2026-10-01). 유리왕 14년(기록상 BC 6) 인질 교환 요구 → 태자 도절 거부 → 5만 침공 → 큰 눈으로 퇴각(한국민족문화대백과 '대소'로 확인) + 『삼국지』 동이전 지형·사출도([추정] 해석). 14장면이라 "그림이 너무 빨리 지나간다"는 피드백 → v7.5. **지표**: 게시 약 2일 유효 조회 824, 계속 시청 61.1% / 이탈 38.9%, 평균 시청 1:19 → ⑥ 대비 계속 시청 +17.6%p(주제 비틀기 효과로 추정)
- ⑧ 부여 왕의 협박에 맞선 게 6살 왕자라고?(유리왕 28년, 기록상 AD 9) — **완료**(43.7초, 2026-10-03, v7.5 첫 적용: 9장면, 337자 42.9초 = 초당 7.9자, 지도는 국내성 표지). 무휼은 서기 4년생(한국민족문화대백과 '대무신왕') → 세는나이 6세, 원문 '年尙幼少'. 알을 쌓는 비유(今有累卵於此), 부여 노파의 풀이. 결말에서 '4년 뒤 대소의 군대' 예고. 사용자 반응 "좋았어". **지표**: 게시 약 6시간 유효 조회 636, 계속 시청 62.6% / 이탈 37.4%, 평균 시청 0:48(초기 수치 — ⑦보다 반복 시청이 적음, 24시간 뒤 재확인)
- ⑨ 활 하나 꺾었다고 태자가 죽어야 했다고?(해명태자, 기록상 AD 8~9) — **완료**(45.16초, 2026-10-04, v7.6 첫 적용: 8장면, 약 300자 44.4초 = 초당 6.7자). 사용자 요청으로 '사건'이 아니라 **외교 문제**(굽힐 것인가 맞설 것인가)로 구성. 근거: 한국민족문화대백과 '해명'(책봉 AD 4, 졸본 잔류, 황룡국 왕의 활을 꺾음, 유리왕이 황룡국에 죽여 달라고 청함, 황룡국 왕은 죽이지 못함, AD 9 칼을 내려 자결 명령, 여원 동쪽 들에서 창에 찔려 죽음, 창원). 나이 21세·대사는 위키백과 인용(원문 미확인, 생몰년 BC 12~AD 9와는 일치). '복종하라는 활'·'외교 마찰'은 [해석](나무위키 각주 수준 — 설명란 고지). 황룡국 위치는 [미상] → 졸본 서쪽에 임의 색칠 영역. 6번 장면에 도트 기마 무사. 끝은 시청자 질문("여러분이 왕이었다면…"), 다음 편 예고는 고정 댓글. 크레딧 약 21.6(첫 장면 후보 8장 포함)
- **⑩ 이후 (2026-10-23 갱신)**: 롱폼 대무신왕 3부작 완성(1부 10/6 · 2부 10/14 · 3부 10/17). 재편집 숏츠: 1부 5편(10/7 — ① 예고편 0:00–0:57 ② 열 살에게 맡겼다고? ③ 매복을 길가에 안 숨겼다고? ④ 대군이 한 줄로 갇혔다고? ⑤ 붉은 까마귀), 2부 5편(history-longform 0번), 3부 진행(설정 백업 history-production-standards 4절). 신작: 온조 비트 예고편 v2(10/20, 음악만 — standards 5절). 건축: 「고구려 수도에 성이 두 개였다고?」(10/14) · 온돌 편(10/19, history-architecture-shorts). 업로드 여부·지표는 미기록 → 다음 작업 때 사용자에게 받아 적는다. 다음 롱폼 = 백제 온조(마한 병합). 롱폼 진행 상황은 history-longform 0번이 기준
- 학반령 매복·붉은 까마귀는 재편집으로 냈으므로 신작으로 다시 만들지 않는다. 사용자가 "다음 숏폼"을 요청하면 ① 새로 완성된 롱폼이 있는지(있으면 재편집) ② 없으면 곁가지 신작 후보를 낸다
- 곁가지 후보(롱폼과 겹치지 않는 것 — 사용자가 원할 때만): 돼지가 고른 수도(유리왕 21~22년 국내 천도), '하구려'로 불린 나라(왕망과의 충돌, 유리왕 31년 — 기억 기반이라 조사 필요)
- 주의: 남쪽으로 온 쪽(비류·온조)은 기록상 졸본(고구려) 쪽 왕자·백성. 부여에서 온 쪽은 유리.
- 주의(v7.3 교훈): 3세기 『삼국지』의 5부 기록으로 기원전 1세기 사건(유리 태자 책봉)을 설명하면 약 250년의 시대 소급이다. 5부는 '훗날 이렇게 된다' 수준으로만 쓴다.


## 〔원래 위치: 원본 973–983줄〕 L-0. 지도 v3 (v8.0 채널 표준 — 사용자 결정 2026-10-12, 롱폼과 통일)
> 이동 이유: 지도 v3 표준 → 현행은 history-map-v4 v4-S(원장 C1, 11/04). v3 문법 중 유지 항목은 원장 map_version

### L-0. 지도 v3 (v8.0 채널 표준 — 사용자 결정 2026-10-12, 롱폼과 통일)
- 원칙(롱폼 E-3과 같음): 지형·위치는 코드, 그림체는 지형 음영, 세력 면·글자·화살표·표지는 코드
- **국경은 지형을 따른다**: 롱폼 지도 키트(키트 zip의 mapkit/: `tiles.py` terrarium 고도 타일 → `style.py` 지형 음영 → `bake3.py` 세력 면 → `sA.py`·`sO.py` 장면 JSON). bake3는 나라별 대략 다각형을 씨앗으로 두고 비용 = 고도 + 강 + 노이즈로 skimage watershed → 국경이 산줄기·큰 강을 따른다. 중립 씨앗으로 빈 땅을 남기고, 면 음영 `sh = 1 + 0.7*(lum - mu)`로 지형이 비친다. 직선·다각형·톱니 국경 금지
- **세력 색(진한 저채도)**: 고구려 (96,34,29) / 부여 (42,58,86) / 신(新)·낙랑 (70,74,22) / 흉노·선비·옥저·삼한은 bake3 표 그대로. 영동 낙랑 동부도위는 `xin_e`로 따로 둔다(삼한 색이 북으로 번지지 않게). 백제·신라·가야 색은 처음 나오는 편에서 정하고 시리즈 안에서 바꾸지 않는다
- **영역은 그 시점 기록으로**: 1세기 초 고구려는 동해에 닿지 않는다(옥저가 사이에 — C-2 고정 사실). 근거를 고증 시트에 적는다
- 표시: 지도 장면은 다크 톤. 부여 화살표 흰 붓선 [234,230,220], 고구려 붉은 붓선 [204,36,34]. 국명은 지도 위 큰 글자, 지명·거점 핵심 표지는 붉은 원 표지(anim.json markers — 10/19). 인장('§', 한자 숫자는 글꼴에 없음)은 이름표에만 쓰고, 선택지·작전 설명에는 쓰지 않는다(롱폼 E-6). 모든 라벨은 내레이션에도 나온다(A-0)
- 세 단계 줌(concept 7-1): 전략도 → 작전도 → 전술도. 45초 신작은 보통 한 단계만 쓰고, 줌으로 범위가 바뀌면 내레이션에서도 말한다
- **세로 적용 [미검증 — 첫 적용 편에서 시안 1장으로 확정]**: 키트는 16:9 기준이다. ① bake3 결과를 같은 투영으로 9:16 범위(세로 위도 폭 기준)로 다시 굽거나 ② 넓게 구운 결과에서 세로로 잘라 쓴다. 이 배경을 scenes.json 지도 장면 `image`로, 표지·경로·라벨은 L-3 spec → anim.py로 올린다. anim.py는 경위도 선형(cos(lat) 보정) 투영이므로 bake3 배경도 같은 center·span_lat·투영이어야 표지가 제자리에 온다 — 투영이 다르면 배경을 anim.py 투영으로 다시 샘플링한다. 제목(y 300~470)·자막 띠(1130~1610)를 피해 핵심 표지를 y 600~1100에
- 재편집 편(M)은 롱폼의 지도 컷을 박스 모드로 그대로 쓴다
- **이전 방식(L-1~L-7: AI 재채색 korea_full + 붉은 표지)은 대체용**으로 남긴다 — 나라 영역 없이 도시 위치·이동 경로만 보일 때, 또는 v3 세로 판이 준비되기 전. 나라 영역을 보일 때는 v3


## 〔원래 위치: 원본 1296–1494줄〕 L-7. 대체용: 코드로 그리는 채색 지도 (map.py v7)
> 이동 이유: 대체용 map.py v7 — 코드는 kit/map/map_v7.py

### L-7. 대체용: 코드로 그리는 채색 지도 (map.py v7)
AI 재채색이 검수를 통과하지 못하거나 크레딧을 아낄 때 쓴다. 고도 기반 채색 + 과장된 산 그림 + 굵은 강. 산 그림은 장식이며 좁은 범위(span_lat < 2)는 고도 자료가 거칠어 산을 생략한다. 결과 PNG를 `image`로, 같은 폴더의 `.anim.json`을 `map`으로 쓴다.
```python
#!/usr/bin/env python3
"""채색 산수 지도 렌더러 v7: spec.json -> 배경 PNG(2160x3840) + 영역 레이어 + 애니메이션 JSON.
v7: 고도(ETOPO1 색 음영도에서 추정) 기반 청록·황토 채색 + 음영 + 과장된 산 그림 + 굵은 물길 + 수채 바다.
영역·경로·표지·note는 render.py가 시간에 맞춰 그린다(원본 좌표계에 그려서 줌해도 글자가 떨리지 않음)."""
import json, math, sys, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

W, H = 2160, 3840
DATA = os.environ.get('MAPDATA', 'mapdata')
RELIEF = os.environ.get('RELIEF', 'relief')          # etopo1.jpg(5400x2700), shadedrelief.jpg(10800x5400) — basemap-data
FB = os.environ.get('FONT_B', 'fonts/B.ttf')
PAPER = (240, 232, 212); INK = (58, 48, 40)
RIVER = (62, 118, 160)
LAND_STOPS = [(0.0, (178, 204, 142)), (0.3, (196, 202, 146)), (0.55, (210, 186, 132)), (0.8, (196, 158, 112)), (1.0, (160, 128, 100))]

def font(p, s): return ImageFont.truetype(p, s)
def load_geo(n): return json.load(open(os.path.join(DATA, n + '.geojson')))
def polys_of(g):
    t, c = g['type'], g['coordinates']
    return [c] if t == 'Polygon' else (c if t == 'MultiPolygon' else [])
def lines_of(g):
    t, c = g['type'], g['coordinates']
    return [c] if t == 'LineString' else (c if t == 'MultiLineString' else [])
def lowfreq(w, h, cells, seed):
    r = np.random.default_rng(seed).random((cells[1], cells[0])).astype(np.float32)
    return np.asarray(Image.fromarray((r * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255

def crop_eq(path, lon0, lon1, lat0, lat1):
    """등장방형 전지구 이미지에서 경위도 범위를 잘라 W x H로(이 지도의 투영은 경위도에 선형이므로 정확히 맞음)."""
    im = Image.open(path).convert('RGB'); iw, ih = im.size
    box = ((lon0 + 180) / 360 * iw, (90 - lat1) / 180 * ih, (lon1 + 180) / 360 * iw, (90 - lat0) / 180 * ih)
    return im.resize((W, H), Image.BICUBIC, box=box)

def elevation(rgb):
    """ETOPO1 색(초록=저지 → 황갈=중간 → 짙은 갈색=고지)에서 0~1 고도 지수 추정."""
    a = np.asarray(rgb, np.float32) / 255; r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1); v = mx; d = mx - mn + 1e-6
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    tan = np.clip((0.86 - v) / 0.5, 0, 1) * 0.75 + 0.25
    green = np.clip((0.62 - v) / 0.5, 0, 0.15)
    return np.where(h < 75, tan, green).astype(np.float32)

def palette(e):
    out = np.zeros(e.shape + (3,), np.float32)
    xs = [s[0] for s in LAND_STOPS]
    for c in range(3): out[..., c] = np.interp(e, xs, [s[1][c] for s in LAND_STOPS])
    return out

def mountain_img(h, rng, lit, shade):
    """수묵 채색 산 한 덩이(RGBA): 부드럽게 들쭉날쭉한 능선, 왼쪽 위 빛, 바위 주름결, 청록 산자락, 먹 능선, 아래는 번지듯 사라짐."""
    w = h * rng.uniform(1.25, 1.8); ww, hh = int(w) + 10, int(h) + 10
    n = int(rng.integers(9, 15)); kx = np.linspace(0, w, n)
    env = np.clip(np.sin(np.pi * kx / w), 0, 1) ** .7
    jag = rng.uniform(.45, 1.0, n); jag[int(rng.integers(n // 3, 2 * n // 3 + 1))] = 1.0
    ky = env * jag * h; ky[0] = ky[-1] = 0
    X = np.arange(ww, dtype=np.float32) - 5
    hp = np.interp(X, kx, ky)
    hp = np.convolve(hp, np.ones(5) / 5, 'same') + (np.random.default_rng(int(rng.integers(1e9))).random(ww) - .5) * h * .015
    hp = np.clip(hp, 0, None)
    Y = np.arange(hh, dtype=np.float32)[:, None]; top = hh - 5 - hp[None, :]
    depth = (Y - top) / max(8., h)                       # 능선 0 → 아래로 증가
    slope = np.gradient(np.convolve(hp, np.ones(9) / 9, 'same'))
    litf = np.tanh(slope * 1.6) * .5 + .5
    g = np.random.default_rng(int(rng.integers(1e9)))
    furrow = np.asarray(Image.fromarray((g.random((max(2, hh // 18), max(2, ww // 4))) * 255).astype(np.uint8)).resize((ww, hh), Image.BICUBIC), np.float32) / 255
    lit_c, sh_c = np.array(lit, np.float32), np.array(shade, np.float32)
    col = sh_c + (lit_c - sh_c) * np.clip(litf[None, :] + (furrow - .5) * .5, 0, 1)[..., None]
    col = col * (1 - .22 * np.clip(depth, 0, 1))[..., None]
    rim = np.exp(-np.clip(depth, 0, None) * h / 4)[..., None] * litf[None, :, None] * .35
    col = col + (255 - col) * rim                          # 빛 받는 능선 가장자리 밝게
    foot = np.clip((depth - .35) / .45, 0, 1)[..., None] * .7
    col = col * (1 - foot) + np.array([92, 142, 110], np.float32) * foot
    alpha = (depth >= 0) * np.clip(1 - (depth - .85) / .3, 0, 1) * 240
    im = Image.fromarray(np.dstack([np.clip(col, 0, 255), alpha[..., None]]).astype(np.uint8), 'RGBA')
    d = ImageDraw.Draw(im, 'RGBA'); ridge = [(float(x) + 5, hh - 5 - float(y)) for x, y in zip(X - 5 + 5, hp)][::3]
    d.line(ridge, fill=INK + (190,), width=max(2, int(h / 45)), joint='curve')
    pk = [j for j in range(1, n - 1) if ky[j] >= ky[j - 1] and ky[j] >= ky[j + 1]]
    for j in pk:
        x0, y0 = kx[j] + 5, hh - 5 - ky[j]
        for q in range(int(1 + h / 55)):
            L = h * rng.uniform(.12, .32) * (ky[j] / h); dx = rng.uniform(.05, .35) * L
            d.line([(x0 + dx * .2, y0 + 3), (x0 + dx * .6, y0 + L * .6), (x0 + dx, y0 + L)], fill=INK + (95,), width=max(1, int(h / 75)))
    return im

def main(spec_path):
    S = json.load(open(spec_path))
    cx, cy = S['center']; span = S.get('span_lat', 9.0); ex = S.get('exaggerate', 1.0)
    k = math.cos(math.radians(cy)); ppd = H / span
    P = lambda lon, lat: (W / 2 + (lon - cx) * k * ppd, H / 2 - (lat - cy) * ppd)
    lh, th = (W / 2) / (k * ppd), span / 2
    inview = lambda pts, m=1.5: any(cx - lh - m < p[0] < cx + lh + m and cy - th - m < p[1] < cy + th + m for p in pts)
    lon0, lon1, lat0, lat1 = cx - lh, cx + lh, cy - th, cy + th

    lm = Image.new('L', (W, H), 0); md = ImageDraw.Draw(lm); rings = []
    for f in load_geo('ne_10m_land')['features']:
        for poly in polys_of(f['geometry']):
            if not inview(poly[0]): continue
            pts = [P(*p[:2]) for p in poly[0]]; md.polygon(pts, fill=255); rings.append(pts)
            for hole in poly[1:]: md.polygon([P(*p[:2]) for p in hole], fill=0)
    land = np.asarray(lm.filter(ImageFilter.GaussianBlur(2)), np.float32)[..., None] / 255

    relief = S.get('relief', span >= 2.0)   # 도성 주변처럼 좁은 범위는 고도 자료(약 7km 격자)가 너무 거칠어 끔
    e = elevation(crop_eq(os.path.join(RELIEF, 'etopo1.jpg'), lon0, lon1, lat0, lat1)) if relief else np.zeros((H, W), np.float32)
    e = np.asarray(Image.fromarray((e * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)), np.float32) / 255
    sh = np.zeros((H, W), np.float32) if not relief else np.asarray(crop_eq(os.path.join(RELIEF, 'shadedrelief.jpg'), lon0, lon1, lat0, lat1).convert('L').filter(ImageFilter.GaussianBlur(4)), np.float32) / 255
    sh = ((sh - sh[land[..., 0] > .5].mean() if (land > .5).any() else sh - .5) * (1.6 * ex)) if relief else sh
    wash = lowfreq(W, H, (14, 24), 3)[..., None]; fine = lowfreq(W, H, (120, 210), 4)[..., None]

    col = palette(e) * (1 + np.clip(sh, -.45, .35)[..., None]) * (0.94 + 0.1 * wash) * (0.97 + 0.06 * fine)
    coast = np.asarray(lm.filter(ImageFilter.GaussianBlur(70)), np.float32)[..., None] / 255
    seaC = np.array([118, 176, 196], np.float32); seaF = np.array([200, 218, 212], np.float32)
    far = np.clip(1 - coast * 2.2, 0, 1)
    sea = seaC * (1 - far) + seaF * far
    sea = sea * (0.93 + 0.12 * wash) + (np.array(PAPER, np.float32) - sea) * np.clip(far - .55, 0, 1) * .6
    img = col * land + sea * (1 - land)
    rose = lowfreq(W, H, (4, 6), 8)[..., None]
    if S.get('rose', True):  # 예시처럼 가장자리 분홍 번짐
        edge = np.clip(np.maximum(np.abs(np.linspace(-1, 1, W))[None, :], np.abs(np.linspace(-1, 1, H))[:, None]) - .72, 0, 1)[..., None] / .28
        img = img * (1 - edge * rose * .55) + np.array([228, 190, 190], np.float32) * edge * rose * .55
    hanji = (lowfreq(W // 2, H // 2, (300, 520), 9) - .5)
    img = img * (1 + np.asarray(Image.fromarray(((hanji + .5) * 255).astype(np.uint8)).resize((W, H)), np.float32)[..., None] / 255 * .08 - .04)
    img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

    d = ImageDraw.Draw(img, 'RGBA')
    ln = Image.new('L', (W, H), 0); ld = ImageDraw.Draw(ln)
    for pts in rings: ld.line(pts + [pts[0]], fill=255, width=5, joint='curve')
    img = Image.composite(Image.new('RGB', (W, H), (70, 98, 108)), img, ln.filter(ImageFilter.GaussianBlur(1.3)).point(lambda v: int(v * .85)))

    # 과장된 산: 고지일수록 크고 촘촘히. 뒤(위)에서 앞(아래) 순서로 겹쳐 그림
    rng = np.random.default_rng(S.get('seed', 11)); step = int(S.get('mountain_step', 54)); mts = []
    thr = S.get('mountain_min', .34)
    for yy in range(step, H, step):
        for xx in range(step // 2, W, step):
            x = xx + rng.uniform(-.45, .45) * step; y = yy + rng.uniform(-.45, .45) * step
            xi, yi = int(min(W - 1, max(0, x))), int(min(H - 1, max(0, y)))
            ev = e[yi, xi]
            if land[yi, xi, 0] < .9 or ev < thr or rng.random() > (ev - thr) / (1 - thr) * S.get('mountain_density', 2.0): continue
            mts.append((y, x, ev))
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for y, x, ev in sorted(mts):
        h = (50 + 170 * ((ev - thr) / (1 - thr)) ** 1.2) * ex * S.get('mountain_scale', 1.0)
        lit = tuple(min(255, int(v * 1.12)) for v in palette(np.array([min(1, ev * .75)]))[0])
        shade = tuple(int(v * .66) for v in palette(np.array([ev]))[0])
        g = mountain_img(h, rng, lit, shade)
        ox, oy = int(x - g.width / 2), int(y - g.height + 6); layer.paste(g, (ox, oy), g)
    img.paste(layer.filter(ImageFilter.GaussianBlur(.8)), (0, 0), layer.filter(ImageFilter.GaussianBlur(.8)))

    d = ImageDraw.Draw(img, 'RGBA')
    rw = S.get('river_width', 15)
    riv = [[P(*p[:2]) for p in l] for f in load_geo('ne_10m_rivers_lake_centerlines')['features'] for l in lines_of(f['geometry']) if inview(l, 0.5)]
    riv += [[P(*p) for p in rv['pts']] for rv in S.get('rivers_extra', [])]
    for l in riv: d.line(l, fill=(236, 242, 236, 170), width=int(rw * 2.1), joint='curve')
    for l in riv: d.line(l, fill=RIVER + (235,), width=rw, joint='curve')
    for lb in S.get('labels', []):
        d.text(P(lb['lon'], lb['lat']), lb['text'], font=font(FB, lb.get('size', 50)), fill=tuple(lb.get('color', [40, 80, 105])) + (235,),
               anchor='mm', stroke_width=5, stroke_fill=PAPER + (210,))
    out = S['out']; img.save(out)

    A = {'regions': [], 'routes': [], 'markers': [], 'note': S.get('note', ''), 'zoom': S.get('zoom', 1.5)}
    lmask = lm
    if S.get('regions'):
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        for r in S['regions']:
            c = tuple(r.get('color', [150, 60, 40])); pts = [P(*p) for p in r['poly']]
            pm = Image.new('L', (W, H), 0); ImageDraw.Draw(pm).polygon(pts, fill=255)
            pm = pm.filter(ImageFilter.GaussianBlur(18))
            edge = ImageChops.multiply(ImageChops.subtract(pm, pm.filter(ImageFilter.MinFilter(15))), lmask)
            a = ImageChops.lighter(ImageChops.multiply(pm, lmask).point(lambda v: int(v * 0.30)), edge.point(lambda v: min(255, int(v * 1.6))))
            layer = Image.alpha_composite(layer, Image.merge('RGBA', [Image.new('L', (W, H), v) for v in c] + [a]))
            lx, ly = P(*r['label_at']) if r.get('label_at') else (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
            A['regions'].append({'name': r['name'], 'xy': [lx, ly], 'color': list(c), 'size': r.get('size', 76),
                                 'at': r.get('at', 0.2), 'dur': r.get('dur', 1.3)})
        lp = out.replace('.png', '.layer.png'); layer.save(lp); A['layer'] = lp
    t = 0.5
    for rt in S.get('routes', []):
        at = rt.get('at', t); dur = rt.get('dur', 1.6); t = at + dur + 0.2
        A['routes'].append({'pts': [list(P(*p)) for p in rt['pts']], 'color': rt.get('color', [178, 34, 30]),
                            'label': rt.get('label', ''), 'at': at, 'dur': dur})
    ms = sorted(S.get('markers', []), key=lambda m: not m.get('main'))
    t = t if S.get('routes') else 0.4
    for i, m in enumerate(ms):
        x, y = P(m['lon'], m['lat'])
        A['markers'].append({'xy': [x, y], 'name': m['name'], 'sub': m.get('sub', ''), 'side': m.get('side', 'r'),
                             'main': bool(m.get('main')), 'at': m.get('at', t + 0.3 * i)})
    f = S.get('focus')
    A['focus'] = [v / s for v, s in zip(P(*f) if f else (A['markers'][0]['xy'] if A['markers'] else (W / 2, H / 2)), (W, H))]
    json.dump(A, open(out.replace('.png', '.anim.json'), 'w'), ensure_ascii=False)
    print('saved', out, 'mountains', len(mts))

if __name__ == '__main__':
    for p in sys.argv[1:]: main(p)
```
- 실행: `MAPDATA=mapdata RELIEF=relief FONT_B=fonts/B.ttf python3 map.py ep/m_*.json` (spec은 L-3 형식 + `exaggerate`, `mountain_step`, `mountain_scale`, `river_width`, `rose`, `relief` 선택)
- Natural Earth 1:10m 하천에는 한강·남한강·낙동강·압록강·두만강 정도만 있다. 대동강·금강·임진강 등은 `rivers_extra`에 좌표로 추가(근거 확인 후).


## 〔원래 위치: 원본 1688–1702줄〕 M-8. 설정 예 (10/7 ③ 매복 작전 — 자막 일부 생략)
> 이동 이유: 10/7 편별 설정 예 — 코드는 kit/shorts/cfgs_example_ep1-3.py

### M-8. 설정 예 (10/7 ③ 매복 작전 — 자막 일부 생략)
```python
END = '대무신왕 1부 〈열 살의 장수〉'
s3 = dict(end=END, name='s3_ambush_plan', title='매복을 {길가}에\\N안 숨겼다고?', ranges=[(221.2, 277.0)],
 segs=[S(221.2,224.25,(0,800,400),(820,1920,1370)), B(224.25,257.8,1050,1150), B(257.8,259.3,950,1000),
       F(259.3,262.25,680), F(262.25,267.25,330), F(267.25,272.3,740), F(272.3,277.0,800)],
 caps=[(221.2,223.6,'"매복 부대는\\N어디에 배치합니까?"'), (224.2,226.2,'"길가 바로 옆이 아니네."'),
       (226.4,229.6,'"산 깊숙이 숨어\\N숨을 죽이고 있다가,"'),
       # … 중간 자막 생략 …
       (272.8,277.0,'이제 남은 것은,\\N기다리는 일뿐이었습니다.')])
s5_extra = [(0.3, 5.0, ('Tag', '{\\pos(46,440)\\fad(200,300)}기록상 서기 20년'))]   # 좌상단 연도 태그
CFGS = [s3]
```
- 10/7 5편의 전체 설정(구간·모드·자막)은 이 대화의 cfgs.py였다. 2부부터는 롱폼 대본 문서의 컷 표·받아쓰기 시각에서 새로 짠다
- 10/7 실제 길이: ① 57.5 ② 53.7 ③ 55.8 ④ 58.6 ⑤ 55.3초. 조각 수 ① 18 ② 9 ③ 7 ④ 22 ⑤ 10
