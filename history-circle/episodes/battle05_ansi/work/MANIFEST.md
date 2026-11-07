# 5편 안시성 작업 코드 (sandbox `~/ansi/` → 11/07 동기화)

- 최종본: `~/ansi/k10/ansi_anim_v13.mp4` (17.8MB, sandbox) — 파이프라인 = `k10/scenes10.py` → `k/scenes9.py`(+ `an/an10.py`) + `k10/maps10.py` + `k10/siege10.py`, 렌더 `k10/run10.sh` → `seg10.py`, 소리 `k10/mix16.py`, 합치기 `k10/mux16.sh`
- 대본 최종: `an/script15.txt` (장면\t문구 | 문구 …)
- 실행 위치: 스크립트가 `~/ansi/...` 절대경로로 서로를 읽으므로 sandbox에서는 `~/ansi/`에 둔 채 실행한다. 이 폴더는 원본 보관용.

## git에 있는 파일 (md5 = sandbox 원본과 대조 완료)
| 파일 | md5 |
|---|---|
| an/script15.txt | 5b15ef2f75bb28927a6aa67945899a77 |
| k10/scenes10.py | d7fa53618b3a05306dd9b8fc41da87d3 |
| k10/run10.sh | 33667843c453fe28dde160f83ec8758e |
| k10/mux16.sh | aab2a3ff02b5cdba485cf198f2bea4d5 |
| k10/seg10.py | 8995814270fa833564bee688b6310241 |
| th/raw.py | 20f641f79b9b8b699f544720f0fc7882 |

## 묶음에만 있는 파일 (git 미반영 — 작업 공간에서 Higgsfield 주소 접속 허용 후 옮긴다)
- 묶음: https://d2ol7oe51mr4n9.cloudfront.net/user_3Juf1bLtazzBl3p1xDJV2TokuBm/4a37b58a-e063-4347-910b-3157c13d0126.gz (tar.gz 15MB, md5 7f2e83722e41f31b0f1a5453e567e530) — `history-circle/` 전체 + `ansi/` 텍스트 파일 112개
- 받기(sandbox): `curl -sSfL -o hc_sync.tar.gz <위 주소> && md5sum hc_sync.tar.gz && tar -xzf hc_sync.tar.gz`

| 파일 | 크기 | md5 |
|---|---|---|
| ansi/k/scenes9.py | 37106 | cc1aff37058f832a692bea9739a6239d |
| ansi/k10/maps10.py | 22021 | d10615b88e5407045e726b48dae2e700 |
| ansi/k10/siege10.py | 24752 | a59b4bdd7a78bf9a111ed442d247f37f |
| ansi/k10/mix16.py | 4310 | b9008695016ea2bb008d3b7992525230 |
| ansi/an/an10.py | 9964 | 71a36d9c2b6896f738b7431bc5a3c1e7 |
| ansi/b10/sw.py | 408 | e020efa7c9067650f828f8e29f96967d |
| ansi/b10/sw.json | 6054 | 891c7c0e5409bc6178d5496f35662631 |
| ansi/d/split.py | 2008 | 0a9e3777f011d466474c14e93098a633 |
| ansi/d/cuts.json | 267 | 2139e60bc405a59d5af9a4508ac30942 |
| ansi/hero/hero12b.py | 7802 | 212cc212029fdcd8d0266f9f830d05a7 |
| ansi/hero/relief.py | 981 | 2a7adfc58d77ffae62443f86d53fe772 |
| ansi/hero/base2.py | 1773 | cfb604ef10d72bf2eef73d87d1c75cec |
| history-circle/components/icons/tinf.png | — | e4be8d0b28cdb055ae6ee01c0377713e |
| history-circle/components/icons/tinf_w.png | — | 030c95c05ff2eccd62fb8c8a7d857305 |
| history-circle/episodes/battle06_sasu/src/ (사료 원문 12개, 347KB) | — | zh.wikisource에서 다시 받을 수 있음 |

## 남은 정리
- `an/an10.py`는 아직 `~/salsu/bmap3.py`를 직접 불러온다(키트 밖 의존). 6편부터는 style/·animatic/만 쓴다.
- `components/spec.json`이 `icons/tinf_w.png`를 가리키지만 PNG는 위 묶음에만 있다 — sandbox 키트에는 들어 있음.
- 백업 잔재(`curated_bak1106*.yaml`, `*_v15bak*`)는 git에 넣지 않았다. 이력은 git이 대신한다.
