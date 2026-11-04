"""롱폼(16:9) -> 세로 숏츠 재편집기 (history-shorts M). 사용: SRC=롱폼.mp4 OUT=out FD=fd python3 build_short.py cfgs.py [이름...]
모드: F 채우기(세로 크롭, cx->cx2 패닝) / B 박스(흐린 배경 위 가로 박스) / S 2단(화면 분할 컷) / K 검정"""
import json,subprocess,sys,os,math
from PIL import Image
import numpy as np
SRC=os.environ.get('SRC','src.mp4'); OUT=os.environ.get('OUT','out'); FD=os.environ.get('FD','fd')
PH=int(os.environ.get('PH',802)); PY=int(os.environ.get('PY',139)); FW=int(round(PH*9/16))  # 원본 그림 영역 높이·시작 y(레터박스·자막 띠 제외)
GOLD='&H4CC9F2&'; WHITE='&HFFFFFF&'
def F(s,e,cx,cx2=None): return dict(s=s,e=e,m='F',cx=cx,cx2=cx2)
def B(s,e,cx,w,y=None): return dict(s=s,e=e,m='B',cx=cx,w=w,y=y)
def S(s,e,top,bot): return dict(s=s,e=e,m='S',top=top,bot=bot)   # top/bot=(x0,x1,cx)
def K(s,e): return dict(s=s,e=e,m='K')
def gold(t): # {word} -> gold
    import re
    return re.sub(r'\{([^{}\\]+)\}',lambda m:'{\\c'+GOLD+'}'+m.group(1)+'{\\c'+WHITE+'}',t)
def wrap(t):
    if '\\N' in t: return t
    plain=t.replace('{','').replace('}','')
    if len(plain)<=15: return t
    sp=[i for i,c in enumerate(t) if c==' ']
    if not sp: return t
    k=min(sp,key=lambda i:abs(i-len(t)/2)); return t[:k]+'\\N'+t[k+1:]
def ts(x):
    h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h}:{m:02d}:{s:05.2f}"
def scrim(path):
    a=np.zeros((1920,1080,4),np.uint8); y=np.arange(1920)
    al=np.interp(y,[0,150,470,620],[.62,.55,.30,0])+np.interp(y,[1150,1250,1470,1640,1920],[0,.50,.50,.30,.30])
    a[...,3]=(np.clip(al,0,1)*255)[:,None].astype(np.uint8); Image.fromarray(a,'RGBA').save(path)
def build(cfg):
    name=cfg['name']; segs=cfg['segs']; ranges=cfg['ranges']
    # map source time -> output time
    offs=[];acc=0
    for (a,b) in ranges: offs.append((a,b,acc)); acc+=b-a
    T=acc
    def omap(t):
        for a,b,o in offs:
            if a-1e-6<=t<=b+1e-6: return o+(t-a)
        return None
    # split segs by ranges
    parts=[]
    for (a,b) in ranges:
        for sg in segs:
            s=max(a,sg['s']); e=min(b,sg['e'])
            if e-s>0.02:
                p=dict(sg); p['s']=s; p['e']=e; p['os']=sg['s']; p['oe']=sg['e']; parts.append(p)
    cov=sum(p['e']-p['s'] for p in parts)
    assert abs(cov-T)<0.05,(name,cov,T)
    fc=[];labels=[];inputs=[]
    for i,p in enumerate(parts):
        d=p['e']-p['s']; inputs+=['-ss',f"{p['s']:.3f}",'-t',f"{d:.3f}",'-i',SRC]; base=f"[{i+1}:v]setpts=PTS-STARTPTS,crop=1920:{PH}:0:{PY}"
        if p['m']=='F':
            c1=p['cx']; c2=p.get('cx2')
            if c2 is None: x=str(int(min(1920-FW,max(0,c1-FW/2))))
            else:
                D=p['oe']-p['os']; t0=p['s']-p['os']
                x0=min(1920-FW,max(0,c1-FW/2)); x1=min(1920-FW,max(0,c2-FW/2))
                x=f"'{x0:.1f}+({x1-x0:.1f})*(t+{t0:.3f})/{D:.3f}'"
            fc.append(f"{base},crop={FW}:{PH}:{x}:0,scale=1080:1920:flags=lanczos,setsar=1,fps=24,format=yuv420p[v{i}]")
        elif p['m']=='B':
            w=p['w']; x=int(min(1920-w,max(0,p['cx']-w/2))); h=int(round(PH*1080/w/2)*2); bx=int(min(1920-FW,max(0,p['cx']-FW/2)))
            fc.append(f"{base},split[a{i}][b{i}];[a{i}]crop={FW}:{PH}:{bx}:0,scale=270:480,boxblur=12:2,eq=brightness=-0.22:saturation=0.7,scale=1080:1920[bg{i}];[b{i}]crop={w}:{PH}:{x}:0,scale=1080:{h}:flags=lanczos[fg{i}];[bg{i}][fg{i}]overlay=0:{(p.get('y') or cfg.get('boxy',880))-h//2},setsar=1,fps=24,format=yuv420p[v{i}]")
        elif p['m']=='S':
            outs=[]
            for j,(x0,x1,cx) in enumerate((p['top'],p['bot'])):
                pw=x1-x0; w=min(pw,1036); h=min(PH,int(w/1.2933)//2*2); x=int(min(x1-w,max(x0,cx-w/2))); y=int((PH-h)*0.15)
                outs.append(f"crop={w}:{h}:{x}:{y},scale=1080:836:flags=lanczos")
            fc.append(f"{base},split[a{i}][b{i}];[a{i}]{outs[0]}[t{i}];[b{i}]{outs[1]}[u{i}];[t{i}][u{i}]vstack,drawbox=0:833:1080:6:black:fill,pad=1080:1920:0:248:black,setsar=1,fps=24,format=yuv420p[v{i}]")
        elif p['m']=='K':
            fc.append(f"{base},crop={FW}:{PH}:0:0,scale=1080:1920,drawbox=0:0:1080:1920:black:fill,setsar=1,fps=24,format=yuv420p[v{i}]")
        labels.append(f"[v{i}]")
    fc.append(''.join(labels)+f"concat=n={len(parts)}:v=1:a=0[vc]")
    al=[]
    for i,(a,b) in enumerate(ranges):
        fi=0.15 if i==0 else 0.04; fo=0.5 if i==len(ranges)-1 else 0.04
        inputs+=['-ss',f"{a:.3f}",'-t',f"{b-a:.3f}",'-i',SRC]
        fc.append(f"[{len(parts)+1+i}:a]asetpts=PTS-STARTPTS,afade=t=in:d={fi},afade=t=out:st={b-a-fo:.3f}:d={fo}[a{i}x]"); al.append(f"[a{i}x]")
    fc.append(''.join(al)+f"concat=n={len(ranges)}:v=0:a=1[ac]")
    # ASS
    L=[]
    L.append("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\nScaledBorderAndShadow: yes\n")
    L.append("[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding")
    L.append("Style: Title,NSK Black,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,7,4,5,20,20,20,1")
    L.append("Style: Cap,Song Myung,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,5,3,5,40,40,20,1")
    L.append("Style: WM,NanumMyeongjo,32,&H40FFFFFF,&H00FFFFFF,&H60000000,&H96000000,0,0,0,0,100,100,0,0,1,2,1,9,20,20,20,1")
    L.append("Style: Src,NanumMyeongjo,27,&H30FFFFFF,&H00FFFFFF,&H50000000,&H96000000,0,0,0,0,100,100,0,0,1,2,1,5,20,20,20,1")
    L.append("Style: End,NSK Black,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,6,4,5,20,20,20,1")
    L.append("Style: Card,Song Myung,92,&H00F0F0F0,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,6,0,1,0,0,5,20,20,20,1")
    L.append("Style: Tag,NanumMyeongjo,40,&H004CC9F2,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,4,2,7,20,20,20,1\n")
    L.append("[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")
    ev=lambda s,e,st,tx,layer=1: L.append(f"Dialogue: {layer},{ts(s)},{ts(e)},{st},,0,0,0,,{tx}")
    tin=cfg.get('title_in',0.15); endd=cfg.get('end_dur',3.0)
    ty=cfg.get('title_y',330)
    ev(tin,T-endd,'Title',f"{{\\pos(540,{ty})\\fad(150,150)}}"+gold(cfg['title']))
    ev(T-endd,T,'End',f"{{\\pos(540,{ty})\\fad(250,0)}}{{\\c{GOLD}}}▶ 전체 이야기는 롱폼에서{{\\c{WHITE}}}\\N{{\\fs56}}"+cfg['end'])
    ev(0,T,'WM',"{\\pos(1040,150)}역사서클",0)
    ev(0,T,'Src',"{\\pos(540,1500)}"+cfg.get('source','『삼국사기』 고구려본기 · 영상은 AI 재현'),0)
    for (a,b,tx) in cfg.get('extra',[]): ev(a,b,tx[0],tx[1])
    caps=cfg['caps']
    oc=[]
    for (a,b,tx) in caps:
        oa=omap(a+0.01); ob=omap(b-0.01)
        if oa is None or ob is None: print('WARN cap outside',name,a,b,tx); continue
        oc.append([oa,ob,tx])
    for i,c in enumerate(oc):
        if i+1<len(oc) and oc[i+1][0]-c[1]<0.45: c[1]=oc[i+1][0]-0.04
        ev(c[0],min(c[1],T),'Cap',f"{{\\pos(540,{cfg.get('cap_y',1335)})\\fad(80,60)}}"+gold(wrap(c[2])))
    os.makedirs(OUT,exist_ok=True); ass=f"{OUT}/{name}.ass"; open(ass,'w').write('\n'.join(L)+'\n')
    sc=f"{OUT}/scrim.png"
    if not os.path.exists(sc): scrim(sc)
    fc.append(f"[vc][0:v]overlay=0:0,ass={ass}:fontsdir={FD},fade=t=in:d=0.2,fade=t=out:st={T-0.35:.3f}:d=0.35[vo]")
    out=f"{OUT}/{name}.mp4"
    cmd=['ffmpeg','-v','error','-y','-loop','1','-framerate','24','-t',f"{T:.3f}",'-i',sc]+inputs+['-filter_complex',';'.join(fc),'-map','[vo]','-map','[ac]','-t',f"{T:.3f}",
         '-c:v','libx264','-preset',os.environ.get('PRESET','medium'),'-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',out]
    if os.environ.get('DRY'): print(name,'T=%.2f'%T,len(parts),'parts'); return out,T
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-3000:]); raise SystemExit(1)
    print('done',out,'T=%.2f'%T); return out,T
if __name__=='__main__':
    import importlib.util
    spec=importlib.util.spec_from_file_location('cfgs',sys.argv[1]); m=importlib.util.module_from_spec(spec); m.F=F;m.B=B;m.S=S;m.K=K; spec.loader.exec_module(m)
    want=sys.argv[2:]
    for c in m.CFGS:
        if not want or c['name'] in want: build(c)
