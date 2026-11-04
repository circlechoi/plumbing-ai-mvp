---
name: "history-shorts"
description: "역사서클 세로 쇼츠 제작 — 완성된 롱폼을 잘라 만드는 재편집 하이라이트(롱폼 1편당 3~5편)와 롱폼에 없는 곁가지를 다루는 45초 신작(청록산수 그림·지도 v3·시그니처 3초)을 사용자와 함께 기획·고증·Higgsfield 생성·렌더할 때 사용. '숏츠 만들어줘', '롱폼으로 숏츠', '역사 숏폼 만들어줘', '/history-shorts 주제', '다음 편 만들어줘' 등."
---

> **history-core를 먼저 읽는다.** 현행 값은 원장(decisions.yaml) 하나뿐 — 이 본문과 다르면 원장 우선. 폐기·보류·편별 이력·변경 이력 원문은 같은 폴더 `archive.md`(규칙으로 따르지 않음).

# 역사 숏폼 제작 파이프라인 (채널 표준 v8.1 · 2026-10-23 스킬 정비 · 두 형식: 롱폼 재편집 + 45초 신작 · 지도 v4-S(원장 C1) · 시그니처 3초 · 도트 필수)

> **충돌 규칙(11/04 개편 — history-core)**: 현행 값은 원장(decisions.yaml) 하나뿐이다. 이 스킬 본문과 원장이 다르면 원장을 따른다. 원장에 없는 항목끼리 부딪히면 기존 '날짜가 붙은 최신 사용자 결정' 원칙을 따른다(원문은 archive.md '교체 원문').

> 〔머리말의 버전별 변경 이력(v6~v8.1) — archive.md '머리말에서 옮긴 줄'〕

결과물: (가) **롱폼 재편집**(M) — 1080x1920, 24fps, 편당 50~59초, 롱폼 1편당 3~5편 / (나) **45초 신작** — 1080x1920, **41~44초**, 30fps mp4 1개. 공통: 유튜브 업로드 메타데이터 + 갱신된 '편성표'.
(나) 포맷: **8~9장면**(장면 길이는 내레이션 문장에 맞춤), **청록산수 채색 AI 이미지(2k)** + **AI로 다시 칠한 채색 지도(정확한 밑그림 기반) 위에 움직이는 표지·경로** + 이징 카메라(펀치·컷인·포커스) + 장면별 전환(먹 번짐·휩·플래시) + 세이프존 2줄 자막(송명·팝인·금색 강조·잉크 폭 기준 중앙 정렬) + 효과음·앰비언스(·BGM 덕킹) + **다큐 내레이션(Harrison, v7.4)** + 첫 장면 움직이는 컷(Kling). v8.0부터 첫 장면은 **시그니처 3초**(수묵 → 먹 번짐 → 실사 움직이는 컷), 나라 영역 지도는 **지도 v3**(L-0).







사용자 선호: 결론선행, 개조식(□/-/·), 출처 표기, 추정/미확인 구분, 군더더기·칭찬 없음. 결정은 선택지 2~4개 + 추천안으로 묻는다. 사용자는 말보다 **시안(이미지·영상)을 보고 판단**한다 — 큰 방향 결정 전에 저비용 시안을 먼저 만든다.

## 최우선 원칙
1. **고증이 연출보다 우선**이다. 재미를 위해 사실을 단정하거나 꾸미지 않는다.
2. **애매한 것은 애매하다고 말한다** — 대본·자막·설명란·사용자 보고 모두에서.
3. **구성은 사용자와 함께 정한다.** 크레딧을 쓰기 전 반드시 체크포인트(섹션 B)에서 확인받는다. 필요한 게 있으면 질문한다.
4. **지도를 자주 쓴다.** 시청자가 도시 위치·나라 영역·이동 경로를 파악할 수 있도록 매 편 지도 장면을 넣는다(섹션 L, 현행 표준은 지도 v4-S — history-map-v4, 원장 C1 11/04. v8.0의 지도 v3(L-0)은 archive.md).
5. **채널 컨셉을 먼저 읽는다**(A-0). 우선순위는 머리말 공통 문단(최신 날짜 결정 우선).

## A-0. 채널 컨셉과의 관계 (v8.0)
- 기획·대본·제목을 시작할 때 `history-channel-concept`을 먼저 읽는다. 롱폼 내용(인물·고증·지도)은 `history-longform`이 기준
- 쇼츠의 역할 [concept 8 제안]: 쇼츠 = 질문을 던지는 곳 / 롱폼 = 답하는 곳. 재편집 편(M)은 롱폼으로 데려가는 입구, 신작은 롱폼에 없는 곁가지의 결정 또는 의외의 사실 하나
- 두 형식 병행(사용자 결정 2026-10-12): 롱폼이 나오면 재편집 3~5편 → 그 사이에 곁가지 신작. 롱폼과 내용이 겹치는 사건은 신작으로 다시 만들지 않는다
- 45초에 맞춘 컨셉 적용:
  - 한 편 = 결정(또는 의외의 사실) 하나 = 질문 하나. 편 구성 공식(딜레마 → 당신이라면? → 실제 선택 → 결과 → 남긴 것)을 압축: 훅(결말 또는 질문) → 딜레마 1~2문장(제약을 말로) → 선택 → 결과 → 시청자 질문 또는 다음 편
  - **상대를 바보로 그리지 않는다**: 상대의 계산을 한 구절이라도 그럴 만하게 세우고, 승자가 그것을 어떻게 역이용했는지로 답한다
  - **라디오 기준**: 화면에만 있는 정보를 두지 않는다(지도 라벨·연도 배지·태그도 내레이션에 나온다). "여기", "이쪽", "보시는 것처럼" 금지. 지형은 방향과 비유로 말한다
  - **신이한 기사**: "기록은 이렇게 전합니다" → "오늘의 눈으로 읽으면" 두 단계로 말해 기록과 해석을 섞지 않는다
  - **역사적 상상력**(concept 5-1): 기록이 한 줄이어도 주제를 버리지 않는다. 조건(지형·계절·정세·앞뒤 기록)으로 판단을 재구성하고 [해석]·[상상]으로 밝힌다. 기록에 없는 사건·실존 인물의 발언·숫자는 사실처럼 만들지 않는다
  - 국제 정세는 '틈'으로만 말한다(정세가 전쟁을 일으켰다고 단정하지 않음)
- **보고할 때마다 밝힌다**: Claude는 움직임을 볼 수 없고 소리를 들을 수 없다. 정지 프레임·음량 수치·받아쓰기 결과로만 확인했다고 적고, 억양·음향 밸런스·전환 느낌은 사용자 확인을 부탁한다
- 작업 관점: 기획·대본·컷을 볼 때 concept 0의 두 역할(유튜브 기획자 / 영상 디자이너)로 차례로 검토하고 보고를 두 이름으로 나눠 적는다

> 〔현행 규칙 — `reference-planning.md`에 있음: 'A. 곁가지 후보 발굴 도구: '이야기 사슬' (v8.1)'. 곁가지 신작 후보를 고를 때만 읽는다〕
> 〔현행 규칙 — `reference-planning.md`에 있음: 'A-1. 다음 편으로 가는 3가지 방향'. 곁가지 신작 후보를 고를 때만 읽는다〕
> 〔현행 규칙 — `reference-planning.md`에 있음: 'A-2. 파생 질문 발굴 틀 (앵커마다 훑어보고 후보를 사용자에게 제시)'. 곁가지 신작 후보를 고를 때만 읽는다〕
> 〔현행 규칙 — `reference-planning.md`에 있음: 'A-3. 편성표(에피소드 트래커)'. 곁가지 신작 후보를 고를 때만 읽는다〕
> 〔archive.md로 이동: 'A-4. 사슬 진행 상황 (2026-10-12 기준)' — 10/12 기준 진행 현황(편별 이력)〕
> 〔현행 규칙 — `reference-planning.md`에 있음: 'A-5. 장기 서사 아크 (사용자 결정, 2026-09-29 · 순서 변경 2026-10-04 — 완료된 아크, 기록용)'. 곁가지 신작 후보를 고를 때만 읽는다〕
## B. 공동 구성 체크포인트 (크레딧 쓰기 전 필수)
사용자가 있을 때는 `AskUserQuestion`(없으면 텍스트)으로 확인한다. 한 번에 1~3개만 묻는다.
1. **편 선정**: 편성표 + 다음 후보(◀●▶) 제시 → 사용자 선택(자유 입력 허용)
2. **고증 시트 확인**(섹션 C): 특히 학설이 갈리는 항목은 "어느 설을 중심으로, 나머지는 언급만?" 또는 "여러 설을 나란히 소개?"를 묻는다
3. **대본·장면 구성 확인**: 내레이션 전문 + 8~9장면 한 줄 설명(지도 장면 포함) + 지도 미리보기 이미지 + 예상 크레딧 → 승인 후에만 이미지·음성 생성
4. **완성본 확인**: 영상 전달 후 수정 요청 반영(해당 장면/음성만 재생성)
- 사용자가 "알아서 해줘"라고 한 단계는 합리적 선택을 하고 그 선택을 보고에 밝힌다.
- 사용자 도메인 지식이나 선호(어느 사료 중심, 감정 톤, 특정 인물 강조 등)가 필요하면 질문한다.
- **대본은 사용자와 주고받으며 고친다(v7.6, ⑨)**: 사용자가 직접 쓴 대본이나 다른 AI가 만든 초안·이미지를 가져오면 ① 기준(훅/흐름/고증/분량/핵심 메시지)을 먼저 밝히고 평가 ② 고증 오류·비문·오해를 부르는 표현만 고치고 **사용자 문장과 말투는 그대로 살린다** ③ 고친 곳마다 이유를 한 줄씩. ⑨ 최종 대본은 사용자가 쓴 8문장이었고, 고친 것은 '칼로 목숨을 끊은→칼을 받고'(실제 죽음은 창), '적국→이웃 나라', '서신→말' 정도
- 사용자가 방향만 주면(예: "외교 이슈를 부각", "이런 해설도 버무리자") 고증 등급을 붙여 반영안을 내고, 근거가 약한 해설은 [해석]으로만 싣는다(C-2)
- **재편집 편(M)은 체크포인트를 줄인다**: ① 편 수·구간·화면 배치·끝 문구(AskUserQuestion, 배치 목업 1장) ② 완성본 확인. 내용 고증은 롱폼에서 끝났으므로 다시 하지 않고, 설명란에 롱폼의 고지를 옮긴다

## C. 고증 프로토콜 (가장 중요)
### C-1. 조사
- WebSearch/WebFetch로 조사. 우선 출처: 국사편찬위원회(한국사데이터베이스·우리역사넷), 한국민족문화대백과사전, 국립중앙박물관·지역 국립박물관, 국가유산포털, 학술논문(KCI). 블로그·나무위키는 단서로만 쓰고 근거로 쓰지 않는다.
- 한국사데이터베이스(db.history.go.kr/id/...)와 한국민족문화대백과(encykorea.aks.ac.kr/Article/...)는 WebFetch로 읽힌다. 우리역사넷(contents.history.go.kr)은 robots 차단으로 읽히지 않음.
- 핵심 사실 하나당 가능하면 독립 출처 2곳 이상으로 확인.
- 읽지 못한 페이지(차단·오류)는 그 사실을 사용자에게 알리고, 그 페이지에 기대는 주장은 '미확인'으로 둔다.
- (v8.0, 롱폼에서) 위키문헌·한국사DB·우리역사넷은 WebFetch에서 막힐 때가 많고, WebFetch 요약기는 원문 전문 인용을 거부한다 → 짧은 사실 확인 질문으로 묻거나, 앱 안 브라우저를 쓰거나, 사용자에게 원문을 붙여 달라고 한다

### C-2. 근거 등급 (모든 문장에 부여)
- (v8.1) 태그의 뜻·전체 목록은 concept 5-1 마스터 태그 표가 원본이다. 쇼츠는 [기록][통설][추정][여러 설][미상][해석][상상][연출]을 쓴다. 아래 표의 '내레이션 표현'은 쇼츠용 보조 기준이며, 문체는 D-2 v8.1 기본 문체를 따른다
| 등급 | 의미 | 내레이션 표현 | 자막 태그 |
|---|---|---|---|
| 기록 | 사료에 그렇게 적혀 있음(사실 여부와 별개) | '『○○』에 따르면 ~했다' | (없음) |
| 통설 | 학계 다수가 받아들이는 해석 | '~라고 보는 학자가 많다' | [통설] |
| 추정 | 학계가 '추정'으로만 제시(반대 설은 못 찾았지만 확정 아님) | '~로 짐작한다' | [추정] |
| 여러 설 | 학계 의견이 갈림 | '~했다고도, ~했다고도 전한다' | [여러 설] |
| 미상 | 알 수 없음 | '이건 아무도 모른다' | [미상] |
- 내레이션 표현은 v7.4 다큐체 기준. v7 이야기꾼체('~단다', '~지')는 D-2 참고.
- [추정] 등급은 사용자 결정(2026-09-27)으로 추가. 예: 부아악 = 북한산 인수봉 부근(한국사데이터베이스 주석).
- **[해석] 태그(v7.6, ⑨)**: 사료가 사실만 적고 의미는 말하지 않는데 영상이 의미를 덧붙일 때(예: '활 선물 = 복종 요구', '외교 마찰') 쓴다. 학계 서술로 확인되면 [통설]/[추정], 확인되지 않은 해설(위키 각주·블로그·강의)은 [해석]. 내레이션은 단정하지 않고 '~라는 듯', '~로 읽힌다', '~셈'으로, 자막 1줄 앞에 `[해석]`, 설명란 첫 항목에 "기록이 아닌 해석"이라고 밝힌다
- 신화·전설은 '기록'이라도 사실처럼 말하지 않는다('~라고 전한다').
- 사료 간 기록·학설이 갈리면 **기본값은 '주류 설 중심으로 영상 진행, 나머지 설은 설명란'**(사용자 결정, 2026-09-27). 단, 핵심 주장 자체가 불확실하면 영상 안에서도 짧게 '확실하지 않다'고 말한다. 편에 따라 사용자가 달리 원하면 그에 따른다.
- 연도는 '기록상 연도'인지 '추정 연대'인지 구분한다(배지에 '기록상 BC 18', '약 BC 1세기' 등).
- **태그를 롱폼과 맞춤(v8.0)**: [기록]·[통설]·[추정]·[여러 설]·[미상]·[해석]에 더해 **[상상]**(concept 5-1 절차로 조건을 재구성한 판단 — 내레이션에서 경계를 말한다: "기록은 여기까지입니다. 여기서부터는 그날의 조건으로 재구성한 이야기입니다.") / **[연출]**(가상 인물·대사·복식 색 등 화면의 연출 — 설명란 고지). 내레이터 문장은 [기록]·[통설] + 원리를 설명하는 [해석]까지, 기록에 적힌 것처럼 말하지 않는다
- **고정 사실(v8.0, 롱폼 고증)**: 국내 천도 서기 3년(유리왕 22년) / 1세기 초 고구려는 동해에 닿지 않는다 — 동옥저 복속은 태조대왕 4년(56년) '東至滄海', 그 전 동해안은 옥저, 영동 일대는 낙랑 동부도위 [통설] / 국내성 [통설] 지안 / 졸본 [통설] 환런 / 부여 중심 [여러 설]. 인과 주장·시대 소급 금지는 D-0 그대로

### C-3. 고증 시트 (체크포인트 2에서 사용자에게 제시)
- 사건/질문, 관련 1차 사료(가능하면 원문 구절 병기), 연도(기록상/추정)
- 핵심 사실 3~6개: 각각 등급(C-2) + 출처
- 이설·논쟁 지점과 처리 방안 제안
- 시각 고증: 복식(재질·색·장식), 머리모양, 건축(움집/목책/토성/기와), 무기, 깃발·문양 — 각각 근거 또는 '미확인'
  - **확인되지 않은 국가 문양·깃발 문장은 만들지 않는다** → 무늬 없는 천 깃발 또는 깃발 없음
  - 시대가 이를수록 소박하게(삼베·무명, 무채색). 비단·금관 등은 유물·사료로 확인된 시기·신분에만
  - 복식·건축 자료가 거의 없는 시기는 인물을 원경·실루엣으로 처리해 디테일 단정을 피한다
- AI 이미지는 고증이 완벽하지 않음을 전제로, 생성 후 이미지를 보고(가능하면 Read로 확인) 시대에 맞지 않는 요소(화려한 옷, 문양, 후대 건축)를 사용자에게 보고한다. 이미지를 직접 볼 수 없으면(작업공간은 Higgsfield CDN 차단) 그 사실을 밝히고 사용자 확인을 요청한다.
- 최종 영상 하단에 '이미지는 AI 재현' 문구를 출처와 함께 표기한다.
- **지도 고증**(L-2): 표시할 도시·유적의 비정 위치와 등급, 영역 경계의 근거(어느 문헌/지도 기준인지)를 시트에 적는다.

## D. 대본 설계 — 45초 신작 (약 43초)
### D-0. 서사 점검표 (v7.3, 대본을 사용자에게 보이기 전에 반드시 통과)
2026-09-29 교훈: ⑤ 초안이 '3세기 5부'와 '기원전 1세기 유리 태자 책봉'을 "실마리는 여기!"로 억지 연결했고, 사용자가 개연성을 지적함. 또 2~4번 문장이 사실 나열이라 흐름이 끊김.
1. **핵심 메시지 한 문장**을 먼저 쓴다(예: "부여를 등진 주몽 무리가 졸본 세력과 손잡아 고구려를 세웠고, 부여의 대소는 적이 된다"). 모든 문장은 이 메시지를 밀어야 한다. 밀지 않는 사실은 설명란으로.
2. **문장 간 연결 테스트**: 이웃한 두 문장 사이에 '그래서 / 그런데 / 그러자 / 한편' 중 하나를 넣어 말이 되는지 확인. 어느 것도 안 들어가면 순서를 바꾸거나 연결 문장을 넣는다.
3. **인과 주장 검증**: "A 때문에 B" "실마리는 A"처럼 원인을 말하는 문장은 사료나 학계 서술이 그 인과를 직접 말하는지 확인. 아니면 인과 표현을 빼고 사실만 나란히 두거나 [추정]으로.
4. **시대 소급 금지**: 근거 사료의 시점과 사건 시점을 나란히 적어 본다. 수십 년 이상 차이 나면 '훗날'로만 연결하고 원인으로 쓰지 않는다.
5. **대립·인물 축 확인**: A-5 아크에서 이번 편이 심어야 할 인물·갈등이 들어갔는지(예: ⑤는 대소).
6. **예고 약속 확인**: 마지막 질문을 다음 편이 실제로 사료로 답할 수 있는지. 답이 기록에 없으면 '미스터리 편'이라고 사용자에게 알린다.
7. 점검 결과(핵심 메시지 문장 + 각 문장의 역할 한 단어: 훅/배경/갈등/전환/근거/반전/예고)를 대본과 함께 사용자에게 보여 준다.

### D-1. 기본 구조 (10비트 + 연출 기본값) — 사용자와 합의해 변형 가능. v7.5부터 비트를 8~9장면으로 묶는다(예: 2+3, 9+10)
| # | 역할 | 대략 시간 | 연출 기본값(move / trans) |
|---|---|---|---|
| 1 | 훅: 이번 편 질문(또는 사건) — 화면 상단 타이틀 | 0~4.5s | 움직이는 컷(`video`) 또는 `punch` / 첫 장면(타이틀 슬램 + 북 소리) |
| 2 | 이전 편 연결 또는 갈등 제시 | ~9s | `in` / `ink` |
| 3 | 배경/전개 | ~13.5s | `pan_l`·`pan_r` / `ink`·`whip_*` |
| 4 | 전개 또는 단서 1 | ~18s | 지도 `focus`(경로·영역) / `ink` |
| 5 | 전개 또는 단서 2 | ~22s | `in` / 무음 `cut` |
| 6 | 핵심(답 또는 절정) | ~27s | `punch` / `cut`(타격음) + 펀치 자막 |
| 7 | 근거와 확실성 수준(기록/통설/추정/여러 설/미상) | ~31s | 지도 `focus` 또는 `out`+`mist` / `ink` |
| 8 | 한 단계 더(의외의 사실 또는 반대 설) | ~36s | `in` / `flash` |
| 9 | 새 궁금증(◀●▶ 중 합의한 방향) | ~40s | `in` / 무음 `cut` + 펀치 자막 |
| 10 | 다음 편 예고 | ~45s | `in` / `ink` |
- 실제 장면 전환 시각은 내레이션 받아쓰기로 문장 시작에 맞춘다(H 참고).
- **첫 장면(v7.3)**: 지도가 아니라 가장 강렬한 장면(인물·긴장) + 상단 제목(4~5어절, `{핵심어}` 금색). 내레이션 첫 문장은 곧바로 이번 편 질문. "자, 옛날 옛적" 같은 도입은 쓰지 않는다(스와이프 방어, 2026-09-29 사용자 결정). 지도는 2번째 장면 이후. ⑤부터 첫 장면은 움직이는 컷(F-4). **v7.6**: 첫 문장은 질문 대신 **결말을 먼저 던지는 한 문장**도 된다(⑨ "아버지가 보낸 칼을 받고 스스로 목숨을 끊은 고구려 태자, 해명."). 사용자가 "약하다"고 한 훅: 원인과 결과를 한 문장에 다 설명하는 문장("선물로 받은 활을 꺾었다가, 아버지에게 칼을 받은 태자가 있습니다")
- **시그니처 3초 축약판(v8.0, 사용자 결정 2026-10-12)**: 신작 첫 장면은 수묵화 스틸 → 먹물 한 방울이 번져 화면을 덮음 → 같은 구도의 움직이는 실사 컷, 모두 약 3초 안. 그 뒤 본편은 청록산수. 채널이 수묵화에서 시작했다는 정체성(concept 7-2)을 쇼츠에도 새기되 훅이 늦어지지 않게 ① 제목은 0.15초부터(지금처럼) ② 첫 내레이션(질문 또는 결말 한 문장)도 0초부터 ③ 실사 컷은 가장 강한 액션 순간(아래 '첫 장면 구도' 규칙). 만드는 법 F-5. 실사는 이 3초에만 쓰고 본편 그림체는 바꾸지 않는다. [미검증 — 첫 적용 편에서 시안으로 길이·먹 번짐 속도·톤 차이를 사용자에게 확인]
- **템포(v7.5, 사용자 피드백 "그림이 너무 빨리 지나간다")**: **8~9장면**, 장면당 **4.5초 이상**(훅 구간인 첫 장면·둘째 장면만 3.5초까지 허용). 같은 그림을 다시 확대해 끊는 무음 컷은 쓰지 않는다(꼭 필요하면 편당 1회). 한 장면에 내레이션 1~2문장을 통째로 싣고, 장면 전환은 문장·절이 바뀌는 곳에서만. ⑦은 14장면(평균 3.3초)이라 빨랐고 ⑧은 9장면(평균 4.9초). 화면 변화가 필요하면 컷 대신 느린 카메라(`in`·`out`·`pan`)와 `mist`로. 강한 효과(punch·flash·타격음)는 편당 2~3회
- **끝맺음(v7.5)**: 내레이션은 **다음 편 질문(훅)에서 끝낸다** — "다음 이야기에서"는 읽지 않고 마지막 장면 자막 1줄 '다음 이야기'로만. `total` = 마지막 단어 끝 + 0.4 + **0.6초**(이전 2초 안팎), 페이드아웃 0.3초
- **끝맺음 대안(v7.6, ⑨ 사용자 작성)**: 다음 편 질문 대신 **시청자에게 묻는 질문**으로 끝낼 수 있다("여러분이 왕이었다면, 나라를 위태롭게 한 아들을 살리셨겠습니까, 죽이셨겠습니까?"). 이때 마지막 장면 자막은 그 질문(1줄 '여러분이 왕이었다면' / 2줄 '살릴까, 죽일까?'), 다음 편 예고는 고정 댓글로 돌린다. 논쟁이 되는 결정이 있는 편에 쓴다
- **도트 — 매 편 1곳 이상(v8.1, concept 7-3 · 10/17 결정, 10/23 재확인 · 죽음·비극 장면에는 넣지 않음)**: 자체 제작 도트 스프라이트(기마병·행군·배·불꽃 등, sprite.py)가 한 장면을 작게 지나간다. 놓는 자리는 들판·길·물 위(산 단면·건물 속 금지), 그 장면의 움직임과 같은 방향·같은 세력 색. 내레이션에서 언급하지 않는다(정보가 아니라 장식). 체크포인트 3 장면 구성안에 '도트: n번 장면, 무엇이, 어느 방향'을 한 줄로 적는다. 게임·만화의 실제 그림·로고·캐릭터 도안은 쓰지 않고, 작품 이름도 화면·설명란에 넣지 않는다. 참고 사례: ⑨ 6번 장면 도트 기마 무사, 온돌 편 지게 진 나무꾼
- **펀치 자막(하이브리드, v7.3)**: 핵심 대목 3~4곳만 화면 중앙(y 900)에 큰 단어를 0.6~0.9초 띄운다(scenes.json `punch`, `at` = 해당 단어가 들리는 시각 − 장면 시작). ⑤ 예: "결국 {항복}!", "{고구려}"(sfx boom), "곧바로 {태자}!".
- **움직이는 컷(v7.3)**: 편당 1개 기본(첫 장면), 최대 2개. 연기·불·물·안개처럼 자연스럽게 움직일 장면만, 인물 얼굴 클로즈업은 제외. 이미지 확인 → 사용자 승인 → 생성 순서(F-4).
- **지도 장면 배치(기본)**: 1~3장면을 지도로 한다(이동 경로·방위·영역·근거 유적). 지도는 L-5 라이브러리 재사용 시 무료, 새 범위는 장당 2.75크레딧.
- **액션 강도 조절**: `punch`·`cutin`·`whip`·`flash`는 편당 합쳐 3~4회까지. 매 장면에 쓰면 오히려 단조롭다. 전환 방향 규칙: 과거로 가는 장면은 `whip_r`(화면이 오른쪽→왼쪽으로 되감기듯), 앞으로는 `whip_l`, 시대 점프·반전은 `flash`.
- `fx`: `mist`(안개가 흐름 — 풍경·새벽 장면), `shake`(미세 흔들림 — 추격·전투·긴장 장면에만).

### D-2. 내레이션 규칙
**v7.4 확정(사용자 결정, 2026-09-29): Kings and Generals식 다큐 내레이션**
- **기본 문체(v8.1, 10/23 사용자 결정)**: 롱폼 D-1의 '설명하듯 잇는 합니다체'를 바탕으로 '~죠 / ~요 / 명사 종결'을 섞는 대화체(⑨ 사용자 최종본이 본보기). 같은 어미 연속 0회, 평서 '~다.' 종결은 쓰지 않는다. 사실과 해설을 번갈아 끊지 않고, 해설은 문장 안 한 구절로 녹인다(⑨ 교훈). 아래 v7.5 '~다' 관련 규칙과 ⑧ 예는 이전 기준
- 목소리: Qwen 프리셋 **Harrison**(젊은 남성) — F-2 참조. 기존 할아버지 이야기꾼은 사용자가 '별로'라고 해 폐기. ⑤ 청취 확인 결과 사용자 '굳'
- **문체(v7.5, 사용자 피드백 3회: "~다, ~다 반복으로 툭툭 끊긴다")**: 다큐 서술체를 유지하되 ① **'~다.'로 끝나는 문장을 쓰지 않는다**(v8.1 — 이전 기준은 전체 3회 이하) ② 종결을 섞는다 — 연결어미로 다음 절에 잇기(~는데, ~자, ~지만, ~더니), 명사·체언 종결("…여섯 살 무휼.", "…바로 부여 자신이라는 뜻."), 물음, 인용("~라고 전한다" 1회) ③ 문장 첫머리는 앞 문장을 받는 말(그런데·바로 그때·그리고 4년 뒤)로 시작 ④ 종결 어미 목록을 대본 옆에 적어 사용자에게 보여 준다(같은 어미 연속 0회 확인). 질문은 첫 문장·마지막 문장(중간 1회까지). 한 장면에 1~2문장
  - ⑧ 대본(v7.5 다큐 '~다'체 — 이전 기준, 참고용): "부여 왕의 협박에 맞선 게, 여섯 살 왕자라고? 큰 눈에 물러났던 대소가 다시 사신을 보내, 작은 나라는 큰 나라를 섬기는 게 예의라며 굴복을 요구했는데, 나라가 아직 약하다고 여긴 유리왕은 치욕을 참고 따르려 했다. 바로 그때 사신 앞에 나선 이는, 기록이 아직 어렸다고 적은 왕자, 여섯 살 무휼. 아이의 대답은 이랬다고 전한다. 여기 알을 쌓아 두었으니, 대왕이 이 알을 무너뜨리지 않으면 섬기겠소. 수수께끼 같은 이 말을 풀어낸 건 부여의 한 노파였는데, 쌓아 올린 알처럼 위태로운 건 바로 부여 자신이라는 뜻. 그리고 사 년 뒤 대소가 군대를 보냈을 때, 이 아이는 어떻게 맞섰을까?" (숫자는 '오만 대군', '사 년 뒤'처럼 한글로 써야 읽기가 안정적)
  - ⑨ 대본(사용자 작성 최종본, 참고 — 합쇼체·해요체를 섞은 말투): "아버지가 보낸 칼을 받고 스스로 목숨을 끊은 고구려 태자, 해명. 황룡국 왕이 복종하라는 듯 강한 활을 보내오자, 해명은 사신 앞에서 그 활을 동강 내 버립니다. 부여와의 전쟁을 앞둔 상황에서, 이웃 나라와 큰 외교 마찰이 생긴 셈이었어요. 국력의 한계로 전쟁을 두려워한 유리왕은 아들을 황룡국에 보내죠. 아들을 죽여도 좋다는 말과 함께요. 태자는 살아 돌아왔지만, 이듬해 아버지는 칼을 보내 자결을 명합니다. 스물한 살 태자는 들판에 창을 거꾸로 박아 두고, 말을 몰아 그 위로 몸을 던져요. 굽혀서 나라를 지키려던 왕과, 굽히지 않아 목숨을 잃은 아들. 여러분이 왕이었다면, 나라를 위태롭게 한 아들을 살리셨겠습니까, 죽이셨겠습니까?"
  - **⑨ 교훈(사용자 피드백 "재미없고 뚝뚝 끊긴다")**: '사실 한 문장 → 해설 한 문장'을 번갈아 놓으면 끊긴다. 한 인물의 행동이 다음 인물의 반응을 부르는 **원인→결과 한 줄기**로 쓰고, 해설은 문장 안의 한 구절('복종하라는 듯', '~셈이었어요')로 녹인다. 종결은 '~합니다 / ~죠 / ~요 / 명사 종결'을 섞는다. 대비 문장("굽혀서 지키려던 왕과, 굽히지 않아 목숨을 잃은 아들")을 끝 질문 바로 앞에 둔다
- 분량: 낭독 속도가 회마다 크게 다르다(초당 7.2자 ⑤ / 8.7자 ⑥ / 같은 날 9.7자·8.0자 ⑦ / 7.9자 ⑧ / **6.7자 ⑨** — 쉼표와 짧은 문장이 많으면 느려진다: 약 300자가 44.4초). **목표 40~43초 ≈ 330~350자**로 쓰고 실측 후 조정. 길면 `atempo`(⑦에서 1.12배 사용)·문장 잘라내기(`atrim`+`concat`)로 맞추고, 짧으면 사실을 보태 재생성(약 0.1)
- 마지막 문장: "{다음 편 질문}?" 또는 시청자에게 묻는 질문으로 끝(v7.5 — "다음 이야기에서"는 자막으로만, v7.6 — 시청자 질문형은 D-1)
- 과장 금지선: 기록이 '두려워했다'면 '없애려 했다'까지(사료에 있을 때)는 되지만 사료에 없는 행동은 만들지 않는다. 사료에 없는 대사는 쓰지 않는다
- 발음: '맏왕자'→'마당자'로 흐려짐 → '왕자'/'큰아들'. '세 친구'→'새 친구' → '친구 셋'. 받아쓰기 오인식(⑤): 고구려→보구려, 소서노→소선우, 태자→퇴자 — 사용자 청취 결과 음성은 정상. 받아쓰기(small 모델)가 틀려도 사용자 청취 확인 후 넘어간다. ⑨ 오인식: 활을→화를, 끊은→끄는(연음이라 정상), 이듬해→이듬의(청취 확인 요청)
- **목소리 후보 비교 기록(2026-09-29 같은 문장 104자, 모두 남성 프리셋)** — 바꿀 때 참고:
  | 후보 | voice_id | 엔진 | 길이 | 속도 | 비고 |
  |---|---|---|---|---|---|
  | Gideon(중년) | 1ad38ba4-9cc4-4f2f-9fde-b0fefdf67ae5 | qwen_audio_tts(0.1) | 13.4초 | 7.75자/초 | |
  | Sterling(중년) | dc382508-c8bd-443c-8cb2-46e57b8d2e6f | qwen_audio_tts | 14.0초 | 7.45자/초 | |
  | **Harrison(젊음) — 채택** | 573e5163-59b3-4926-aab1-951ef2985f81 | qwen_audio_tts | 13.8초 | 7.52자/초 | ⑤ 실제 313자 43.2초 |
  | Alistair(노년) | d9d5c263-f84e-4752-97b5-3750fcc6fd2f | qwen_audio_tts | 14.9초 | 7.0자/초 | 가장 느림 |
  | Arthur(이전) | 30fc8796-ceb6-4a66-b3a7-4a145ef7f346 | qwen_audio_tts | 13.2초 | 7.89자/초 | 다큐 지시문 |
  | Gideon | 위와 같음 | text2speech_v2 `variant:elevenlabs`(0.3) | 17.7초 | 5.8자/초 | 느리고 무게감, 첫 문장 끝 발음 흐림 |
  | Sterling | 위와 같음 | text2speech_v2 elevenlabs | 13.8초 | 7.4자/초 | |
  - elevenlabs 엔진은 지시문(instruction)이 없다 → 문장부호·줄바꿈으로 완급 조절. 속도가 목소리마다 달라 글자 수 목표를 다시 잡는다.
- **설명하듯 잇기(v8.0, 롱폼 D-1에서 — 사용자가 롱폼 1부 내레이션을 '설명하듯 자연스럽다'고 승인)**: 사실을 나열하지 않고 옆에서 설명해 주듯 잇는다. 듣는 사람이 "왜?"를 떠올리기 전에 다음 문장이 답한다
  - 첫 문장은 짧게 단정, 다음 문장이 이유를 푼다("두 나라의 악연은 뿌리가 깊었습니다. … 그 주몽을 없애려 했던 이가 바로, 부여의 왕자 대소였기 때문입니다.")
  - 연결어미로 인과를 넣는다(~고, ~지만, ~으니, ~다가, ~자). 마침표 단문 셋 이상 연속 금지
  - 해석은 풀이 종결로(~기 때문입니다 / ~것이었습니다 / ~셈입니다). 예: "그러니 이 까마귀는 선물이 아니라, 무릎을 꿇으라는 통첩이었던 셈입니다."
  - 사건은 현재형, 배경·평가는 과거형. 셈을 예고하고 센다("이유는 둘이었습니다")
  - "~다고, 기록은 전합니다"는 [기록]에만. 쉼표는 숨 쉬는 자리(음성 합성이 쉰다)
  - 음성 원고는 숫자를 한글로, 자막은 아라비아 숫자
  - 45초에서는 문장 수를 늘리지 않는다 — 위 규칙으로 문장 사이를 잇고, 위의 '~다' 반복 금지·종결 섞기 규칙과 같이 쓴다
(아래 v7 이야기꾼 문체 규칙은 폐기 — 참고용)
**v7: 흥나는 이야기꾼(폐기)**
- 총 290~310자, 경쾌한 지시문 기준 306자 → 41.1초(④ v7). 말투 '~했지 / ~했어 / ~했대 / ~란다', 부름말 도입, 시청자에게 되묻기, 사료 속 실제 말 인용(출처가 본문이 아니면 "다른 기록엔 ~")

### D-3. 자막 규칙
- 장면당 2줄: 1줄(작게, **≤13자**) + 2줄(크게, **≤10자**). 평서문 요약. **v7.5 크기: 1줄 60px / 2줄 80px(마지막 장면 84px)**(사용자 지정 2026-10-03) — 넘으면 840px 안으로 자동 축소되므로 글자 수를 지켜야 커진 효과가 난다(`cap1_size`·`cap2_size`로 조정)
- **상단 제목(v7.5: 영상 내내 표시)**: 첫 장면에서는 크게(92px, y 425), 첫 장면 끝 0.5초 동안 **80%**로 줄며 **y 392에 끝까지 고정**(`title_keep` 기본 0.8 — 사용자 지정, 0이면 첫 장면에만). 제목은 요약·어그로 역할이므로 의외의 사실 + 물음으로 쓰고, 첫 장면 자막은 제목과 겹치지 않는 문구로. **본고딕 Black(Noto Sans KR 가변 서체, fonts/NSK.ttf) 92px**(v7.6, 사용자 결정 2026-10-04 — 검은고딕(Black Han Sans)은 '꺾·었·했'처럼 획이 많은 글자를 가늘게 그려 글자마다 굵기가 달라 보였다. 획을 덧칠하는 방식은 글자가 뭉개져 기각), 흰 글자 + `{핵심어}` 금색, 굵은 테두리·그림자, 뒤에 상단 어둠 그라데이션. 4~5어절, 12자 넘으면 가운데 띄어쓰기에서 자동 2줄(`\n`으로 지정 가능). 중심 y 425. 0.15초에 크게 떴다가 줄어드는 '슬램' + 북 소리
- **좌상단 연도 배지(v7.4, 사용자 결정 2026-09-29)**: 붉은 낙관 '史' 문양(46px) + 금색 글자(나눔명조 Bold 38), **배경 상자 없음**(검은 테두리·부드러운 그림자로 가독성). ◀▶ 기호는 쓰지 않는다(`year`에 넣어도 렌더러가 지움). '기록상'/'약' 구분은 유지. 낙관 글자는 Noto Serif KR Black(fonts/SEAL.ttf; 없으면 글자 없는 낙관). 후보였던 청동거울·삼족오·해 문양은 미채택(삼족오는 고구려 전용이라 백제·신라 편에 맞지 않음)
- **영상 화면에 시리즈 표시 없음(v7.4, 사용자 결정)**: scenes.json에 `series`를 넣지 않는다. 그 자리(우상단)에 워터마크가 간다. 업로드 제목의 시리즈명은 유지(J)
- 통설·추정·여러 설·미상 장면은 1줄 앞에 태그(태그 부분은 옅은 금색으로 자동 표시)
- **핵심어 강조**: `{한강}`처럼 중괄호로 감싸면 금색. 장면당 1곳까지(인물·지명·숫자)
- 마지막 장면: 1줄 '다음 이야기', 2줄 다음 편 질문(금색). 시청자 질문형(D-1)이면 1줄 질문의 앞부분, 2줄 선택지(금색)
- 출처 줄: '『삼국사기』 고구려본기 · 이미지는 AI 재현' — 자막 바로 아래(세이프존 안)
- 자막 등장: 1줄 → 0.12초 뒤 2줄, 살짝 커지며 떠오름(팝인). 이전 자막은 다음 자막이 뜨기 전에 사라짐(겹침 없음)
- **중앙 정렬(v7)**: 글자 이미지를 실제 잉크 폭으로 잘라 좌우 여백을 같게 만든다(『』, [ ] 쏠림 해결)
- **세이프존 레이아웃(v7.4, 1080x1920 기준 y좌표·중심)**: 연도 배지(왼쪽 x 54)·워터마크(오른쪽 끝 x 960) 245 / 고정 제목 392(첫 장면 425) / 지도 note 550 / 펀치 자막 900 / 자막 1줄 1276 / 2줄 1380 / 출처 1508 / 자막 최대 폭 840px / 어두운 띠 1130~1710(v7.5). 지도 핵심 표지는 y 600~1100.
  - 근거: 여러 쇼츠 세이프존 가이드가 하단 약 300~380px(채널명·구독·설명), 오른쪽 약 96~120px(버튼 열)을 가림 영역으로 본다(제3자 가이드이며 공식 수치 아님, 가이드마다 차이 있음).
  - 바꾸려면 scenes.json `layout`으로 덮어쓴다(예: `"layout":{"cap1_y":1280}`).
- **워터마크(v7.4)**: `"watermark":"역사서클"` 글자만(사용자 결정 2026-09-29), 반투명 70%, 전 구간, 우상단(`series`가 있을 때만 가운데). 선택 `"watermark_logo":"fonts/logo.png"` → 원형 로고 56px + 채널명. 로고 원본은 152x140px라 흐림 → 고해상도(1000px 이상, 투명 PNG) 또는 단순화 버전을 받으면 쓴다. sandbox에서 쓰려면 로고가 Higgsfield에 올라가 있어야 함(사용자가 업로드 위젯으로 올림 → URL로 curl).
- **서체·크기(사용자 결정, 2026-09-28)**: 자막은 **송명(Song Myung)** — 1줄 60 / 2줄 80(마지막 장면 84)(v7.5, 이전 48/58/66). 연도 배지·출처·note는 나눔명조 Bold(38/28/26). 워터마크는 나눔명조 ExtraBold 30. 송명에 없는 글자(· 『 』 등)는 **글자 단위로** 나눔명조로 대체.
- **①~⑳ 원문자**: 송명·나눔명조에 글리프가 없다(2026-09-28 확인). render.py가 원+숫자로 직접 그린다.

## E. 이미지 프롬프트 — 45초 신작 (그림체 고정, v7 채색 — v8.0에서도 청록산수 유지, 사용자 결정 2026-10-12)
각 장면 = [STYLE] + [SCENE] + [ERA] + [NEGATIVE]. STYLE·NEGATIVE는 절대 바꾸지 않는다(채널 일관성). 해상도 `2k`(1520x2688), quality `medium`.

[STYLE] (v7, 사용자 결정 2026-09-28: 무채색 → 채색)
```
Korean blue-green landscape painting (cheongnok sansu) blended with ink-wash brushwork, rich mineral pigments — azurite blue, malachite green, warm ochre, touches of cinnabar red — on hanji paper, dramatic golden-hour light, strong depth and atmosphere, cinematic vertical composition, generous empty space in the lower third for subtitles.
```
- 밤·실내 장면은 `dramatic golden-hour light` 대신 `dramatic night light` / `dramatic light`로 바꿔도 된다(나머지는 고정)
- 색은 풍경·하늘·빛에 쓰고, **인물 옷은 ERA의 고증(무명·삼베)을 바탕으로 아래 의상 색 포인트만 더한다**

[SCENE] `{주체} {행동}, {장소/배경}, {시간대·빛과 색 대비}, {분위기}.` 인물 1~3명 중심, 군중은 원경 실루엣.
- 빛과 색 대비를 한 구절 넣으면 영상미가 산다: `warm golden light outside versus cool blue shadow inside`, `warm orange firelight against cool blue night`, `golden morning mist filling the valleys`
- **정확한 위치·영역이 필요한 장면은 AI 자유 생성이 아니라 섹션 L의 지도 파이프라인으로 만든다**
- 유적·유물 장면: `excavated earthen fortress walls`, `pottery shards on earth` 등 — 실제 출토품과 다를 수 있으므로 특정 유물명을 자막에 붙이지 않는다
- 인물 장면에는 `no flags`를 추가하고, 얼굴 디테일 없이 원경·뒷모습으로. (v7.6 예외: **첫 장면 주인공**은 3/4 정면 허용 — `fierce determined expression painted with simple bold brush strokes`처럼 붓 터치 수준의 표정까지. 사용자가 ⑨에서 얼굴이 보이는 안을 골랐다) (v7.5 예외: 무늬 없는 진영 색 깃발은 허용 — 고구려 `plain crimson banners`, 부여 `plain black banner`. 문양은 여전히 금지 — 롱폼의 깃발 문양은 쇼츠에 쓰지 않는다)
- **의상 색 포인트(v7.5, 사용자 요청 2026-10-03 — 롱폼 history-longform E와 통일)**: 고구려 = `ochre-brown hemp wrap jacket with a bright crimson sash and crimson cuffs`(병사는 `crimson arm bands and sashes, quilted leather vests, spears with short red tassels`, 왕·지휘관은 `dark brown knee-length wrap jacket with crimson cuffs and hem, crimson sash, deep crimson wool cloak`) / 부여 = `long white hemp robes with very wide sleeves, tall leather boots, heavy black sable fur coats`. 흰옷·갖옷은 『삼국지』 부여조 [기록], 붉은색·검은색 대비는 [연출](붉은 까마귀 일화의 '북방의 검은색·남방의 붉은색'에서 착안) → 설명란에 고지
- **피아 색 구분(v8.0, 롱폼 10/12)**: 전투·대치 컷은 고구려 = 붉은 띠·붉은 깃발 / 부여 = 흰 삼베옷·짙은 모피·검은 깃발. 돌격 컷은 진행 방향 앞에 적의 색만, 뒤에 아군 색만 둔다(색이 섞이면 아군을 치는 것처럼 보인다는 피드백)
- **물리·규모 고증(v8.0, 롱폼 10/11~12)**: 해빙기 진창은 발목~무릎 — 말 몸통이 잠기는 그림 금지(계속 깊게 그리면 `the horse STANDS UPRIGHT, knees visible at the mud surface`). 고구려 진영은 넓은 마른 언덕 위 다수 천막 `tents only, no tiled-roof buildings`. 어긋나면 몰입을 깨는 결함으로 본다
- **롱폼 인물과 맞춤(v8.0)**: 롱폼 인물 시트(history-longform E-1: 무휼·노장·대소·청년 대무신왕·괴유·마로)는 실사라 청록산수 장면의 참조로 쓰지 않고 생김새(나이·옷색·소품)만 문장으로 옮긴다. 시그니처 3초의 실사 컷에는 롱폼 시트를 image_references로 쓸 수 있다. 롱폼 실사 STYLE·NEGATIVE·의상 문장은 history-longform E-1
- **첫 장면은 밝고 강하게(v7.5, 사용자 피드백 "후킹해야 하는데 칙칙하다")**: 어두운 실내·밤 금지. `dramatic bright winter daylight`, 야외 또는 빛이 쏟아지는 공간, `vivid crimson against white snow and bright blue mountains, crisp high contrast, bold saturated color`, 주인공을 전경에 크게, 대립 구도(작은 인물 대 큰 무리). 상단 30%는 `bright clear sky`
- **첫 장면 구도(v7.6, ⑨ 사용자 피드백 "임팩트가 부족하다")**: 물건을 건네는 중간 거리 장면은 약하다. **전경 액션 클로즈업** — 주인공을 허리(또는 허벅지) 위로 크게, 핵심 소품이 화면을 대각선으로 가르고, 파편·천이 앞으로 날리고, 배경에 놀라 물러서는 상대(작게, 약간 흐리게). 문구: `Dynamic close foreground action shot: on the right, large in frame from the thighs up, … along a strong diagonal across the frame, … splinters bursting toward the viewer; in the background on the left, smaller and slightly soft, … staggers back in shock; … sense of frozen motion`
  - **후보 비교**: 첫 장면은 구도가 다른 후보 2~3장(예: 소품 전경 / 혼자 선 주인공 / 등 너머 대립 / 액션 클로즈업)을 한 번에 만들어 사용자에게 고르게 한다(장당 1크레딧 — 움직이는 컷을 다시 만드는 것보다 싸다)
  - **동작·신체 명시**: 손이 소품을 쥐는 장면은 자세를 풀어 쓴다 — `He is breaking a large wooden war bow over his raised left knee: both hands grip the bow about shoulder-width apart, one on each side of the knee, pushing down … Anatomically correct body: exactly two arms and two legs, natural shoulders, elbows and wrists, each hand with five fingers wrapped firmly around the wooden limb, believable proportions.` (⑨에서 첫 시도는 팔 위치가 어색해 사용자가 재제작 요청)
  - **외부 참고 이미지**(사용자가 다른 AI로 만든 그림 등): 구도만 가져오고 그림체·고증은 우리 기준으로 다시 그린다. 실사풍·찰갑 갑옷·벽돌 성벽·기와 누각·금실 비단은 `no armor, no stone brick walls, no tiled roofs`로 막는다
  - 첫 장면 그림이 내레이션 첫 문장과 다른 순간이어도 된다(⑨: 그림은 활을 꺾는 순간, 첫 자막은 "아버지가 보낸 {칼}") — 가장 강한 그림을 맨 앞에
- **샷 종류(v7.3)**: 무대 소개 `extreme wide establishing shot, tiny figures` / 긴장 `low-angle shot looking up at` / 결단 `over-the-shoulder shot from behind` / 회상 `soft-focus distant silhouettes` / 절정 `dramatic diagonal composition, strong backlight`. 같은 샷이 연달아 나오지 않게.
- **여백 배치 문구(v7.3)**: 첫 장면 `Keep the top 30% as calm sky or mist with very little detail for a title overlay; place the main subject in the middle band; keep the lower third simple for subtitles.` / 나머지 `Keep the lower third simple for subtitles.`
- **인물 시트(채널 설정, 고증 아님)**: 주몽 `longbow on his back, dark umber hemp coat`(젊을 때 young / 왕일 때 grey-streaked topknot) · 유리 `young man, travel-worn grey cloak, broken sword fragment` · 비류 `deep brown coat, broad-shouldered` · 온조 `light beige coat, slimmer` · 소서노 `middle-aged woman, dark indigo wrap robe, low bun` · 대소 `stern prince/king in a white robe with a dark fur-trimmed cloak`(⑤ 사용, 『삼국지』 부여조 흰옷·갖옷 묘사 기반 — 매번 고증 확인) · 어린 무휼 `small boy prince of about six, ochre-brown jacket with a bright crimson sash, small topknot, seen from behind` · 해명 `young Goguryeo crown prince of twenty-one, dark brown wrap jacket with crimson cuffs, crimson sash, deep crimson wool cloak, simple topknot` · 늙은 유리왕 `aging king with a grey-streaked topknot, dark brown knee-length wrap jacket with crimson cuffs and hem, deep crimson wool cloak, seen from behind` · 황룡국 사신 `foreign envoy in a plain grey-blue hemp robe`(복식 근거 없음 — [연출], 설명란 고지)

[ERA] 시대별 출발점(미검증 — 매번 C의 조사로 보정)
- 청동기·원삼국: `Bronze Age Korean villagers in plain hemp clothing, pit houses with thatched conical roofs, wooden palisade, bronze daggers and plain pottery`
- 삼국 초기/건국기: `plain undyed hemp and cotton clothing in white, beige and earthy brown, short jacket (jeogori) with a simple belt, wide trousers, simple topknot, no silk, no gold ornaments, thatched roofs and earthen walls`
- 3세기 고구려 공식 모임(『삼국지』 公會衣服皆錦繡金銀, 大加 幘·小加 折風): `clan chiefs at formal gatherings wear dark robes with modest embroidered trim and small gold and silver ornaments; senior chiefs wear a soft cloth headwrap, lesser chiefs a plain conical cap` — 이 시기 족장 장면에만 비단·금 금지를 완화
- 삼국 후기(4~7세기): `Three Kingdoms period Korean attire, knee-length wrap jacket with contrasting cuffs and hem, wide trousers, rank colors only for officials, wooden palaces with tiled roofs`
- 고려: `Goryeo dynasty attire, officials in round-collared robes (danryeongpo) with belts, Buddhist temple architecture`
- 조선: `Joseon dynasty attire, commoners in white hanbok, scholars in white dopo with black gat hat, officials in danryeong robes with hyungbae insignia`

[NEGATIVE]
```
No text, no letters, no calligraphy, no map labels, no logos, no emblems or symbols on flags or clothing, no modern objects, no Chinese or Japanese costume elements, no fantasy armor, no excessive gold or ornate silk.
```

## F. 생성 (Higgsfield) — 체크포인트 3 승인 후
0. `balance` 확인. 비용(get_cost 실측, Plus 요금제): 이미지 `gpt_image_2_5` medium **2k 장당 1.0** / 지도 재채색 high 2k **장당 2.75** / 내레이션 약 0.1 / 움직이는 컷 7.5. ⑤ 실제: 이미지 7장 + 음성 + 컷 1개 = 약 14.6. ⑧은 재작업 포함 26.1(이미지 11장·컷 2회). ⑨는 21.6(이미지 14장 — 첫 장면 후보 8장 포함 — + 음성 + 컷 1회). 무료 플랜이면 gpt_image_2_5 불가 → `nano_banana_2`. `get_cost:true` 프리플라이트는 무료.
1. 이미지: `generate_image_batch`(최대 12) `model: gpt_image_2_5`, `quality: medium`, `resolution: 2k`, `aspect_ratio: 9:16` → `jobs_wait`(timeout ≤15, 반복) → `show_generation_by_ids`로 한 번에 표시 → 사용자 확인(고증 어긋난 장면만 재생성). 이전 편 인물 이미지는 L-5 재사용 목록에서 골라 크레딧을 아낀다. **첫 장면은 구도가 다른 후보 2~3장을 같은 배치에 넣는다**(E, v7.6). 고르고 남은 후보는 다른 장면에 돌려쓴다(⑨: 칼 전경 후보 → 5번 장면).
   - 도구 이름은 MCP 접두사가 붙은 전체 이름으로 부른다(접두사 없이 부르면 'No such tool'). 지연 도구는 ToolSearch로 먼저 불러온다.
   - 배치 제출 중 한 건이 'Out of credits'로 실패하는 일시 오류가 있었음 → 잔액 확인 후 그 건만 재제출.
   - **움직이는 컷은 사용자가 첫 장면 이미지를 본 뒤에 만든다** — ⑧에서 확인 전에 만들었다가 "칙칙하다"는 피드백으로 이미지 5장과 컷을 다시 만들었다(약 12.5크레딧 추가).
2. 내레이션: `generate_audio`
   - `model: qwen_audio_tts`, `voice_type: preset`, `voice_id: 573e5163-59b3-4926-aab1-951ef2985f81`(**Harrison**, v7.4 확정), `language: ko`
   - `instruction`(**128자 제한** — 넘으면 422 오류): `웅장한 역사 다큐멘터리 내레이터. 낮고 굵은 성인 남성 목소리, 차분하고 무게감 있게, 문장 끝은 단호하게, 긴장감 있는 완급 조절.`
   - 이전(폐기): Arthur 30fc8796-… + 할아버지 이야기꾼 지시문
   - 같은 대본·지시문도 낭독 속도가 회마다 다르다(⑦: 333자 34.3초, 403자 50.4초). 길이가 맞지 않으면 재생성하거나 sandbox에서 `ffmpeg atrim/concat/atempo`로 다듬는다(다듬은 뒤 다시 받아써서 이음매 확인).
3. 지도: 섹션 L 파이프라인(라이브러리에 같은 범위가 있으면 재사용, 무료).
4. **움직이는 컷(v7.4)**: `generate_video`, `model: kling3_0`, `mode: std`, `duration: 5`, `aspect_ratio: 9:16`, `medias: [{value: 장면 이미지 job_id, role: start_image}]` → **컷당 7.5크레딧**. Seedance 2.5 720p 4초는 28크레딧이라 비추천. 순서: 이미지 생성 → 사용자 확인 → 승인된 컷만 생성 → 렌더.
   - 프롬프트 틀: `Subtle living-painting motion. Camera: very slow push-in. Motion: {움직임}. Keep the exact painting style, brush texture, colors and composition of the start image. No new objects, no text, no face close-ups, no morphing, no camera cut.`
   - ⑤ 실제 움직임 문구: `mist drifts through the valley below, the archer's cloak ripples in the wind, clouds move slowly` / ⑧: `the crimson banners and the black banner snap and ripple in the wind, light snow drifts across the courtyard, … the small boy stands perfectly still` / ⑨(액션 컷): `the wooden bow finishes cracking over the knee and splinters drift outward through the air, the loose bowstring whips, the crimson cloak ripples in the wind, light snow drifts across the courtyard, the envoy in the background staggers back half a step` + 금지 문구에 `no extra limbs` 추가
   - **`sound: "off"`(문자열)로 제출한다**(v8.1) — `false`는 무시돼 소리가 켜지고 크레딧이 더 나간다(롱폼 10/16 사고: 5초 pro 8.75 → 12.5). 렌더러는 영상 소리를 버리므로 소리는 필요 없다. 프롬프트가 프리셋과 비슷하면 preset_recommendation이 오니 `declined_preset_id`(24bae836-2c4a-48e0-89b6-49fcc0b21612)를 넣어 다시 제출(프리셋은 쓰지 않음)
   - 출력은 720x1276·24fps·5초(⑤ 실측) → 렌더러가 1080x1920·30fps로 키움(다른 장면보다 약간 덜 선명)
   - scenes.json: 그 장면에 `"video":"v1.mp4"`(sandbox에 curl로 받은 파일 또는 URL), `image`는 빈 문자열. 카메라 무브 없이 영상 그대로 + 톤 보정(채도 1.15·대비 1.05·검정 띄움). `vstart`로 시작 지점 조정 가능. 장면이 영상보다 길면 마지막 프레임 정지
   - 편당 1컷(첫 장면) 기본 — ⑤에서 사용자가 1번만 선택
   - (v8.0) 롱폼은 비교 시험(C03·V01·V09)으로 `mode: pro`를 확정했다(16:9 1912x1080). 시그니처 실사 컷처럼 질이 중요한 컷은 pro 9:16 비용을 `get_cost`로 확인해 std와 함께 사용자에게 고르게 한다. 영상 제출에는 `declined_preset_id: "24bae836-2c4a-48e0-89b6-49fcc0b21612"`, 다른 추천 88fcca71-4430-4324-851b-b061a8e134bc(Sword and Sorcery)가 오면 그것도 반려
5. **시그니처 3초(v8.0, D-1)**:
   1. 수묵화 스틸(`gpt_image_2_5`, 9:16, 2k): 먹 농담 + 인물, 여백 많음 — 첫 장면 액션 구도와 같은 구도. 상단 30%는 제목 자리
   2. 같은 스틸을 참조(image_references)로 실사 스틸: `Recreate reference image 1 as a photorealistic live-action cinematic film still with the EXACT same composition … Change only the medium.` + 롱폼 실사 STYLE의 `16:9 widescreen`을 `vertical 9:16`으로 + 롱폼 NEGATIVE
   3. 실사 스틸 → Kling 움직이는 컷(호흡·옷자락·파편·눈). 수묵 쪽은 3초라 정지 스틸로 충분
   4. 먹 번짐은 **코드로** 합성: 롱폼 키트 zip(B + `bdedbf88-07ac-4224-9bd1-0ce6cec64236.zip`, history-longform 0번)의 `sig/sig2.py` 엔진(왜곡된 거리장 + 로브 마스크, 번지는 먹 띠 → 페더 → 실사 드러남)을 1080x1920으로. 롱폼 인자 TOT·T0·T1 = 10·3.6·6.6 → 쇼츠 출발점 3.0·0.3·2.1, 떨어지는 위치 X0·Y0는 인물 가슴께(제목 띠 y < 0.25, 자막 띠 y > 0.6을 피함). 먹 테두리가 점선처럼 '탄 종이' 느낌이 나면 띠·페더를 넓힌다. Kling으로 먹물 영상을 만들면 화면을 덮지 못하고 회색 배경이 남는다 → 쓰지 않는다
   5. 결과 mp4를 scenes.json 첫 장면 `video`로. 렌더러가 영상 컷에도 톤 보정(채도 1.15·대비 1.05)을 거므로 실사가 약간 진해진다 — 문제가 되면 톤 보정을 끄는 옵션을 render.py에 추가한다[미구현]
   6. 효과음: 먹 떨어지는 소리(롱폼 inkdrop job 3dfbeeea 재사용 가능)를 첫 boom과 함께 또는 대신
   - 비용(대략): 스틸 2장 약 2 + 움직이는 컷 1개(std 7.5, pro는 확인). 기존 첫 장면 컷 대비 이미지 1장 추가
6. **음향(v8.0, 롱폼 F·K에서)**:
   - 기본은 render.py 합성 효과음(boom·hit·whoosh·brush) + 바람 앰비언스. 전투·행군 장면이 있는 편은 `mirelo_text_to_audio`(duration 필수, 소량 크레딧)로 현장음을 만들 수 있다. 생성 뒤 평균 음량(RMS)을 재서 무음·클리핑을 거른다(롱폼 sword beec1205는 거의 무음이라 불채택). 재사용 가능한 롱폼 2부 효과음 job: melee fefc84ca · horsemud 909de03f · breath 296fe193 · march 5c514ec6 · wind 13f7ed42 · camp b50eaf4a · inkdrop 3dfbeeea · charge cdf1a681 · siege d8e7867d
   - 음량은 피크가 아니라 **RMS 기준**으로 맞춘다(피크 기준이면 효과음이 −35dB로 묻힌다 — 롱폼 10/12 사고). 롱폼 실측: 내레이션 약 −17.5 dB RMS, 행군·전투 효과음 −19~−20, 내레이션 아래 10dB 감쇠. render.py의 `bgm`은 피크 정규화(`bgm_db` −17)이므로 효과음 파일을 `bgm`으로 깔 때는 미리 RMS로 맞춘 파일을 쓴다
   - BGM: 사용자가 Suno 유료 플랜으로 만든 곡. 채팅 첨부는 sandbox로 못 보낸다 → 구글 드라이브 폴더를 '링크가 있는 모든 사용자'로 공유받아 Drive 커넥터 `search_files`(`parentId = '<폴더 id>'`)로 id → sandbox에서 `https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t`. 유튜브·Suno 링크에서 음원을 뽑지 않는다. Suno 무료 플랜 곡은 상업 이용 불가
   - 롱폼에서 승인된 음악 음량(참고): 곡 약 −16 LUFS 기준 일반 −2dB / 전투 0dB, 원음을 키로 `sidechaincompress=threshold=0.08:ratio=1.5:attack=150:release=900`, 마지막 `alimiter=limit=0.89` → 음악 −21~−23 dB, 원음 −18 dB, 전체 약 −13.4 LUFS('거의 안 들린다' 피드백 두 번 뒤 승인). 바람 앰비언스 때문에 문턱을 낮게 잡으면 음악이 내내 눌린다
   - 보고에는 내레이션·효과음·음악 평균 dB를 표로 주고, 들을 수 없어 수치로만 맞췄다고 적는다

## G. 렌더링 (Higgsfield `sandbox_exec`에서만)
- 작업공간(Bash)은 Higgsfield CDN·업로드 주소 접근이 403 → 다운로드·합성·업로드는 모두 sandbox_exec에서. 작업공간은 **코드 미리보기용**(GitHub raw·PyPI는 됨).
- sandbox 사양(2026-09-28 확인): 8코어, 메모리 7GB, Python 3 + Pillow 12.3 + numpy 2.4 + faster-whisper, ffmpeg 5.1. 명령 1회 최대 16,000자.
- **sandbox 유지**: 호출이 끝나고 약 10초 뒤 폐기되지만, `background:true` 작업이 도는 동안은 15분 임대가 유지된다. 첫 호출을 '다운로드 + sleep 840' 백그라운드로 띄워 두고, 15분이 지나기 전에 같은 방식으로 다시 띄운다.
- **스크립트 전달**: render.py(**v7.6, 29,510바이트, md5 197958161508814c8e813be3cb66864c**)가 16,000자를 넘으므로 sandbox에 `rA.py`·`rB.py`로 따로 쓴 뒤 `cat rA.py rB.py > render.py`(파트 A 13,525바이트, 파트 B 15,985바이트·15,207자 — 16,000자 한도에 가까우니 같은 명령에 다른 내용을 붙이지 않는다). `sprite.py`(4,099바이트)는 **항상** 같은 폴더에 따로 쓴다(v8.1 도트 필수 — 없으면 렌더러가 조용히 건너뛰므로 H에서 확인). 각각 `md5sum`으로 확인. 스크립트를 base64로 옮기지 않는다(Higgsfield 도구 지침).
- 영상 컷 프레임은 uint8 배열(5초 약 0.9GB)로 두고 톤 보정은 ffmpeg 필터에서 한다(numpy float 변환은 메모리 3GB를 써서 작업공간에서 OOM이 났음).
- 렌더를 중간에 멈출 때 `pkill -f render.py`를 쓰면 그 명령을 실행한 셸까지 죽는다 → `pkill -f 'python3 render'`처럼 쓴다.
- 긴 명령이 API 502로 끊겨도 sandbox 안에서는 실행됐을 수 있다 → 파일 존재부터 확인하고, 업로드 PUT이 412면 이미 올라간 것(If-None-Match).
- 실측: 45초 렌더 약 100초(8코어), 받아쓰기 약 30초, 지도 검수(qa.py) 약 60초. 결과 파일 약 70MB.
- **메모리 초과(v7.6, ⑨에서 2회 실패)**: `pool.imap`으로 전 프레임을 한꺼번에 넘기면 인코딩이 밀릴 때 주 프로세스에 프레임(장당 6.2MB)이 쌓여 3.9GB에서 OOM으로 죽었다(`dmesg | grep -i oom`, 배경 작업 로그에 'Killed'). → 48프레임 묶음(`pool.map`)으로 수정. 그래도 렌더 중 사용 메모리가 6GB 안팎까지 오르므로 렌더 중에는 다른 무거운 작업을 띄우지 않는다
- **업로드 전 검증(v7.6)**: 렌더가 죽으면 깨진 final.mp4가 남고, 그대로 PUT하면 200이 떨어져 그 업로드 주소를 못 쓰게 된다. `ffprobe … > probe.txt && grep -q "^4" probe.txt && curl … PUT`처럼 길이가 정상일 때만 올린다. 깨진 파일이 올라갔으면 `media_confirm`하지 말고 `media_upload`로 새 주소를 받는다
- **(v8.0) 롱폼 작업에서 겪은 sandbox 규칙**: foreground 호출이 약 60초를 넘으면 502 → 오래 걸리는 건 background로 돌리고 `sleep ≤58`로 폴링. 502 난 작업이 뒤에서 계속 돌 수 있으니 pid로 중복 확인 후 kill / `pkill -f <자기 명령 문자열>`은 자기 셸을 죽인다 → pid로 kill / 디스크 약 26GB — 영상 raw 캐시는 작업 사이에 지운다 / 병렬 curl은 잘린다 → 순차 받기 + 재시도, PNG는 PIL로 load 검사 / 업로드 주소는 한 번만 쓸 수 있고 1GB 넘는 파일은 400·502 / 몽타주 정책 오류가 나면 접촉 시트는 PIL로 직접 만든다
- 수정본 재렌더(자막·지도·서체만 바꿈)는 크레딧 0, 약 2분. sandbox가 살아 있으면(`ls ~/hs`) 파일을 다시 올리지 않고 scenes.json·spec만 고쳐 다시 돌린다

### G-1. 호출 순서
1. `sandbox_exec`(background): 폴더·폰트·Natural Earth·고도 자료 다운로드 후 `sleep 840` (지도 새로 안 만드는 편은 mapdata·relief 생략 가능)
   ```bash
   cd ~ && mkdir -p hs && cd hs && mkdir -p fonts mapdata maps img relief ep
   for f in ne_10m_land ne_10m_rivers_lake_centerlines; do [ -f mapdata/$f.geojson ] || curl -sSfL -o mapdata/$f.geojson "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/$f.geojson"; done
   [ -f fonts/B.ttf ] || curl -sSfL -o fonts/B.ttf https://raw.githubusercontent.com/google/fonts/main/ofl/nanummyeongjo/NanumMyeongjo-Bold.ttf
   [ -f fonts/X.ttf ] || curl -sSfL -o fonts/X.ttf https://raw.githubusercontent.com/google/fonts/main/ofl/nanummyeongjo/NanumMyeongjo-ExtraBold.ttf
   [ -f fonts/SM.ttf ] || curl -sSfL -o fonts/SM.ttf https://raw.githubusercontent.com/google/fonts/main/ofl/songmyung/SongMyung-Regular.ttf
   [ -f fonts/NSK.ttf ] || curl -sSfL -o fonts/NSK.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf"   # v7.6 제목 = 본고딕 Black(가변 서체, 약 10MB)
   [ -f fonts/SEAL.ttf ] || curl -sSfL -o fonts/SEAL.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/notoserifkr/NotoSerifKR%5Bwght%5D.ttf"   # 연도 배지 낙관 '史'(약 24MB)
   [ -f relief/etopo1.jpg ] || (pip download basemap-data==2.0.0 --no-deps -d /tmp/bm -q && python3 -c "
   import zipfile;z=zipfile.ZipFile('/tmp/bm/basemap_data-2.0.0-py3-none-any.whl')
   for n in ['etopo1.jpg','shadedrelief.jpg']: open('relief/'+n,'wb').write(z.read('mpl_toolkits/basemap_data/'+n))")
   echo READY; sleep 840
   ```
2. 지도(L-4): 라이브러리에 없으면 ctl.py로 밑그림 → `media_upload`(png) → sandbox에서 PUT → `media_confirm(image)` → 재채색 생성 → qa.py 검수. 재사용이면 작업공간에서 anim.py로 `.anim.json`을 만들어 sandbox에 heredoc으로 쓴다
3. `sandbox_exec`: AI 지도 PNG·내레이션·움직이는 컷 받기 + 받아쓰기(H)
4. `sandbox_exec`: `cat > rA.py <<'PYEOF'` 파트 A → `md5sum rA.py`
5. `sandbox_exec`: `cat > rB.py <<'PYEOF'` 파트 B → `cat rA.py rB.py > render.py && md5sum render.py` (다음 호출에서 `cat > sprite.py <<'PYEOF'` — 필수, v8.1)
6. `media_upload`(filename .mp4)로 upload_url 먼저 받기
7. `sandbox_exec`(background): scenes.json·anim.json 작성(영역이 있으면 sandbox에서 anim.py를 돌려 `.layer.png`까지 만든다) + `python3 render.py scenes.json > render.log 2>&1` + `ffprobe … > probe.txt && grep -q "^4" probe.txt &&` `curl -f -X PUT -H "Content-Type: video/mp4" -H "If-None-Match: *" --upload-file final.mp4 '<upload_url>'`
8. 폴링(sleep ≤55) → HTTP 200 확인 → `media_confirm(type:video)` → url 전달
- 작업공간에서 먼저 임시 이미지로 PREVIEW(G-3)를 돌려 레이아웃을 확인한 뒤 sandbox에 올린다(영상 컷은 `ffmpeg -f lavfi -i testsrc` 로 대체).

### G-2. scenes.json 형식 (v7.4, ⑤ 실제 예)
> 〔코드 11줄(원본 368–380줄) → `history-circle/kit/shorts/scenes_example.snippet.json` — 같은 내용이 kit에 그대로 있음(verify_skills.py)〕
- **v7.4 필드**: 장면 `"video"`(움직이는 컷, F-4)·`"vstart"`, 효과음 없는 컷 `"trans":"cut","sfx":"none"`, `series` 생략(화면 표시 안 함), `year`에 ◀▶ 쓰지 않음, 선택 `"font_seal"`(기본 fonts/SEAL.ttf)
- v7.3 필드: `"watermark"`, `"watermark_logo"`, `"title"`(`\n` 줄바꿈 가능, `title_size` 기본 92), 장면별 `"punch":[{"text","at","dur","size","sfx"}]`(at은 장면 시작 기준 초, sfx 기본 hit)
- 지도 장면: `image`=AI 재채색 지도(URL 또는 로컬), `map`=같은 center/span_lat의 spec으로 anim.py가 만든 `.anim.json`. AI 지도는 자르지 않고 2160x3840으로 늘려 맞춘다(밑그림과 좌표 일치)
- `start`: 문장 시작(받아쓰기) + 0.4초. `total` = 마지막 단어 끝 + 0.4 + **0.6초**(v7.5)
- **v7.5 선택 필드**: `title_keep`(0.8), `cap1_size`(60), `cap2_size`(80), `fade_out`(0.3), `layout.title_s_y`(392). ⑧ 실제 구성: 9장면 시작 시각 0(움직이는 컷) / 3.52(지도) / 6.80 / 11.06 / 16.24(`flash`) / 22.48(펀치 자막 1회) / 29.40 / 33.56 / 38.38, total 43.72, 제목 `"부여 왕의 협박에 맞선 게\n{6살} 왕자라고?"`
- **v7.6 선택 필드**: `font_title`(기본 fonts/NSK.ttf), 장면 `"sprite":{"at":1.0,"dur":3.8,"y":1012,"alpha":0.9}`(**필수 — 매 편 1곳 이상, D-1(v8.1).** sprite.py가 있을 때 — 장면 시작 `at`초 뒤부터 `dur`초 동안 도트가 왼→오로 지나감, `y`는 도트 윗변. 자막 띠 시작 1130 바로 위인 1012가 기본). ⑨ 실제 구성: 8장면 시작 시각 0(움직이는 컷) / 4.8(`flash`) / 11.56(지도) / 16.7 / 23.72(`punch`) / 28.62(도트) / 34.44 / 38.76, total 45.16, 제목 `"활 하나 꺾었다고\n태자가 {죽어야} 했다고?"`, 자막 예 `["[해석] 복종하라는 활","사신 앞에서 {꺾다}"]`, 마지막 `["여러분이 왕이었다면","살릴까, 죽일까?"]`
- move `in`·`out`·`pan_l`·`pan_r`·`punch`·`cutin`·`still`·`focus` / trans `ink`(0.6)·`whip_l`·`whip_r`(0.32)·`flash`(0.4)·`fade`·`cut` / fx `mist`·`shake` / `sfx`: `boom`·`hit`·`whoosh`·`brush`·`none` / `amb`: `wind`·`river`·`none` / `bgm`·`bgm_db`·`duck_db` / `layout`
- 톤: AI 이미지는 채도 +22%·대비 +8%·하이라이트 따뜻/그림자 청록·한지 결. 영상 컷은 근사 보정. 지도는 그레이딩하지 않음. 모든 장면에 비네트·그레인
- 떨림 방지: 카메라는 `resize(box=부동소수)`, 지도 표지·라벨은 원본 좌표계에 고정 크기로 그린 뒤 함께 샘플링

### G-3. 미리보기
- `PREVIEW=1.0,4.5,8.2 python3 render.py scenes.json` → 해당 시각 프레임만 `prev_XXX.X.png`로 저장. 작업공간에서도 레이아웃 점검에 쓴다(AI 이미지는 작업공간에서 못 받으므로 임시 이미지로 대체).

### G-4. render.py 전문 (v7.6 — 본고딕 제목·도트 선택 모듈·묶음 렌더 + v7.5 기능, 29,510바이트)
파트 A (`cat > rA.py <<'PYEOF'` … `PYEOF`, 13,525바이트, md5 b0974d8f773a966e7016d499fdf1d6fd):
> 〔코드 206줄(원본 396–613줄) → `history-circle/kit/shorts/render_v76.py` — 같은 내용이 kit에 그대로 있음(verify_skills.py)〕
파트 B (`cat > rB.py <<'PYEOF'` … `PYEOF`, 15,985바이트, md5 91b444f47d7029e80ac32349e2791385; 합친 render.py md5 197958161508814c8e813be3cb66864c):
> 〔코드 213줄(원본 615–834줄) → `history-circle/kit/shorts/render_v76.py` — 같은 내용이 kit에 그대로 있음(verify_skills.py)〕
sprite.py (v7.6 선택 모듈 — 깨알 도트 기마 무사, 4,099바이트, md5 e0b0d68c8999a5603bc5b29d5c2bf5e7). **필수(v8.1) — 매 편 올린다.** 다른 도안(행군·배·나무꾼 등)이 필요하면 `_frame()`의 사각형 좌표를 바꾼다. render.py와 같은 폴더에 두면 `sprite`가 있는 장면에서 그려지고, 없으면 무시된다. **자체 제작 도안**(황토 저고리 + 진홍 망토 + 갈색 말, 4프레임 달리기, 30x24칸을 4배 = 120x96px)이며 게임·만화의 그림을 본뜨지 않는다:
> 〔코드 61줄(원본 836–898줄) → `history-circle/kit/shorts/sprite.py` — 같은 내용이 kit에 그대로 있음(verify_skills.py)〕
- 도안 확인: 작업공간에서 프레임 4장을 이어 붙여 사용자에게 보여 줄 수 있다(FR 리스트). 다른 도트가 필요하면 `_frame()`의 사각형 좌표만 바꾼다
- 분위기 주의: 죽음·패배처럼 무거운 장면에 넣을 때는 작게(높이 100px 이하)·한 번만·자막 위쪽으로. ⑨는 사용자가 무거운 장면(6번)에 넣기를 택했다

## H. QA (전달 전 필수)
- **렌더 전에** sandbox에서 faster-whisper(`small`, language=ko, word_timestamps)로 받아쓰기 → 각 문장 첫 단어 시각 +0.4초를 `start`에 넣는다
- 받아쓰기에서 고유명사가 이상하게 인식되면 사용자에게 해당 대목 청취 확인을 요청하고, 필요 시 표현을 바꿔 음성만 재생성
- ffprobe: 1080x1920, 41~44초, 오디오 스트림 존재
- 자막: text_img()가 840px 내로 자동 축소하고 잉크 폭 기준 중앙 정렬
- 지도: qa.py 수치(L-4) + 겹침본을 사용자에게 링크로 전달. 바다가 작거나 없는 지도는 수치가 무의미하므로 강 위치를 사용자 눈으로 확인
- 세이프존·레이아웃 미리보기: 작업공간에서 G-3 PREVIEW(임시 이미지)로 확인
- 액션 과다 점검: punch·cutin·whip·flash 합계 편당 3~4회 이하
- 고증 재점검: 내레이션·자막의 모든 문장이 고증 시트의 등급과 일치하는지, 인용 대사가 사료에 실제로 있는지, 연도 배지가 사료 DB로 확인됐는지
- 서사 재점검(D-0): 핵심 메시지 한 문장, 문장 간 연결어 테스트, 인과 표현·시대 소급 여부
- 업로드 후: 유튜브 스튜디오 '참여도' 탭의 **계속 시청함/이탈함** 비율과 게시 24시간 유효 조회수를 편마다 A-4에 기록해 첫 화면·주제를 비교(지표는 공식, 목표치는 비공식). 기준선: ⑥ 43.5% / 210회. 평균 시청 시간이 영상 길이보다 길면 내용은 통과, 계속 시청 비율이 낮으면 주제·첫 화면 문제로 본다
- 템포 점검(v7.5): 장면 수 9 이하, 장면 평균 4.5초 이상(최소 3.5초), 같은 그림 연속 컷 없음
- 문체 점검(v8.1): 종결 어미 목록에서 같은 어미 연속 0회, 평서 '~다.' 0회, '합니다'체 바탕에 '~죠/~요'가 섞였는가
- 제목 점검(v7.6): 작업공간 PREVIEW로 제목 글자 굵기가 고른지 확인(본고딕 Black). 지도 장면에서 제목(y 300~470)·note(y 550)가 지도 라벨을 가리지 않는지도 PREVIEW로 확인 — ⑨에서 '부여 ?' 라벨이 제목 뒤에 숨어 위치를 옮겼다
- 해석 점검(v7.6): 내레이션에서 사료에 없는 의미 부여가 단정형으로 쓰이지 않았는지, 자막 [해석] 태그와 설명란 고지가 있는지
- 도트 점검(v8.1): 1곳 이상 있는가, 놓인 자리(들판·길·물 위)와 방향·세력 색이 장면과 맞는가, sprite.py가 실제로 렌더됐는가(PREVIEW로 확인)
- 첫 장면 점검(v7.5): 밝은가(어두운 실내·밤 아님), 진영 색 포인트(붉은색 대 흰색+검은색)가 보이는가 — 직접 볼 수 없으므로 움직이는 컷을 만들기 전에 사용자에게 이미지 확인을 요청
- 한계 고지: 영상·음성·AI 이미지를 직접 보고/듣지 못하므로(움직임은 정지 프레임으로, 소리는 음량 수치·받아쓰기로만 확인) 사용자에게 1회 시청 확인 요청(색감, 움직이는 컷 화질, 효과음 음량, 가짜 글자, 지도 강 위치, 시그니처 먹 번짐 속도)
- 글자 확인(v8.0, 롱폼 교훈): '무휼'→'무휴', '솥'(U+C1A5)을 '솜'·'쇥'으로 잘못 넣은 적이 있다 — 대본·자막의 한글 고유어는 쓰고 나서 글자를 확인한다(음성은 틀린 글자를 그대로 읽는다)
- 라디오 점검(v8.0, A-0): 화면 설명 없이 대본만 읽어 질문·선택·결과가 이해되는지, 지도 라벨·연도 배지·태그가 내레이션에도 나오는지
- 컨셉 점검(v8.0): 상대의 판단이 그럴 만하게 그려졌는가, 신이한 기사를 두 단계로 말했는가, [상상]·[연출]을 밝혔는가
- 재편집 편은 M-6 QA를 따른다

## I. 전달 형식 (사용자에게)
□ 결론: 영상 링크 1줄
□ 구성: 질문 → 답 한 줄(등급 포함), 장면 한 줄 요약, 내레이션 전문
□ 고증: 애매하거나 미확인인 항목과 영상에서의 처리 방식
□ 확인 필요: 타이밍/발음 이슈, 사용 크레딧·잔액
□ 편성표 갱신본 + 다음 편 후보(◀●▶) → 체크포인트 1로 연결
□ 업로드 메타데이터(J)
출처 목록

> 〔현행 규칙 — `reference-upload.md`에 있음: 'J. 유튜브 업로드 메타데이터 템플릿'. 업로드 메타데이터를 쓸 때만 읽는다〕
> 〔현행 규칙 — `reference-planning.md`에 있음: 'K. 앵커 후보 (시대순, 사용자와 선택)'. 곁가지 신작 후보를 고를 때만 읽는다〕
## L. 지도
> 〔archive.md로 이동: 'L-0. 지도 v3 (v8.0 채널 표준 — 사용자 결정 2026-10-12, 롱폼과 통일)' — 지도 v3 표준 → 현행은 history-map-v4 v4-S(원장 C1, 11/04). v3 문법 중 유지 항목은 원장 map_version〕
> 〔현행 규칙 — `reference-map-legacy.md`에 있음: '(대체용) 채색 지도 (v7: 코드 밑그림 + AI 재채색 + 코드 표지)'. v4-S가 아닌 AI 재채색·라이브러리 지도를 쓸 때만 읽는다〕
> 〔현행 규칙 — `reference-map-legacy.md`에 있음: 'L-1. 언제 쓰나'. v4-S가 아닌 AI 재채색·라이브러리 지도를 쓸 때만 읽는다〕
> 〔현행 규칙 — `reference-map-legacy.md`에 있음: 'L-2. 지도 고증 규칙'. 지도 고증을 점검할 때만 읽는다〕
> 〔현행 규칙 — `reference-map-legacy.md`에 있음: 'L-3. spec 형식 (ep/m_이름.json) — anim.py 입력'. v4-S가 아닌 AI 재채색·라이브러리 지도를 쓸 때만 읽는다〕
> 〔현행 규칙 — `reference-map-legacy.md`에 있음: 'L-4. 새 지도 만들기 (라이브러리에 같은 범위가 없을 때)'. v4-S가 아닌 AI 재채색·라이브러리 지도를 쓸 때만 읽는다〕
> 〔현행 규칙 — `reference-map-legacy.md`에 있음: 'L-5. 승인 지도·이미지 라이브러리 (재사용 — 같은 범위면 새로 만들지 않는다)'. 지난 편 지도·이미지를 재사용할 때만 읽는다〕
> 〔현행 규칙 — `reference-map-legacy.md`에 있음: 'L-6. 스크립트'. v4-S가 아닌 AI 재채색·라이브러리 지도를 쓸 때만 읽는다〕
> 〔archive.md로 이동: 'L-7. 대체용: 코드로 그리는 채색 지도 (map.py v7)' — 대체용 map.py v7 — 코드는 kit/map/map_v7.py〕
> 〔현행 규칙 — `reference-remix.md`에 있음: 'M. 롱폼 재편집 숏츠 (v8.0 — 2026-10-07 대무신왕 1부 5편 제작 방식, 사용자 승인)'. 롱폼 재편집 쇼츠를 만들 때만 읽는다〕
> 〔현행 규칙 — `reference-remix.md`에 있음: 'M-1. 편 고르기 (롱폼 1편당 3~5편, 사용자 결정 10/7 '추천 5편')'. 롱폼 재편집 쇼츠를 만들 때만 읽는다〕
> 〔현행 규칙 — `reference-remix.md`에 있음: 'M-2. 원본 준비'. 롱폼 재편집 쇼츠를 만들 때만 읽는다〕
> 〔현행 규칙 — `reference-remix.md`에 있음: 'M-3. 화면 배치 — 혼합(사용자 결정 10/7)'. 롱폼 재편집 쇼츠를 만들 때만 읽는다〕
> 〔현행 규칙 — `reference-remix.md`에 있음: 'M-4. 화면 글자 (ASS, 1080x1920)'. 롱폼 재편집 쇼츠를 만들 때만 읽는다〕
> 〔현행 규칙 — `reference-remix.md`에 있음: 'M-5. 소리와 컷 경계'. 롱폼 재편집 쇼츠를 만들 때만 읽는다〕
> 〔현행 규칙 — `reference-remix.md`에 있음: 'M-6. 렌더·QA·전달'. 롱폼 재편집 쇼츠를 만들 때만 읽는다〕
> 〔현행 규칙 — `reference-remix.md`에 있음: 'M-7. build_short.py (8,368바이트 — v8.0 구판. **v8.1은 드라이브 `kit_build_short_v81.py`(id 1IZveJgYtsIoi9jn4kIGearse5LypZnNA)에서 받아 쓴다**: `curl -sSL -o build_short.py "https://drive.usercontent.google.com/download?id=1IZveJgYtsIoi9jn4kIGearse5LypZnNA&export=download&confirm=t"` 후 md5 1362e95870c47298b02436fd37ab0ba3 확인. 폰트: fd/에 B.ttf·X.ttf·SM.ttf·SEAL.ttf·NSKBlack.ttf(M-2). sandbox에서 fontTools가 없으면 `env -u PYTHONPATH python3 -m pip install --target ~/pylib fonttools` 후 `PYTHONPATH=~/pylib`)'. 롱폼 재편집 쇼츠를 만들 때만 읽는다〕
> 〔archive.md로 이동: 'M-8. 설정 예 (10/7 ③ 매복 작전 — 자막 일부 생략)' — 10/7 편별 설정 예 — 코드는 kit/shorts/cfgs_example_ep1-3.py〕
