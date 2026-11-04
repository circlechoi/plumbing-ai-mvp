# 비류 숏츠(10/23) — 내레이션 압축 + scenes.json/지도 json 생성. render.py v7.6과 함께 사용.
# 1) comp.py 단계: vo/n{i}.mp3 -> atempo 1.06, 0.55s 넘는 무음은 앞0.22+뒤0.18만 남김 -> a/c{i}.wav, a/dur.json
# 2) 아래 build.py: 0.35s 간격으로 이어 nar.wav, 장면 시작 = delay0.4 + 문장시작 - 0.15
# 첫 장면 Kling 5초 컷은 setpts=1.65*PTS,minterpolate=fps=30:mi_mode=blend 로 8.2초로 늘림(render.py는 영상 끝에서 마지막 프레임 정지)
# BGM: 战后清晨(비극·여운) 1oXiS0tkN4ah1l6oW827UranZwjRtK34K, bgm_db -19
import json, numpy as np, subprocess
D=json.load(open('a/dur.json')); GAP=0.35; SR=48000
offs=[];t=0;parts=[]
for i in range(1,10):
    offs.append(t)
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'a/c{i}.wav','-f','s16le','-'],capture_output=True).stdout,np.int16)
    parts.append(x); t+=len(x)/SR
    if i<9: parts.append(np.zeros(int(GAP*SR),np.int16)); t+=GAP
subprocess.run(['ffmpeg','-v','error','-y','-f','s16le','-ar','48000','-ac','1','-i','-','nar.wav'],input=np.concatenate(parts).tobytes())
DL=0.4; st=[0]+[round(DL+o-0.15,2) for o in offs[1:]]; T=round(DL+t+1.4,2)
def ll(lon,lat):  # korea_full 지도 투영
    ppd=3840/15.2;k=np.cos(np.radians(38.8));return [round(1080+(lon-126.4)*k*ppd),round(1920-(lat-38.8)*ppd)]
m2=dict(focus=[.53,.47],zoom=1.55,note='위치: 미추홀=인천(통설) · 위례성은 여러 설',labels=[],regions=[],
  routes=[dict(pts=[ll(125.42,41.15),ll(126.2,39.6),ll(127.02,37.66)],color=[170,38,32],at=.2,dur=1.6,label='')],
  markers=[dict(name='졸본',sub='',xy=ll(125.417,41.328),main=False,side='l',at=.05),
           dict(name='위례',sub='',xy=ll(127.117,37.528),main=True,side='r',at=1.7),
           dict(name='미추홀',sub='',xy=ll(126.67,37.44),main=True,side='l',at=2.3)])
json.dump(m2,open('m2.json','w'),ensure_ascii=False)
C=[40,32,26]
m3=dict(focus=[.5,.45],zoom=1.25,labels=[dict(xy=[1080,1000],text='북 · 한강',size=104,color=[28,74,140]),dict(xy=[1600,1800],text='동 · 높은 산',size=96,color=C),
  dict(xy=[1080,2900],text='남 · 기름진 들',size=96,color=[60,100,30]),dict(xy=[520,1800],text='서 · 바다',size=96,color=[28,74,140])],regions=[],routes=[],markers=[])
json.dump(m3,open('m3.json','w'),ensure_ascii=False)
Y='기록상 BC 18'
SC=[dict(video='k1s.mp4',cap=['같이 내려온 형제','한 명만 {나라}를?'],year=Y),
 dict(image='map.png',map='m2.json',cap=['따라온 {열 신하}','한곳을 권하다'],year=Y,trans='whip_l'),
 dict(image='i3.png',map='m3.json',cap=['강·산·들·바다','{하남}의 땅'],year=Y),
 dict(image='i4.png',move='pan_l',cap=['형은 듣지 않고','바닷가 {미추홀}로']),
 dict(image='i5.png',move='in',cap=['[기록] 土濕水鹹','습하고 {물이 짠} 땅'],year=Y),
 dict(image='i6.png',move='out',cap=['[해석] 바다는 길이지만','{물과 곡식}은?']),
 dict(image='i7.png',move='in',focus=[.5,.55],cap=['아우의 도읍을 보고','{부끄러워하다} 죽다'],trans='fade'),
 dict(image='i8.png',move='pan_r',cap=['백성이 위례로','십제에서 {백제}로'],year='기록상 BC 18 무렵'),
 dict(image='i9.png',move='out',cap=['여러분이라면','강인가, 바다인가?'])]
for s,a in zip(SC,st): s['start']=a
S=dict(total=T,title='형은 {바닷가}를 골랐다가\n무너졌다고?',watermark='역사서클',source='『삼국사기』 백제본기 · 이미지는 AI 재현',
  narration='nar.wav',delay=DL,amb='wind',bgm='bgm.wav',bgm_db=-19,out='final.mp4',scenes=SC)
json.dump(S,open('scenes.json','w'),ensure_ascii=False,indent=1)
print(st,T)
