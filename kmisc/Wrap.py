# Kage Park
from klib.MODULE import *
MODULE().Import('klib.Tap import Tap')

def Wrap(src,space='',space_mode='space',sym='\n',default=None,NFLT=False,out=str):
    if not isinstance(src,(str,list,tuple)): return default
    if isinstance(src,str): src=src.split(sym)
    # No First Line Tap (NFLT)
    if isinstance(space,int): space=Tap(space,mode=space_mode)
    rt=[]
    if NFLT:
        rt.append('%s'%(src.pop(0)))
    for ii in src:
        rt.append('%s%s'%(space,ii))
    if rt and out in [str,'str']: return sym.join(rt)
    return rt
