"""롱폼(16:9) -> 세로 숏츠 재편집기 (history-shorts M, v8.1 2026-10-23: 제목 92→80% · 史 연도 배지 · 표준 워터마크 · wrap 패치). 사용: SRC=롱폼.mp4 OUT=out FD=fd python3 build_short.py cfgs.py [이름...]
모드: F 채우기(세로 크롭, cx->cx2 패닝) / B 박스(흐린 배경 위 가로 박스) / S 2단(화면 분할 컷) / K 검정"""
import json,subprocess,sys,os,math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
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
    dep=0; sp=[]
    for i,c in enumerate(t):
        if c=='{': dep+=1
        elif c=='}': dep-=1
        elif c==' ' and dep==0: sp.append(i)
    if not sp: return t
    k=min(sp,key=lambda i:abs(i-len(t)/2)); return t[:k]+'\\N'+t[k+1:]
FB_=os.environ.get('FONT_B',FD+'/B.ttf'); FX_=os.environ.get('FONT_X',FD+'/X.ttf'); FSEAL=os.environ.get('FONT_SEAL',FD+'/SEAL.ttf')
GOLDRGB=(242,201,76)
def _txt(s,size,fill,fp,stroke):
    f=ImageFont.truetype(fp,size); d=ImageDraw.Draw(Image.new('RGBA',(1,1))); bb=d.textbbox((0,0),s,font=f,stroke_width=stroke)
    im=Image.new('RGBA',(bb[2]-bb[0]+stroke*2+8,bb[3]-bb[1]+stroke*2+8)); ImageDraw.Draw(im).text((stroke+4-bb[0],stroke+4-bb[1]),s,font=f,fill=fill,stroke_width=stroke,stroke_fill=(0,0,0))
    return im
def seal_img(sz=46):
    im=Image.new('RGBA',(sz,sz)); d=ImageDraw.Draw(im); red,pap=(170,38,32),(245,232,210)
    d.rounded_rectangle([2,2,sz-3,sz-3],radius=sz//9,fill=red); d.rounded_rectangle([sz*.1,sz*.1,sz*.9,sz*.9],radius=sz//12,outline=pap,width=max(2,sz//22))
    if os.path.exists(FSEAL):
        f=ImageFont.truetype(FSEAL,int(sz*.62))
        try: f.set_variation_by_name('Black')
        except Exception: pass
        d.text((sz/2,sz/2+1),'史',font=f,fill=pap,anchor='mm')
    a=np.asarray(im).copy(); n=np.random.default_rng(1).random(a.shape[:2])<.06; a[n&(a[...,3]>0),3]=90
    return Image.fromarray(a)
def badge_png(txt,path):  # 좌상단 史 연도 배지 — x 54(왼쪽 끝) · 중심 y 245
    txt=txt.replace('◀','').replace('▶','').strip(); t=_txt(txt,38,GOLDRGB,FB_,4); sz=46
    im=Image.new('RGBA',(sz+12+t.width,max(sz,t.height)+8)); im.alpha_composite(seal_img(sz),(0,(im.height-sz)//2)); im.alpha_composite(t,(sz+12,(im.height-t.height)//2))
    sh=Image.new('RGBA',(im.width+10,im.height+10)); sa=Image.new('L',sh.size,0); sa.paste(im.getchannel('A'),(4,6))
    sh.putalpha(sa.filter(ImageFilter.GaussianBlur(6)).point(lambda v:int(v*.6))); sh.alpha_composite(im,(0,0)); sh.save(path); return sh.size
def wm_png(path):  # 우상단 워터마크 — 나눔명조 ExtraBold 30, 70%, 오른쪽 끝 x 960 · 중심 y 245
    t=_txt('역사서클',30,(255,255,255),FX_,2); t.putalpha(t.getchannel('A').point(lambda v:int(v*.7))); t.save(path); return t.size
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
    L.append("Style: Title,NSK Black,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,8,4,5,20,20,20,1")
    L.append("Style: Cap,Song Myung,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,5,3,5,40,40,20,1")
    L.append("Style: WM,NanumMyeongjo,32,&H40FFFFFF,&H00FFFFFF,&H60000000,&H96000000,0,0,0,0,100,100,0,0,1,2,1,9,20,20,20,1")
    L.append("Style: Src,NanumMyeongjo,27,&H30FFFFFF,&H00FFFFFF,&H50000000,&H96000000,0,0,0,0,100,100,0,0,1,2,1,5,20,20,20,1")
    L.append("Style: End,NSK Black,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,6,4,5,20,20,20,1")
    L.append("Style: Card,Song Myung,92,&H00F0F0F0,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,6,0,1,0,0,5,20,20,20,1")
    L.append("Style: Tag,NanumMyeongjo,40,&H004CC9F2,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,4,2,7,20,20,20,1\n")
    L.append("[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")
    ev=lambda s,e,st,tx,layer=1: L.append(f"Dialogue: {layer},{ts(s)},{ts(e)},{st},,0,0,0,,{tx}")
    tin=cfg.get('title_in',0.15); endd=cfg.get('end_dur',3.0)
    ty=cfg.get('title_y',392); ty0=cfg.get('title_y0',425)
    shr=cfg.get('title_shrink', min(parts[0]['e']-parts[0]['s'], 4.0))   # 첫 조각(첫 장면) 끝에 줄어듦 — 출력 기준 초
    t1=max(0,int((shr-tin-0.5)*1000)); t2=t1+500
    ev(tin,T-endd,'Title',f"{{\\move(540,{ty0},540,{ty},{t1},{t2})\\t({t1},{t2},\\fscx80\\fscy80)\\fad(150,150)}}"+gold(cfg['title']))
    ev(T-endd,T,'End',f"{{\\pos(540,{ty})\\fad(250,0)}}{{\\c{GOLD}}}▶ 전체 이야기는 롱폼에서{{\\c{WHITE}}}\\N{{\\fs56}}"+cfg['end'])
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
    # v8.1: 史 연도 배지(필수) + 표준 워터마크 — render.py와 같은 PIL 그림을 overlay
    yr=cfg.get('year')
    if not yr: raise SystemExit(f'[{name}] year 필수(v8.1): cfg에 year="기록상 서기 20년" 또는 [(출력 시작, 끝, 글)]')
    yrs=[(0,T,yr)] if isinstance(yr,str) else yr
    ov=[]; k0=len(parts)+1+len(ranges)
    for j,(a,b,tx) in enumerate(yrs):
        pth=f"{OUT}/{name}_yr{j}.png"; w,h=badge_png(tx,pth); inputs+=['-loop','1','-framerate','24','-t',f"{T:.3f}",'-i',pth]; ov.append((k0+j,54,245-h//2,a,b))
    wp=f"{OUT}/wm.png"; w,h=wm_png(wp); inputs+=['-loop','1','-framerate','24','-t',f"{T:.3f}",'-i',wp]; ov.append((k0+len(yrs),960-w,245-h//2,0,T))
    fc.append(f"[vc][0:v]overlay=0:0,ass={ass}:fontsdir={FD}[va]"); cur='va'
    for n,(idx,x,y,a,b) in enumerate(ov):
        fc.append(f"[{cur}][{idx}:v]overlay={x}:{y}:enable='between(t,{a:.3f},{b:.3f})'[o{n}]"); cur=f"o{n}"
    fc.append(f"[{cur}]fade=t=in:d=0.2,fade=t=out:st={T-0.35:.3f}:d=0.35[vo]")
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
