#Kage Park
from distutils.version import LooseVersion
from kmisc.Import import *
Import('from kmisc.Type import Type')

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

