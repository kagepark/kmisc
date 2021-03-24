# Kage Park
from klib.MODULE import *
MODULE().Import('klib.Find import Find')
MODULE().Import('klib.Type import Type')

def Keys(src,find=None,start=None,end=None,sym='\n',default=[],word=False,pattern=False,findall=False,out=None):
    rt=[]
    if isinstance(src,str,list,tuple) and find:
        if isinstance(src,str): src=src.split(sym)
        
        for row in range(0,len(src)):
            for ff in Find(find,src=src[row],pattern=pattern,word=word,findall=findall,default=[],out=list):
                if findall:
                    rt=rt+[(row,[m.start() for m in re.finditer(ff,src[row])])]
                else:
                    idx=src[row].index(ff,start,end)
                    if idx >= 0:
                        rt.append((row,idx))
    elif isinstance(src,dict):
        if find is None: 
            if out in ['raw',None] and len(src.keys()) == 1 : return list(src.keys())[0]
            if out in ['tuple',tuple]: return tuple(list(src.keys()))
            return list(src.keys())
        # if it has found need code for recurring search at each all data and path of keys
        # return [ (keypath,[found data]), .... ]
    #elif Type(src,'instance','classobj'):
    # if src is instance or classobj then search in description and made function name at key
    if rt:
        if out in ['tuple',tuple]: return tuple(rt)
        if out not in ['list',list] and len(rt) == 1 and rt[0][0] == 0:
            if len(rt[0][1]) == 1:return rt[0][1][0]
            return rt[0][1]
        return rt
    return default

