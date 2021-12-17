#Kage Park
from distutils.version import LooseVersion
from kmisc.Import import *
Import('from kmisc.Split import Split')

class VERSION:
    def __init__(self):
        pass

    def Clear(self,string,sym='.'):
        if type(string) in [int,str]:
            string='{}'.format(string)
        else:
            return False
        arr=string.split(sym)
        for ii in range(len(arr)-1,0,-1):
            if arr[ii].replace('0','') == '':
                arr.pop(-1)
            else:
                break
        return sym.join(arr)

    def Check(self,a,sym,b):
        a=self.Clear(a)
        b=self.Clear(b)
        if a is False or b is False:
            return False
        if sym == '>':
            if LooseVersion(a) > LooseVersion(b):
                return True
        elif sym == '>=':
            if LooseVersion(a) >= LooseVersion(b):
                return True
        elif sym == '==':
            if LooseVersion(a) == LooseVersion(b):
                return True
        elif sym == '<=':
            if LooseVersion(a) <= LooseVersion(b):
                return True
        elif sym == '<':
            if LooseVersion(a) < LooseVersion(b):
                return True
        return False

    def Compare(self,src,compare_symbol,dest,compare_range='dest',version_symbol='.'):
        if isinstance(src,dict): src=src.get('version')
        if isinstance(dest,dict): dest=dest.get('version')
        if isinstance(src,str):
            src=Split(src,version_symbol)
        elif isinstance(src,tuple):
            src=list(src)
        if isinstance(dest,str):
            dest=Split(dest,version_symbol)
        elif isinstance(dest,tuple):
            dest=list(dest)
        src=[ Int(i) for i in src]
        dest=[ Int(i) for i in dest]
        if compare_range == 'dest':
            src=src[:len(dest)]
        elif compare_range == 'src':
             dest=dest[:len(src)]
        elif isinstance(compare_range,(tuple,list)) and len(compare_range) == 2:
            if isinstance(compare_range[0],int) and isinstance(compare_range[1],int):
                 src=src[compare_range[0]:compare_range[1]]
                 dest=dest[compare_range[0]:compare_range[1]]
            elif not compare_range[0] and isinstance(compare_range[1],int):
                 src=src[:compare_range[1]]
                 dest=dest[:compare_range[1]]
            elif isinstance(compare_range[0],int) and not compare_range[1]:
                 src=src[compare_range[0]:]
                 dest=dest[compare_range[0]:]
        elif isinstance(compare_range,int):
            if len(src) > compare_range and len(dest) > compare_range:
                 src=src[compare_range]
                 dest=dest[compare_range]
            else:
                 return
        return eval('{} {} {}'.format(src,compare_symbol,dest))

