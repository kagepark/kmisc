#Kage Park
import string

def Random(length=8,strs=None,mode='*',letter='*'):
    if mode in [int,'int','num','number']:
        if isinstance(strs,(list,tuple)) and len(strs) == 2:
            try:
                s=int(strs[0])
                n=int(strs[1])
                return random.randint(s,int(n))
            except:
                pass
        s=0
        n=''
        for i in range(0,length):
            n=n+'9'
        return random.randint(s,int(n))
    new=''
#    if mode in [int,'int','num']:
#        for i in range(0,length):
#            new='{0}{1}'.format(new,random.randint(0,9))
#        return int(num)
    if not isinstance(strs,str) or not str:
        strs=''
        if 'alpha' in mode or mode in ['all','*']:
            if letter == 'upper':
                strs=string.ascii_uppercase
            elif letter == 'lower':
                strs=string.ascii_lowercase
            elif letter in ['*','all']:
                strs=string.ascii_letters
        if 'num' in mode or mode in ['all','*']:
            strs=strs+string.digits
        if 'char' in mode or 'sym' in mode or mode in ['all','*']:
            strs=strs+string.punctuation
#        if mode in ['all','*','alphanumchar']:
#            strs='0aA-1b+2Bc=C3d_D,4.eE?5"fF6g7G!h8H@i9#Ij$JkK%lLmMn^N&oO*p(Pq)Q/r\Rs:St;TuUv{V<wW}x[Xy>Y]z|Z'
#        elif mode in ['alphachar']:
#            strs='aA-b+Bc=Cd_D,.eE?"fFgG!hH@i#Ij$JkK%lLmMn^N&oO*p(Pq)Q/r\Rs:St;TuUv{V<wW}x[Xy>Y]z|Z'
#        elif mode in ['alphanum']:
#            strs='aA1b2BcC3dD4eE5fF6g7Gh8Hi9IjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'
#        elif mode in ['char']:
#            strs='-+=_,.?"!@#$%^&*()/\:;{<}x[>]|'
#        else:
#            strs='aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'
    strn=len(strs)-1
    for i in range(0,length):
        new='{0}{1}'.format(new,strs[random.randint(0,strn)])
    return new

