"""롱폼에 구워진 자막 띠를 OCR해 (시작, 끝, 글) 목록을 만든다 (2026-10-22 대무신왕 3부 재편집에서 사용).
준비: band/%05d.png = ffmpeg -i src.mp4 -vf "fps=5,crop=1920:64:0:976,format=gray" band/%05d.png
      tess/kor.traineddata = https://raw.githubusercontent.com/tesseract-ocr/tessdata_best/main/kor.traineddata
출력: ocr.json [[시작초, 끝초, 글], ...] — 이후 FIX 표로 오인식 교정(kit_shorts_p3_cfgs.py 참고)"""
import numpy as np, glob, json, subprocess
from PIL import Image
fs=sorted(glob.glob('band/*.png'))
B=[np.asarray(Image.open(f),np.float32)>140 for f in fs]
groups=[]; cur=None
for i,b in enumerate(B):
    on=b.sum()>200
    if not on:
        if cur: groups.append(cur); cur=None
        continue
    if cur and (np.logical_xor(b,B[cur[1]]).sum()/max(1,b.sum()))<0.25: cur[1]=i
    else:
        if cur: groups.append(cur)
        cur=[i,i]
if cur: groups.append(cur)
out=[]
for a,b in groups:
    m=(a+b)//2; im=Image.open(fs[m]); im=im.resize((im.width*2,im.height*2)); im=Image.eval(im,lambda v:255-v); im.save('/tmp/ocr.png')
    t=subprocess.run(['tesseract','/tmp/ocr.png','-','-l','kor','--psm','7','--tessdata-dir','tess'],capture_output=True,text=True).stdout.strip()
    out.append((round(a/5,2),round((b+1)/5,2),t))
json.dump(out,open('ocr.json','w'),ensure_ascii=False,indent=0)
