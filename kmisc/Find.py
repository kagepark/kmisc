#Kage Park
import re
from kmisc.Import import *
Import('kmisc.OutFormat import OutFormat')
Import('kmisc.Type import Type')

def Find(src,find,prs=None,sym='\n',pattern=True,default=[],out=None,findall=False,word=False,mode='value'):
    #if Type(src,'instance','classobj'):
    # if src is instance or classobj then search in description and made function name at key
    if isinstance(src,(list,tuple)):
        rt=[]
        for i in range(0,len(self.root)):
            for j in inps:
                j=j.replace('*','.+').replace('?','.')
                mm=re.compile(j)
                if bool(re.match(mm,self.root[i])):
                    if mode in ['index','idx']:
                        rt.append(i)
                    else:
                        rt.append(src[i])
        if len(rt):
            return rt
    elif isinstance(src,dict):
        path=[]
        for key in src:
            if mode in ['key','*','all']: # find in key only
                if find == key:
                    path.append(key)
            found=src.get(key,None)
            if isinstance(found,dict):
                if dep in found:
                     if mode in ['value','*','all'] and (find == found[dep] or (type(found[dep]) in [DICT,dict,list,tuple] and find in found[dep]) or (type(find) is str and type(found[dep]) is str and find in found[dep])): # find in 'find' only
                          # Value find
                          path.append(key)
                     elif isinstance(found[dep], dict): # recursing
                          path=path+Find(found[dep],find,proper=proper,mode=mode)
                else:
                     if mode in ['value','*','all'] and find == found or (type(found) in [list,tuple] and find in found) or (type(find) is str and type(found) is str and find in found):
                         path.append(key)
                     else:
                         for kk in Find(src[key],find,proper=proper,mode=mode): # recursing
                             path.append(key+'/'+kk)
            else:
                if mode in ['value','*','all'] and find == found or (type(found) in [list,tuple] and find in found) or (type(find) is str and type(found) is str and find in found):
                    path.append(key)
        return path
    elif isinstance(src,str):
        if word:
            find_re=re.compile(r'\b({0})\b'.format(find),flags=re.IGNORECASE)
        else:
            find_re=re.compile(find,flags=re.IGNORECASE)
        if findall:
            match=find_re.findall(src)
            if match: return OutFormat(match,out=out)
        else:
            match=find_re.search(src)
            if match: return OutFormat([match.group()],out=out)
    return OutFormat(default,out=out)

