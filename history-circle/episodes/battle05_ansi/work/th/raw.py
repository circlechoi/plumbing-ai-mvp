import sys,os
exec(open(os.path.expanduser('~/ansi/k10/scenes10.py')).read())
def raw(s,u):
    HUD.clear(); D=DUR[s]; cv=SF[s](u,D)
    for f in HUD: f(cv)
    HUD.clear(); return cv.im.convert('RGB')
if __name__=='__main__':
    from PIL import Image
    print({k:round(v,1) for k,v in DUR.items()}, KK)
    shots=[(a,float(b)) for a,b in (x.split(':') for x in sys.argv[1:])]
    sh=Image.new('RGB',(len(shots)*272,480),(20,20,20))
    for i,(s,u) in enumerate(shots):
        im=raw(s,u); im.save(f'/home/user/ansi/th/raw_{s}_{u}.png'); sh.paste(im.resize((270,480)),(i*272,0))
    sh.save('/home/user/ansi/th/rawsheet.jpg',quality=85)
