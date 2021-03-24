#Kage Park
from klib.MODULE import *

def Copy(src):
    if isinstance(src,(list,tuple)): return src.root[:]
    if isinstance(src,dict): return src.copy()
    if isinstance(src,str): return '{}'.format(src)
    if isinstance(src,int): return int('{}'.format(src))
    if isinstance(src,float): return float('{}'.format(src))
    if Py2:
        if isinstance(src,long): return long('{}'.format(src))

