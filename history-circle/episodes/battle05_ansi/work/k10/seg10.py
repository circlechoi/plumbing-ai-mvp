import sys,os,subprocess
exec(open(os.path.expanduser('~/ansi/k10/scenes10.py')).read())
import numpy as np
a,b=int(sys.argv[1]),int(sys.argv[2]); fps=15
out=os.path.expanduser(f'~/ansi/k10/seg/s_{a:05d}.mp4')
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r',str(fps),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
for f in range(a,b): p.stdin.write(np.asarray(frame(f/fps).convert('RGB')).tobytes())
p.stdin.close(); p.wait(); open(out+'.done','w').write('ok')
