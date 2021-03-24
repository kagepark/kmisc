#Kage Park

def Split(src,sym=None,default=None):
    if isinstance(src,str):
        try:
            return re.split(sym,src) # splited by '|' or expression
        except:
            return src.split(sym)
    return default
