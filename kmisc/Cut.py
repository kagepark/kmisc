#Kage Park

def Cut(src,head_len=None,body_len=None,new_line='\n',out=str):
    if not isinstance(src,str): return False
#    if not isinstance(src,str):
#       src='''{}'''.format(src)
    source=src.split(new_line)
    if len(source) == 1 and not head_len or head_len >= len(src):
       return [src]
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

