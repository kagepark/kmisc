#Kage

def Sort(src,reverse=False,func=None,order=None,field=None,base='key',sym=None):
    if isinstance(src,str) and sym is not None: src=src.split(sym)
    if isinstance(src,dict) and base == 'data':
        field=1
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
    def _cstr_(e):
        if isinstance(field,int):
            if isinstance(e,(list,tuple)) and len(e) > field:
                return '''{}'''.format(e[field])
            else:
                return 'zzzzzzzzz'
        return '''{}'''.format(e)
    if isinstance(src,(list,tuple)):
        if order in [int,'int','digit','number']:
            #def _cint_(e):
            #    try:
            #        if isinstance(field,int):
            #            if isinstance(e,(list,tuple)) and len(e) > field:
            #                return int(e[field])
            #            else:
            #                return 9999999
            #        return int(e)
            #    except:
            #        return e
            return self.root.sort(reverse=reverse,key=_cint_)
        elif order in [str,'str']:
            #def _cint_(e):
            #    if isinstance(field,int):
            #        if isinstance(e,(list,tuple)) and len(e) > field:
            #            return '''{}'''.format(e[field])
            #        else:
            #            return 'zzzzzzzzz'
            #    return '''{}'''.format(e)
            #return self.root.sort(reverse=reverse,key=_cint_)
            return self.root.sort(reverse=reverse,key=_cstr_)
        else:
            if isinstance(field,int):
                #def _cint_(e):
                #    if isinstance(e,(list,tuple)) and len(e) > field:
                #        return e[field]
                return self.root.sort(reverse=reverse,key=_cint_)
            else:
                return self.root.sort(reverse=reverse,key=func)
    elif isinstance(src,dict):
        lst=[]
        if base == 'key':
            lst=list(self.keys())
            if order in [int,'int','digit','number']:
                #def _cint_(e):
                #    try:
                #        return int(e)
                #    except:
                #        return e
                return lst.sort(reverse=reverse,key=_cint_)
            elif order in [str,'str']:
                #def _cint_(e):
                #    return '''{}'''.format(e)
                #return lst.sort(reverse=reverse,key=_cint_)
                return lst.sort(reverse=reverse,key=_cstr_)
            else:
                return lst.sort(reverse=reverse,func=func)
        elif base == 'value':
            lst=self.items()
            if order in [int,'int','digit','number']:
                #def _cint_(e):
                #    try:
                #        return int(e[1])
                #    except:
                #        return e[1]
                lst.sort(reverse=reverse,key=_cint_)
            elif order in [str,'str']:
                #def _cint_(e):
                #    return '''{}'''.format(e[1])
                #lst.sort(reverse=reverse,key=_cint_)
                lst.sort(reverse=reverse,key=_cstr_)
            else:
                lst.sort(reverse=reverse,func=func)
            return [i[0] for i in lst]
