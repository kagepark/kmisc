#Kage Park

def Random(length=8,strs=None,mode='*'):
    new=''
    if mode in [int,'int','num']:
        for i in range(0,length):
            new='{0}{1}'.format(new,random.randint(0,9))
        return int(num)
    if not isinstance(strs,str):
        if mode in ['all','*','alphanumchar']:
            strs='0aA-1b+2Bc=C3d_D,4.eE?5"fF6g7G!h8H@i9#Ij$JkK%lLmMn^N&oO*p(Pq)Q/r\Rs:St;TuUv{V<wW}x[Xy>Y]z|Z'
        elif mode in ['alphanum']:
            strs='aA1b2BcC3dD4eE5fF6g7Gh8Hi9IjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'
        else:
            strs='aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'
    strn=len(strs)-1
    for i in range(0,length):
        new='{0}{1}'.format(new,strs[random.randint(0,strn)])
    return new

