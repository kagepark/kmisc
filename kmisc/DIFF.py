#Kage park
from kmisc.Import import Import
Import('from kmisc.Type import Type')

class DIFF:
    def __init__(self):
        pass

    def Data(self,a,sym,b,ignore=None,default=None):
        if isinstance(ignore,(list,tuple)):
            if a in ignore or b in ignore:
                return default
        elif ignore is not None:
            if eval('{} == {}'.format(a,ignore)) or eval('{} == {}'.format(b,ignore)):
                return default
        if sym == '==':
            try:
                return eval('{} == {}'.format(a,b))
            except:
                return default
        elif isinstance(a,int) and isinstance(b,int):
            try:
                return eval('{} {} {}'.format(a,sym,b))
            except:
                return default
        elif isinstance(a,str) and isinstance(b,str) and a.isdigit() and b.isdigit():
            try:
                return eval('{} {} {}'.format(a,sym,b))
            except:
                return default
        return default

    def Code(self):
        pass

    def File(self):
        pass
