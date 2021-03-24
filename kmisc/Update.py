# Kage park

def Update(src,*inps,**opts):
    at=opts.pop('at',0)
    err=opts.pop('err',False)
    default=opts.pop('default',False)
    force=opts.pop('force',False)
    sym=opts.pop('sym',None)
    if isinstance(src,(list,tuple,str)):
        if isinstance(src,str) and sym: src=src.split(sym)
        tuple_out=False
        if isinstance(src,tuple) and force:
            src=list(src)
            tuple_out=True
        n=len(src)
        if n == 0:
            if err is True:
                return default
            else:
                src=list(inps)
        elif isinstance(at,int) and n > at:
            for i in range(0,len(inps)):
                if n > at+i:
                    src[at+i]=inps[i]
                elif err is True:
                    return default
                else:
                    src=src+list(inps)[i:]
                    break
        elif isinstance(at,(tuple,list)):
            if len(inps) == len(at):
                for i in range(0,len(at)):
                    if isinstance(at[i],int) and n > at[i]:
                        src[at[i]]=inps[i]
                    elif err is True:
                        return default
                    else:
                        src.append(inps[i])
        if tuple_out: return tuple(src)
        return src
    elif isinstance(src,dict):
        for ii in inps:
           if isinstance(ii,dict):
               src.update(ii)
        if opts:
           src.update(opts)
    return src

