# 기준 화면 세트 v1 (스타일 키트 · 11/05 확정)

PNG 원본은 용량 때문에 git에 넣지 않고 Higgsfield 파일 저장소에 둡니다. 아래 한 줄로 이 폴더에 받습니다(sandbox).

```
cd ~/history-circle/golden/style_ref && curl -sSfL -o sr.zip https://d2ol7oe51mr4n9.cloudfront.net/user_3Juf1bLtazzBl3p1xDJV2TokuBm/0d027ddf-46e7-468b-aa88-bbc602be4ad1.zip && unzip -o -q sr.zip && rm sr.zip && md5sum -c MD5SUMS
```

| 파일 | 역할 | 출처 |
|---|---|---|
| f1_ep4_40s.png | F1 화면 틀 기준 | 4편 주필산 jupil_anim_v10.mp4 40초 |
| ep1_21s.png | R1 지도 컷(부품) | 1편 백제 멸망전 최종본 21초 |
| ep1_31s.png | R2 카드 | 1편 31초 |
| ep1_46s.png | R3 말풍선 | 1편 46초 |
| ep1_61s.png | R4 도식 컷 | 1편 61초 |
| (R5) | 'ㅗ' 블록 | `components/preview/a_units.png` (git에 있음) |

- zip md5: 0ec4fb30e4d080d17ad95084c350f959
- `lint/style_check.py frame`의 기준 비교(`--ref`)와 `--sheet`가 이 폴더를 읽습니다. 파일이 없으면 기준 비교만 건너뜁니다.
