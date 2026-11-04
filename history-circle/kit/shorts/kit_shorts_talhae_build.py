# 석탈해 숏츠(10/25) — render.py v7.6용 + 내레이션 압축(comp)
# 10/25 sandbox 초기화 → 복구 순서: fonts(history-shorts G-1 GitHub 주소) + render.py(드라이브 1YYNzLR6RmFhGwLnQLVAoWwMwNYGVNYIo, md5 1979581615…)
# 그림 job: i1 aa0531d5(탈해 기준컷·Kling 시작) i2 de554a2a i3 19c58b07 i4 487cc026 i5 08f8e333 i6 807638e8 i7 4459ba68 i8 047887ae / Kling b55a39e3
# BGM: The Closing Trap 1Aoit34TGLpzqzwDrkhR_H2DyQn93Rmq8, bgm_db -19
# ---- comp.py (python3 comp.py 8 1.2) ----
COMP = r'''
import numpy as np, subprocess, json, re, sys
SR=48000; out={}; N=int(sys.argv[1]); TEMPO=sys.argv[2] if len(sys.argv)>2 else '1.10'
for i in range(1,N+1):
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'vo/n{i}.mp3','-af',f'atempo={TEMPO},aresample=48000','-ac','1',f'a/n{i}.wav'])
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'a/n{i}.wav','-f','s16le','-'],capture_output=True).stdout,np.int16)
    s=subprocess.run(['ffmpeg','-i',f'a/n{i}.wav','-af','silencedetect=n=-40dB:d=0.25','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(v) for v in re.findall(r'silence_start: ([\d.]+)',s)]; en=[float(v) for v in re.findall(r'silence_end: ([\d.]+)',s)]
    pieces=[];cur=0
    for a,b in zip(st,en):
        if b-a>0.4: pieces.append(x[int(cur*SR):int((a+0.16)*SR)]); cur=b-0.14
    pieces.append(x[int(cur*SR):])
    y=np.concatenate(pieces); env=np.abs(y.astype(np.float32)); idx=np.where(env>300)[0]
    y=y[max(0,idx[0]-2400):min(len(y),idx[-1]+4800)]
    subprocess.run(['ffmpeg','-v','error','-y','-f','s16le','-ar','48000','-ac','1','-i','-',f'a/c{i}.wav'],input=y.tobytes())
    out[i]=round(len(y)/SR,2)
print(out, sum(out.values())); json.dump(out,open('a/dur.json','w'))
'''
# ---- build.py ----
import json, numpy as np, subprocess
GAP=0.3; SR=48000; N=8
offs=[];t=0;parts=[]
for i in range(1,N+1):
    offs.append(t)
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'a/c{i}.wav','-f','s16le','-'],capture_output=True).stdout,np.int16)
    parts.append(x); t+=len(x)/SR
    if i<N: parts.append(np.zeros(int(GAP*SR),np.int16)); t+=GAP
subprocess.run(['ffmpeg','-v','error','-y','-f','s16le','-ar','48000','-ac','1','-i','-','nar.wav'],input=np.concatenate(parts).tobytes())
DL=0.4; st=[0]+[round(DL+o-0.15,2) for o in offs[1:]]; T=round(DL+t+1.4,2)
SC=[dict(video='k1.mp4',cap=['칼 대신 꺼낸 것','{숫돌}과 숯']),
 dict(image='i2.png',move='pan_r',cap=['궤짝에 실려 온 소년','이방인 {탈해}']),
 dict(image='i3.png',move='in',focus=[.5,.6],cap=['초승달 언덕의 {명당}','주인 호공도 {이주민}'],year='기록상 남해왕 때'),
 dict(image='i4.png',move='in',focus=[.5,.55],cap=['[해석] 힘 대신 {증거}','한밤중 {숫돌과 숯}']),
 dict(image='i5.png',move='pan_l',cap=['[기록] 我本冶匠','"땅을 {파 보시오}"']),
 dict(image='i6.png',move='in',focus=[.5,.5],cap=['땅에서 나온 {증거}','훗날 왕성 {월성}']),
 dict(image='i7.png',move='punch',trans='flash',cap=['[해석] 가짜 증거, {진짜 정체}','{쇠}를 다룬 사람']),
 dict(image='i8.png',move='out',cap=['여러분이 남해왕이라면','사기일까, 지혜일까?'],year='기록상 57년·62세 즉위')]
for s,a in zip(SC,st): s['start']=a
S=dict(total=T,title='증거를 {조작}해\n집을 빼앗고 왕이 됐다고?',watermark='역사서클',source='『삼국유사』·『삼국사기』 · 이미지는 AI 재현',
  narration='nar.wav',delay=DL,amb='wind',bgm='bgm.wav',bgm_db=-19,out='final.mp4',scenes=SC)
json.dump(S,open('scenes.json','w'),ensure_ascii=False,indent=1)
print(st,T)
