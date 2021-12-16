import os
import pickle
import sys
import inspect
from kmisc.Import import *
Import('from kmisc.Type import Type')
Import('from kmisc.FILE import FILE')
Import('from kmisc.OutFormat import OutFormat')
Import('from kmisc.Abs import Abs')

class GET:
    def __init__(self,src=None,**opts):
        self.src=src

    def __repr__(self):
        if self.src is None: return repr(self.MyAddr())
        if Type(self.src,('instance','classobj')):
            def method_in_class(class_name):
                ret=dir(class_name)
                if hasattr(class_name,'__bases__'):
                    for base in class_name.__bases__:
                        ret=ret+method_in_class(base)
                return repr(ret)
            return repr(method_in_class(self.src))
        elif Type(self.src,'dict'):
            return repr(list(self.src.keys()))
        elif Type(self.src,('str','list','tuple')):
            return repr(len(self.src))
        else:
            #return repr(type(self.src).__name__)
            return repr(self.src)

    def MyAddr(self):
        return hex(id(self))

    def Index(self,*find,**opts):
        default=opts.get('default',None)
        err=opts.get('err',False)
        out=opts.get('out',None)
        rt=[]
        if Type(self.src,(list,tuple,str)):
            for ff in find:
                if ff in self.src: rt.append(self.src.index(ff))
        elif Type(self.src,dict):
            for i in self.src:
                for ff in find:
                    if find == self.src[i]: rt.append(i)
        if rt: return OutFormat(rt,out=out)
        if err == {'org'}: return self.src
        return OutFormat(default,out=out)

    def Value(self,*find,**opts):
        default=opts.get('default',None)
        err=opts.get('err',False)
        out=opts.get('out',None)
        check=opts.get('check',('str','list','tuple','dict','instance','classobj'))
        rt=[]
        src_name=type(self.src).__name__
        if len(find) == 0:
            if src_name in ['kDict','kList','DICT']: return self.src.Get()
            if Type(self.src,('instance','classobj')):
                def method_in_class(class_name):
                    ret=dir(class_name)
                    if hasattr(class_name,'__bases__'):
                        for base in class_name.__bases__:
                            ret=ret+method_in_class(base)
                    return ret
                return method_in_class(self.src)
        elif Type(self.src,tuple(check)):
            # Support
            if Type(self.src,(list,tuple,str)):
                if src_name in ['kList']: self.src=self.src.Get()
                for ff in Abs(*find,obj=self.src,out=list,default=None,err=err):
                    if ff is None:
                        if err in [True,'True','err']: rt.append(default)
                    else:
                        rt.append(self.src[ff])
            elif Type(self.src,dict):
                if src_name in ['kDict','DICT']: self.src=self.src.Get()
                for ff in find:
                    gval=self.src.get(ff,default)
                    if gval == default:
                        if err in [True,'True','err']: rt.append(gval)
                    else:
                        rt.append(gval)
            elif Type(self.src,('instance','classobj')):
                # get function object of finding string name in the class/instance
                for ff in find:
                    if isinstance(ff,(list,tuple,dict)):
                        for kk in ff:
                            rt.append(getattr(self.src,kk,default))
                    elif isinstance(ff,str): 
                        rt.append(getattr(self.src,ff,default))
            if rt: return OutFormat(rt,out=out)
        # Not support format or if not class/instance then return error
        if err in [True,'True','true','err','ERR','ERROR','error']: OutFormat(default,out=out)
        return OutFormat(self.src,out=out)

    def Read(self,default=False):
        if Is(self.src).Pickle():
            try:
                with open(self.src,'rb') as handle:
                    return pickle.load(handle)
            except:
                pass
        elif os.path.isfile(self.src):
            return FILE().Get(self.src)
        return default

    def Args(self,field='all',default={}):
        rt={}
        if Type(self.src,('classobj,instance')):
            try:
                self.src=getattr(self.src,'__init__')
            except:
                return self.src.__dict__
        elif not Type(self.src,'function'):
            return default
        args, varargs, keywords, defaults = inspect.getargspec(self.src)
        if defaults is not None:
            defaults=dict(zip(args[-len(defaults):], defaults))
            del args[-len(defaults):]
            rt['defaults']=defaults
        if args:
            rt['args']=args
        if varargs:
            rt['varargs']=varargs
        if keywords:
            rt['keywards']=keywords
        if Type(field,(list,tuple)):
            rts=[]
            for ii in field:
                rts.append(rt.get(ii,default))
            return rts
        else:
            if field in ['*','all']:
                return rt
            if field in rt:
                return rt[field]
        return default

    def ArgType(self,arg,want='_',get_data=['_']):
        type_arg=type(arg)
        if want in get_data:
            if type_arg.__name__ == 'Request':
                return arg.method.lower()
            return type_arg.__name__.lower()
        if Type(want,str):
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

    def FuncList(self):
        rt={}
        if Type(self.src,'instance'):
            self.src=self.src.__class__
        if Type(self.src,('classobj','module')):
            for name,fobj in inspect.getmembers(self.src):
                if Type(fobj,('function','instancemethod')):
                    rt.update({name:fobj})
        return rt

    def FunctionList(self):
        return self.FuncList()

    def Func(self,name,default=None):
        funcList=self.FuncList()
        if isinstance(name,str):
            if name in funcList: return funcList[name]
        elif Type(name,('function','instancemeethod')):
            return name
        return default

    def Function(self,name,default=None):
        return self.Func(name,default=default)

    def FuncName(self,default=False,detail=False):
        #return traceback.extract_stack(None, 2)[0][2]
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
            return default

    def FunctionName(self,default=False,detail=False):
        return self.FuncName(default=default,detail=detail)

    def ParentName(self):
        return traceback.extract_stack(None, 3)[0][2]

    def Class(self,default=None):
        if Type(self.src,'instance'):
            return self.src.__class__
        elif Type(self.src,'classobj'):
            return self.src
        else:
            return default

    def ClassName(self,default=None):
        if Type(self.src,'instance'):
            return self.src.__class__.__name__
        elif Type(self.src,'classobj'):
            return self.src.__name__
        else:
            return default

    def DirName(self,default=None):
        if Type(self.src,str):
            dirname=os.path.dirname(self.src)
            if dirname == '': return '.'
            return dirname
        return default

    def DirectoryName(self,default=None):
        return self.DirName(default=default)

    def Pwd(self):
        #return os.path.abspath(__file__)
        return os.path.dirname(os.path.realpath(__file__))

    def Basename(self):
        if Type(self.src,str): return os.path.basename(self.src)
        return __file__

def Get(*inps,**opts):
    key=None
    if len(inps) >= 2:
        src=inps[0]
        key=inps[1:]
    elif len(inps) == 1:
        src=inps[0]
        key=opts.get('key',None)
        if isinstance(key,list):
            key=tuple(key)
        elif key is not None:
            key=(key,)
        else: #None key
            return GET(src).Value(**opts)
    return GET(src).Value(*key,**opts)
