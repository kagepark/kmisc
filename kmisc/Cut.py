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

def cut_string(string,max_len=None,sub_len=None,new_line='\n',front_space=False,out_format=list):
    rc=[]
    if not isinstance(string,str):
        string='{0}'.format(string)
    if new_line:
        string_a=string.split(new_line)
    else:
        string_a=[string]
    if max_len is None or (max_len is None and sub_len is None):
        if new_line and out_format in [str,'str','string']:
            return string
        return [string]
    max_num=len(string_a)
    space=''
    if sub_len and front_space:
        for ii in range(0,max_len-sub_len):
            space=space+' '
    elif sub_len is None:
        sub_len=max_len
    for ii in range(0,max_num):
        str_len=len(string_a[ii])
        if max_num == 1:
            if max_len is None or max_len >= str_len:
                if new_line and out_format in [str,'str','string']:
                    return string_a[ii]
                return [string_a[ii]]
            if sub_len is None:
                rc=[string_a[i:i + max_len] for i in range(0, str_len, max_len)]
                if new_line and out_format in [str,'str','string']:
                    return new_line.join(rc)
                return rc
        rc.append(string_a[ii][0:max_len])
        string_tmp=string_a[ii][max_len:]
        string_tmp_len=len(string_tmp)
        if string_tmp_len > 0:
            for i in range(0, (string_tmp_len//sub_len)+1):
                if (i+1)*sub_len > string_tmp_len:
                    rc.append(space+string_tmp[sub_len*i:])
                else:
                    rc.append(space+string_tmp[sub_len*i:(i+1)*sub_len])
#        else:
#            rc.append('')
    if new_line and out_format in [str,'str','string']:
        return new_line.join(rc)
    return rc

