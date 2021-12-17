#Kage park

#######################################
# Load All files
#######################################
import os
from kmisc.Import import *
for iii in os.listdir(os.path.dirname(__file__)):
    ii_a=iii.split('.')
    if len(ii_a) == 2 and ii_a[-1] == 'py':
        if ii_a[0] in ['__init__','MODULE','test','setup','kmisc','Misc','kBmc']: continue
        if ii_a[0].isupper():
            Import('from kmisc.{0} import {0}'.format(ii_a[0]))
        else:
            Import('from kmisc import {0}'.format(ii_a[0]))

Import('from kmisc.Misc import *')
Import('from kmisc.kBmc import kBmc,Ipmitool,Smcipmitool,')

def mac2str(mac,case='lower'):
    return MAC(mac).ToStr(case=case)

def str2mac(mac,sym=':',case='lower',chk=False):
    return MAC(mac).FromStr(case=case,sym=sym,chk=chk)

def is_mac4(mac=None,symbol=':',convert=True):
    return MAC(mac).IsV4(symbol=symbol)

def str2url(string):
    return WEB().str2url(string)

def is_bmc_ipv4(ipaddr,port=(623,664,443)):
    return IP(ipaddr).IsBmcIp(port=port)

def is_port_ip(ipadd,port):
    return IP(ipaddr).IsOpenPort(port)

def ipv4(ipaddr=None,chk=False):
    return IP(ipaddr).V4(out='str',default=False)

def ip_in_range(ip,start,end):
    return IP(ip).InRange(start,end)

def is_ipv4(ipadd=None):
    return IP(ipaddr).IsV4()

def ip2num(ip):
    return IP(ip).Ip2Num()

def web_server_ip(request):
    web=WEB(request)
    return web.ServerIp()

def web_client_ip(request):
    web=WEB(request)
    return web.ClientIp()

def web_session(request):
    web=WEB(request)
    return web.Session()

def web_req(host_url=None,**opts):
    return WEB().Request(host_url,**opts)

def printf(*msg,**opts):
    return Print.printf(*msg,**opts)

def sprintf(string,*inps,**opts):
    return Print.sprintf(string,*inps,**opts)

def format_string(string,inps):
    return Print.format_string(string,inps)

def format_print(string,rc=False,num=0,bstr=None,NFLT=False):
    return Print.format_print(string,rc=rc,num=num,bstr=bstr,NFLT=NFLT)

def logging(*msg,**opts):
    return Print.printf(*msg,**opts)

def is_py3():
    return PyVer(3)

#def rshell(cmd,timeout=None,ansi=True,path=None,progress=False,progress_pre_new_line=False,progress_post_new_line=False,log=None,progress_interval=5):
#    return SHELL().Run(cmd,timeout=timeout,ansi=ansi,path=path,progress=progress,progress_pre_new_line=progress_pre_new_line,progress_post_new_line=progress_post_new_line,log=log,progress_interval=progress_interval)

def gen_random_string(length=8,letter='*',digits=True,symbols=True,custom=''):
    mode='alpha'
    if digits:mode=mode+'num'
    if symbols:mode=mode+'char'
    return Random(length=length,strs=custom,mode='*',letter=letter)

def string2data(string,default='org',want_type=None):
    return CONVERT(string).Ast(default=default,want_type=want_type)

def append(src,addendum):
    type_src=type(src)
    type_data=type(addendum)
    if src is None:
        if type_data is str:
            src=''
        elif type_data is dict:
            src={}
        elif type_data is list:
            src=[]
        elif type_data is tuple:
            src=()
        type_src=type(src)
    if addendum is None:
        return src
    if type_src == type_data:
        if type_src is dict:
            return src.update(addendum)
        elif type_src in [list,tuple]:
            src=list(src)
            for ii in addendum:
                if ii not in src:
                    src.append(ii)
            if type_src is tuple:
                src=tuple(src)
            return src
        elif type_src is str:
            return src+addendum
    return False

def compare(a,sym,b,ignore=None):
    if type(a) is not int or type(b) is not int:
        return False
    if ignore is not None:
        if eval('{} == {}'.format(a,ignore)) or eval('{} == {}'.format(b,ignore)):
            return False
    return eval('{} {} {}'.format(a,sym,b))

def integer(a,default=0):
    try:
        return int(a)
    except:
        return default

def argtype(arg,want='_',get_data=['_']):
    type_arg=type(arg)
    if want in get_data:
        if type_arg.__name__ == 'Request':
            return arg.method.lower()
        return type_arg.__name__.lower()
    if type(want) is str:
        if type_arg.__name__ == 'Request':
            if want.upper() == 'REQUEST' or want.upper() == arg.method:
                return True
            return False
        else:
            if type_arg.__name__.lower() == want.lower():
                return True
    else:
        if type_arg == want:
            return True
    return False

def get_data(data,key=None,ekey=None,default=None,method=None,strip=True,find=[],out_form=str):
    if argtype(data,'Request'):
        if key:
            if method is None:
                method=data.method
            if method.upper() == 'GET':
                rc=data.GET.get(key,default)
            elif method == 'FILE':
                if out_form is list:
                    rc=data.FILES.getlist(key,default)
                else:
                    rc=data.FILES.get(key,default)
            else:
                if out_form is list:
                    rc=data.POST.getlist(key,default)
                else:
                    rc=data.POST.get(key,default)
            if argtype(rc,str) and strip:
                rc=rc.strip()
            if find and rc in find:
                return True
            if rc == 'true':
                return True
            elif rc == '':
                return default
            return rc
        else:
            if data.method == 'GET':
                return data.GET
            else:
                return data.data
    else:
        type_data=type(data)
        if type_data in [tuple,list]:
            if len(data) > key:
                if ekey and len(data) > ekey:
                    return data[key:ekey]
                else:
                    return data[key]
        elif type_data is dict:
            return data.get(key,default)
    return default

def file_rw(name,data=None,out='string',append=False,read=None,overwrite=True):
    return FILE().Rw(name,data=data,out=out,append=append,read=read,overwrite=overwrite,finfo={})

def cat(filename,no_end_newline=False):
    tmp=file_rw(filename)
    tmp=Get(tmp,1)
    if isinstance(tmp,str) and no_end_newline:
        tmp_a=tmp.split('\n')
        ntmp=''
        for ii in tmp_a[:-1]:
            if ntmp:
                ntmp='{}\n{}'.format(ntmp,ii)
            else:
                ntmp='{}'.format(ii)
        if len(tmp_a[-1]) > 0:
            ntmp='{}\n{}'.format(ntmp,tmp_a[-1])
        tmp=ntmp
    return tmp

def ls(dirname,opt=''):
    if os.path.isdir(dirname):
        dirlist=[]
        dirinfo=list(os.walk(dirname))[0]
        if opt == 'd':
            dirlist=dirinfo[1]
        elif opt == 'f':
            dirlist=dirinfo[2]
        else:
            dirlist=dirinfo[1]+dirinfo[2]
        return dirlist
    return False

def rm_file(filelist):
    if type(filelist) == type([]):
       filelist_tmp=filelist
    else:
       filelist_tmp=filelist.split(',')
    for ii in list(filelist_tmp):
        if os.path.isfile(ii):
            os.unlink(ii)
        else:
            print('not found {0}'.format(ii))

def append2list(*inps,**opts):
    return LIST(inps[0]).Append(*inps[1:],**opts)

def ping(host,**opts):
    count=opts.get('count',3)
    interval=opts.get('interval',1)
    keep_good=opts.get('keep_good',0)
    timeout=opts.get('timeout',opts.get('timeout_sec',5))
    lost_mon=opts.get('lost_mon',False)
    log=opts.get('log',None)
    stop_func=opts.get('stop_func',None)
    log_format=opts.get('log_format','.')
    cancel_func=opts.get('cancel_func',None)
    return IP().Ping(host=host,count=count,interval=interval,keep_good=keep_good, timeout=timeout_sec,lost_mon=lost_mon,log=log,stop_func=stop_func,log_format=log_format,cancel_func=cancel_func)

def is_lost(ip,**opts):
    timeout=opts.get('timeout',opts.get('timeout_sec',1800))
    interval=opts.get('interval',5)
    stop_func=opts.get('stop_func',None)
    cancel_func=opts.get('cancel_func',None)
    log=opts.get('log',None)
    init_time=None
    if not ping(ip,count=3):
        if not ping(ip,count=0,timeout=timeout,keep_good=30,interval=2,stop_func=stop_func,log=log,cancel_func=cancel_func):
            return True,'Lost network'
    return False,'OK'

def is_comeback(ip,**opts):
    timeout=opts.get('timeout',opts.get('timeout_sec',1800))
    interval=opts.get('interval',3)
    keep=opts.get('keep',20)
    stop_func=opts.get('stop_func',None)
    cancel_func=opts.get('cancel_func',None)
    log=opts.get('log',None)
    init_time=None
    run_time=int_sec()
    if keep == 0 or keep is None:
        return True,'N/A(Missing keep parameter data)'
    if log:
        log('[',direct=True,log_level=1)
    time=TIME()
    while True:
        if time.Out(timeout_sec):
            if log:
                log(']\n',direct=True,log_level=1)
            return False,'Timeout monitor'
        if is_cancel(cancel_func) or stop_func is True:
            if log:
                log(']\n',direct=True,log_level=1)
            return True,'Stopped monitor by Custom'
        if ping(ip,cancel_func=cancel_func):
            if (int_sec() - run_time) > keep:
                if log:
                    log(']\n',direct=True,log_level=1)
                return True,'OK'
            if log:
                log('-',direct=True,log_level=1)
        else:
            run_time=int_sec()
            if log:
                log('.',direct=True,log_level=1)
        time.sleep(interval)
    if log:
        log(']\n',direct=True,log_level=1)
    return False,'Timeout/Unknown issue'

def sizeConvert(sz=None,unit='b:g'):
    return CONVERT(sz).Size(unit=unit)

def Join(*inps,symbol=''):
    if len(inps) == 1 and isinstance(inps[0],(list,tuple)):
        src=inps[0]
    else:
        src=inps
    rt=''
    for i in src:
        if rt:
            rt=rt+symbol+'{}'.format(i)
        else:
            rt='{}'.format(i)
    return rt

def list2str(arr):
    return Join(arr,symbol=' ')


def _u_str2int(val,encode='utf-8'):
    return CONVERT(val).Str2Int(encode)

def _u_bytes(val,encode='utf-8'):
    return CONVERT(val).Bytes(encode)

def _u_bytes2str(val,encode='latin1'):
    return _u_byte2str(val,encode=encode)

def _u_byte2str(val,encode='latin1'):
    return CONVERT(val).Str(encode=encode)

def file_mode(val):
    return FILE().Mode(val)

def get_file(filename,**opts)
    return FILE(filename,**opts)

def save_file(data,dest):
    return data.Save(dest)
