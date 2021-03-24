#Kage Park
import re

def Replace(src,replace_what,replace_to,default=None):
    if isinstance(src,str):
        if replace_what[-1] == '$' or replace_what[0] == '^':
            return re.sub(replace_what, replace_to, src)
        else:
            head, _sep, tail = src.rpartition(replace_what)
            return head + replace_to + tail
    if default == {'org'}: return src
    return default
