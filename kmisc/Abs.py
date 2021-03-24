# Kage Park
#
from kmisc.OutFormat import OutFormat

def Abs(*inps,**opts):
    default=opts.get('default',None)
    out=opts.get('out','auto')
    obj=opts.get('obj',None)
    err=opts.get('err',True)
    def int_idx(idx,nobj,default,err,out='auto'):
        if idx < 0:
            if abs(idx) <= nobj:
                if out in ['list',list]:
                    return [nobj+idx]
                elif out in ['tuple',tuple]:
                    return (nobj+idx,)
                return nobj+idx
            elif err not in [True,'err','True']:
                return 0
        else:
            if nobj > idx:
                if out in ['list',list]:
                    return [idx]
                elif out in ['tuple',tuple]:
                    return (idx,)
                return idx
            elif err not in [True,'err','True']:
                return nobj-1
        return default
    if len(inps) > 0:
        ss=None
        ee=None
        rt=[]
        if obj is None:
            for i in inps:
                if isinstance(i,int):
                    rt.append(abs(i))
                elif err in [True,'err','True']:
                    rt.append(default)
#        elif isinstance(obj,dict):
#            keys=list(obj)
#            for idx in inps:
#                if isinstance(idx,int):
#                    int_index=int_idx(idx,len(keys),default,err)
#                    if int_index != default: rt.append(keys[int_index])
#                elif isinstance(idx,tuple) and len(idx) == 2:
#                    ss=Abs(idx[0],**opts)
#                    ee=Abs(idx[1],**opts)
#                    for i in range(ss,ee+1):
#                        rt.append(keys[i])
#                elif isinstance(idx,str):
#                    try:
#                        idx=int(idx)
#                        rt.append(int_idx(idx,len(keys),default,err))
#                    except:
#                        if len(idx.split(':')) == 2:
#                            ss,ee=tuple(idx.split(':'))
#                            if isinstance(ss,int) and isinstance(ee,int):
#                                for i in range(ss,ee+1):
#                                    rt.append(keys[i])
#                        elif len(idx.split('-')) == 2:
#                            ss,ee=tuple(idx.split('-'))
#                            if isinstance(ss,int) and isinstance(ee,int):
#                                for i in range(ss,ee+1):
#                                    rt.append(keys[i])
#                        elif len(idx.split('|')) > 1:
#                            rt=rt+idx.split('|')
        elif isinstance(obj,(list,tuple,str)):
            nobj=len(obj)
            for idx in inps:
                if isinstance(idx,list):
                    for ii in idx:
                        if isinstance(ii,int):
                            if nobj > ii:
                                rt.append(ii)
                            else:
                                rt.append(OutFormat(default))
                elif isinstance(idx,int):
                    rt.append(int_idx(idx,nobj,default,err))
                elif isinstance(idx,tuple) and len(idx) == 2:
                    ss=Abs(idx[0],**opts)
                    ee=Abs(idx[1],**opts)
                    rt=rt+list(range(ss,ee+1))
                elif isinstance(idx,str):
                    try:
                        idx=int(idx)
                        rt.append(int_idx(idx,nobj,default,err))
                    except:
                        if len(idx.split(':')) == 2:
                            ss,ee=tuple(idx.split(':'))
                            ss=Abs(ss,**opts)
                            ee=Abs(ee,**opts)
                            if isinstance(ss,int) and isinstance(ee,int):
                                rt=rt+list(range(ss,ee+1))
                        elif len(idx.split('-')) == 2:
                            ss,ee=tuple(idx.split('-'))
                            ss=Abs(ss,**opts)
                            ee=Abs(ee,**opts)
                            if isinstance(ss,int) and isinstance(ee,int):
                                rt=rt+list(range(ss,ee+1))
                        elif len(idx.split('|')) > 1:
                            for i in idx.split('|'):
                                ss=Abs(i,obj=obj,out='raw')
                                if isinstance(ss,int):
                                    rt.append(ss)
                        else:
                            rt.append(OutFormat(default))
        return OutFormat(rt,out=out)
    elif obj:
        if isinstance(obj,(list,tuple,str)):
            return len(obj)
        elif isinstance(obj,dict):
            return list(obj.keys())
    return default

