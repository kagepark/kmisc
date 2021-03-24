#Kage Park

def OutFormat(data,out=None):
    if out in [tuple,'tuple']:
        if not isinstance(data,tuple):
            return (data,)
        elif not isinstance(data,list):
            return tuple(data)
    elif out in [list,'list']:
        if not isinstance(data,list):
            return [data]
        elif not isinstance(data,tuple):
            return list(data)
    elif out in ['raw',None]:
        if isinstance(data,(list,tuple)) and len(data) == 1:
            return data[0]
        elif isinstance(data,dict) and len(data) == 1:
            return data.values()[0]
    return data

