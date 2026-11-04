from fontTools.ttLib import TTFont; from fontTools.varLib import instancer
f = instancer.instantiateVariableFont(TTFont('fonts/NSK.ttf'), {'wght': 900})
for r in f['name'].names:
    if r.nameID in (1, 4, 16): r.string = 'NSK Black'
    if r.nameID in (2, 17): r.string = 'Regular'
f.save('fd/NSKBlack.ttf')   # fd/ = ass 필터 fontsdir: NSKBlack.ttf, SM.ttf, B.ttf, X.ttf
