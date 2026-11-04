# 역사서클 제작 키트 — git 이전 목록 (2026-11-04, 세션 1 작업 B)

원칙: 파일 내용은 원본 그대로(재작성·헤더 수정 없음). 출처·검증은 이 표에만 적는다.
검증 기준: md5 = 스킬에 기록된 값과 대조 / 크기 = Drive 메타데이터(fileSize)와 대조 / 구문 = `python3 -m py_compile`.

## 1. 확보한 파일 (27개)

### shorts/
| 파일 | 버전 | 출처 | md5 | 검증 | 상태 |
|---|---|---|---|---|---|
| render_v76.py | render.py v7.6 (29,510B) | history-shorts:396-613(파트 A) + 615-834(파트 B) 연결. Drive `kit_shorts_render_v7.6.py` 1YYNzLR6RmFhGwLnQLVAoWwMwNYGVNYIo와 동일본(아래 주1) | 197958161508814c8e813be3cb66864c | 파트 A·B·합본 md5 모두 스킬 기록과 **일치**, 크기 = Drive 29,510B, 구문 OK | 현행 |
| sprite.py | v7.6 도트 기마 무사 (4,099B) | history-shorts:836-898 | e0b0d68c8999a5603bc5b29d5c2bf5e7 | md5 **일치**, 구문 OK | 현행(v8.1 필수) |
| build_short_v81.drive.py | build_short.py v8.1 (11,713B) | Drive `kit_build_short_v81.py` 1IZveJgYtsIoi9jn4kIGearse5LypZnNA | 1362e95870c47298b02436fd37ab0ba3 | md5·크기 **일치**, 구문 OK | 현행 |
| build_short_v80.skill.py | build_short.py v8.0 (8,368B) | history-shorts:1559-1683 (M-7 본문, 스킬이 '구판'으로 표기) | 0737cacda62824b12af3679aa98b945e | 크기 = 스킬 기록 8,368B, 구문 OK | 구판(참고) — 주2 |
| build_short_wrap_patch.snippet.py | wrap 패치 조각(10/22) | history-production-standards:96-102 | c4a859977e45a279fe73dd6c3e390eec | 조각이라 단독 구문 검사 불가(정상) | v8.1에 반영됨 |
| cfgs_example_ep1-3.py | 재편집 설정 예(10/7 ③) | history-shorts:1689-1700 | 04ad094547d76a223d5518f444e634bb | 구문 OK | 예시 |
| kit_shorts_p3_cfgs.py | 대무신왕 3부 재편집 5편 설정(10/22) | Drive 18P1ybBICaXzF-dPGxCn0w2QvBK7-wHVw | ac031406c0142fa5aa811acb4faba7ab | 크기 4,592B **일치**, 구문 OK | 기록 |
| kit_shorts_ocr_subs.py | 자막 OCR(10/22) | Drive 16zS7ZqX7dvYyYSrIt6NYvfwYb_UiRVYc | fbe85c29c600ee8abcf027f2b2354f04 | 크기 1,362B **일치**, 구문 OK | 현행 |
| kit_shorts_biryu_build.py | 비류 편 빌드(10/23) | Drive 13XeJNNwSfjwHECrpf8LVYnkVhODA8LpL | 8076fe84d5d323f5455e20531a931dde | 크기 3,623B **일치**, 구문 OK | 편별 기록 |
| kit_shorts_wiryeseong_build.py | 위례성 편 빌드(10/24) | Drive 1LmNnvmHKZldFNAYIWhEzkDgUl2PyVg3k | f14d200e135bc69e01d6ae1367b3ca6c | 크기 2,781B **일치**, 구문 OK | 편별 기록 |
| kit_shorts_talhae_build.py | 탈해 편 빌드 + comp.py(COMP 문자열)(10/25) | Drive 17obD5uOSmXIfmhB8gIzZQmlkCIeRP8Pp | 8426f016331be03ff904eb52a871f014 | 크기 3,620B **일치**, 구문 OK | 현행(comp.py 원본) |
| sandbox_setup.snippet.sh | G-1 sandbox 준비 명령 | history-shorts:345-357 | 613bca43b2b5bc95961e6e5f8a8665bd | — | 참고 |
| scenes_example.snippet.json | G-2 scenes.json 예 | history-shorts:368-380 | 1a3a49b26280b2b13caf33480aa05f59 | — | 참고 |

### longform/
| 파일 | 버전 | 출처 | md5 | 검증 | 상태 |
|---|---|---|---|---|---|
| kit_longform_render_long_v1.4.py | render_long.py v1.4 (10/27 복구판, 45,931B) | Drive 146kWC3B3ct7DTS7Dx4tEAZUoXuDAPvpg | 17cecc9c1648152c7af06187e516467c | 크기 **일치**, 구문 OK | **현행 추정**(최신 날짜) — 주3 |
| kit_longform_render_long_v14.py | render_long.py v1.4 (10/23 복구판, 45,532B) | Drive 1ZIBaurZZtiiV_vOZ5XvYYwFtlL0dGZ9q | 565f69ecd1db43b892d40c8cced77c05 | 크기 **일치**, 구문 OK | 구판 — 주3 |
| kit_longform_rider_v1.1.py | 도트 기마병 v1.1 (11/02) | Drive 18Xe_gkgpb0aLoubi154D86lpuCpQsraC | 1d846922f97c0793cd1ea1e10a1ee1f9 | 크기 3,691B **일치**, 구문 OK | 현행 |
| kit_longform_sneak_v1.1.py | 도트 잠입 병사 v1.1 (11/02) | Drive 1Yuz0D5_9_WEm432iBB3Y6v29Ur2yb5Wa | 8bfbd21c3d6cb02d9b0547c4bb1c2aaa | 크기 3,186B **일치**, 구문 OK | 현행 |
| kit_longform_pxlib.py | 도트 공통 함수 (10/27) | Drive 1ZpOP0GW41JfCU7hVZU1UHen2hCchun1- | 0397b921d662d7d01224991e027202b5 | 크기 948B **일치**, 구문 OK | rider·sneak v1.1에 내장됨 |

### map/
| 파일 | 버전 | 출처 | md5 | 검증 | 상태 |
|---|---|---|---|---|---|
| ctl.py | 쇼츠 지도 밑그림 v7.1 | history-shorts:1062-1111 | b191add76f97b53fa3c6000e10d08a32 | 구문 OK | 지도 v3 계열(쇼츠 AI 재채색용) |
| qa.py | 해안선 검수 | history-shorts:1113-1156 | f6aa2f8a9932e429af58611c7e7ae6c0 | 구문 OK | 〃 |
| anim_shorts_map.py | 쇼츠 anim.py (표지·경로 좌표 계산) | history-shorts:1158-1193 | 62e869f0324f0c5078f7d6fe4c1f8940 | 구문 OK | 〃 — **전투 쇼츠 anim.py(~/salsu)와 다른 파일** |
| han_mask.py | 한강 하천 마스크 v7.1 | history-shorts:1197-1241 | bb62860d6df5d10de0bb5f85e06c52cd | 구문 OK | 〃 |
| fix_river.py | AI 재채색 하천 보정 v7.1 | history-shorts:1245-1293 | 4e90125d02383313b7a0d5b83346ba48 | 구문 OK | 〃 |
| map_v7.py | 코드 채색 지도 map.py v7 (대체용) | history-shorts:1298-1491 | c5503c157cbc188e4751b8881ae4b3ec | 구문 OK | 대체용 |
| spec_example.snippet.json | L-3 spec 예 | history-shorts:1005-1012 | 3dc7d6fa6eae7dd76525ac3651315890 | — | 참고 |
| mapvid_fullscreen.snippet.py | mapvid 전체 화면 트릭 조각 | history-map-v4:88-97 | 03031f25fba24ddd1433ef0f2e93dc3c | 구문 OK | 조각(본체 mapvid.py는 유실/미확인) |

### common/
| 파일 | 버전 | 출처 | md5 | 검증 | 상태 |
|---|---|---|---|---|---|
| font_black_instance.snippet.py | 가변 서체 Black 인스턴스 만들기 | history-shorts:1517-1524 | 7e974fb0924fd144efe28a9458836d26 | 구문 OK | 참고 |

### battle/
- 비어 있음. 전투 쇼츠 엔진 코드는 스킬 본문에도 Drive에도 없음(아래 3절).

주1. Drive판 render.py는 크기(29,510B)만 대조하고 내용은 받지 않았다. 스킬 G-4 본문 합본이 스킬 기록 md5(197958…)와 일치하고, 스킬이 Drive판을 같은 md5로 기록하고 있어 동일본으로 판단(추정 — Drive판 md5 직접 계산은 안 함).
주2. build_short v8.0(스킬 본문) ↔ v8.1(Drive) 차이: 55줄. v8.1에 `_txt`·`seal_img`·`badge_png`·`wm_png` 추가(史 연도 배지·워터마크·표준 화면), wrap 패치 반영. 스킬 M-7 본문은 여전히 v8.0 → **스킬 본문과 실사용 버전이 다르다**.
주3. render_long v1.4가 Drive에 두 벌(10/23 `v14`, 10/27 `v1.4`) 있다. 차이 123줄: 10/27판에 `voice_gate` 추가, `_rmsdb`→`_win_db`, `seal_metrics`→`_seal_metrics` 등. 10/27판을 현행으로 추정. 같은 폴더에 rider·sneak 구판 2벌씩(10/23 4,521B·4,354B / 10/27 2,930B·2,425B)이 더 있으나 v1.1(11/02)로 대체되어 이전하지 않았다(Drive에 남아 있음).

## 2. 스킬 기록과 실제 상태가 다른 곳
- history-production-standards 4절 표는 "롱폼 렌더러 v1.3·p3lib·p3build·도트 코드(sneak·rider) **유실**"이라고 적지만, Drive 같은 폴더에 `render_long v1.4`(v1.3 기능 복구 포함)·`rider/sneak v1.1`·`pxlib`가 있다. 표가 10/23 이후 갱신되지 않음.
- 같은 표에 Drive 롱폼 파일 6개(render_long v14·v1.4, rider×3, sneak×3, pxlib)의 id가 없다.

## 3. 유실 / 미확인 (스킬에 언급되나 이번에 확보 못 함)
접근 시도: Drive 공유 폴더(1sfx-ttR2vpY2DOcqKI_vPtqHi3qQm8ag)의 .py 전체 목록 조회, 스킬 본문 코드 블록 전체 추출. CloudFront 백업 zip은 이 환경 프록시가 차단(CONNECT 403)해 내용 확인 불가.

| 자산 | 스킬 기록 위치 | 기록상 백업 | 판정 |
|---|---|---|---|
| 전투 쇼츠 3편 엔진 anim.py, edit3.py, thumb.py (~/salsu) | history-battle-shorts:184 | 3편 키트 final zip(CDN 18c492b8…) | **미확인**(CDN 접근 불가) |
| 전투 쇼츠 4편 엔진 anim4.py, scenes.py, lay2.py, unit.py, pv.py, runseg.sh, muxN.sh, pauses.py, thumb.py (~/jupil) | history-battle-shorts:185-186, 195 | **미백업**(스킬이 직접 명시) | **유실 위험 높음** |
| 전투 쇼츠 4편 시안 mkb4.py, mkb5.py, topo.py | history-battle-shorts:186 | 없음 | 유실/미확인 |
| chk.py (ev 키워드 검사) | history-battle-shorts:142, 217 | 없음 | 유실/미확인 |
| bmap3.py, bmap16, terrain.py, rivers_osm.py, m1v4.py | history-battle-shorts:183, history-map-v4:28-48 | 지도 키트 v2 zip(CDN 1f011f9e…) | 미확인(CDN) |
| terrain3.py, mkbase.py, mkstyl.py, mkstyl_run.py (v4-S) | history-map-v4:36-39 | 쇼츠 전투 키트 v8 zip(CDN f17675c8…) | 미확인(CDN) |
| mapvid.py, sigs.py, thumb.py (오노성 편) | history-map-v4:6, 77 | 오노성 편 키트 zip(CDN 97ecf09f…) | 미확인(CDN) |
| 롱폼 2부 키트: render_long v1.2, tiles.py, style.py, bake3.py, sA.py, sO.py, sig2.py, cold.py, p2lib.py, p2build.py | history-longform:26, 186, 297 | 롱폼 키트 zip v1.2(CDN bdedbf88…) | 미확인(CDN) |
| p3lib.py, p3build.py (롱폼 3부) | history-longform:25, 297 / production-standards 표 | 없음 | **유실**(스킬 기록) |
| 백제 1편 렌더 t0d.py, mix0d.py(mixer), run36.sh, fin36.sh, run38.sh, r39a/b/c.sh, ~/tools/postfix.py·liven.py·assemble.py·qa.py | history-longform-craft:23, 71 | 없음(sandbox ~/t25 등) | **미백업 추정** |
| achk.py (롱폼 내레이션 자동 점검) | history-longform:352 | 없음 | 유실/미확인 |
| mont.py (온조 비트 예고편) | history-production-standards:93 | 없음 | **유실**(스킬 기록) |
| diag.py, city_grow.py (건축 쇼츠) | history-architecture-shorts:28-33, 116-121 | — | 미구현(스킬 기록) |
| 폰트 5종(B·X·SM·NSK·SEAL) | history-shorts G-1 | GitHub 주소 | 바이너리라 이번 범위 밖 |

## 4. 실행 검사
- 구문 검사: .py 24개 중 23개 통과. 실패 1개는 wrap_patch 조각(함수 일부라 단독 구문이 아님 — 정상).
- render.py 실제 렌더: **생략.** 이 환경에 한글 폰트 0종(fc-list), scenes.json·이미지·내레이션 입력 없음. PIL 12.3·numpy 2.5·ffmpeg는 있음. 2일차 재렌더 동일성 확인 때 폰트(G-1 GitHub)와 기존 편 입력이 필요.

---

## 11/04 sandbox 키트 백업 (유실 위험 해소)

- 대상: Higgsfield sandbox `~/jupil`(주필산 4편) · `~/tools`(온조 자동 검수 도구) · `~/t25`(백제 1편 렌더) · `~/salsu`(전투 3편) · `~/r`(롱폼 렌더러) · `~/spr`(도트 rider·sneak)
- 범위: .py · .sh 전부 + 200KB 미만 .json (영상·음성·이미지 제외)
- 파일: `kit_backup_1104.tar.gz` — 279개, 504,959바이트, md5 `af1f1b6a27c80861f908bab3c89d508c`
- 위치: Higgsfield 일반 파일 media_id `a5ad0721-6b3e-4a22-8358-54570d9b1d03`
  - `https://d2ol7oe51mr4n9.cloudfront.net/user_3Juf1bLtazzBl3p1xDJV2TokuBm/a5ad0721-6b3e-4a22-8358-54570d9b1d03.gz` (업로드 HTTP 200, confirm 완료)
- git 반입: **아직 안 됨**. 이 Claude Code 환경의 네트워크 정책이 `d2ol7oe51mr4n9.cloudfront.net`을 막음(connect_rejected). 허용 도메인에 추가하면 내려받아 `kit/`에 풀고 이 표를 갱신한다.

| 폴더 | 파일 수 | 주요 파일 |
|---|---|---|
| jupil | 46 | anim4.py(+v1·v2·v4), scenes.py, lay2.py, layout.py, unit.py, icons.py, pv.py, thumb.py, topo.py, chk.py, mux.sh~mux10.sh, runseg.sh, b/(split4·pauses·tight·sw) |
| tools | 7 | qa.py, liven.py, assemble.py, postfix.py, vio.py, segdb.py, patch14.py |
| t25 | 194 | t0d.py, t1c.py, tboard.py, mix0d.py, mixer.py, mixall.py, normvo*.py, kanji2.py, yearfmt.py, run*.sh, up*.sh, full38~41.sh, r39a~c.sh, fin36.sh, tl*.json, vo*/asr |
| salsu | 23 | anim.py(+v2~v4), salsu.py, v3.py, b/·a/ 내레이션 분할 |
| r | 6 | render_long.py, render_long_v12.py, oper.json, strat.json |
| spr | 3 | pxlib.py, rider.py, sneak.py |

- 관찰: 같은 스크립트가 번호로만 갈라져 있다(normvo 1~12, run2~38, up26~37, anim4_v1~v4). 어느 것이 현행인지 파일만으로는 알 수 없다 → git으로 옮긴 뒤 현행만 남기고 나머지는 이력으로.
