#Kage Park
import re
from kmisc.Import import *
Import('from kmisc.Abs import Abs')
Import('from kmisc.Misc import *')


class LIST(list):
    def __init__(self,*inps):
        if len(inps) == 1 and isinstance(inps[0],(list,tuple)):
            self.root=list(inps[0])
        else:
            self.root=list(inps)

#    def __new__(cls,*inps):
#        if len(inps) == 1 and isinstance(inps[0],(list,tuple)):
#            return list(inps[0])
#        else:
#            return list(inps)

    # reply self.root back to the Class's output a=List(['a']), return the data to a
    def __repr__(self):
        return repr(self.root)

    def Convert(self,src,path=False,default=False,symbol=':white_space:',**opts):
        if isinstance(src,str) and src:
            if path and isinstance(symbol,str):
                if symbol == ':white_space:':
                    symbol='/'
                start=0
                if src[0] == symbol:
                    start=1
                if src[-1] == symbol:
                    return src.split(symbol)[start:-1]
                return src.split(symbol)[start:]
            else:
                if symbol == ':white_space:':
                    return src.strip().split()
                elif isinstance(symbol,str):
                    return src.split(symbol)
                elif isinstance(symbol,(tuple,list)):
                    regexPattern = '|'.join(map(re.escape,tuple(symbol)))
                    return re.split(regexPattern,src)
                return default
        elif isinstance(src,(list,tuple)):
            return list(src)
        else:
            return [src]
 
    def Append(self,*inps,**opts):
        uniq=opts.get('uniq',False)
        symbol=opts.get('symbol',':white_space:')
        path=opts.get('path',False)
        default=opts.get('default',False)
        for pp in inps:
            for rp in self.Convert(pp,symbol=symbol,path=path,default=default):
                if rp == default: continue
                if uniq and rp in rt: continue
                if path:
                    if rp == '.': continue
                    if rp == '..' and len(rt):
                        del self.root[-1]
                        continue
                self.root.append(rp)
        return self.root

    def append(self,inp):
        self.root.append(inp)

    def Uniq(self,*inps,**opts):
        symbol=opts.get('symbol',':white_space:')
        path=opts.get('path',False)
        default=opts.get('default',False)
        for pp in self.root + list(inps):
            for rp in self.Convert(pp,symbol=symbol,path=path,default=default):
                if rp == default: continue
                if rp in rt: continue
                if path:
                    if rp == '.': continue
                    if rp == '..' and len(rt):
                        del self.root[-1]
                        continue
                self.root.append(rp)
        return self.root

    def Delete(self,*inps,**opts):
        find=opts.get('find','index')
        default=opts.get('default',False)
        if find in ['data','element']:
            for i in inps:
                if i in self.root:
                    self.root.remove(i)
        else:
            if len(inps) == 1 and isinstance(inps[0],int):
                if len(self.root) > inps[0]:
                    del self.root[inps[0]]
            else:
                rt=[]
                del_list=Abs(*inps,obj=self.root,out=list)
                for i in range(0,len(self.root)):
                    if i in del_list: continue
                    rt.append(self.root[i])
                self.root=rt

    def Get(self,*inps,**opts):
        if not inps: return self.root
        find=opts.get('find','data')
        default=opts.get('default',None)
        out=opts.get('out',list)
        err=opts.get('err',False)
        if len(self.root) == 0 and err:
            return default
        rt=[]
        if find in ['index','idx']:
            for i in inps:
                if i in self.root:
                    rt.append(self.root.index(i))
                elif err is True:
                    rt.append(default)
        else:
            for i in Abs(*inps,obj=self.root,err=err,out=list,default=None):
                if isinstance(i,int) and self.root:
                    rt.append(self.root[i])
                elif err is True:
                    return default
        if rt:
            if out in [list,'list']:
                return rt
            elif out in [tuple,'tuple']:
                return tuple(rt)
            elif out in [None,'raw']:
                if len(rt) == 1:
                    return rt[0]
                return rt
        return default

    def Index(self,*inps):
        return self.Get(*inps,find='index')

    def Insert(self,*inps,**opts):
        start=opts.get('at',0)
        default=opts.get('default',False)
        err=opts.get('err',False)
        if isinstance(at,str):
            if at in ['start','first']: self.root=list(inps)+self.root
            if at in ['end','last']: self.root=self.root+list(inps)
        elif len(self.root) == 0:
            self.root=list(inps)
        elif isinstance(start,int) and len(self.root) > start:
            self.root=self.root[:start]+list(inps)+self.root[start:]
        else:
            if err:
                return default
            self.root=self.root+list(inps)

    def Update(self,*inps,**opts):
        at=opts.get('at',0)
        err=opts.get('err',False)
        default=opts.get('default',False)
        n=len(self.root)
        if n == 0:
            if err is True:
                return default
            else:
                self.root=list(inps)
        elif isinstance(at,int) and n > at:
            for i in range(0,len(inps)):
                if n > at+i:
                    self.root[at+i]=inps[i]
                elif err is True:
                    return default
                else:
                    self.root=self.root+list(inps)[i:]
                    break
        elif isinstance(at,(tuple,list)):
            if len(inps) == len(at):
                for i in range(0,len(at)):
                    if isinstance(at[i],int) and n > at[i]:
                        self.root[at[i]]=inps[i]
                    elif err is True:
                        return default
                    else:
                        self.root.append(inps[i])

    def Find(self,*inps,**opts):
        find=opts.get('find','index')
        default=opts.get('default',[])
        rt=[]
        for i in range(0,len(self.root)):
            for j in inps:
                j=j.replace('*','.+').replace('?','.')
                mm=re.compile(j)
                if bool(re.match(mm,self.root[i])):
                    if find in ['index','idx']:
                        rt.append(i)
                    else:
                        rt.append(self.root[i])
        if len(rt):
            return rt
        return default

    def Copy(self):
        return self.root[:]
    def copy(self):
        return self.root[:]

    def Tuple(self):
        return tuple(self.root)

    def Move2first(self,find):
        if find in self.root:
            self.Delete(*(find),find='data')
            self.root=[find]+self.root
        return self.root

    def Move2end(self,find):
        if find in self.root:
            self.Delete(*(find),find='data')
            self.root=self.root+[find]
        return self.root

    def Sort(self,reverse=False,func=None,order=None,field=None):
        if order in [int,'int','digit','number']:
            def _cint_(e):
                try:
                    if isinstance(field,int):
                        if isinstance(e,(list,tuple)) and len(e) > field:
                            return int(e[field])
                        else:
                            return 9999999
                    return int(e)
                except:
                    return e
            return self.root.sort(reverse=reverse,key=_cint_)
        elif order in [str,'str']:
            def _cint_(e):
                if isinstance(field,int):
                    if isinstance(e,(list,tuple)) and len(e) > field:
                        return '''{}'''.format(e[field])
                    else:
                        return 'zzzzzzzzz'
                return '''{}'''.format(e)
            return self.root.sort(reverse=reverse,key=_cint_)
        else:
            if isinstance(field,int):
                def _cint_(e):
                    if isinstance(e,(list,tuple)) and len(e) > field:
                        return e[field]
                return self.root.sort(reverse=reverse,key=_cint_)
            else:
                return self.root.sort(reverse=reverse,key=func)

    def Str(self,sym=' ',default=None):
        if isinstance(self.src,(tuple,list)):
            rt_str=''
            for ii in self.src:
                if rt_str:
                    rt_str='''{}{}{}'''.format(rt_str,sym,ii)
                else:
                    rt_str='''{}'''.format(ii)
            self.src=rt_str
            return rt_str
        return default

