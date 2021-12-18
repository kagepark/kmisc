#Kage Park
import sys
import traceback,inspect
from kmisc.Import import *
Import('kmisc.TIME import TIME')

def get_function_name():
    return traceback.extract_stack(None, 2)[0][2]

def get_pfunction_name():
    return traceback.extract_stack(None, 3)[0][2]

def get_function_args(func,mode='defaults'):
    rc={}
    args, varargs, keywords, defaults = inspect.getargspec(func)
    if defaults is not None:
        defaults=dict(zip(args[-len(defaults):], defaults))
        del args[-len(defaults):]
        rc['defaults']=defaults
    if args:
        rc['args']=args
    if varargs:
        rc['varargs']=varargs
    if keywords:
        rc['keywards']=keywords
    if mode in ['*','all']:
        return rc
    if mode in rc:
        return rc[mode]

def get_function_list(objName=None,obj=None):
    aa={}
    if obj is None and objName is not None:
       obj=sys.modules[objName]
    if obj is not None:
        for name,fobj in inspect.getmembers(obj):
            if inspect.isfunction(fobj): # inspect.ismodule(obj) check the obj is module or not
                aa.update({name:fobj})
    return aa

def get_caller_fcuntion_name(detail=False):
    try:
        dep=len(inspect.stack())-2
        if detail:
            return sys._getframe(dep).f_code.co_name,sys._getframe(dep).f_lineno,sys._getframe(dep).f_code.co_filename
        else:
            name=sys._getframe(dep).f_code.co_name
            if name == '_bootstrap_inner' or name == '_run_code':
                return sys._getframe(3).f_code.co_name
            return name
    except:
        return False


def is_function(find,src=None):
    if src is None:
        if isinstance(find,str):
            find=sys.modules.get(find)
        return inspect.isfunction(find)
    aa=[]
    if not isinstance(find,str): find=find.__name__
    if isinstance(src,str):
        src=sys.modules.get(src)
    if inspect.ismodule(src) or inspect.isclass(src):
        for name,fobj in inspect.getmembers(src):
            if inspect.isfunction(fobj): # inspect.ismodule(obj) check the obj is module or not
                aa.append(name)
    else:
        for name,fobj in inspect.getmembers(src):
            if inspect.ismethod(fobj): # inspect.ismodule(obj) check the obj is module or not
                aa.append(name)
    if find in aa: return True
    return False

def code_error(email_func=None,email=None,email_title=None,email_server=None,log=None,log_msg='',default=None):
    e=sys.exc_info()[0]
    er=traceback.format_exc()
    if log_msg:
        log_msg='{}\n\n*SYS ERR:\n{}\n\n*FORM ERR:\n{}'.format(log_msg,e,er)
    else:
        log_msg='*SYS ERR:\n{}\n\n*FORM ERR:\n{}'.format(e,er)
    if log: log('\n!!ERROR!!: {}'.format(log_msg),log_level=1)
    if email_func and email and email_title:
        a=email_func(email,email_title,log_msg,dj_ip=email_server)
    TIME().Sleep(5)
    return default

