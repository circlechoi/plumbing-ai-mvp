# 강북 위례성 숏츠(10/24) — render.py v7.6용 scenes.json 생성
# 내레이션 압축: kit_shorts_biryu_build.py 머리말의 comp.py 방식(atempo 1.10, range(1,9))
# 그림 job: i1 9fbf2f5f(첫 장면·2번 라벨 재사용) i2 15a4bc4a i3 b669007c i4 43e6e730 i5 e3cc58e2 i6 035a7f74 i7 795524ad / Kling ca065c27 (setpts 1.72)
# 온조 참조: 얼굴 61df4347, 시트 ff6019d1 / BGM The King's Departure 1c5OHM5d5lD2fguRnOKBINYX6NNzCu9zP
import json, numpy as np, subprocess
GAP=0.35; SR=48000; N=8
offs=[];t=0;parts=[]
for i in range(1,N+1):
    offs.append(t)
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'a/c{i}.wav','-f','s16le','-'],capture_output=True).stdout,np.int16)
    parts.append(x); t+=len(x)/SR
    if i<N: parts.append(np.zeros(int((0.6 if i==6 else GAP)*SR),np.int16)); t+=(0.6 if i==6 else GAP)
subprocess.run(['ffmpeg','-v','error','-y','-f','s16le','-ar','48000','-ac','1','-i','-','nar.wav'],input=np.concatenate(parts).tobytes())
DL=0.4; st=[0]+[round(DL+o-0.15,2) for o in offs[1:]]; T=round(DL+t+1.4,2)
D=[40,32,26]
m2=dict(focus=[.5,.45],labels=[dict(xy=[850,1180],text='강북 · 위례성',size=124,color=D),dict(xy=[850,1320],text='위치 미확인 · 여러 설',size=68,color=[90,70,55]),
  dict(xy=[600,1680],text='한강',size=120,color=[28,74,140]),dict(xy=[700,2150],text='강남',size=110,color=D)],regions=[],routes=[],markers=[])
json.dump(m2,open('m2.json','w'),ensure_ascii=False)
SC=[dict(video='k1s.mp4',cap=['백제의 첫 수도','원래 {강북}이었다고?']),
 dict(image='i1.png',map='m2.json',move='still',cap=['처음 세운 {위례성}','한강 북쪽'],year='기록상 BC 18'),
 dict(image='i2.png',move='in',cap=['[기록] 東有樂浪 北有靺鞨','편할 날이 {드물다}'],year='기록상 BC 6'),
 dict(image='i3.png',move='pan_l',cap=['성에 든 {호랑이 다섯}','그리고 어머니의 죽음'],year='기록상 BC 6',trans='fade'),
 dict(image='i4.png',move='in',focus=[.5,.5],cap=['[기록] 勢不自安 必將遷國','더는 {버틸 수 없다}']),
 dict(image='i5.png',move='pan_r',cap=['쫓기듯 강을 건너다','그리고 {3년 뒤}'],year='기록상 BC 5'),
 dict(image='i6.png',move='punch',trans='flash',cap=['[기록] 樂浪來侵 焚慰禮城','{위례성}이 불타다'],year='기록상 BC 2'),
 dict(image='i7.png',move='out',cap=['강남은 {풍납·몽촌}','강북은 아직 못 찾았다'])]
for s,a in zip(SC,st): s['start']=a
S=dict(total=T,title='원래 백제의 수도는\n{강북}이었다고?',watermark='역사서클',source='『삼국사기』 백제본기 · 이미지는 AI 재현',
  narration='nar.wav',delay=DL,amb='wind',bgm='bgm.wav',bgm_db=-19,out='final.mp4',scenes=SC)
json.dump(S,open('scenes.json','w'),ensure_ascii=False,indent=1)
print(st,T)
