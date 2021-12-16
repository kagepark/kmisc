#Kage Park
import random
import re
from kmisc.Import import *
Import('kmisc.OutFormat import OutFormat')
Import('kmisc.Random import Random')
Import('kmisc.FIND import FIND')

class STR(str):
    def __init__(self,src):
        self.src=src

    def Rand(self,length=8,strs=None,mode='*'):
        return Random(length=length,strs=strs,mode=mode)
        #if not isinstance(strs,str):
        #    if mode in ['all','*','alphanumchar']:
        #        strs='0aA-1b+2Bc=C3d_D,4.eE?5"fF6g7G!h8H@i9#Ij$JkK%lLmMn^N&oO*p(Pq)Q/r\Rs:St;TuUv{V<wW}x[Xy>Y]z|Z'
        #    elif mode in ['alphanum']:
        #        strs='aA1b2BcC3dD4eE5fF6g7Gh8Hi9IjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'
        #    else:
        #        strs='aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'
        #new=''
        #strn=len(strs)-1
        #for i in range(0,length):
        #    new='{0}{1}'.format(new,strs[random.randint(0,strn)])
        #return new

    def Cut(self,head_len=None,body_len=None,new_line='\n',out=str):
        if not isinstance(self.src,str):
           self.src='''{}'''.format(self.src)

        source=self.src.split(new_line)

        if len(source) == 1 and not head_len or head_len >= len(self.src):
           return [self.src]

        rt=[]
        for src_idx in range(0,len(source)):
            str_len=len(source[src_idx])

            if not body_len:
                rt=rt+[source[src_idx][i:i + head_len] for i in range(0, str_len, head_len)]
            else:
                if src_idx == 0: 
                    rt.append(source[src_idx][0:head_len]) # Take head
                    if str_len > head_len:
                        rt=rt+[source[src_idx][head_len:][i:i + body_len] for i in range(0, str_len-head_len, body_len)]
                    ## Cut body
                    #string_tmp=self.src[head_len:]
                    #string_tmp_len=len(string_tmp)
                    #for i in range(0, int(string_tmp_len/body_len)+1):
                    #    if (i+1)*body_len > string_tmp_len:
                    #       rt.append(string_tmp[body_len*i:])
                    #    else:
                    #       rt.append(string_tmp[body_len*i:(i+1)*body_len])
                else:
                    rt=rt+[source[src_idx][i:i + body_len] for i in range(0, str_len, body_len)]
        if rt and out in ['str',str]: return new_line.join(rt)
        return rt

    def Tap(self,space='',sym='\n',default=None,NFLT=False,out=str):
        # No First Line Tap (NFLT)
        if isinstance(space,int):
            sspace=''
            for i in range(0,space):
                sspace='{}{}'.format(sspace,' ')
            space=sspace
        if isinstance(self.src,str):
            self.src=self.src.split(sym)
        if isinstance(self.src,(list,tuple)):
            rt=[]
            if NFLT:
                rt.append(self.src.pop(0))
            for ii in self.src:
                rt.append('%s%s'%(space,ii))
            if rt and out in [str,'str']: return sym.join(rt)
            return rt
        return default

    def Reduce(self,start=0,end=None,sym=None,default=None):
        if isinstance(self.src,str):
            if sym:
                arr=self.src.split(sym)
                if isinstance(end,int):
                    return sym.join(arr[start:end])
                else:
                    return sym.join(arr[start])
            else:
                if isinstance(end,int):
                    return self.src[start:end]
                else:
                    return self.src[start:]
        return default

    def Find(self,find,src=None,prs=None,sym='\n',pattern=True,default=[],out=None,findall=False,word=False):
        if src is None: src=self.src
        return FIND().Find(src,find,prs=prs,sym=sym,pattern=pattern,default=default,out=out,findall=findall,word=word,mode='value')
#        if isinstance(src,str):
#            if word:
#                find_re=re.compile(r'\b({0})\b'.format(find),flags=re.IGNORECASE)
#            else:
#                find_re=re.compile(find,flags=re.IGNORECASE)
#            if findall:
#                match=find_re.findall(src)
#                if match: return OutFormat(match,out=out)
#            else:
#                match=find_re.search(src)
#                if match: return OutFormat([match.group()],out=out)
#        return OutFormat(default,out=out)

    def Index(self,find,start=None,end=None,sym='\n',default=[],word=False,pattern=False,findall=False,out=None):
        if not isinstance(self.src,str): return default
        rt=[]
        source=self.src.split(sym)
        for row in range(0,len(source)):
            for ff in self.Find(find,src=source[row],pattern=pattern,word=word,findall=findall,default=[],out=list):
                if findall:
                    rt=rt+[(row,[m.start() for m in re.finditer(ff,source[row])])]
                else:
                    idx=source[row].index(ff,start,end)
                    if idx >= 0:
                        rt.append((row,idx))
        if rt:
            if out in ['tuple',tuple]: return tuple(rt)
            if out not in ['list',list] and len(rt) == 1 and rt[0][0] == 0: 
                if len(rt[0][1]) == 1:return rt[0][1][0]
                return rt[0][1]
            return rt
        return default

    def Replace(self,replace_what,replace_to,default=None):
        if isinstance(self.src,str):
            if replace_what[-1] == '$' or replace_what[0] == '^':
                return re.sub(replace_what, replace_to, self.src)
            else:
                head, _sep, tail = self.src.rpartition(replace_what)
                return head + replace_to + tail
        return default

    def Split(self,sym=None):
        if isinstance(self.src,str):
            try:
                return re.split(sym,self.src) # splited by '|' or expression
            except:
                return self.src.split(sym)
