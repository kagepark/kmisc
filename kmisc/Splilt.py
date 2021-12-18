#Kage Park
import re
from kmisc.Import import *
Import('kmisc.CONVERT import CONVERT')

#def Split(src,sym=None,default=None):
#    if isinstance(src,str):
#        try:
#            return re.split(sym,src) # splited by '|' or expression
#        except:
#            return src.split(sym)
#    return default

def Split(src,sym,default=None):
    if isinstance(src,str):
        #if isinstance(sym,bytes): sym=_u_bytes2str(sym)
        if isinstance(sym,bytes): sym=CONVERT(sym).Str()
    elif isinstance(src,bytes):
        #if isinstance(sym,str): sym=_u_bytes(sym,default={'org'})
        if isinstance(sym,str): sym=CONVERT(sym).Bytes(default={'org'})
    else:
        return default
    if len(sym) > 2 and '|' in sym:
        try:
            sym_a=sym.split('|')
            for i in ['.','+','*']:
                try:
                    x=sym_a.index(i)
                    sym_a[x]='\{}'.format(sym_a[x])
                except:
                    continue
            return re.split('|'.join(sym_a),src) # splited by '|' or expression
        except:
            pass
    return src.split(sym)

