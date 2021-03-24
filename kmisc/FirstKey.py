#Kage park

def FirstKey(src,default=None):
    if src:
        if isinstance(src,(list,tuple)): return 0
        try:
            return next(iter(src))
        except:
            return default
    return default
