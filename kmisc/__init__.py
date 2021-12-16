#Kage park

#######################################
# Load All files
#######################################
import os
from kmisc.Import import *
for iii in os.listdir(os.path.dirname(__file__)):
    ii_a=iii.split('.')
    if len(ii_a) == 2 and ii_a[-1] == 'py':
        if ii_a[0] in ['__init__','MODULE','test','setup','kmisc','Misc']: continue
        if ii_a[0].isupper():
            Import('from kmisc.{0} import {0}'.format(ii_a[0]))
        else:
            Import('from kmisc import {0}'.format(ii_a[0]))

Import('from kmisc.Misc import *')

def str2url(string):
    return WEB().str2url(string)

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

def rshell(cmd,timeout=None,ansi=True,path=None,progress=False,progress_pre_new_line=False,progress_post_new_line=False,log=None,progress_interval=5):
    return SHELL().Run(cmd,timeout=timeout,ansi=ansi,path=path,progress=progress,progress_pre_new_line=progress_pre_new_line,progress_post_new_line=progress_post_new_line,log=log,progress_interval=progress_interval)
