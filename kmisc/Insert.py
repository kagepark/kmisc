# Kage Park

def Insert(src,*inps,**opts):
    start=opts.pop('at',0)
    default=opts.pop('default',False)
    err=opts.pop('err',False)
    force=opts.pop('force',False)
    uniq=opts.pop('uniq',False)
    if isinstance(src,(list,tuple,str)):
        tuple_out=False
        if isinstance(src,tuple) and force:
            src=list(src)
            tuple_out=True
        if uniq:
            new=[]
            for ii in inps:
                if ii not in src:
                    new.append(ii)
            inps=tuple(new)
        if isinstance(at,str):
            if at in ['start','first']: src=list(inps)+src
            if at in ['end','last']: src=src+list(inps)
        elif len(src) == 0:
            src=list(inps)
        elif isinstance(start,int) and len(src) > start:
            src=src[:start]+list(inps)+src[start:]
        else:
            if err:
                return default
            src=src+list(inps)
        if tuple_out: return tuple(src)
    elif isinstance(src,dict):
        for ii in inps:
            if isinstance(ii,dict):
                 src.update(ii)
        if opts:
            src.update(opts)
    return src
