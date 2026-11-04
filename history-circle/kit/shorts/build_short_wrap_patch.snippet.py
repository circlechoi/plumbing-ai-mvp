    dep=0; sp=[]
    for i,c in enumerate(t):
        if c=='{': dep+=1
        elif c=='}': dep-=1
        elif c==' ' and dep==0: sp.append(i)
