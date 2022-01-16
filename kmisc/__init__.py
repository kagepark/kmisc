#!/bin/python
# -*- coding: utf-8 -*-
# Kage personal stuff
#
from __future__ import print_function
import os
import re
import sys
import ast
import ssl
import stat
import time
import uuid
import zlib
import smtplib
import tarfile
import zipfile
import random
import struct
import string
import fnmatch
import pickle
import tarfile
import zipfile
import pickle
import random
import inspect
import base64
import hashlib
import importlib
import subprocess
import traceback
import fcntl,socket,struct
import json as _json
import email.utils
import xml.etree.ElementTree as ET
from sys import modules
from sys import path as mod_path
from sys import version_info
from pprint import pprint
from threading import Thread
from datetime import datetime
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from multiprocessing import Process, Queue
from distutils.spawn import find_executable
from distutils.version import LooseVersion
from kmisc.Import import *
Import('from lz4 import frame')
Import('import bz2')
Import('import magic')

from http.cookies import Morsel # This module for requests when you use build by pyinstaller command
Import('import requests')

url_group = re.compile('^(https|http|ftp)://([^/\r\n]+)(/[^\r\n]*)?')
#log_file=None
log_intro=3
log_new_line='\n'
pipe_file=None

cdrom_ko=['sr_mod','cdrom','libata','ata_piix','ata_generic','usb-storage']

def Global():
    return dict(inspect.getmembers(inspect.stack()[-1][0]))["f_globals"]

def OutFormat(data,out=None,strip=False,peel=False):
    def __peel__(data,peel):
        if peel:
            if isinstance(data,(list,tuple)) and len(data)==1:
                return data[0]
        return data

    def __strip__(data,strip):
        if strip:
            if isinstance(data,(str,bytes)) and len(data) > 0:
                return data.strip()
        return data

    if out in [tuple,'tuple']:
        if not isinstance(data,list):
            return tuple(data)
        elif not isinstance(data,tuple):
            return (data,)
        return data
    elif out in [list,'list']:
        if not isinstance(data,tuple):
            return list(data)
        elif not isinstance(data,list):
            return [data]
        return data
    elif out in ['raw',None]:
        if isinstance(data,dict) and len(data) == 1:
            return __strip__(__peel__(data.values(),True),strip)
        return __strip__(__peel__(data,True),strip)
       # if isinstance(data,(list,tuple)) and len(data) == 1:
       #     return data[0]
       # elif isinstance(data,dict) and len(data) == 1:
       #     return data.values()[0]
    elif out in ['str',str]:
        return '''{}'''.format(__strip__(__peel__(data,peel),strip))
    elif out in ['int',int]:
        try:
            return int(__strip__(__peel__(data,peel),strip))
        except:
            pass
    return __strip__(__peel__(data,peel),strip)

def Abs(*inps,**opts):
    default=opts.get('default',None)
    out=opts.get('out','auto')
    obj=opts.get('obj',None)
    err=opts.get('err',True)
    def int_idx(idx,nobj,default,err,out='auto'):
        if idx < 0:
            if abs(idx) <= nobj:
                if out in ['list',list]:
                    return [nobj+idx]
                elif out in ['tuple',tuple]:
                    return (nobj+idx,)
                return nobj+idx
            elif err not in [True,'err','True']:
                return 0
        else:
            if nobj > idx:
                if out in ['list',list]:
                    return [idx]
                elif out in ['tuple',tuple]:
                    return (idx,)
                return idx
            elif err not in [True,'err','True']:
                return nobj-1
        return default
    if len(inps) > 0:
        ss=None
        ee=None
        rt=[]
        if obj is None:
            for i in inps:
                if isinstance(i,int):
                    rt.append(abs(i))
                elif err in [True,'err','True']:
                    rt.append(default)
#        elif isinstance(obj,dict):
#            keys=list(obj)
#            for idx in inps:
#                if isinstance(idx,int):
#                    int_index=int_idx(idx,len(keys),default,err)
#                    if int_index != default: rt.append(keys[int_index])
#                elif isinstance(idx,tuple) and len(idx) == 2:
#                    ss=Abs(idx[0],**opts)
#                    ee=Abs(idx[1],**opts)
#                    for i in range(ss,ee+1):
#                        rt.append(keys[i])
#                elif isinstance(idx,str):
#                    try:
#                        idx=int(idx)
#                        rt.append(int_idx(idx,len(keys),default,err))
#                    except:
#                        if len(idx.split(':')) == 2:
#                            ss,ee=tuple(idx.split(':'))
#                            if isinstance(ss,int) and isinstance(ee,int):
#                                for i in range(ss,ee+1):
#                                    rt.append(keys[i])
#                        elif len(idx.split('-')) == 2:
#                            ss,ee=tuple(idx.split('-'))
#                            if isinstance(ss,int) and isinstance(ee,int):
#                                for i in range(ss,ee+1):
#                                    rt.append(keys[i])
#                        elif len(idx.split('|')) > 1:
#                            rt=rt+idx.split('|')
        elif isinstance(obj,(list,tuple,str)):
            nobj=len(obj)
            for idx in inps:
                if isinstance(idx,list):
                    for ii in idx:
                        if isinstance(ii,int):
                            if nobj > ii:
                                rt.append(ii)
                            else:
                                rt.append(OutFormat(default))
                elif isinstance(idx,int):
                    rt.append(int_idx(idx,nobj,default,err))
                elif isinstance(idx,tuple) and len(idx) == 2:
                    ss=Abs(idx[0],**opts)
                    ee=Abs(idx[1],**opts)
                    rt=rt+list(range(ss,ee+1))
                elif isinstance(idx,str):
                    try:
                        idx=int(idx)
                        rt.append(int_idx(idx,nobj,default,err))
                    except:
                        if len(idx.split(':')) == 2:
                            ss,ee=tuple(idx.split(':'))
                            ss=Abs(ss,**opts)
                            ee=Abs(ee,**opts)
                            if isinstance(ss,int) and isinstance(ee,int):
                                rt=rt+list(range(ss,ee+1))
                        elif len(idx.split('-')) == 2:
                            ss,ee=tuple(idx.split('-'))
                            ss=Abs(ss,**opts)
                            ee=Abs(ee,**opts)
                            if isinstance(ss,int) and isinstance(ee,int):
                                rt=rt+list(range(ss,ee+1))
                        elif len(idx.split('|')) > 1:
                            for i in idx.split('|'):
                                ss=Abs(i,obj=obj,out='raw')
                                if isinstance(ss,int):
                                    rt.append(ss)
                        else:
                            rt.append(OutFormat(default))
        return OutFormat(rt,out=out)
    elif obj:
        if isinstance(obj,(list,tuple,str)):
            return len(obj)
        elif isinstance(obj,dict):
            return list(obj.keys())
    return default

def ObjName(obj,default=None):
    #if isinstance(obj,str) and obj:
    try:
        if os.path.isfile(obj):
            aa=magic.from_buffer(open(obj,'rb').read(2048))
            if aa: return aa.split()[0].lower()
            try:
                with open(obj,'rb') as f: # Pickle Type
                    pickle.load(f)
                    return 'pickle'
            except:
                pass
        return 'str'
    #else:
    except:
        obj_dir=dir(obj)
        obj_name=type(obj).__name__
        if obj_name in ['function']: return obj_name
        if '__dict__' in obj_dir:
            if obj_name == 'type': return 'classobj'
            return 'instance'
#        elif obj_name == 'type':
#            return obj.__name__
        return obj_name.lower() # Object Name
    return default

#def TypeFixer(name,default=None):
def TypeFixer(obj,default='unknown'):
    if obj == default: return default
    if isinstance(obj,str): 
        name=obj.lower()
    else: 
        name=ObjName(obj).lower()
    # Fix short word to correct name
    if name in ['none']: return 'nonetype'
    if name in ['byte']: return 'bytes'
    if name in ['obj']: return 'object'
    if name in ['func','unboundmethod']: return 'function'
    if name in ['class']: return 'classobj'
    if name in ['yield']: return 'generator'
    if name in ['builtinfunction','builtinmethod','builtin_function_or_method']: return 'builtin_function_or_method'
    # function: function and instance's function in Python3
    # method:  class's function in Python3
    # instancemethod: instance's and class's function in Python2
    if name in ['method','classfunction','instancemethod','unboundmethod']: return 'method' # function in the class
    # it changed name between python versions, so return both name for this name
    if name in ['dictproxy','mappingproxy']: return ['dictproxy','mappingproxy'] # function in the class
    # Fix python version for long
    if name in ['long']:
        if sys.version_info[0] < 3: return name
        return 'int'
    if not isinstance(obj,str) and name == 'type':
        return obj.__name__.lower()
    # return original name
    return name

def Type(*inp,**opts):
    '''
       instance: <class name>()
       classobj : <class name>
       function : <func name>
       return value: <func name>()
       method   : <class name>().<func name>
    '''
    inpn=len(inp)
    default=opts.get('default','unknown')
    if inpn == 0: return default
    obj=inp[0]
    if inpn == 1: return TypeFixer(obj,default=default)
    chk_type=[]
    for name in inp[1:]:
        if not isinstance(name,(tuple,list)): name=[name]
        for ii in name:
            a=TypeFixer(TypeFixer(ii,default=default),default=default)
            if a == default: continue
            if isinstance(a,list): 
                chk_type=chk_type+a
            elif a not in chk_type:
                chk_type.append(a)
    if chk_type: 
        obj_type=ObjName(obj)
#        print('    ::',obj_type,'  in  ',chk_type)
        if obj_type == default: return default
        if obj_type == 'instance':
            if 'int' in chk_type: 
                if isinstance(obj,int): return True
            elif 'dict' in chk_type:
                if isinstance(obj,dict): return True
            elif 'list' in chk_type:
                if isinstance(obj,list): return True
            elif 'tuple' in chk_type:
                if isinstance(obj,tuple): return True
            elif 'float' in chk_type:
                if isinstance(obj,float): return True
        if obj_type in chk_type: return True
    return False

def Copy(src):
    if isinstance(src,(list,tuple)): return src.root[:]
    if isinstance(src,dict): return src.copy()
    if isinstance(src,str): return '{}'.format(src)
    if isinstance(src,int): return int('{}'.format(src))
    if isinstance(src,float): return float('{}'.format(src))
    if PyVer(2):
        if isinstance(src,long): return long('{}'.format(src))

def Join(*inps,symbol='_-_',byte=None):
    if len(inps) == 1 and isinstance(inps[0],(list,tuple)):
        src=inps[0]
    elif len(inps) == 2 and isinstance(inps[0],(list,tuple)) and symbol=='_-_':
        src=inps[0]
        symbol=inps[1]
    else:
        src=inps
    if symbol=='_-_': symbol=''
    rt=''
    if isinstance(byte,bool):
        if byte:
            rt=b''
            symbol=BYTES().From(symbol)
        else:
            symbol=BYTES(symbol).Str()
    else:
        byte=False
        if src and isinstance(src,(list,tuple)):
            if IS(src[0]).Bytes():
                rt=b''
                byte=True
                symbol=BYTES().From(symbol)
    for i in src:
        if not isinstance(i,(str,bytes)):
            i='{}'.format(i)
        if byte:
            i=BYTES().From(i)
        else:
            i=BYTES(i).Str()
        if rt:
            rt=rt+symbol+i
        else:
            rt=i
    return rt

def FixIndex(src,idx,default=0):
    if isinstance(src,(list,tuple,str,dict)) and isinstance(idx,int):
        if idx < 0:
            if len(src) > abs(idx):
                idx=len(src)-abs(idx)
            else:
                idx=0
        else:
            if len(src) <= idx: idx=len(src)-1
        return idx
    return default

def Next(src,step=0,out=None,default='org'):
    if isinstance(src,(list,tuple,dict)):
        step=FixIndex(src,step)
        iterator=iter(src)
        for i in range(-1,step):
            rt=next(iterator)
        return OutFormat(rt,out=out)
    elif isinstance(src,str):
        step=FixIndex(src,step)
        if len(src) == 0:
            return ''
        elif len(src) >= 0 or len(src) <= step:
            return OutFormat(src[step],out=out)
    if default == 'org': return src
    OutFormat(default,out=out)

def Delete(*inps,**opts):
    if len(inps) >= 2:
        obj=inps[0]
        keys=inps[1:]
    elif len(inps) == 1:
        obj=inps[0]
        keys=opts.get('key',None)
        if isinstance(keys,list):
            keys=tuple(keys)
        elif keys is not None:
            keys=(keys,)
    default=opts.get('default',None)
    _type=opts.get('type','index')

    if isinstance(obj,(list,tuple)):
        nobj=len(obj)
        rt=[]
        if _type == 'index':
            nkeys=Abs(*tuple(keys),obj=obj,out=list)
            for i in range(0,len(obj)):
                if i not in nkeys:
                    rt.append(obj[i])
        else:
            for i in obj:
                if i not in keys:
                    rt.append(i)
        return rt
    elif isinstance(obj,dict):
        if isinstance(keys,(list,tuple,dict)):
            for key in keys:
                obj.pop(key,default)
        else:
            obj.pop(keys,default)
        return obj
    elif isinstance(obj,str):
        nkeys=[]
        for i in keys:
            if isinstance(i,(tuple,str,int)):
                tt=Abs(i,obj=obj,out=list)
                if tt:
                    nkeys=nkeys+tt
        rt=''
        for i in range(0,len(obj)):
            if i in nkeys:
                continue
            rt=rt+obj[i]
        return rt
    return default

class COLOR:
    def __init__(self,**opts):
       self.color_db=opts.get('color',{'blue': 34, 'grey': 30, 'yellow': 33, 'green': 32, 'cyan': 36, 'magenta': 35, 'white': 37, 'red': 31})
       self.bg_color_db=opts.get('bg',{'cyan': 46, 'white': 47, 'grey': 40, 'yellow': 43, 'blue': 44, 'magenta': 45, 'red': 41, 'green': 42})
       self.attr_db=opts.get('attr',{'reverse': 7, 'blink': 5,'concealed': 8, 'underline': 4, 'bold': 1})

    def Color_code(self,name,default=None):
       return self.color_db.get(name,default)

    def Background_code(self,name,default=None):
       return self.color_db.get(name,default)

    def Attr_code(self,name,default=None):
       return self.color_db.get(name,default)

    def Get(self,color,mode='color',default=None):
       color_code=None
       if mode == 'color':
           color_code=self.Color_code(color,default=default)
       elif mode in ['background','bg']:
           color_code=self.Background_code(color,default=default)
       elif mode in ['attr','attribute']:
           color_code=self.Attr_code(color,default=default)
       return color_code

    def String(self,msg,color,bg=False,attr=False,mode='shell'):
       if mode in ['html','HTML']:
           if bg:
               return '''<p style="background-color: {}">{}</p>'''.format(format(color,msg))
           else:
               return '''<font color={}>{}</font>'''.format(color,msg)
       else:
           if bg:
               color_code=self.Get(color,mode='bg',default=None)
           elif attr:
               color_code=self.Get(color,mode='attr',default=None)
           else:
               color_code=self.Get(color,default=None)
           if color_code is None:
               return msg
           if os.getenv('ANSI_COLORS_DISABLED') is None:
               reset='''\033[0m'''
               fmt_msg='''\033[%dm%s'''
               msg=fmt_msg % (color_code,msg)
               return msg+reset

class FIND:
    def __init__(self,string,out='index',word=False):
        string=string.replace('*','.+').replace('?','.')
        if word:
            self.find_re=re.compile(r'\b({0})\b'.format(string),flags=re.IGNORECASE)
        else:
            self.find_re=re.compile(string,flags=re.IGNORECASE)
        self.out=out

    def From(self,data,symbol='\n'):
        rt=[]

        def Search(data,key,rt):
            found=self.find_re.findall(data)
            if found:
                if self.out in ['found']:
                    rt=rt+found
                elif self.out in ['index','idx','key']:
                    rt.append(key)
                elif self.out in ['all','*']:
                    rt.append((key,data))
                else:
                    rt.append(data)
            return rt

        if Type(data,str):
            data=data.split(symbol)
        if Type(data,list,tuple):
            for i in range(0,len(data)):
                if Type(data[i],(list,tuple,dict)):
                    sub=self.From(data[i],symbol=symbol)
                    if sub:
                        if self.out in ['key','index','idx']:
                            for z in sub:
                                rt.append('{}/{}'.format(i,z))
                        else:
                            rt=rt+sub
                elif Type(data[i],str):
                    rt=Search(data[i],i,rt)
        elif Type(data,dict):
            for i in data:
                if Type(data[i],(list,tuple,dict)):
                    sub=self.From(data[i],symbol=symbol)
                    if sub:
                        if self.out in ['key','index','idx']:
                            for z in sub:
                                rt.append('{}/{}'.format(i,z))
                        else:
                            rt=rt+sub
                elif Type(data[i],str):
                    rt=Search(data[i],i,rt)
        else:
             return 'Unknown format'
        return rt

    def Find(self,src,find,prs=None,sym='\n',pattern=True,default=[],out=None,findall=False,word=False,mode='value'):
        #if Type(src,'instance','classobj'):
        # if src is instance or classobj then search in description and made function name at key
        if isinstance(src,(list,tuple)):
            rt=[]
            for i in range(0,len(self.root)):
                for j in inps:
                    j=j.replace('*','.+').replace('?','.')
                    mm=re.compile(j)
                    if bool(re.match(mm,self.root[i])):
                        if mode in ['index','idx']:
                            rt.append(i)
                        else:
                            rt.append(src[i])
            if len(rt):
                return rt
        elif isinstance(src,dict):
            path=[]
            for key in src:
                if mode in ['key','*','all']: # find in key only
                    if find == key:
                        path.append(key)
                found=src.get(key,None)
                if isinstance(found,dict):
                    if dep in found:
                         if mode in ['value','*','all'] and (find == found[dep] or (type(found[dep]) in [DICT,dict,list,tuple] and find in found[dep]) or (type(find) is str and type(found[dep]) is str and find in found[dep])): # find in 'find' only
                              # Value find
                              path.append(key)
                         elif isinstance(found[dep], dict): # recursing
                              path=path+Find(found[dep],find,proper=proper,mode=mode)
                    else:
                         if mode in ['value','*','all'] and find == found or (type(found) in [list,tuple] and find in found) or (type(find) is str and type(found) is str and find in found):
                             path.append(key)
                         else:
                             for kk in Find(src[key],find,proper=proper,mode=mode): # recursing
                                 path.append(key+'/'+kk)
                else:
                    if mode in ['value','*','all'] and find == found or (type(found) in [list,tuple] and find in found) or (type(find) is str and type(found) is str and find in found):
                        path.append(key)
            return path
        elif isinstance(src,str):
            if word:
                find_re=re.compile(r'\b({0})\b'.format(find),flags=re.IGNORECASE)
            else:
                find_re=re.compile(find,flags=re.IGNORECASE)
            if findall:
                match=find_re.findall(src)
                if match: return OutFormat(match,out=out)
            else:
                match=find_re.search(src)
                if match: return OutFormat([match.group()],out=out)
        return OutFormat(default,out=out)

class DIFF:
    def __init__(self):
        pass

    def Data(self,a,sym,b,ignore=None,default=None):
        if isinstance(ignore,(list,tuple)):
            if a in ignore or b in ignore:
                return default
        elif ignore is not None:
            if eval('{} == {}'.format(a,ignore)) or eval('{} == {}'.format(b,ignore)):
                return default
        if sym == '==':
            try:
                return eval('{} == {}'.format(a,b))
            except:
                return default
        elif isinstance(a,int) and isinstance(b,int):
            try:
                return eval('{} {} {}'.format(a,sym,b))
            except:
                return default
        elif isinstance(a,str) and isinstance(b,str) and a.isdigit() and b.isdigit():
            try:
                return eval('{} {} {}'.format(a,sym,b))
            except:
                return default
        return default

    def Code(self):
        pass

    def File(self):
        pass


class LIST(list):
    def __init__(self,*inps):
        if len(inps) == 1 and isinstance(inps[0],(list,tuple)):
            self.root=list(inps[0])
        else:
            self.root=list(inps)

#    def __new__(cls,*inps):
#        if len(inps) == 1 and isinstance(inps[0],(list,tuple)):
#            return list(inps[0])
#        else:
#            return list(inps)

    # reply self.root back to the Class's output a=List(['a']), return the data to a
    def __repr__(self):
        return repr(self.root)

    def Convert(self,src,path=False,default=False,symbol=':white_space:',**opts):
        if isinstance(src,str) and src:
            if path and isinstance(symbol,str):
                if symbol == ':white_space:':
                    symbol='/'
                start=0
                if src[0] == symbol:
                    start=1
                if src[-1] == symbol:
                    return src.split(symbol)[start:-1]
                return src.split(symbol)[start:]
            else:
                if symbol == ':white_space:':
                    return src.strip().split()
                elif isinstance(symbol,str):
                    return src.split(symbol)
                elif isinstance(symbol,(tuple,list)):
                    #regexPattern = '|'.join(map(re.escape,tuple(symbol)))
                    regexPattern = Join(map(re.escape,tuple(symbol)),symbol='|')
                    return re.split(regexPattern,src)
                return default
        elif isinstance(src,(list,tuple)):
            return list(src)
        else:
            return [src]
 
    def Append(self,*inps,**opts):
        uniq=opts.get('uniq',False)
        symbol=opts.get('symbol',':white_space:')
        path=opts.get('path',False)
        default=opts.get('default',False)
        for pp in inps:
            for rp in self.Convert(pp,symbol=symbol,path=path,default=default):
                if rp == default: continue
                if uniq and rp in self.root: continue
                if path:
                    if rp == '.': continue
                    if rp == '..' and len(self.root):
                        del self.root[-1]
                        continue
                self.root.append(rp)
        return self.root

    def append(self,inp):
        self.root.append(inp)

    def Uniq(self,*inps,**opts):
        symbol=opts.get('symbol',':white_space:')
        path=opts.get('path',False)
        default=opts.get('default',False)
        for pp in self.root + list(inps):
            for rp in self.Convert(pp,symbol=symbol,path=path,default=default):
                if rp == default: continue
                if rp in rt: continue
                if path:
                    if rp == '.': continue
                    if rp == '..' and len(rt):
                        del self.root[-1]
                        continue
                self.root.append(rp)
        return self.root

    def Delete(self,*inps,**opts):
        find=opts.get('find','index')
        default=opts.get('default',False)
        if find in ['data','element']:
            for i in inps:
                if i in self.root:
                    self.root.remove(i)
        else:
            if len(inps) == 1 and isinstance(inps[0],int):
                if len(self.root) > inps[0]:
                    del self.root[inps[0]]
            else:
                rt=[]
                del_list=Abs(*inps,obj=self.root,out=list)
                for i in range(0,len(self.root)):
                    if i in del_list: continue
                    rt.append(self.root[i])
                self.root=rt

    def Get(self,*inps,**opts):
        if not inps: return self.root
        find=opts.get('find','data')
        default=opts.get('default',None)
        out=opts.get('out',list)
        err=opts.get('err',False)
        if len(self.root) == 0 and err:
            return default
        rt=[]
        if find in ['index','idx']:
            for i in inps:
                if i in self.root:
                    rt.append(self.root.index(i))
                elif err is True:
                    rt.append(default)
        else:
            for i in Abs(*inps,obj=self.root,err=err,out=list,default=None):
                if isinstance(i,int) and self.root:
                    rt.append(self.root[i])
                elif err is True:
                    return default
        if rt:
            if out in [list,'list']:
                return rt
            elif out in [tuple,'tuple']:
                return tuple(rt)
            elif out in [None,'raw']:
                if len(rt) == 1:
                    return rt[0]
                return rt
        return default

    def Index(self,*inps):
        return self.Get(*inps,find='index')

    def Insert(self,*inps,**opts):
        start=opts.get('at',0)
        default=opts.get('default',False)
        err=opts.get('err',False)
        if isinstance(at,str):
            if at in ['start','first']: self.root=list(inps)+self.root
            if at in ['end','last']: self.root=self.root+list(inps)
        elif len(self.root) == 0:
            self.root=list(inps)
        elif isinstance(start,int) and len(self.root) > start:
            self.root=self.root[:start]+list(inps)+self.root[start:]
        else:
            if err:
                return default
            self.root=self.root+list(inps)

    def Update(self,*inps,**opts):
        at=opts.get('at',0)
        err=opts.get('err',False)
        default=opts.get('default',False)
        n=len(self.root)
        if n == 0:
            if err is True:
                return default
            else:
                self.root=list(inps)
        elif isinstance(at,int) and n > at:
            for i in range(0,len(inps)):
                if n > at+i:
                    self.root[at+i]=inps[i]
                elif err is True:
                    return default
                else:
                    self.root=self.root+list(inps)[i:]
                    break
        elif isinstance(at,(tuple,list)):
            if len(inps) == len(at):
                for i in range(0,len(at)):
                    if isinstance(at[i],int) and n > at[i]:
                        self.root[at[i]]=inps[i]
                    elif err is True:
                        return default
                    else:
                        self.root.append(inps[i])

    def Find(self,*inps,**opts):
        find=opts.get('find','index')
        default=opts.get('default',[])
        rt=[]
        for i in range(0,len(self.root)):
            for j in inps:
                j=j.replace('*','.+').replace('?','.')
                mm=re.compile(j)
                if bool(re.match(mm,self.root[i])):
                    if find in ['index','idx']:
                        rt.append(i)
                    else:
                        rt.append(self.root[i])
        if len(rt):
            return rt
        return default

    def Copy(self):
        return self.root[:]
    def copy(self):
        return self.root[:]

    def Tuple(self):
        return tuple(self.root)

    def Move2first(self,find):
        if isinstance(find,(list,tuple)):
            self.Delete(*find,find='data')
            self.root=list(find)+self.root
        else:
            self.Delete(*(find,),find='data')
            self.root=[find]+self.root
        return self.root

    def Move2end(self,find):
        if isinstance(find,(list,tuple)):
            self.Delete(*find,find='data')
            self.root=self.root+list(find)
        else:
            self.Delete(*(find,),find='data')
            self.root=self.root+[find]
        return self.root

    def Sort(self,reverse=False,func=None,order=None,field=None):
        if order in [int,'int','digit','number']:
            def _cint_(e):
                try:
                    if isinstance(field,int):
                        if isinstance(e,(list,tuple)) and len(e) > field:
                            return int(e[field])
                        else:
                            return 9999999
                    return int(e)
                except:
                    return e
            return self.root.sort(reverse=reverse,key=_cint_)
        elif order in [str,'str']:
            def _cint_(e):
                if isinstance(field,int):
                    if isinstance(e,(list,tuple)) and len(e) > field:
                        return '''{}'''.format(e[field])
                    else:
                        return 'zzzzzzzzz'
                return '''{}'''.format(e)
            return self.root.sort(reverse=reverse,key=_cint_)
        else:
            if isinstance(field,int):
                def _cint_(e):
                    if isinstance(e,(list,tuple)) and len(e) > field:
                        return e[field]
                return self.root.sort(reverse=reverse,key=_cint_)
            else:
                return self.root.sort(reverse=reverse,key=func)

    def Str(self,sym=' ',default=None):
        if isinstance(self.src,(tuple,list)):
            rt_str=''
            for ii in self.src:
                if rt_str:
                    rt_str='''{}{}{}'''.format(rt_str,sym,ii)
                else:
                    rt_str='''{}'''.format(ii)
            self.src=rt_str
            return rt_str
        return default

class STR(str):
    def __init__(self,src,byte=None):
        if isinstance(byte,bool):
            if byte:
                self.src=BYTES().From(src)
            else:
                self.src=BYTES(src).Str()
        else:
            self.src=src

    def Rand(self,length=8,strs=None,mode='*'):
        return Random(length=length,strs=strs,mode=mode)

    def Cut(self,head_len=None,body_len=None,new_line='\n',out=str):
        if not isinstance(self.src,str):
           self.src='''{}'''.format(self.src)

        source=self.src.split(new_line)

        if len(source) == 1 and not head_len or head_len >= len(self.src):
           return [self.src]

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
        #if rt and out in ['str',str]: return new_line.join(rt)
        if rt and out in ['str',str]: return Join(rt,symbol=new_line)
        return rt

    def Space(num=1,fill=' ',mode='space'):
        if mode.lower() =='tap':
            fill='\t'
        tap=''
        for i in range(0,num):
            tap=tap+fill
        return tap

    def Tap(self,space='',sym='\n',default=None,NFLT=False,out=str):
        # No First Line Tap (NFLT)
        if isinstance(space,int):
            space=self.Space(space)
        if isinstance(self.src,str):
            self.src=self.src.split(sym)
        if isinstance(self.src,(list,tuple)):
            rt=[]
            if NFLT:
                rt.append(self.src.pop(0))
            for ii in self.src:
                rt.append('%s%s'%(space,ii))
            #if rt and out in [str,'str']: return sym.join(rt)
            if rt and out in [str,'str']: return Join(rt,symbol=sym)
            return rt
        return default

    def Wrap(self,src=None,space='',space_mode='space',sym='\n',default=None,NFLT=False,out=str):
        if src is None: src=self.src
        if not isinstance(src,(str,list,tuple)): return src
        if isinstance(src,str): src=src.split(sym)
        if isinstance(space,int): space=self.Space(space,mode=space_mode)
        rt=[]
        # No First Line Tap (NFLT)
        if NFLT: rt.append('%s'%(src.pop(0)))
        for ii in src:
            rt.append('%s%s'%(space,ii))
        #if rt and out in [str,'str']: return sym.join(rt)
        if rt and out in [str,'str']: return Join(rt,symbol=sym)
        return rt

    def Reduce(self,start=0,end=None,sym=None,default=None):
        if isinstance(self.src,str):
            if sym:
                arr=self.src.split(sym)
                if isinstance(end,int):
                    #return sym.join(arr[start:end])
                    return Join(arr[start:end],symbol=sym)
                else:
                    #return sym.join(arr[start])
                    return Join(arr[start],symbol=sym)
            else:
                if isinstance(end,int):
                    return self.src[start:end]
                else:
                    return self.src[start:]
        return default

    def Find(self,find,src=None,prs=None,sym='\n',pattern=True,default=[],out=None,findall=False,word=False):
        if src is None: src=self.src
        return FIND().Find(src,find,prs=prs,sym=sym,pattern=pattern,default=default,out=out,findall=findall,word=word,mode='value')

    def Index(self,find,start=None,end=None,sym='\n',default=[],word=False,pattern=False,findall=False,out=None):
        if not isinstance(self.src,str): return default
        rt=[]
        source=self.src.split(sym)
        for row in range(0,len(source)):
            for ff in self.Find(find,src=source[row],pattern=pattern,word=word,findall=findall,default=[],out=list):
                if findall:
                    rt=rt+[(row,[m.start() for m in re.finditer(ff,source[row])])]
                else:
                    idx=source[row].index(ff,start,end)
                    if idx >= 0:
                        rt.append((row,idx))
        if rt:
            if out in ['tuple',tuple]: return tuple(rt)
            if out not in ['list',list] and len(rt) == 1 and rt[0][0] == 0: 
                if len(rt[0][1]) == 1:return rt[0][1][0]
                return rt[0][1]
            return rt
        return default

    def Replace(self,replace_what,replace_to,default=None):
        if isinstance(self.src,str):
            if replace_what[-1] == '$' or replace_what[0] == '^':
                return re.sub(replace_what, replace_to, self.src)
            else:
                head, _sep, tail = self.src.rpartition(replace_what)
                return head + replace_to + tail
        return default

    def Split(self,sym,src=None,default='org'):
        if not isinstance(sym,str):
            if default in ['org',{'org'}]:
                return src
            return default
        if src is None: src=self.src
        if isinstance(src,str):
            if isinstance(sym,bytes): sym=CONVERT(sym).Str()
        elif isinstance(src,bytes):
            if isinstance(sym,str): sym=BYTES().From(sym,default={'org'})
        else:
            if default in ['org',{'org'}]:
                return src
            return default
        if len(sym) > 2 and '|' in sym:
            try:
                sym_a=sym.split('|')
                for i in ['.','+','*']:
                    try:
                        x=sym_a.index(i)
                        sym_a[x]='\{}'.format(sym_a[x])
                    except:
                        continue
                #return re.split('|'.join(sym_a),src) # splited by '|' or expression
                return re.split(Join(sym_a,symbol='|'),src) # splited by '|' or expression
            except:
                pass
        try:
            return src.split(sym)
        except:
            if default in ['org',{'org'}]:
                return src
            return default

    def RemoveNewline(self,src=None,mode='edge',newline='\n',byte=None):
        if src is None:
            src=self.src
        if isinstance(byte,bool):
            if byte:
                src=BYTES().From(src)
            else:
                src=BYTES(src).Str()
        src_a=self.Split(newline,src=src,default=False)
        if src_a is False:
            return src
        #if IS(src).Bytes():
        #    newline=BYTES().From(newline)
        if mode in ['edge','both']:
            if not src_a[0].strip() and not src_a[-1].strip():
                return Join(src_a[1:-1],symbol=newline)
#                return newline.join(src_a[1:-1])
            elif not src_a[0].strip():
                return Join(src_a[1:],symbol=newline)
#                return newline.join(src_a[1:])
            elif not src_a[-1].strip():
                return Join(src_a[:-1],symbol=newline)
#                return newline.join(src_a[:-1])
        elif mode in ['first','start',0]:
            if not src_a[0].strip():
                return Join(src_a[1:],symbol=newline)
#                return newline.join(src_a[1:])
        elif mode in ['end','last',-1]:
            if not src_a[-1].strip():
                return Join(src_a[:-1],symbol=newline)
#                return newline.join(src_a[:-1])
        elif mode in ['*','all','everything']:
            return Join(src_a,symbol='')
#            return ''.join(src_a)
        return src

#    def Split(self,sym=None):
#        if isinstance(self.src,str):
#            try:
#                return re.split(sym,self.src) # splited by '|' or expression
#            except:
#                return self.src.split(sym)

class TIME:
    def __init__(self):
        self.init_sec=int(datetime.now().strftime('%s'))

    def Reset(self):
        self.init_sec=int(datetime.now().strftime('%s'))

    def Sleep(self,try_wait=None,default=1):
        if isinstance(try_wait,(int,str)): try_wait=(try_wait,)
        if isinstance(try_wait,(list,tuple)) and len(try_wait):
            if len(try_wait) == 2:
                try:
                    time.sleep(random.randint(int(try_wait[0]),int(try_wait[1])))
                except:
                    pass
            else:
                try:
                    time.sleep(int(try_wait[0]))
                except:
                    pass
        else:
            time.sleep(default)

    def Rand(self,try_wait=None,default=1):
        if isinstance(try_wait,(int,str)): try_wait=(try_wait,)
        if isinstance(try_wait,(list,tuple)) and len(try_wait):
            if len(try_wait) == 2:
                try:
                    return random.randint(int(try_wait[0]),int(try_wait[1]))
                except:
                    pass
            else:
                try:
                    return int(try_wait[0])
                except:
                    pass
        return default

    def Int(self):
        return int(datetime.now().strftime('%s'))

    def Now(self,mode=None):
        if mode in [int,'int','INT','sec']:return self.Int()
        return time.now()

    def Out(self,timeout_sec,default=(24*3600)):
        try:
            timeout_sec=int(timeout_sec)
        except:
            timeout_sec=default
        if timeout_sec == 0:
            return False
        if self.Int() - self.init_sec >  timeout_sec:
            return True
        return False


    def Format(self,time=0,tformat='%s',read_format='%S'):
        if time in [0,'0',None]:
            return datetime.now().strftime(tformat)
        elif isinstance(time,int) or (isinstance(time,str) and time.isdigit()):
            #if type(time) is int or (type(time) is str and time.isdigit()):
            if read_format == '%S':
                return datetime.fromtimestamp(int(time)).strftime(tformat)
            else:
                return datetime.strptime(str(time),read_format).strftime(tformat)

    def Init(self):
        return self.init_sec

    def Time(self):
        return time.time()

    def Datetime(self):
        return datetime()

class SHELL:
    def __init__(self):
        pass

    def Pprog(self,stop,progress_pre_new_line=False,progress_post_new_line=False,log=None,progress_interval=5):
        TIME().Sleep(progress_interval)
        if stop():
            return
        if progress_pre_new_line:
            if log:
                log('\n',direct=True,log_level=1)
            else:
                sys.stdout.write('\n')
                sys.stdout.flush()
        post_chk=False
        while True:
            if stop():
                break
            if log:
                log('>',direct=True,log_level=1)
            else:
                sys.stdout.write('>')
                sys.stdout.flush()
            post_chk=True
            TIME().Sleep(progress_interval)
        if post_chk and progress_post_new_line:
            if log:
                log('\n',direct=True,log_level=1)
            else:
                sys.stdout.write('\n')
                sys.stdout.flush()

    def Run(self,cmd,timeout=None,ansi=True,path=None,progress=False,progress_pre_new_line=False,progress_post_new_line=False,log=None,progress_interval=5,cd=False):
        start_time=TIME()
        if not isinstance(cmd,str):
            return -1,'wrong command information :{0}'.format(cmd),'',start_time.Init(),start_time.Init(),start_time.Now(int),cmd,path
        Popen=subprocess.Popen
        PIPE=subprocess.PIPE
        cmd_env=''
        cmd_a=cmd.split()
        cmd_file=cmd_a[0]
        if cmd_a[0] == 'sudo': cmd_file=cmd_a[1]
        if path and isinstance(path,str) and os.path.isdir(path):
            if cd or os.path.isfile(os.path.join(path,cmd_file)):
                cmd_env='''export PATH=%s:${PATH}; '''%(path)
                if os.path.join(path,cmd_file):
                    cmd_env=cmd_env+'''cd %s && '''%(path)
        elif cmd_file[0] != '/' and cmd_file == os.path.basename(cmd_file) and os.path.isfile(cmd_file):
            cmd_env='./'
        p = Popen(cmd_env+cmd , shell=True, stdout=PIPE, stderr=PIPE)
        out=None
        err=None
        if progress:
            stop_threads=False
            ppth=Thread(target=self.Pprog,args=(lambda:stop_threads,progress_pre_new_line,progress_post_new_line,log,progress_interval))
            ppth.start()
        if isinstance(timeout,(int,str)):
            try:
                timeout=int(timeout)
            except:
                timeout=600
            if timeout < 3:
                timeout=3
        if PyVer(3):
            try:
                out, err = p.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                p.kill()
                if progress:
                    stop_threads=True
                    ppth.join()
                return -1, 'Kill process after timeout ({0} sec)'.format(timeout), 'Error: Kill process after Timeout {0}'.format(timeout),start_time.Init(),start_time.Now(int),cmd,path
        else:
            if isinstance(timeout,int):
                countdown=int('{}'.format(timeout))
                while p.poll() is None and countdown > 0:
                    TIME().Sleep(2)
                    countdown -= 2
                if countdown < 1:
                    p.kill()
                    if progress:
                        stop_threads=True
                        ppth.join()
                    return -1, 'Kill process after timeout ({0} sec)'.format(timeout), 'Error: Kill process after Timeout {0}'.format(timeout),start_time.Init(),start_time.Now(int),cmd,path
            out, err = p.communicate()

        if progress:
            stop_threads=True
            ppth.join()
        if PyVer(3):
            out=out.decode("ISO-8859-1")
            err=err.decode("ISO-8859-1")
        if ansi:
            return p.returncode, out.rstrip(), err.rstrip(),start_time.Init(),start_time.Now(int),cmd,path
        else:
            return p.returncode, ansi_escape.sub('',out).rstrip(), ansi_escape.sub('',err).rstrip(),start_time.Init(),start_time.Now(int),cmd,path

class BYTES:
    def __init__(self,src=None,encode='utf-8',default='org'):
        '''encode: utf-8(basic),latin1(enhance),windows-1252'''
        self.src=src
        self.encode=encode
        self.default=default

    def From(self,src,default='_._'):
        self.src=src
        if default=='_._': default=self.default
        return self.Bytes(encode=self.encode,default=default)

    def Bytes(self,encode='utf-8',default='org'):
        def _bytes_(src,encode,default='org'):
            try:
                if PyVer(3):
                    if isinstance(src,bytes):
                        return src
                    else:
                        return bytes(src,encode)
                return bytes(src) # if change to decode then network packet broken
            except:
                if default == 'org' or default =={'org'}:
                    return src
                return default

        tuple_data=False
        if isinstance(self.src,tuple):
            self.src=list(self.src)
            tuple_data=True
        if isinstance(self.src,list):
            for i in range(0,len(self.src)):
                self.src[i]=_bytes_(self.src[i],encode,default)
            if tuple_data:
                return tuple(self.src)
            else:
                return self.src
        else:
            return _bytes_(self.src,encode,default)

    def Str(self,encode='latin1',default='org'): # or windows-1252
        def _byte2str_(src,encode,default='org'):
            if PyVer(3) and isinstance(src,bytes):
                return src.decode(encode)
            #elif isinstance(src,unicode): # type(self.src).__name__ == 'unicode':
            elif Type(src,'unicode'):
                return src.encode(encode)
            #return '''{}'''.format(src)
            if default =='org' or default == {'org'}:
                return src
            return default

        tuple_data=False
        if isinstance(self.src,tuple):
            self.src=list(self.src)
            tuple_data=True
        if isinstance(self.src,list):
            for i in range(0,len(self.src)):
                self.src[i]=_byte2str_(self.src[i],encode,default)
            if tuple_data:
                return tuple(self.src)
            else:
                return self.src
        else:
            return _byte2str_(self.src,encode,default)

    def Str2Int(self,encode='utf-8'):
        if PyVer(3):
            if isinstance(self.src,bytes):
                return int(self.src.hex(),16)
            else:
                return int(self.Bytes(encode=encode).hex(),16)
        return int(self.src.encode('hex'),16)


class CONVERT:
    def __init__(self,src):
        self.src=src

    def Int(self,default=False):
        if isinstance(self.src,int): return self.src
        if Type(self.src,('float','long','str')):
            try:return int(self.src)
            except: pass
        if default == 'org' or default == {'org'}: return self.src
        return default

    def Str(self,default='org'):
        if isinstance(self.src,bytes):
            return BYTES(self.src).Str()
        else:
            try:
                return '{}'.format(self.src)
            except:
                if default == 'org' or default == {'org'}: return self.src
                return default

    def Ast(self,default=False,want_type=None):
        if isinstance(self.src,str):
            try:
                return ast.literal_eval(self.src)
            except:
                if default == 'org' or default == {'org'}:
                    return self.src
                return default
        if want_type:
            if isinstance(self.src,want_type):
                return self.src
        if default == 'org' or default == {'org'}:
            return self.src
        return default

    def Form(self,default=False):
        return self.Ast(default=default)

    def Json(self,src=None,default=None):
        if src is None: src=self.src
        try:
            return _json.loads(src)
        except:
            return default

    def Mac2Str(self,case='lower',default=False):
        if MAC(self.src).IsV4():
            if case == 'lower':
                self.src=self.src.strip().replace(':','').replace('-','').lower()
            else:
                self.src=self.src.strip().replace(':','').replace('-','').upper()
            return self.src
        return default

    def Str2Mac(self,case='lower',default=False,sym=':',chk=False):
        if isinstance(self.src, str):
            self.src=self.src.strip()
            if len(self.src) in [12,17]:
                self.src=self.src.replace(':','').replace('-','')
                if len(self.src) == 12:
                    #self.src=sym.join(self.src[i:i+2] for i in range(0,12,2))
                    self.src=Join([self.src[i:i+2] for i in range(0,12,2)],symbol=sym)
                if case == 'lower':
                    self.src=self.src.lower()
                else:
                    self.src=self.src.upper()
        if chk:
            if not MAC(self.src).IsV4():
                return  default
        return self.src

    def Size(self,unit='b:g',default=False):
        try:
            self.src=int(self.src)
        except:
            return default
        unit_a=unit.lower().split(':')
        if len(unit_a) != 2:
            return False
        def inc(sz):
            return '%.1f'%(float(sz) / 1024)
        def dec(sz):
            return int(sz) * 1024
        sunit=unit_a[0]
        eunit=unit_a[1]
        unit_m=['b','k','m','g','t','p']
        si=unit_m.index(sunit)
        ei=unit_m.index(eunit)
        h=ei-si
        for i in range(0,abs(h)):
            if h > 0:
                self.src=inc(self.src)
            else:
                self.src=dec(self.src)
        return self.src

    def Url(self):
        if isinstance(self.src,str):
            return self.src.replace('+','%2B').replace('?','%3F').replace('/','%2F').replace(':','%3A').replace('=','%3D').replace(' ','+')
        return self.src

class MAC:
    def __init__(self,src=None):
        self.src=src

    def IsV4(self,**opts):
        symbol=opts.get('symbol',':')
        default=opts.get('default',False)
        if isinstance(self.src,str):
            self.src=self.src.strip()
            # make sure the format
            if 12 <= len(self.src) <= 17:
                for i in [':','-']:
                    self.src=self.src.replace(i,'')
                #self.src=symbol.join(self.src[i:i+2] for i in range(0,12,2))
                self.src=Join([self.src[i:i+2] for i in range(0,12,2)],symbol=symbol)
            # Check the normal mac format
            octets = self.src.split(symbol)
            if len(octets) != 6: return False
            for i in octets:
                try:
                   if len(i) != 2 or int(i, 16) > 255:
                       return False
                except:
                   return False
            return True
        return default

    def FromStr(self,case='lower',default=False,sym=':',chk=False):
        if isinstance(self.src, str):
            self.src=self.src.strip()
            if len(self.src) in [12,17]:
                self.src=self.src.replace(':','').replace('-','')
                if len(self.src) == 12:
                    #self.src=sym.join(self.src[i:i+2] for i in range(0,12,2))
                    self.src=Join([self.src[i:i+2] for i in range(0,12,2)],symbol=sym)
                if case == 'lower':
                    self.src=self.src.lower()
                else:
                    self.src=self.src.upper()
        if chk:
            if not self.IsV4():
                return  default
        return self.src

    def ToStr(self,case='lower',default=False):
        if self.IsV4():
            if case == 'lower':
                self.src=self.src.strip().replace(':','').replace('-','').lower()
            else:
                self.src=self.src.strip().replace(':','').replace('-','').upper()
            return self.src
        return default

    def GetIfname(self):
        if not self.FromStr(): return False
        net_dir='/sys/class/net'
        if os.path.isdir(net_dir):
            dirpath,dirnames,filenames = list(os.walk(net_dir))[0]
            for dev in dirnames:
                fmac=cat('{}/{}/address'.format(dirpath,dev),no_end_newline=True)
                if type(fmac) is str and fmac.strip().lower() == self.src.lower():
                    return dev

    def FromIfname(self,ifname,default=None):
        if isinstance(ifname,str):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                if PyVer(3):
                    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', BYTES(encode='utf-8').From(ifname[:15])))
                    return ':'.join(['%02x' % char for char in info[18:24]])
                else:
                    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
                    return ':'.join(['%02x' % ord(char) for char in info[18:24]])
            except:
                pass
        return default

class VERSION:
    def __init__(self):
        pass

    def Clear(self,string,sym='.'):
        if isinstance(string,(int,str,float)) and string:
            if isinstance(string,str):
                string=string.strip()
            else:
                string='{}'.format(string)
            arr=string.split(sym)
            for ii in range(len(arr)-1,0,-1):
                if arr[ii].replace('0','') == '':
                    arr.pop(-1)
                else:
                    break
            #return sym.join(arr)
            return Join(arr,symbol=sym)
        return False

    def Check(self,a,sym,b):
        a=self.Clear(a)
        b=self.Clear(b)
        if a is False or b is False:
            return False
        if sym == '>':
            if LooseVersion(a) > LooseVersion(b):
                return True
        elif sym == '>=':
            if LooseVersion(a) >= LooseVersion(b):
                return True
        elif sym == '==':
            if LooseVersion(a) == LooseVersion(b):
                return True
        elif sym == '<=':
            if LooseVersion(a) <= LooseVersion(b):
                return True
        elif sym == '<':
            if LooseVersion(a) < LooseVersion(b):
                return True
        return False

    def Compare(self,src,compare_symbol,dest,compare_range='dest',version_symbol='.'):
        if isinstance(src,dict): src=src.get('version')
        if isinstance(dest,dict): dest=dest.get('version')
        if isinstance(src,str):
            src=STR(src).Split(version_symbol)
        elif isinstance(src,tuple):
            src=list(src)
        if isinstance(dest,str):
            dest=STR(dest).Split(version_symbol)
        elif isinstance(dest,tuple):
            dest=list(dest)
        src=[ Int(i) for i in src]
        dest=[ Int(i) for i in dest]
        if compare_range == 'dest':
            src=src[:len(dest)]
        elif compare_range == 'src':
             dest=dest[:len(src)]
        elif isinstance(compare_range,(tuple,list)) and len(compare_range) == 2:
            if isinstance(compare_range[0],int) and isinstance(compare_range[1],int):
                 src=src[compare_range[0]:compare_range[1]]
                 dest=dest[compare_range[0]:compare_range[1]]
            elif not compare_range[0] and isinstance(compare_range[1],int):
                 src=src[:compare_range[1]]
                 dest=dest[:compare_range[1]]
            elif isinstance(compare_range[0],int) and not compare_range[1]:
                 src=src[compare_range[0]:]
                 dest=dest[compare_range[0]:]
        elif isinstance(compare_range,int):
            if len(src) > compare_range and len(dest) > compare_range:
                 src=src[compare_range]
                 dest=dest[compare_range]
            else:
                 return
        return eval('{} {} {}'.format(src,compare_symbol,dest))

class IP:
    def __init__(self,ip=None):
        self.ip=ip

    def IsV4(self,ip=None):
        if not ip: ip=self.ip
        if self.V4(ip,default=False) is False: return False
        return True

    def IsBmcIp(self,ip=None,port=(623,664,443)):
        return self.IsOpenPort(port,ip=ip)

    def IsOpenPort(self,port,**opts):
        '''
        It connectionable port(?) like as ssh, ftp, telnet, web, ...
        '''
        default=opts.get('default',False)
        ip=opts.get('ip')
        if not ip:
            ip=self.ip
        tcp_sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_sk.settimeout(1)
        if self.IsV4(ip) is False or not isinstance(port,(str,int,list,tuple)):
            return default
        if isinstance(port,(str,int)):
            try:
                port=[int(port)]
            except:
                return default
        for pt in port:
            try:
                tcp_sk.connect((ip,pt))
                tcp_sk.close()
                return True
            except:
                pass
        return False

    def IsUsedPort(self,port,ip=None):
        if ip is None:
            ip=self.ip
        if ip in ['localhost','local',None]:
            ip='127.0.0.1'
        '''
        The IP used the port, it just checkup used port. (open port or dedicated port)
        '''
        soc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        location=(ip,int(port))
        rc=soc.connect_ex(location)
        soc.close()
        if rc== 0:
            return True
        return False

    def Ip2Num(self,ip=None,default=False):
        if not ip: ip=self.ip
        return self.V4(ip,out=int,default=default)

    def Ip2Str(self,ip=None,default=False):
        if not ip:ip=self.ip
        return self.V4(ip,out=str,default=default)

    def Ip2hex(self,ip=None,default=False):
        if not ip: ip=self.ip
        return self.V4(ip,out=hex,default=default)

    def InRange(self,start_ip,end_ip,**opts):
        ip=opts.get('ip')
        if not ip: ip=self.ip
        default=opts.get('default',False)
        startip=self.Ip2Num(start_ip)
        myip=self.Ip2Num(ip)
        endip=self.Ip2Num(end_ip)
        if isinstance(startip,int) and isinstance(myip,int) and isinstance(endip,int):
            if startip <= myip <= endip: return True
            return False
        return default

    def LostNetwork(self,**opts):
        ip=opts.get('ip')
        if not ip: ip=self.ip
        default=opts.get('default',False)
        timeout_sec=opts.get('timeout',1800)
        interval=opts.get('interval',2)
        keep_good=opts.get('keep_good',30)
        cancel_func=opts.get('cancel_func',None)
        log=opts.get('log',None)
        init_time=None
        if self.IsV4(ip):
            if not self.Ping(ip,count=5):
                if not self.Ping(ip,count=0,timeout=timeout_sec,keep_good=keep_good,interval=interval,cancel_func=cancel_func,log=log):
                    return True
            return False
        return default

    def V4(self,ip=None,out='str',default=False):
        if ip is None: ip=self.ip
        ip_int=None
        if isinstance(ip,str):
            ipstr=ip.strip()
            if '0x' in ipstr:
                ip_int=int(ipstr,16)
            elif ipstr.isdigit():
                ip_int=int(ipstr)
            elif '.' in ipstr:
                try:
                    ip_int=struct.unpack("!I", socket.inet_aton(ipstr))[0] # convert Int IP
                    #struct.unpack("!L", socket.inet_aton(ip))[0]
                except:
                    return default
        elif isinstance(ip,int):
            try:
                socket.inet_ntoa(struct.pack("!I", ip)) # check int is IP or not
                ip_int=ip
            except:
                return default
        elif isinstance(ip,type(hex)):
            ip_int=int(ip,16)

        if ip_int is not None:
            try:
                if out in ['str',str]:
                    return socket.inet_ntoa(struct.pack("!I", ip_int))
                elif out in ['int',int]:
                    return ip_int
                elif out in ['hex',hex]:
                    return hex(ip_int)
            except:
                pass
        return default

    def Online(self,**opts):
        ip=opts.get('ip')
        if not ip: ip=self.ip
        default=opts.get('default',False)
        timeout_sec=opts.get('timeout',1800)
        interval=opts.get('interval',3)
        keep=opts.get('keep',20)
        cancel_func=opts.get('cancel_func',None)
        log=opts.get('log',None)
        time=TIME()
        run_time=time.Int()
        if self.IsV4(ip):
            if log:
                log('[',direct=True,log_level=1)
            while True:
                if time.Out(timeout_sec):
                    if log:
                        log(']\n',direct=True,log_level=1)
                    return False,'Timeout monitor'
                if is_cancel(cancel_func):
                    if log:
                        log(']\n',direct=True,log_level=1)
                    return True,'Stopped monitor by Custom'
                if self.Ping(ip,cancel_func=cancel_func):
                    if (time.Int() - run_time) > keep:
                        if log:
                            log(']\n',direct=True,log_level=1)
                        return True,'OK'
                    if log:
                        log('-',direct=True,log_level=1)
                else:
                    run_time=time.Int()
                    if log:
                        log('.',direct=True,log_level=1)
                time.Sleep(interval)
            if log:
                log(']\n',direct=True,log_level=1)
            return False,'Timeout/Unknown issue'
        return default,'IP format error'

    def Ping(self,host=None,count=0,interval=1,keep_good=0, timeout=0,lost_mon=False,log=None,stop_func=None,log_format='.',cancel_func=None):
        if host is None: host=self.ip
        ICMP_ECHO_REQUEST = 8 # Seems to be the same on Solaris. From /usr/include/linux/icmp.h;
        ICMP_CODE = socket.getprotobyname('icmp')
        ERROR_DESCR = {
            1: ' - Note that ICMP messages can only be '
               'sent from processes running as root.',
            10013: ' - Note that ICMP messages can only be sent by'
                   ' users or processes with administrator rights.'
            }

        def checksum(msg):
            sum = 0
            size = (len(msg) // 2) * 2
            for c in range(0,size, 2):
                sum = (sum + ord(msg[c + 1])*256+ord(msg[c])) & 0xffffffff
            if size < len(msg):
                sum = (sum+ord(msg[len(msg) - 1])) & 0xffffffff
            ra = ~((sum >> 16) + (sum & 0xffff) + (sum >> 16)) & 0xffff
            ra = ra >> 8 | (ra << 8 & 0xff00)
            return ra

        def mk_packet(size):
            """Make a new echo request packet according to size"""
            # Header is type (8), code (8), checksum (16), id (16), sequence (16)
            header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, size, 1)
            #data = struct.calcsize('bbHHh') * 'Q'
            data = size * 'Q'
            my_checksum = checksum(CONVERT(header).Str() + data)
            header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,
                                 socket.htons(my_checksum), size, 1)
            return header + BYTES().From(data)

        def receive(my_socket, ssize, stime, timeout):
            while True:
                if timeout <= 0:
                    return
                ready = select.select([my_socket], [], [], timeout)
                if ready[0] == []: # Timeout
                    return
                received_time = time.time()
                packet, addr = my_socket.recvfrom(1024)
                type, code, checksum, gsize, seq = struct.unpack('bbHHh', packet[20:28]) # Get Header
                if gsize == ssize:
                    return received_time - stime
                timeout -= received_time - stime

        def pinging(ip,timeout=1,size=64):
            try:
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
            except socket.error as e:
                if e.errno in ERROR_DESCR:
                    #raise socket.error(''.join((e.args[1], ERROR_DESCR[e.errno])))
                    raise socket.error(Join((e.args[1], ERROR_DESCR[e.errno]),symbol=''))
                raise
            if size in ['rnd','random']:
                # Maximum size for an unsigned short int c object(65535)
                size = int((id(timeout) * random.random()) % 65535)
            packet = mk_packet(size)
            while packet:
                sent = my_socket.sendto(packet, (ip, 1)) # ICMP have no port, So just put dummy port 1
                packet = packet[sent:]
            delay = receive(my_socket, size, TIME().Time(), timeout)
            my_socket.close()
            if delay:
                return delay,size

        def do_ping(ip,timeout=1,size=64,count=None,interval=0.7,log_format='ping',cancel_func=None):
            ok=1
            i=1
            while True:
                if is_cancel(cancel_func):
                    return -1,'canceled'
                delay=pinging(ip,timeout,size)
                if delay:
                    ok=0
                    if log_format == '.':
                        sys.stdout.write('.')
                        sys.stdout.flush()
                    elif log_format == 'ping':
                        sys.stdout.write('{} bytes from {}: icmp_seq={} ttl={} time={} ms\n'.format(delay[1],ip,i,size,round(delay[0]*1000.0,4)))
                        sys.stdout.flush()
                else:
                    ok=1
                    if log_format == '.':
                        sys.stdout.write('x')
                        sys.stdout.flush()
                    elif log_format == 'ping':
                        sys.stdout.write('{} icmp_seq={} timeout ({} second)\n'.format(ip,i,timeout))
                        sys.stdout.flush()
                if count:
                    count-=1
                    if count < 1:
                        return ok,'{} is alive'.format(ip)
                i+=1
                TIME().Sleep(interval)


        if log_format=='ping':
            if not count: count=1
            if find_executable('ping'):
                os.system("ping -c {0} {1}".format(count,host))
            else:
                do_ping(host,timeout=timeout,size=64,count=count,log_format='ping',cancel_func=cancel_func)
        else:
            Time=TIME()
            init_sec=0
            infinit=False
            if not count and not timeout:
                count=1
                infinit=True
            if not infinit and not count:
                init_sec=Time.Init()
                if keep_good and keep_good > timeout:
                    timeout=keep_good + timeout
                count=timeout
            chk_sec=Time.Init()
            log_type=type(log).__name__
            found_lost=False
            good=False
            while count > 0:
               if is_cancel(cancel_func):
                   log(' - Canceled ping')
                   return False
               if stop_func:
                   if log_type == 'function':
                       log(' - Stopped ping')
                   return False
               if find_executable('ping'):
                   rc=SHELL().Run("ping -c 1 {}".format(host))
               else:
                   rc=do_ping(host,timeout=1,size=64,count=1,log_format=None)
               if rc[0] == 0:
                  good=True
                  if keep_good:
                      if good and keep_good and TIME().Now(int) - chk_sec >= keep_good:
                          return True
                  else:
                      return True
                  if log_type == 'function':
                      log('.',direct=True,log_level=1)
                  else:
                      sys.stdout.write('.')
                      sys.stdout.flush()
               else:
                  good=False
                  chk_sec=TIME().Now(int)
                  if log_type == 'function':
                      log('x',direct=True,log_level=1)
                  else:
                      sys.stdout.write('.')
                      sys.stdout.flush()
               if init_sec:
                   count=count-(TIME().Now(int)-init_sec)
               elif not infinit:
                   count-=1
               TIME().Sleep(interval)
            return good

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

    def Value(self,*key,**opts):
        default=opts.get('default',None)
        err=opts.get('err',False)
        out=opts.get('out',opts.get('out_form',None))
        strip=opts.get('strip',False)
        peel=opts.get('peel',False)
        check=opts.get('check',('str','list','tuple','dict','instance','classobj'))
        # Added
        if len(key) == 0 and opts.get('key') is not None:
            if isinstance(opts.get('key'),(tuple,list)):
                key=tuple(opts.get('key'))
            else:
                key=(opts.get('key'),)
        rt=[]

        # Web Data
        if self.ArgType(self.src,'Request'):
            if key:
                key=key[0]
            else:
                key=opts.get('key',None)
            method=opts.get('method',None)
            strip=opts.get('strip',True)
            find=opts.get('find',[])
            if key is not None:
                if method is None:
                    method=self.src.method
                if method.upper() == 'GET':
                    rc=self.src.GET.get(key,default)
                elif method.upper() == 'FILE':
                    if out is list:
                        rc=self.src.FILES.getlist(key,default)
                    else:
                        rc=self.src.FILES.get(key,default)
                else:
                    if out is list:
                        rc=self.src.POST.getlist(key,default)
                    else:
                        rc=self.src.POST.get(key,default)
                if self.ArgType(rc,str) and strip:
                    rc=rc.strip()
                if find and rc in find:
                    return True
                if rc == 'true':
                    return True
                elif rc == '':
                    return default
                return rc
            else:
                if self.src.method == 'GET':
                    return self.src.GET
                else:
                    return self.src.data


        # Other Python Data
        src_name=type(self.src).__name__
        if len(key) == 0:
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
                for ff in Abs(*key,obj=self.src,out=list,default=None,err=err):
#                    if ff is None:
#                        if err in [True,'True','err']: rt.append(default)
#                    else:
                    if IS(ff).Int() and ff < len(self.src):
                        rt.append(self.src[ff])
                    else:
                        if err in [True,'True','err']: rt.append(default)
            elif Type(self.src,dict):
                if src_name in ['kDict','DICT']: self.src=self.src.Get()
                for ff in key:
                    gval=self.src.get(ff,default)
                    if gval == default:
                        if err in [True,'True','err']: rt.append(gval)
                    else:
                        rt.append(gval)
            elif Type(self.src,('instance','classobj')):
                # get function object of finding string name in the class/instance
                for ff in key:
                    if isinstance(ff,(list,tuple,dict)):
                        for kk in ff:
                            rt.append(getattr(self.src,kk,default))
                    elif isinstance(ff,str): 
                        rt.append(getattr(self.src,ff,default))
            if rt: return OutFormat(rt,out=out,strip=strip,peel=peel)
        # Not support format or if not class/instance then return error
        if err in [True,'True','true','err','ERR','ERROR','error']: OutFormat(default,out=out,strip=strip,peel=peel)
        return OutFormat(self.src,out=out,strip=strip,peel=peel)

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
        return FUNCTION(self.src).Args(mode=field,default=default)

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
        return FUNCTION().CallerName(detail=detail)

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

    def DirName(self,src=None,default=None):
        if src is None: src=self.src
        if Type(src,str):
            dirname=os.path.dirname(src)
            if dirname == '': return '.'
            return dirname
        return default

    def Dirname(self,src=None,default=None):
        return self.DirName(src=src,default=default)

    def DirectoryName(self,default=None):
        return self.DirName(default=default)

    def Pwd(self,default=None):
        #return os.path.abspath(__file__)
        #return os.path.dirname(os.path.realpath(__file__))
        try:
            frame=inspect.stack()[1]
            module=inspect.getmodule(frame[0])
            return os.path.dirname(os.path.realpath(module.__file__))
        except:
            return default

    def Basename(self,src=None):
        if src is None: src=self.src
        if Type(src,str): return os.path.basename(src)
        return os.path.basename(inspect.stack()[1].filename)

    def Me(self,default=False):
        try:
            frame=inspect.stack()[-1]
            module=inspect.getmodule(frame[0])
            return module
        except:
            return default

class IS:
    def __init__(self,src=None,**opts):
        self.src=src
        self.rtd=opts.get('rtd',{'GOOD':[True,'True','Good','Ok','Pass',{'OK'},0],'FAIL':[False,'False','Fail',{'FAL'}],'NONE':[None,'None','N/A',{'NA'}],'IGNO':['IGNO','Ignore',{'IGN'}],'ERRO':['ERR','Error',{'ERR'}],'WARN':['Warn',{'WAR'}],'UNKN':['Unknown','UNKN',{'UNK'}],'JUMP':['Jump',{'JUMP'}]})

    def Py2(self):
        if PyVer(2): return True
        return False

    def Py3(self):
        if PyVer(3): return True
        return False

    def Int(self):
        try:
            int(self.src)
            return True
        except:
            return False

    def Bytes(self):
        if self.Py3():
            if isinstance(self.src,bytes):
                return True
        return False

    def Ipv4(self):
        return IP(self.src).IsV4()

    def Mac4(self,**opts):
        return MAC(self.src).IsV4()

    def Ip_with_port(self,port,**opts):
        return IP(self.src).WithPort(port,**opts)

    def File(self):
        if isinstance(self.src,str): return os.path.isfile(self.src)
        return False

    def Dir(self):
        if isinstance(self.src,str): return os.path.isdir(self.src)
        return False

    def Xml(self):
        firstLine=file_rw(self.src,out='string',read='firstline')
        if firstLine is False:
            #filename_str=_u_byte2str(self.src)
            filename_str=CONVERT(self.src).Str()
            if isinstance(filename_str,str):
                firstLine=filename_str.split('\n')[0]
        if isinstance(firstLine,str) and firstLine.split(' ')[0] == '<?xml': return True
        return False

    def Json(self,src=None):
        if src is None: src=self.src
        try:
            _json.loads(self.src)
            return True
        except:
            return False

    def Pickle(self):
        if isinstance(self.src,str) and os.path.isfile(self.src):
            try:
                with open(self.src,'rb') as f: # Pickle Type
                    pickle.load(f)
                    return True
            except:
                pass
        return False

    def Matrix(self,**opts):
        default=opts.get('default',False)
        if isinstance(self.src,(tuple,list)) and len(self.src) >= 1:
            if isinstance(self.src[0],(tuple,list)): # |a,b,c|
                first_ln=len(self.src[0])            # |d,e,f|
                for ii in self.src[1:]:
                    if isinstance(ii,(tuple,list)) and len(ii) == first_ln: continue
                    return False
                return True
            else: # |a,b,c,d|
                first_typ=type(self.src[0])
                for ii in self.src[1:]:
                    if type(ii) != first_type: return False
                return True
        return default

    def Lost_network(self,**opts):
        return IP(self.src).LostNetwork(**opts)

    def Comback_network(self,**opts):
        return IP(self.src).Online(**opts)

    def Rc(self,chk='_'):
        def trans(irt):
            type_irt=type(irt)
            for ii in rtd:
                for jj in rtd[ii]:
                    if type(jj) == type_irt and ((type_irt is str and jj.lower() == irt.lower()) or jj == irt):
                        return ii
            return 'UNKN'
        rtc=Get(self.src,'0|rc',out='raw',err='ignore',check=(list,tuple,dict))
        nrtc=trans(rtc)
        if chk != '_':
            if trans(chk) == nrtc:
                return True
            return False
        return nrtc

    def Cancel(self,func=None):
        if func is None:
            func=self.src
        ttt=type(func).__name__
        if ttt in ['function','instancemethod','method']:
            if func():
                return True
        elif ttt in ['bool','str'] and func in [True,'cancel']:
            return True
        return False

    def Window(self):
        return False

    def Android(self):
        return False

    def IOS(self):
        return False

    def Centos(self):
        return False

    def Unbuntu(self):
        return False

    def Suse(self):
        return False

    def Linux(self):
        if self.centos() or self.ubuntu() or self.suse(): return True
        return False

    def Function(self,obj=None,default=False):
        if Type(self.src,'function'): return True
        if obj is None:
            obj=sys.modules.get('__name__',default)
        elif isinstance(obj,str):
            obj=sys.modules.get(obj,default)
        if obj == default: return default
        if Type(obj,'Class','module'):
            if GET(obj).FuncList().get(self.src,default) == default: return default
            return True
            #return vars(obj).get(self.src,default)
        return default

    def Var(self,obj=None,default=False):
        if obj is None:
            obj=sys.modules.get('__main__',default)
        elif isinstance(obj,str):
            obj=sys.modules.get(obj,default)
        if obj == default: return default
        if Type(obj,'class','function','instance'):
            ARGS=GET(obj).Args()
            for tt in ARGS:
                if self.src in ARGS[tt]: return True 
        else:
            get_var=dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"].get(self.src,'_#_')
            if get_var != '_#_':
                if not Type(get_var,'module','class','function'): return True
#        if hasattr(obj,self.src):
#            return True
        return False

    def Exec(self):
        if isinstance(self.src,str):
            if find_executable(self.src):
                return True
        return False

    def Bin(self):
        return self.Exec()

    def Same(self,src=None,chk_val=None,sense=False):
        def _IsSame_(src,chk,sense):
            src_type=type(src).__name__
            chk_type=type(chk).__name__
            if src_type == 'bytes' or chk_type == 'bytes':
                if chk_type=='int': chk='{}'.format(chk)
                if isinstance(chk,str):
                    chk=BYTES().From(chk)
                if not sense:
                    chk=chk.lower()
                if src_type=='int': src='{}'.format(src)
                if isinstance(src,str):
                    src=BYTES().From(src)
                if not sense:
                    src=src.lower()
                if src == chk: return True
            else:
                if src_type == 'str' and src.isdigit(): src=int(src)
                if chk_type == 'str' and chk.isdigit(): chk=int(chk)
                if not sense and isinstance(src,str) and isinstance(chk,str):
                    if src.lower() == chk.lower(): return True
                elif src == chk:
                    return True
            return False
        if isinstance(src,(list,tuple)) and isinstance(chk_val,(list,tuple)):
            for j in src:
                ok=False
                for i in chk_val:
                    aa=_IsSame_(j,i,sense)
                    if aa is True:
                        ok=True
                        break
                if ok is False: return False
            for j in chk_val:
                ok=False
                for i in src:
                    aa=_IsSame_(j,i,sense)
                    if aa is True:
                        ok=True
                        break
                if ok is False: return False
            return True
        else:
            if isinstance(chk_val,(list,tuple)):
                for i in chk_val:
                    aa=_IsSame_(src,i,sense)
                    if aa is True: return True
                return False
            else:
                return _IsSame_(src,chk_val,sense)

    def In(self,src,idx=False,default=False):
        find=self.src
        '''Check key or value in the dict, list or tuple then True, not then False'''
        if isinstance(src, (list,tuple,str)):
            if isinstance(idx,int):
                if isinstance(src,str):
                    if idx < 0:
                        if src[idx-len(find):idx] == find:
                            return True
                    else:
                        if src[idx:idx+len(find)] == find:
                            return True
                else:
                    if Get(src,idx,out='raw') == find:
                        return True
            else:
                for i in src:
                    if self.Same(i,find): return True
        elif isinstance(src, dict):
            if idx is None:
                for i in src:
                    if self.Same(i,find): return True
            else:
                if Get(src,idx,out='raw') == find:
                    return True
        return default

class LOG:
    def __init__(self,**opts):
        self.limit=opts.get('limit',3)
        self.dbg_level=opts.get('dbg_level',None)
        self.path=opts.get('path','/tmp')
        self.log_file=opts.get('log_file',None)
        self.info_file=opts.get('info_file',None)
        self.error_file=opts.get('error_file',None)
        self.dbg_file=opts.get('dbg_file',None)
        self.screen=opts.get('screen',False)
        self.date_format=opts.get('date_format','[%m/%d/%Y %H:%M:%S]')

    def Format(self,*msg,**opts):
        log_date_format=opts.get('date_format',self.date_format)
        func_name=opts.get('func_name',None)
        end_new_line=opts.get('end_new_line','')
        start_new_line=opts.get('start_new_line','\n')
        if len(msg) > 0:
            m_str=None
            intro=''
            intro_space=''
            if log_date_format:
                intro=TIME().Format(tformat=log_date_format)+' '
            func_name_name=type(func_name).__name__
            if func_name_name == 'str':
                intro=intro+'{0} '.format(func_name)
            elif func_name is True:
                intro=intro+'{0}() '.format(get_caller_fcuntion_name())
            elif func_name_name in ['function','instancemethod']:
                intro=intro+'{0}() '.format(func_name.__name__)
            if intro:
               for i in range(0,len(intro)):
                   intro_space=intro_space+' '
            for m in list(msg):
                n=m.split('\n')
                if m_str is None:
                    m_str='{0}{1}{2}{3}'.format(start_new_line,intro,n[0],end_new_line)
                else:
                    m_str='{0}{1}{2}{3}{4}'.format(m_str,start_new_line,intro_space,n[0],end_new_line)
                for nn in n[1:]:
                    m_str='{0}{1}{2}{3}{4}'.format(m_str,start_new_line,intro_space,nn,end_new_line)
            return m_str

    def Syslogd(self,*msg,**opts):
        syslogd=opts.get('syslogd',None)
        if syslogd:
            #syslog_msg=' '.join(msg)
            syslog_msg=Join(msg,symbol=' ')
            if syslogd in ['INFO','info']:
                syslog.syslog(syslog.LOG_INFO,syslog_msg)
            elif syslogd in ['KERN','kern']:
                syslog.syslog(syslog.LOG_KERN,syslog_msg)
            elif syslogd in ['ERR','err']:
                syslog.syslog(syslog.LOG_ERR,syslog_msg)
            elif syslogd in ['CRIT','crit']:
                syslog.syslog(syslog.LOG_CRIT,syslog_msg)
            elif syslogd in ['WARN','warn']:
                syslog.syslog(syslog.LOG_WARNING,syslog_msg)
            elif syslogd in ['DBG','DEBUG','dbg','debug']:
                syslog.syslog(syslog.LOG_DEBUG,syslog_msg)
            else:
                syslog.syslog(syslog_msg)


    def File(self,log_str,log_level,special_file=None):
        log_file=None
        if os.path.isdir(self.path):
            if (log_level in ['dbg','debug'] or (isinstance(log_level,int) and isinstance(self.dbg_level,int) and self.dbg_level <= log_level <= self.limit)) and isinstance(self.dbg_file,str):
                log_file=os.path.join(self.path,self.dbg_file)
            elif log_level in ['info'] and isinstance(self.info_file,str):
                log_file=os.path.join(self.path,self.info_file)
            elif log_level in ['error'] and isinstance(self.error_file,str):
                log_file=os.path.join(self.path,self.error_file)
            elif isinstance(self.log_file,str) or isinstance(special_file,str):
                if special_file:
                    log_file=os.path.join(self.path,special_file)
                elif log_level in ['dbg','debug','info','error'] or (isinstance(log_level,int) and log_level <= self.limit):
                    log_file=os.path.join(self.path,self.log_file)
            if log_file:
                with open(log_file,'a+') as f:
                    f.write(log_str)
        return log_file

    def Screen(self,log_str,log_level):
        if log_level in ['error']:
            sys.stderr.write(log_str)
            sys.stderr.flush()
        elif log_level <= self.limit:
            sys.stdout.write(log_str)
            sys.stdout.flush()


    def Log(self,*msg,**opts):
        direct=opts.get('direct',False)
        func_name=opts.get('func_name',None)
        date_format=opts.get('date_format','[%m/%d/%Y %H:%M:%S]')
        start_new_line=opts.get('start_new_line','\n')
        end_new_line=opts.get('end_new_line','')
        log_level=opts.get('log_level',3)
        special_file=opts.get('filename',None)
        screen=opts.get('screen',None)
        syslogd=opts.get('syslogd',None)
        if msg:
            # send log at syslogd
            self.Syslogd(*msg,syslogd=syslogd)

            if date_format in [False,None,'','no','ignore']:
                date_format=None
            if func_name in [False,None,'','no','ignore']:
                func_name=None
            if direct:
                #log_str=' '.join(msg)
                log_str=Join(msg,symbol=' ')
            else:
                log_str=self.Format(*msg,func_name=func_name,date_format=date_format,end_new_line=end_new_line,start_new_line=start_new_line)

            # Saving log at file
            log_file=self.File(log_str,log_level,special_file=special_file)

            # print at screen
            if screen is True or (screen is None and self.screen is True):
                self.Screen(log_str,log_level)
 
            # Send Log Data to logging function (self.log_file)
            if log_file is None:
                self.Function(log_str)

    def Function(self,*msg,**opts):
        if type(self.log_file).__name__ == 'function': 
            log_func_arg=get_function_args(self.log_file,mode='all')
            if 'args' in log_func_arg or 'varargs' in log_func_arg:
                log_p=True
                args=log_func_arg.get('args',[])
                if args and len(args) <= 4 and ('direct' in args or 'log_level' in args or 'func_name' in args):
                    tmp=[]
                    for i in range(0,len(args)):
                        tmp.append(i)
                    if 'direct' in args:
                        didx=args.index('direct')
                        del tmp[didx]
                        args[didx]=direct
                    if 'log_level' in args:
                        lidx=args.index('log_level')
                        del tmp[lidx]
                        args[lidx]=log_level
                    if 'func_name' in args:
                        lidx=args.index('func_name')
                        del tmp[lidx]
                        args[lidx]=func_name
                    if 'date_format' in args:
                        lidx=args.index('date_format')
                        del tmp[lidx]
                        args[lidx]=date_format
                    args[tmp[0]]=log_str
                    self.log_file(*args)
                elif 'keywards' in log_func_arg:
                    self.log_file(log_str,direct=direct,log_level=log_level,func_name=func_name,date_format=date_format)
                elif 'defaults' in log_func_arg:
                    if 'direct' in log_func_arg['defaults'] and 'log_level' in log_func_arg['defaults']:
                        self.log_file(log_str,direct=direct,log_level=log_level)
                    elif 'log_level' in log_func_arg['defaults']:
                        self.log_file(log_str,log_level=log_level)
                    elif 'direct' in log_func_arg['defaults']:
                        self.log_file(log_str,direct=direct)
                    else:
                        self.log_file(log_str)
                else:
                    self.log_file(log_str)

class HOST:
    def __init__(self):
        pass

    def Name(self):
        return socket.gethostname()

    def DefaultRouteDev(self,default=None,gw=None):
        for ii in STR(cat('/proc/net/route',no_edge=True)).Split('\n'):
            ii_a=ii.split()
            #if len(ii_a) > 8 and '00000000' == ii_a[1] and '00000000' == ii_a[7]: return ii_a[0]
            if len(ii_a) < 4 or ii_a[1] != '00000000' or not int(ii_a[3], 16) & 2:
                #If not default route or not RTF_GATEWAY, skip it
                continue
            if gw:
                if IS().Same(socket.inet_ntoa(struct.pack("<L", int(ii_a[2], 16))),gw):
                    return ii_a[0]
            else:
                return ii_a[0]
        return default

    def DefaultRouteIp(self,default=None):
        for ii in STR(cat('/proc/net/route',no_edge=True)).Split('\n'):
            ii_a=ii.split()
            if len(ii_a) < 4 or ii_a[1] != '00000000' or not int(ii_a[3], 16) & 2:
                #If not default route or not RTF_GATEWAY, skip it
                continue
            return socket.inet_ntoa(struct.pack("<L", int(ii_a[2], 16)))
        return default

    def Ip(self,ifname=None,mac=None,default=None):
        if ifname is None: 
            if mac is None : mac=self.Mac()
            ifname=self.DevName(mac)

        if ifname:
            if not os.path.isdir('/sys/class/net/{}'.format(ifname)):
                return default
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                return socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', ifname[:15])
                )[20:24])
            except:
                try:
                    return os.popen('ip addr show {}'.format(ifname)).read().split("inet ")[1].split("/")[0]
                except:
                    pass
        return socket.gethostbyname(socket.gethostname())

    def IpmiIp(self,default=None):
        rt=SHELL().Run('''ipmitool lan print 2>/dev/null| grep "IP Address" | grep -v Source | awk '{print $4}' ''')
        if rt[0]:return rt[1]
        return default

    def IpmiMac(self,default=None):
        rt=SHELL().Run(""" ipmitool lan print 2>/dev/null | grep "MAC Address" | awk """ + """ '{print $4}' """)
        if rt[0]:return rt[1]
        return default

    def Mac(self,ip=None,dev=None,default=None,ifname=None):
        if dev is None and ifname: dev=ifname
        if IP(ip).IsV4():
            dev_info=self.NetDevice()
            for dev in dev_info.keys():
                if self.Ip(dev) == ip:
                    return dev_info[dev]['mac']
        #ip or anyother input of device then getting default gw's dev
        if dev is None: dev=self.DefaultRouteDev()
        if dev:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', BYTES().From(dev[:15])))
                return Join(['%02x' % ord(char) for char in BYTES(info[18:24]).Str()],symbol=':')
            except:
                pass
        #return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
        return CONVERT('%012x' % uuid.getnode()).Str2Mac()

    def DevName(self,mac=None,default=None):
        if mac is None:
            mac=self.Mac()
        net_dir='/sys/class/net'
        if isinstance(mac,str) and os.path.isdir(net_dir):
            dirpath,dirnames,filenames = list(os.walk(net_dir))[0]
            for dev in dirnames:
                fmac=cat('{}/{}/address'.format(dirpath,dev),no_edge=True)
                if isinstance(fmac,str) and fmac.strip().lower() == mac.lower():
                    return dev
        return default

    def Info(self):
        return {
         'host_name':self.Name(),
         'host_ip':self.Ip(),
         'host_mac':self.Mac(),
         'ipmi_ip':self.IpmiIp(),
         'ipmi_mac':self.IpmiMac(),
         }

    def NetDevice(self,name=None,default=False):
        def _dev_info_(path,name):
            drv=ls('{}/{}/device/driver/module/drivers'.format(path,name))
            if drv is False:
                drv='unknown'
            else:
                drv=drv[0].split(':')[1]
            return {
                'mac':cat('{}/{}/address'.format(path,name),no_end_newline=True),
                'duplex':cat('{}/{}/duplex'.format(path,name),no_end_newline=True,file_only=False),
                'mtu':cat('{}/{}/mtu'.format(path,name),no_end_newline=True),
                'state':cat('{}/{}/operstate'.format(path,name),no_end_newline=True),
                'speed':cat('{}/{}/speed'.format(path,name),no_end_newline=True,file_only=False),
                'id':cat('{}/{}/ifindex'.format(path,name),no_end_newline=True),
                'driver':drv,
                'drv_ver':cat('{}/{}/device/driver/module/version'.format(path,name),no_end_newline=True,file_only=False,default=''),
                }


        net_dev={}
        net_dir='/sys/class/net'
        if os.path.isdir(net_dir):
            dirpath,dirnames,filenames = list(os.walk(net_dir))[0]
            if name:
                if name in dirnames:
                    net_dev[name]=_dev_info_(dirpath,name)
            else:
                for dev in dirnames:
                    net_dev[dev]=_dev_info_(dirpath,dev)
            return net_dev
        return default

    def Alive(self,ip,keep=20,interval=3,timeout=1800,default=False,log=None,cancel_func=None):
        return IP(ip).Online(keep=keep,interval=interval,timeout=timeout,default=default,log=log,cancel_func=cancel_func)[1]

    def Ping(self,ip,keep_good=10,timeout=3600):
        return IP(ip).Ping(keep_good=10,timeout=timeout)

class FILE:
    '''
    sub_dir  : True (Get files in recuring directory)
    data     : True (Get File Data)
    md5sum   : True (Get File's MD5 SUM)
    link2file: True (Make a real file instead sym-link file)
    '''
    def __init__(self,*inp,**opts):
        self.root_path=opts.get('root_path',None)
        #if self.root_path is None: self.root_path=os.path.dirname(os.path.abspath(__file__))
        if self.root_path is None: self.root_path=self.Path()
        info=opts.get('info',None)
        if isinstance(info,dict):
            self.info=info
        else:
            self.info={}
            sub_dir=opts.get('sub_dir',opts.get('include_sub_dir',opts.get('include_dir',False)))#???
            data=opts.get('data',False)
            md5sum=opts.get('md5sum',False)
            link2file=opts.get('link2file',False) # If True then copy file-data of sym-link file, so get it real file instead of sym-link file
            self.filelist={}
            for filename in inp:
                root,flist=self.FileList(filename,sub_dir=sub_dir,dirname=True)
                if root not in self.filelist: self.filelist[root]=[]
                self.filelist[root]=self.filelist[root]+flist
            for ff in self.filelist:
                self.info.update(self.Get(ff,*self.filelist[ff],data=data,md5sum=md5sum,link2file=link2file))

    def FileList(self,name,sub_dir=False,dirname=False,default=[]):
        if isinstance(name,str):
            if name[0] == '/':  # Start from root path
                if os.path.isfile(name) or os.path.islink(name): return os.path.dirname(name),[os.path.basename(name)]
                if os.path.isdir(name):
                    if sub_dir:
                        rt = []
                        pwd=os.getcwd()
                        os.chdir(name)
                        for base, dirs, files in os.walk('.'): 
                            if dirname: rt.extend(os.path.join(base[2:], d) for d in dirs)
                            rt.extend(os.path.join(base[2:], f) for f in files)
                        os.chdir(pwd)
                        return Path(name),rt
                    else:
                        return Path(name),[f for f in os.listdir(name)]
            elif self.root_path: # start from defined root path
                #chk_path=os.path.join(self.root_path,name)
                chk_path=Path(self.root_path,name)
                if os.path.isfile(chk_path) or os.path.islink(chk_path): return Path(self.root_path),[name]
                if os.path.isdir(chk_path):
                    if sub_dir:
                        rt = []
                        pwd=os.getcwd()
                        os.chdir(self.root_path) # Going to defined root path
                        # Get recuring file list of the name (when current dir then '.')
                        for base, dirs, files in os.walk(name):
                            if dirname: rt.extend(os.path.join(base[2:], d) for d in dirs)
                            rt.extend(os.path.join(base[2:], f) for f in files)
                        os.chdir(pwd) # recover to the original path
                        return Path(self.root_path),rt 
                    else:
                        if name == '.': name=''
                        return Path(self.root_path),[os.path.join(name,f) for f in os.listdir('{}/{}'.format(self.root_path,name))]
        return default

    def CdPath(self,base,path):
        rt=base
        for ii in path.split('/'):
            if ii not in rt: return False
            rt=rt[ii]
        return rt
            
    def FileName(self,filename):
        if isinstance(filename,str):
            filename_info=os.path.basename(filename).split('.')
            if 'tar' in filename_info:
                idx=filename_info.index('tar')
            else:
                idx=-1
            #return '.'.join(filename_info[:idx]),'.'.join(filename_info[idx:])
            return Join(filename_info[:idx],symbol='.'),Join(filename_info[idx:],symbol='.')
        return None,None

    def FileType(self,filename,default=False):
        if not isinstance(filename,str) or not os.path.isfile(filename): return default
        aa=magic.from_buffer(open(filename,'rb').read(2048))
        if aa: return aa.split()[0].lower()
        return 'unknown'

    def GetInfo(self,path=None,*inps):
        if isinstance(path,str):
            if not self.info and os.path.exists(path):
                data={}
                self.MkInfo(data,path)
            else:
                data=self.CdPath(path)
            if isinstance(data,dict):
                if not inps and ' i ' in data: return data[' i ']
                rt=[]
                for ii in inps:
                    if ii == 'data' and ii in data: rt.append(data[ii])
                    if ' i ' in data and ii in data[' i ']: rt.append(data[' i '][ii])
                return rt

    def Get(self,root_path,*filenames,**opts):
        data=opts.get('data',False)
        md5sum=opts.get('md5sum',False)
        link2file=opts.get('link2file',False)
        base={}

        def MkInfo(rt,filename=None,**opts):
            #if not isinstance(rt,dict) or not isinstance(filename,str): return default
            if ' i ' not in rt: rt[' i ']={}
            if filename:
                state=os.stat(filename)
                rt[' i ']['exist']=True
                rt[' i ']['size']=state.st_size
                rt[' i ']['mode']=oct(state.st_mode)[-4:]
                rt[' i ']['atime']=state.st_atime
                rt[' i ']['mtime']=state.st_mtime
                rt[' i ']['ctime']=state.st_ctime
                rt[' i ']['gid']=state.st_gid
                rt[' i ']['uid']=state.st_uid
            if opts: rt[' i '].update(opts)

        def MkPath(base,path,root_path):
            rt=base
            chk_dir='{}'.format(root_path)
            for ii in path.split('/'):
                if ii:
                    chk_dir=Path(chk_dir,ii)
                    if ii not in rt:
                        rt[ii]={}
                        if os.path.isdir(chk_dir): MkInfo(rt[ii],chk_dir,type='dir')
                    rt=rt[ii]
            return rt

        for filename in filenames:
            tfilename=Path(root_path,filename)
            if os.path.exists(tfilename):
                rt=MkPath(base,filename,root_path)
                if os.path.islink(tfilename): # it is a Link File
                    if os.path.isfile(filename): # it is a File
                        if link2file:
                            name,ext=self.FileName(tfilename)
                            _md5=None
                            if data or md5sum: # MD5SUM or Data
                                filedata=self.Rw(tfilename,out='byte')
                                if filedata[0]:
                                    if data: rt['data']=filedata[1]
                                    if md5sum: _md5=md5(filedata[1])
                            MkInfo(rt,filename=tfilename,type=self.FileType(tfilename),name=name,ext=ext,md5=_md5)
                    else:
                        MkInfo(rt,filename=tfilename,type='link',dest=os.readlink(tfilename))
                elif os.path.isdir(tfilename): # it is a directory
                    MkInfo(rt,tfilename,type='dir')
                elif os.path.isfile(tfilename): # it is a File
                    name,ext=self.FileName(tfilename)
                    _md5=None
                    if data or md5sum: # MD5SUM or Data
                        filedata=self.Rw(tfilename,out='byte')
                        if filedata[0]:
                            if data: rt['data']=filedata[1]
                            if md5sum: _md5=md5(filedata[1])
                    MkInfo(rt,filename=tfilename,type=self.FileType(tfilename),name=name,ext=ext,md5=_md5)
            else:
                MkInfo(rt,filename,exist=False)
        if base:
            return {root_path:base}
        return {}

    def GetInfoFile(self,name,roots=None): #get file info dict from Filename path
        if roots is None: roots=self.FindRP()
        if isinstance(name,str):
            for root in roots:
                rt=self.info.get(root,{})
                for ii in name.split('/'):
                    if ii not in rt: break
                    rt=rt[ii]
                fileinfo=rt.get(' i ',{})
                if fileinfo: return fileinfo
        return False

    def GetList(self,name=None,roots=None): #get file info dict from Filename path
        if roots is None: roots=self.FindRP()
        for root in roots:
            if isinstance(root,str):
                rt=self.info.get(root,{})
                if name != root:
                    rt=self.CdPath(rt,name)
                if isinstance(rt,dict):
                    for ii in rt:
                        if ii == ' i ': continue
                        if rt[ii].get(' i ',{}).get('type') == 'dir':
                            print(ii+'/')
                        else:
                            print(ii)
        return False

    def GetFileList(self,name=None,roots=None): #get file info dict from Filename path
        if roots is None: roots=self.FindRP()
        for root in roots:
            if isinstance(root,str):
                rt=self.info.get(root,{})
                if name != root:
                    rt=self.CdPath(rt,name)
                if isinstance(rt,dict):
                    for ii in rt:
                        if ii == ' i ': continue
                        if rt[ii].get(' i ',{}).get('type') == 'dir': continue
                        print(ii)
        return False

    def ExecFile(self,filename,bin_name=None,default=None,work_path='/tmp'):
        # check the filename is excutable in the system bin file then return the file name
        # if compressed file then extract the file and find bin_name file in the extracted directory
        #   and found binary file then return then binary file path
        # if filename is excutable file then return the file path
        # if not found then return default value
        exist=self.GetInfoFile(filename)
        if exist:
            if exist['type'] in ['elf'] and exist['mode'] == 33261:return filename
            if self.Extract(filename,work_path=work_path):
                if bin_name:
                    rt=[]
                    for ff in self.Find(work_path,filename=bin_name):
                        if self.Info(ff).get('mode') == 33261:
                            rt.append(ff)
                    return rt
        else:
            if find_executable(filename): return filename
        return default

    def Basename(self,filename,default=False):
        if isinstance(filename,str):return os.path.basename(filename)
        return default
        
    def Dirname(self,filename,bin_name=None,default=False):
        if not isinstance(filename,str): return default
        if bin_name is None: return os.path.dirname(filename)
        if not isinstance(bin_name,str): return default
        bin_info=bin_name.split('/')
        bin_n=len(bin_info)
        filename_info=filename.split('/')
        filename_n=len(filename_info)
        for ii in range(0,bin_n):
            if filename_info[filename_n-1-ii] != bin_info[bin_n-1-ii]: return default
        #return '/'.join(filename_info[:-bin_n])
        return Join(filename_info[:-bin_n],symbol='/')

    def Find(self,filename,default=[]):
        if not isinstance(filename,str): return default
        filename=os.path.basename(filename)
        if os.path.isdir(self.root_path):
            rt = []
            for base, dirs, files in os.walk(self.root_path):
                found = fnmatch.filter(files, filename)
                rt.extend(os.path.join(base, f) for f in found)
            return rt
        return default
 
#    def Decompress(self,filename,work_path='/tmp',info={},del_org_file=False):
#        if not info and isinstance(filename,str) and os.path.isfile(filename): info=self.Get(filename)
#        filetype=info.get('type',None)
#        fileext=info.get('ext',None)
#        if filetype and fileext:
#            # Tar stuff
#            if fileext in ['tgz','tar','tar.gz','tar.bz2','tar.xz'] and filetype in ['gzip','tar','bzip2','lzma','xz','bz2']:
#                tf=tarfile.open(filename)
#                tf.extractall(work_path)
#                tf.close()
#            elif fileext in ['zip'] and filetype in ['compress']:
#                with zipfile.ZipFile(filename,'r') as zf:
#                    zf.extractall(work_path)
#            if del_org_file: os.unline(filename)
#            return True
#        return False

    def Rw(self,name,data=None,out='byte',append=False,read=None,overwrite=True,finfo={},file_only=True,default={'err'}):
        if isinstance(name,str):
            if data is None: # Read from file
                if os.path.isfile(name) or (not file_only and os.path.exists(name)):
                    try:
                        if read in ['firstread','firstline','first_line','head','readline']:
                            with open(name,'rb') as f:
                                data=f.readline()
                        elif not file_only:
                            data=os.open(name,os.O_RDONLY)
                        else:
                            with open(name,'rb') as f:
                                data=f.read()
                        if out in ['string','str']:
                            return True,CONVERT(data).Str()
                        else:
                            return True,data
                    except:
                        pass
                if default == {'err'}:
                    return False,'File({}) not found'.format(name)
                return False,default
            else: # Write to file
                file_path=os.path.dirname(name)
                if not file_path or os.path.isdir(file_path): # current dir or correct directory
                    if append:
                        with open(name,'ab') as f:
                            f.write(BYTES().From(data))
                    elif not file_only:
                        try:
                            f=os.open(name,os.O_RDWR)
                            os.write(f,data)
                        except:
                            return False,None
                    else:
                        with open(name,'wb') as f:
                            f.write(BYTES().From(data))
                        if isinstance(finfo,dict) and finfo: self.SetIdentity(name,**finfo)
                        #mode=self.Mode(mode)
                        #if mode: os.chmod(name,int(mode,base=8))
                        #if uid and gid: os.chown(name,uid,gid)
                        #if mtime and atime: os.utime(name,(atime,mtime))# Time update must be at last order
                    return True,None
                if default == {'err'}:
                    return False,'Directory({}) not found'.format(file_path)
                return False,default
        if default == {'err'}:
            return False,'Unknown type({}) filename'.format(name)
        return False,default

    def Mode(self,val,default=False):
        if isinstance(val,int):
            #if val >= 32768:  # stat
            if val > 511:
                return oct(val)[-4:]
            elif val > 63:    # mask
                return oct(val)
        elif isinstance(val,str):
            try:
                cnt=len(val)
                val=int(val)
                if cnt >=3 and cnt <=4 and val >= 100 and val <= 777: # string type of permission number 
                    return '%04d'%(val)
                    #return int(val,8)
            except:           # permission string
                if len(val) != 9: return 'Bad permission length'
                if not all(val[k] in 'rw-' for k in [0,1,3,4,6,7]): return 'Bad permission format (read-write)'
                if not all(val[k] in 'xs-' for k in [2,5]): return 'Bad permission format (execute)'
                if val[8] not in 'xt-': return 'Bad permission format (execute other)'

                m = 0

                if val[0] == 'r': m |= stat.S_IRUSR
                if val[1] == 'w': m |= stat.S_IWUSR
                if val[2] == 'x': m |= stat.S_IXUSR
                if val[2] == 's': m |= stat.S_IXUSR | stat.S_ISUID

                if val[3] == 'r': m |= stat.S_IRGRP
                if val[4] == 'w': m |= stat.S_IWGRP
                if val[5] == 'x': m |= stat.S_IXGRP
                if val[5] == 's': m |= stat.S_IXGRP | stat.S_ISGID

                if val[6] == 'r': m |= stat.S_IROTH
                if val[7] == 'w': m |= stat.S_IWOTH
                if val[8] == 'x': m |= stat.S_IXOTH
                if val[8] == 't': m |= stat.S_IXOTH | stat.S_ISVTX
                return oct(m)
        return default

    # Find filename's root path and filename according to the db
    def FindRP(self,filename=None,default=None):
        if isinstance(filename,str) and self.info:
            info_keys=list(self.info.keys())
            info_num=len(info_keys)
            if filename[0] != '/': 
                if info_num == 1: return info_keys[0]
                return self.root_path
            aa='/'
            filename_a=filename.split('/')
            for ii in range(1,len(filename_a)):
                aa=Path(aa,filename_a[ii]) 
                if aa in info_keys:
                    #remain_path='/'.join(filename_a[ii+1:])
                    remain_path=Join(filename_a[ii+1:],symbol='/')
                    if info_num == 1: return aa,remain_path
                    # if info has multi root path then check filename in the db of each root_path
                    if self.GetInfoFile(remain_path,aa): return aa,remain_path
        elif self.info:
            return list(self.info.keys())
        return default
            
    def ExtractRoot(self,**opts):
        root_path=opts.get('root_path',[])
        dirpath=opts.get('dirpath')
        sub_dir=opts.get('sub_dir',False)
        if isinstance(root_path,str):
            root_path=[root_path]
        #if not os.path.isdir(opts.get('dest')): os.makedirs(opts.get('dest'))
        if self.Mkdir(opts.get('dest'),force=True) is False: return False
        for rp in root_path:
            new_dest=opts.get('dest')
            if dirpath:
                rt=self.CdPath(self.info[rp],dirpath)
                if rt is False: 
                    print('{} not found'.format(dirpath))
                    return
            else:
                dirpath=''
                rt=self.info[rp]

            rinfo=rt.get(' i ',{})
            rtype=rinfo.get('type')
            #dir:directory,None:root directory
            if rtype not in ['dir',None]: # File / Link
                mydest=os.path.dirname(dirpath)
                myname=os.path.basename(dirpath)
                if mydest:
                    mydest=os.path.join(new_dest,mydest)
                else:
                    mydest=new_dest
                #if not os.path.isdir(mydest): os.makedirs(mydest)
                if self.Mkdir(mydest,force=True,info=rinfo) is False: return False
                if rtype == 'link':
                    os.symlink(rinfo['dest'],os.path.join(mydest,myname))
                    self.SetIdentity(os.path.join(mydest,myname),**rinfo)
                else: # File
                    if 'data' in rt: self.Rw(Path(mydest,myname),data=rt['data'],finfo=rinfo)
                    else: print('{} file have no data'.format(dirpath))
#                self.SetIdentity(os.path.join(mydest,myname),**rinfo)
            else: # directory or root DB
                for ii in rt:
                    if ii == ' i ': continue
                    finfo=rt[ii].get(' i ',{})
                    ftype=finfo.get('type')
                    if ftype == 'dir': 
                        mydir=os.path.join(new_dest,ii)
                        self.Mkdir(mydir,force=True,info=finfo)
                        #self.SetIdentity(mydir,**finfo)
                        # Sub directory
                        if sub_dir: self.ExtractRoot(dirpath=os.path.join(dirpath,ii),root_path=rp,dest=os.path.join(new_dest,ii),sub_dir=sub_dir)
                        #if dmtime and datime: os.utime(mydir,(datime,dmtime)) # Time update must be at last order
                    elif ftype == 'link':
                        iimm=os.path.join(new_dest,ii)
                        if not os.path.exists(iimm):
                            os.symlink(finfo['dest'],iimm)
                            self.SetIdentity(iimm,**finfo)
                    else: # File
                        if 'data' in rt[ii]: self.Rw(os.path.join(new_dest,ii),data=rt[ii]['data'],finfo=finfo)
                        else: print('{} file have no data'.format(ii))

    def Mkdir(self,path,force=False,info={}):
        if not isinstance(path,str): return None
        if os.path.exists(path): return None
        if force:
            try:
                os.makedirs(path)
                if isinstance(info,dict) and info: self.SetIdentity(path,**info)
            except:
                return False
        else:
            try:
                os.mkdir(path)
                if isinstance(info,dict) and info: self.SetIdentity(path,**info)
            except:
                return False
        return True

    def MkTemp(self,filename=None,suffix='-XXXXXXXX',opt='dry',base_dir='/tmp',custom=None):
        if filename is None:
            filename=os.path.join(base_dir,Random(length=len(suffix)-1,strs=custom,mode='str'))
        dir_name=os.path.dirname(filename)
        file_name=os.path.basename(filename)
        name, ext = os.path.splitext(file_name)
        if type(suffix) is not str:
            suffix='-XXXXXXXX'
        num_type='.%0{}d'.format(len(suffix)-1)
        if dir_name == '.':
            dir_name=os.path.dirname(os.path.realpath(__file__))
        elif dir_name == '':
            dir_name=base_dir
        def new_name(name,ext=None,ext2=None):
            if ext:
                if ext2:
                    return '{}{}{}'.format(name,ext,ext2)
                return '{}{}'.format(name,ext)
            if ext2:
                return '{}{}'.format(name,ext2)
            return name
        def new_dest(dest_dir,name,ext=None):
            if os.path.isdir(dest_dir) is False:
                return False
            i=0
            new_file=new_name(name,ext)
            while True:
                rfile=os.path.join(dest_dir,new_file)
                if os.path.exists(rfile) is False:
                    return rfile
                if suffix:
                    if '0' in suffix or 'n' in suffix or 'N' in suffix:
                        if suffix[-1] not in ['0','n']:
                            new_file=new_name(name,num_type%i,ext)
                        else:
                            new_file=new_name(name,ext,num_type%i)
                    elif 'x' in suffix or 'X' in suffix:
                        rnd_str='.{}'.format(Random(length=len(suffix)-1,mode='str'))
                        if suffix[-1] not in ['X','x']:
                            new_file=new_name(name,rnd_str,ext)
                        else:
                            new_file=new_name(name,ext,rnd_str)
                    else:
                        if i == 0:
                            new_file=new_name(name,ext,'.{}'.format(suffix))
                        else:
                            new_file=new_name(name,ext,'.{}.{}'.format(suffix,i))
                else:
                    new_file=new_name(name,ext,'.{}'.format(i))
                i+=1
        new_dest_file=new_dest(dir_name,name,ext)
        if opt in ['file','f']:
           os.mknode(new_dest_file)
        elif opt in ['dir','d','directory']:
           os.mkdir(new_dest_file)
        else:
           return new_dest_file

    def SetIdentity(self,path,**opts):
        if os.path.exists(path):
            chmod=self.Mode(opts.get('mode',None))
            uid=opts.get('uid',None)
            gid=opts.get('gid',None)
            atime=opts.get('atime',None)
            mtime=opts.get('mtime',None)
            try:
                if chmod: os.chmod(path,int(chmod,base=8))
                if uid and gid: os.chown(path,uid,gid)
                if mtime and atime: os.utime(path,(atime,mtime)) # Time update must be at last order
            except:
                pass

    def Extract(self,*path,**opts):
        dest=opts.get('dest',None)
        root_path=opts.get('root_path',None)
        sub_dir=opts.get('sub_dir',False)
        if dest is None: return False
        if not path: 
            self.ExtractRoot(root_path=self.FindRP(),dest=dest,sub_dir=sub_dir)
        else:
            for filepath in path:
                fileRF=self.FindRP(filepath)
                if isinstance(fileRF,tuple):
                    root_path=[fileRF[0]]
                    filename=fileRF[1]
                    self.ExtractRoot(root_path=root_path,dirpath=filename,dest=dest,sub_dir=sub_dir)
                elif isinstance(fileRF,list):
                    self.ExtractRoot(root_path=fileRF,dest=dest,sub_dir=sub_dir)

    def Save(self,filename):
        pv=b'3'
        if PyVer(2): pv=b'2'
        #self.Rw(filename,data=pv+bz2.compress(pickle.dumps(self.info,protocol=2)))
        self.Rw(filename,data=pv+Compress(pickle.dumps(self.info,protocol=2),mode='lz4'))

    def Open(self,filename):
        if not os.path.isfile(filename):
            print('{} not found'.format(filename))
            return False
        data=self.Rw(filename)
        if data[0]:
            pv=data[1][0]
            if pv == '3' and PyVer(2):
                print('The data version is not matched. Please use Python3')
                return False
            # decompress data
            try:
                #dcdata=bz2.BZ2Decompressor().decompress(data[1][1:])
                dcdata=Decompress(data[1][1:],mode='lz4')
            except:
                print('This is not KFILE format')
                return False
            try:
                self.info=pickle.loads(dcdata) # Load data
            except:
                try:
                    self.info=pickle.loads(dcdata,encoding='latin1') # Convert 2 to 3 format
                except:
                    print('This is not KFILE format')
                    return False
        else:
            print('Can not read {}'.format(filename))
            return False

    def Cd(self,data,path,sym='/'):
        if Type(data,'module') and data == os:
            if isinstance(path,str):
                data.chdir(path)
                return data
        else:
            if isinstance(path,int): path='{}'.format(path)
            for ii in path.split(sym):
                if isinstance(data,dict):
                    if ii in data:
                        data=data[ii]
                elif isinstance(data,(list,tuple)):
                    if not isinstance(ii,str) or not ii.isdigit(): continue
                    ii=int(ii)
                    if len(data) > ii:
                        data=data[ii]
            return data

    def Path(self,filanem=None):
        if filanem:
            return os.path.dirname(os.path.realpath(filename))
        return os.path.dirname(os.path.realpath((inspect.stack()[-1])[1]))
        #if '__file__' in globals() : return os.path.dirname(os.path.realpath(__file__))

    def Rm(self,filelist):
        if isinstance(filelist,str):
            filelist=filelist.split(',')
        if isinstance(filelist,(list,tuple)):
            for ii in list(filelist):
                if os.path.isfile(ii):
                    os.unlink(ii)
                else:
                    print('not found {0}'.format(ii))

class WEB:
    def __init__(self,request=None):
        if request:
            self.requests=request
        else:
            self.requests=requests

    def Session(self):
        return self.requests.session._get_or_create_session_key()

    def ClientIp(self):
        x_forwarded_for = self.requests.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.requests.META.get('REMOTE_ADDR')
        return ip

    def ServerIp(self):
        return self.requests.get_host().split(':')

    def Request(self,host_url,**opts):
        # remove SSL waring error message (test)
        self.requests.packages.urllib3.disable_warnings()

        mode=opts.get('mode','get')
        max_try=opts.get('max_try',3)
        auth=opts.get('auth',None)
        user=opts.get('user',None)
        ip=opts.get('ip',None)
        port=opts.get('port',None)
        passwd=opts.get('passwd',None)
        timeout=opts.get('timeout',None)
        https=opts.get('https',False)
        verify=opts.get('verify',True)
        request_url=opts.get('request_url',None)
        log=opts.get('log',None)
        log_level=opts.get('log_level',8)
        logfile=opts.get('logfile',None)
        ping=opts.get('ping',False)
        if https:
            verify=False
        if auth is None and user and passwd:
            if type(user) is not str or type(passwd) is not str:
                printf("user='<user>',passwd='<pass>' : format(each string)",dsp='e',log=log,log_level=log_level,logfile=logfile)
                return False,"user='<user>',passwd='<pass>' : format(each string)"
            auth=(user,passwd)
        if auth and type(auth) is not tuple:
            printf("auth=('<user>','<pass>') : format(tuple)",dsp='e',log=log,log_level=log_level,logfile=logfile)
            return False,"auth=('<user>','<pass>') : format(tuple)"
        data=opts.get('data',None) # dictionary format
        if data and type(data) is not dict:
            printf("data={'<key>':'<val>',...} : format(dict)",dsp='e',log=log,log_level=log_level,logfile=logfile)
            return False,"data={'<key>':'<val>',...} : format(dict)"
        json_data=opts.get('json',None) # dictionary format
        if json_data and type(json_data) is not dict:
            printf("data={'<key>':'<val>',...} : format(dict)",dsp='e',log=log,log_level=log_level,logfile=logfile)
            return False,"json={'<key>':'<val>',...} : format(dict)"
        files=opts.get('files',None) # dictionary format
        if files and type(files) is not dict:
            printf("files = { '<file parameter name>': (<filename>, open(<filename>,'rb'))} : format(dict)",dsp='e',log=log,log_level=log_level,logfile=logfile)
            return False,"files = { '<file parameter name>': (<filename>, open(<filename>,'rb'))} : format(dict)"
        if type(host_url) is str:
            chk_dest=re.compile('http[s]://([a-zA-Z0-9.]*)[:/]').findall(host_url)
            if len(chk_dest): chk_dest=chk_dest[0]
            if host_url.find('https://') == 0:
                verify=False
        elif ip:
            chk_dest='{}'.format(ip)
            if verify:
                host_url='http://{}'.format(ip)
            else:
                host_url='https://{}'.format(ip)
            if port:
                host_url='{}:{}'.format(host_url,port)
            if request_url:
                host_url='{}/{}'.format(host_url,request_url)
        else:
            return False,'host_url or ip not found'
        if ping and chk_dest:
            if not ping(chk_dest,timeout_sec=3):
                return False,'Can not access to destination({})'.format(chk_dest)
        ss = self.requests.Session()
        for j in range(0,max_try):
            if mode == 'post':
                try:
                    r =ss.post(host_url,verify=verify,auth=auth,data=data,files=files,timeout=timeout,json=json_data)
                    return True,r
                except:
                    pass
            else:
                try:
                    r =ss.get(host_url,verify=verify,auth=auth,data=data,files=files,timeout=timeout,json=json_data)
                    return True,r
                except:
                    pass
            #except requests.exceptions.RequestException as e:
            host_url_a=host_url.split('/')[2]
            server_a=host_url_a.split(':')
            if len(server_a) == 1:
                printf("Server({}) has no response (wait {}/{} (10s))".format(server_a[0],j,max_try),dsp='e',log=log,log_level=log_level,logfile=logfile)
            else:
                printf("Server({}:{}) has no response (wait {}/{} (10s))".format(server_a[0],server_a[1],j,max_try),dsp='e',log=log,log_level=log_level,logfile=logfile)
            TIME().Sleep(10)
        return False,'TimeOut'

    def str2url(self,string):
        if string is None: return ''
        if type(string) is str:
            return string.replace('+','%2B').replace('?','%3F').replace('/','%2F').replace(':','%3A').replace('=','%3D').replace(' ','+')
        return string

class EMAIL:
    # Port Info
    # GMAIL TTLS : 587
    # Postfix    : 25
    def __init__(self,server='127.0.0.1',port=25,user=None,password=None,ssl=False,tls=False):
        self.server=server
        self.port=port
        self.user=user
        self.password=password
        self.ssl=ssl
        self.tls=tls

    def Body(self,sender,receivers,title,msg,filename=None,html=False):
        if isinstance(receivers,str):
            receivers=receivers.split(',')
        if not isinstance(receivers,list):
            print('To mailing list issue')
            return False
        if filename:
            _body=MIMEMultipart()
            if isinstance(sender,tuple) and len(sender) == 2:
                #format: ('NAME',EMAIL)
                _body['From'] = email.utils.formataddr(sender)
            else:
                _body['From'] = sender
            if isinstance(receivers[0],tuple) and len(receivers[0]) == 2:
                #format: ('NAME',EMAIL)
                _body['To'] = email.utils.formataddr(receivers[0])
            else:
                _body['To'] = receivers[0]
            _body['Subject'] = title
            if html:
                _body.attach(MIMEText(msg, "html"))
            else:
                _body.attach(MIMEText(msg, "plain"))
            with open(filename,'rb') as attachment:
                part=MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition','attachment; filename="{filename}"')
            _body.attach(part)
        else:
            if html:
                _body=MIMEMultipart('alternative')
                _body.attach(MIMEText(msg,'html'))
            else:
                _body = MIMEText(msg)
            _body['Subject'] = title
            if isinstance(sender,tuple) and len(sender) == 2:
                #format: ('NAME',EMAIL)
                _body['From'] = email.utils.formataddr(sender)
            else:
                _body['From'] = sender
            if isinstance(receivers[0],tuple) and len(receivers[0]) == 2:
                #format: ('NAME',EMAIL)
                _body['To'] = email.utils.formataddr(receivers[0])
            else:
                _body['To'] = receivers[0]
        return _body.as_string()

    def Server(self):
        if self.ssl:
            if not self.password:
                print('It required mail server({}) login password'.format(self.server))
                return False
            context = ssl.create_default_context()
            if self.user is None: self.user=sender
            try:
                server=smtplib.SMTP_SSL(self.server,self.port,context=context)
                server.login(self.user, self.password)
            except:
                print('Login fail at the server({})'.format(self.server))
                return False
        else:
            server=smtplib.SMTP(self.server,self.port)
            if self.tls:
                if not self.password:
                    print('It required mail server({}) login password'.format(self.server))
                    return False
                if self.ssl:
                    context = ssl.create_default_context()
                    server.starttls(context=context)
                else:
                    server.starttls()
                if self.user is None: self.user=sender
                server.login(self.user, self.password)
        return server

    #def Send(self,sender,receivers,title='Subject',msg='MSG',dbg=False,filename=None,html=False):
    def Send(self,*receivers,**opts):
        sender=opts.get('sender',opts.get('from','root@localhost'))
        title=opts.get('title',opts.get('subject','Unknown Subject'))
        msg=opts.get('msg',opts.get('body','No body'))
        dbg=opts.get('dbg',False)
        filename=opts.get('filename')
        html=opts.get('html',False)
        server=self.Server()
        if not server: return False
        if dbg: server.set_debuglevel(True)
        if len(receivers) == 1 and isinstance(receivers[0],str):
            receivers=receivers[0].split(',')
        elif receivers:
            receivers=list(receivers)
        else:
            receivers=opts.get('to',opts.get('recievers'))
            if isinstance(receivers,str):
                receivers=receivers.split(',')
            elif isinstance(receivers,tuple) and len(receivers) == 2 and isinstance(receivers[0],str) and '@' not in receivers[0]:
                receivers=[receivers]
        email_body=self.Body(sender,receivers,title,msg,filename=filename,html=html)
        if email_body:
            try:
                server.sendmail(sender, receivers, email_body)
                server.quit()
                return True
            except:
                return False
        else:
            print('something wrong input')

class ANSI:
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    def Clean(self,data):
        if data:
            if isinstance(data,str):
                return self.ansi_escape.sub('',data)
            elif isinstance(data,list):
                new_data=[]
                for ii in data:
                    new_data.append(self.ansi_escape.sub('',ii))
                return new_data
        return data

class Multiprocessor():
    def __init__(self):
        self.processes = []
        self.queue = Queue()

    @staticmethod
    def _wrapper(func, queue, args, kwargs):
        ret = func(*args, **kwargs)
        queue.put(ret)

    def run(self, func, *args, **kwargs):
        args2 = [func, self.queue, args, kwargs]
        p = Process(target=self._wrapper, args=args2)
        self.processes.append(p)
        p.start()

    def wait(self):
        rets = []
        for p in self.processes[:]:
            ret = self.queue.get()
            rets.append(ret)
            self.processes.remove(p)
        return rets

####################################FUNCTION##################################################
class FUNCTION:
    def __init__(self,func=None):
        if func:
            if isinstance(func,str):
                func=Global(func)
            self.func=func

    def Name(self,sub=False):
        if sub:
            try:
                return traceback.extract_stack(None, 2+1)[0][2]
            except:
                return False
        return traceback.extract_stack(None, 2)[0][2]

    def ParentName(self,sub=False):
        if sub:
            try:
                return traceback.extract_stack(None, 3+1)[0][2]
            except:
                return False
        return traceback.extract_stack(None, 3)[0][2]

    def Args(self,func=None,**opts):
        mode=opts.get('mode',opts.get('field','defaults'))
        default=opts.get('default',None)
        if func is None: func=self.func
        if not Type(func,'function'):
            return default
        rt={}
        args, varargs, keywords, defaults = inspect.getargspec(func)
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
        if Type(mode,(list,tuple)):
            rts=[]
            for ii in mode:
                rts.append(rt.get(ii,default))
            return rts
        else:
            if mode in rt:
                return rt[mode]
            return rt

    def List(self,obj=None):
        aa={}
        if isinstance(obj,str):
           obj=sys.modules.get(obj)
        else:
           obj=GET().Me()
        if obj is not None:
            for name,fobj in inspect.getmembers(obj):
                if inspect.isfunction(fobj): # inspect.ismodule(obj) check the obj is module or not
                    aa.update({name:fobj})
        return aa

    def CallerName(self,default=False,detail=False):
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

    def Is(self,find=None,src=None):
        if find is None: find=self.func
        if src is None:
            if isinstance(find,str):
                #find=sys.modules.get(find)
                find=Global().get(find)
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


class SCREEN:
    def Kill(self,title):
        ids=self.Id(title)
        if len(ids) == 1:
            rc=rshell('''screen -X -S {} quit'''.format(ids[0]))
            if rc[0] == 0:
                return True
            return False

    def Monitor(self,title,ip,ipmi_user,ipmi_pass,find=[],timeout=600):
        if type(title) is not str or not title:
            print('no title')
            return False
        scr_id=self.Id(title)
        if scr_id:
            print('Already has the title at {}'.format(scr_id))
            return False
        cmd="ipmitool -I lanplus -H {} -U {} -P {} sol activate".format(ip,ipmi_user,ipmi_pass)
        # Linux OS Boot (Completely kernel loaded): find=['initrd0.img','\xff']
        # PXE Boot prompt: find=['boot:']
        # PXE initial : find=['PXE ']
        # DHCP initial : find=['DHCP']
        # ex: aa=screen_monitor('test','ipmitool -I lanplus -H <bmc ip> -U ADMIN -P ADMIN sol activate',find=['initrd0.img','\xff'],timeout=300)
        log_file=self.Log(title,cmd)
        init_time=TIME().Int()
        if log_file:
            mon_line=0
            old_mon_line=-1
            found=0
            find_num=len(find)
            cnt=0
            while True:
                if TIME().Int() - init_time > timeout :
                    print('Monitoring timeout({} sec)'.format(timeout))
                    if self.Kill(title):
                        os.unlink(log_file)
                    break
                with open(log_file,'rb') as f:
                    tmp=f.read()
                #tmp=_u_byte2str(tmp)
                tmp=CONVERT(tmp).Str()
                if '\x1b' in tmp:
                    tmp_a=tmp.split('\x1b')
                elif '\r\n' in tmp:
                    tmp_a=tmp.split('\r\n')
                elif '\r' in tmp:
                    tmp_a=tmp.split('\r')
                else:
                    tmp_a=tmp.split('\n')
                tmp_n=len(tmp_a)
                for ss in tmp_a[tmp_n-2:]:
                    if 'SOL Session operational' in ss:
                        # control+c : "^C", Enter: "^M", any command "<linux command> ^M"
                        rshell('screen -S {} -p 0 -X stuff "^M"'.format(title))
                        cnt+=1
                        if cnt > 5:
                            print('maybe not activated SOL or BMC issue')
                            if self.Kill(title):
                                os.unlink(log_file)
                            return False
                        continue
                if find:
                    for ii in tmp_a[mon_line:]:
                        if find_num == 0:
                            print(ii)
                        else:
                            for ff in range(0,find_num):
                                find_i=find[found]
                                if ii.find(find_i) < 0:
                                    break
                                found=found+1
                                if found >= find_num:
                                    if self.Kill(title):
                                        os.unlink(log_file)
                                    return True
                    if tmp_n > 1:
                        mon_line=tmp_n -1
                    else:
                        mon_line=tmp_n
                else:
                    if self.Kill(title):
                        os.unlink(log_file)
                    return True
                TIME().Sleep(1)
        return False


    def Id(self,title=None):
        scs=[]
        rc=rshell('''screen -ls''')
        if rc[0] == 1:
            for ii in rc[1].split('\n')[1:]:
                jj=ii.split()
                if len(jj) == 2:
                    if title:
                        zz=jj[0].split('.')
                        if zz[1] == title:
                            scs.append(jj[0])
                    else:
                        scs.append(jj[0])
        return scs

    def Log(self,title,cmd):
        # ipmitool -I lanplus -H 172.16.114.80 -U ADMIN -P ADMIN sol activate
        pid=os.getpid()
        tmp_file=FILE().MkTemp('/tmp/.slc.{}_{}.cfg'.format(title,pid))
        log_file=FILE().MkTemp('/tmp/.screen_ck_{}_{}.log'.format(title,pid))
        if os.path.isfile(log_file):
            log_file=''
        with open(tmp_file,'w') as f:
            f.write('''logfile {}\nlogfile flush 0\nlog on\n'''.format(log_file))
        if os.path.isfile(tmp_file):
            rc=rshell('''screen -c {} -dmSL "{}" {}'''.format(tmp_file,title,cmd))
            if rc[0] == 0:
                for ii in range(0,50):
                    if os.path.isfile(log_file):
                        os.unlink(tmp_file)
                        return log_file
                    TIME().Sleep(0.1)

####################################STRING##################################################
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
    #if rt and out in ['str',str]: return new_line.join(rt)
    if rt and out in ['str',str]: return Join(rt,symbol=new_line)
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
                    #return new_line.join(rc)
                    return Join(rc,symbol=new_line)
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
        #return new_line.join(rc)
        return Join(rc,symbol=new_line)
    return rc

def Path(*inp,**opts):
    sym=opts.get('sym','/')
    out=opts.get('out','str')
    if inp:
        full_path=[]
        if isinstance(inp[0],str):
            root_a=inp[0].split(sym)
            if len(root_a):
                if root_a[0] == '~': 
                    full_path=os.environ['HOME'].split(sym)
                else:
                    full_path=[root_a[0]]
            for zz in range(1,len(root_a)):
                if full_path and not root_a[zz]: continue
                full_path.append(root_a[zz])
        for ii in inp[1:]:
            if isinstance(ii,str):
                for zz in ii.split(sym):
                    if full_path and not zz: continue
                    if zz == '.': continue
                    if full_path and full_path[-1] != '..' and zz == '..':
                        del full_path[-1]
                        continue
                    full_path.append(zz)
        if full_path:
            #if out in [str,'str']:return sym.join(full_path)
            if out in [str,'str']:return Join(full_path,symbol=sym)
            return full_path
    return os.path.dirname(os.path.abspath(__file__)) # Not input then get current path

####################################KEYS##################################################
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

def krc(rt,chk='_',rtd={'GOOD':[True,'True','Good','Ok','Pass',{'OK'},0],'FAIL':[False,'False','Fail',{'FAL'}],'NONE':[None,'None','N/A',{'NA'}],'IGNO':['IGNO','Ignore',{'IGN'}],'ERRO':['ERR','Error','error','erro','ERRO',{'ERR'}],'WARN':['Warn','warn',{'WAR'}],'UNKN':['Unknown','UNKN',{'UNK'}],'JUMP':['Jump',{'JUMP'}],'TOUT':['timeout','TimeOut','time out','Time Out','TMOUT','TOUT',{'TOUT'}],'REVD':['cancel','Cancel','CANCEL','REV','REVD','Revoked','revoked','revoke','Revoke',{'REVD'}],'LOST':['lost','connection lost','Connection Lost','Connection lost','CONNECTION LOST',{'LOST'}]},default=False):
    def trans(irt):
        type_irt=type(irt)
        for ii in rtd:
            for jj in rtd[ii]:
                if type(jj) == type_irt and ((type_irt is str and jj.lower() == irt.lower()) or jj == irt):
                    return ii
        return 'UNKN'
    rtc=Get(rt,'0|rc',out='raw',err='ignore',check=(list,tuple,dict))
    nrtc=trans(rtc)
    if chk != '_':
        if not isinstance(chk,list): chk=[chk]
        for cc in chk:
            if trans(cc) == nrtc:
                return True
            if nrtc == 'UNKN' and default == 'org':
                return rtc
        if default == 'org': return rt
        return default
    return nrtc

def Replace(src,replace_what,replace_to,default=None):
    if isinstance(src,str):
        if replace_what[-1] == '$' or replace_what[0] == '^':
            return re.sub(replace_what, replace_to, src)
        else:
            head, _sep, tail = src.rpartition(replace_what)
            return head + replace_to + tail
    if default == {'org'}: return src
    return default

def Insert(src,*inps,**opts):
    start=opts.pop('at',0)
    default=opts.pop('default',False)
    err=opts.pop('err',False)
    force=opts.pop('force',False)
    uniq=opts.pop('uniq',False)
    if isinstance(src,(list,tuple,str)):
        tuple_out=False
        if isinstance(src,tuple) and force:
            src=list(src)
            tuple_out=True
        if uniq:
            new=[]
            for ii in inps:
                if ii not in src:
                    new.append(ii)
            inps=tuple(new)
        if isinstance(at,str):
            if at in ['start','first']: src=list(inps)+src
            if at in ['end','last']: src=src+list(inps)
        elif len(src) == 0:
            src=list(inps)
        elif isinstance(start,int) and len(src) > start:
            src=src[:start]+list(inps)+src[start:]
        else:
            if err:
                return default
            src=src+list(inps)
        if tuple_out: return tuple(src)
    elif isinstance(src,dict):
        for ii in inps:
            if isinstance(ii,dict):
                 src.update(ii)
        if opts:
            src.update(opts)
    return src

def FirstKey(src,default=None):
    if src:
        if isinstance(src,(list,tuple)): return 0
        try:
            return next(iter(src))
        except:
            return default
    return default

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


def printf(*msg,**opts):
    log_p=False
    log=opts.get('log',None)
    log_level=opts.get('log_level',8)
    dsp=opts.get('dsp','a')
    func_name=opts.get('func_name',None)
    date=opts.get('date',False)
    date_format=opts.get('date_format','[%m/%d/%Y %H:%M:%S]')
    intro=opts.get('intro',None)
    caller=opts.get('caller',False)
    caller_detail=opts.get('caller_detail',False)
    msg=list(msg)
    direct=opts.get('direct',False)
    color=opts.get('color',None)
    color_db=opts.get('color_db',{'blue': 34, 'grey': 30, 'yellow': 33, 'green': 32, 'cyan': 36, 'magenta': 35, 'white': 37, 'red': 31})
    bg_color=opts.get('bg_color',None)
    bg_color_db=opts.get('bg_color_db',{'cyan': 46, 'white': 47, 'grey': 40, 'yellow': 43, 'blue': 44, 'magenta': 45, 'red': 41, 'green': 42})
    attr=opts.get('attr',None)
    attr_db=opts.get('attr_db',{'reverse': 7, 'blink': 5,'concealed': 8, 'underline': 4, 'bold': 1})
    syslogd=opts.get('syslogd',None)

    if direct:
        new_line=opts.get('new_line','')
    else:
        new_line=opts.get('new_line','\n')
    logfile=opts.get('logfile',None)
    logfile_type=type(logfile)
    if logfile_type is str:
        logfile=logfile.split(',')
    elif logfile_type in [list,tuple]:
        logfile=list(logfile)
    else:
        logfile=[]
    for ii in msg:
        if type(ii) is str and ':' in ii:
            logfile_list=ii.split(':')
            if logfile_list[0] in ['log_file','logfile']:
                if len(logfile_list) > 2:
                    for jj in logfile_list[1:]:
                        logfile.append(jj)
                else:
                    logfile=logfile+logfile_list[1].split(',')
                msg.remove(ii)
    if os.getenv('ANSI_COLORS_DISABLED') is None and (color or bg_color or attr):
        reset='''\033[0m'''
        fmt_msg='''\033[%dm%s'''
        if color and color in color_db:
            msg=fmt_msg % (color_db[color],msg)
        if bg_color and bg_color in bg_color_db:
            msg=fmt_msg % (color_db[bg_color],msg)
        if attr and attr in attr_db:
            msg=fmt_msg % (attr_db[attr],msg)
        msg=msg+reset

    # Make a Intro
    intro_msg=''
    if date and syslogd is False:
        intro_msg='[{0}] '.format(datetime.now().strftime(date_format))
    if caller:
        call_name=get_caller_fcuntion_name(detail=caller_detail)
        if call_name:
            if len(call_name) == 3:
                intro_msg=intro_msg+'{}({}:{}): '.format(call_name[0],call_name[1],call_name[2])
            else:
                intro_msg=intro_msg+'{}(): '.format(call_name)
    if intro is not None:
        intro_msg=intro_msg+intro+': '

    # Make a Tap
    tap=''
    for ii in range(0,len(intro_msg)):
        tap=tap+' '

    # Make a msg
    msg_str=''
    for ii in msg:
        if msg_str:
            if new_line:
                msg_str=msg_str+new_line+tap+'{}'.format(ii)
            else:
                msg_str=msg_str+'{}'.format(ii)
        else:
            msg_str=intro_msg+'{}'.format(ii)

    # save msg to syslogd
    if syslogd:
        if syslogd in ['INFO','info']:
            syslog.syslog(syslog.LOG_INFO,msg)
        elif syslogd in ['KERN','kern']:
            syslog.syslog(syslog.LOG_KERN,msg)
        elif syslogd in ['ERR','err']:
            syslog.syslog(syslog.LOG_ERR,msg)
        elif syslogd in ['CRIT','crit']:
            syslog.syslog(syslog.LOG_CRIT,msg)
        elif syslogd in ['WARN','warn']:
            syslog.syslog(syslog.LOG_WARNING,msg)
        elif syslogd in ['DBG','DEBUG','dbg','debug']:
            syslog.syslog(syslog.LOG_DEBUG,msg)
        else:
            syslog.syslog(msg)

    # Save msg to file
    if type(logfile) is str:
        logfile=logfile.split(',')
    if type(logfile) in [list,tuple] and ('f' in dsp or 'a' in dsp):
        for ii in logfile:
            if ii and os.path.isdir(os.path.dirname(ii)):
                log_p=True
                with open(ii,'a+') as f:
                    f.write(msg_str+new_line)
    #if type(log).__name__ == 'function':
    if Type(log,'function'):
         log_func_arg=get_function_args(log,mode='all')
         if 'args' in log_func_arg or 'varargs' in log_func_arg:
             log_p=True
             args=log_func_arg.get('args',[])
             if args and len(args) <= 4 and ('direct' in args or 'log_level' in args or 'func_name' in args):
                 tmp=[]
                 for i in range(0,len(args)):
                     tmp.append(i)
                 if 'direct' in args:
                     didx=args.index('direct')
                     del tmp[didx]
                     args[didx]=direct
                 if 'log_level' in args:
                     lidx=args.index('log_level')
                     del tmp[lidx]
                     args[lidx]=log_level
                 if 'func_name' in args:
                     lidx=args.index('func_name')
                     del tmp[lidx]
                     args[lidx]=func_name
                 if 'date_format' in args:
                     lidx=args.index('date_format')
                     del tmp[lidx]
                     args[lidx]=date_format
                 args[tmp[0]]=msg_str
                 log(*args)
             elif 'keywards' in log_func_arg:
                 log(msg_str,direct=direct,log_level=log_level,func_name=func_name,date_format=date_format)
             elif 'defaults' in log_func_arg:
                 if 'direct' in log_func_arg['defaults'] and 'log_level' in log_func_arg['defaults']:
                     log(msg_str,direct=direct,log_level=log_level)
                 elif 'log_level' in log_func_arg['defaults']:
                     log(msg_str,log_level=log_level)
                 elif 'direct' in log_func_arg['defaults']:
                     log(msg_str,direct=direct)
                 else:
                     log(msg_str)
             else:
                 log(msg_str)
    # print msg to screen
    if (log_p is False and 'a' in dsp) or 's' in dsp or 'e' in dsp:
         if 'e' in dsp:
             sys.stderr.write(msg_str+new_line)
             sys.stderr.flush()
         else:
             sys.stdout.write(msg_str+new_line)
             sys.stdout.flush()
    # return msg
    if 'r' in dsp:
         return msg_str

def printf2(*msg,**opts):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    color_db=opts.get('color_db',{'blue': 34, 'grey': 30, 'yellow': 33, 'green': 32, 'cyan': 36, 'magenta': 35, 'white': 37, 'red': 31})
    bg_color_db=opts.get('bg_color_db',{'cyan': 46, 'white': 47, 'grey': 40, 'yellow': 43, 'blue': 44, 'magenta': 45, 'red': 41, 'green': 42})
    attr_db=opts.get('attr_db',{'reverse': 7, 'blink': 5,'concealed': 8, 'underline': 4, 'bold': 1})
    dsp=opts.get('dsp','s')
    limit=opts.get('limit',None)
    if isinstance(limit,int):
        level=opts.get('level',1)
        if limit < level:
            return
    if not isinstance(dsp,str):
        dsp='s'
    filename=opts.get('filename',None)
    color=opts.get('color',None)
    bgcolor=opts.get('bgcolor',None)
    color_mode=opts.get('color_mode','shell')
    wrap=opts.get('wrap',None)
    length=opts.get('length',None)
    form=opts.get('form',False)

    if opts.get('direct',False):
        new_line=''
        start_new_line=''
    else:
        start_new_line=opts.get('start_new_line','')
        new_line=opts.get('new_line','\n')
    filename=opts.get('filename',None)

    msg_str=''
    for ii in msg:
        if msg_str:
            msg_str='''{}{}{}'''.format(msg_str,new_line,ii)
        else:
            msg_str='''{}'''.format(ii)

    #New line
    if new_line:
        msg_str=msg_str.split(new_line)
    # Cut each line
    if isinstance(length,int):
        length=(length,)
    if isinstance(length,(tuple,list)):
        new_msg_str=[]
        if len(length) == 1:
            for mm in range(0,len(msg_str)):
                new_msg_str=new_msg_str+STR(msg_str[mm]).Cut(head_len=length[0])
        elif  len(length) == 2 and len(msg_str):
            new_msg_str=new_msg_str+STR(msg_str[0]).Cut(head_len=length[0],body_len=length[1])
            if len(msg_str) > 1:
                for mm in range(1,len(msg_str)):
                    new_msg_str=new_msg_str+STR(msg_str[mm]).Cut(head_len=length[1])
        msg_str=new_msg_str
    # wrap each line
    if isinstance(wrap,int):
        wrap=(wrap,)
    if isinstance(wrap,(tuple,list)):
        if len(wrap) == 1:
            for mm in range(0,len(msg_str)):
                msg_str[mm]=tap[0]+msg_str[mm]
        elif  len(wrap) == 2 and len(msg_str):
            msg_str[0]=tap[0]+msg_str[0]
            if len(msg_str) > 1:
                for mm in range(1,len(msg_str)):
                    msg_str[mm]=tap[1]+msg_str[mm]
    #msg_str=new_line.join(msg_str)
    msg_str=Join(msg_str,symbol=new_line)
    if color in ['clear','clean','remove','del','delete','mono']:
        if color_mode == 'shell':
            msg_str=ansi_escape.sub('',msg_str)
    elif color:
        msg_str=COLOR().String(msg_str,color,bg=False,attr=False,mode=color_mode)
    elif bgcolor:
        msg_str=COLOR().String(msg_str,bgcolor,bg=True,mode=color_mode)
    # return msg
    if 'f' in dsp:
        if isinstance(filename,(str,list,tuple)):
             if isinstance(filename,str):filename=filename.split(',')
             for ff in filename:
                 if GET(ff).Dirname():
                     with open(ff,filemode) as f:
                         f.write(msg_str+new_line)
        else:
            dsp=dsp+'s' # if nothing filename then display it on screen
    if 's' in dsp or 'a' in dsp:
         if form:
             try:
                 msg_str=ast.literal_eval(msg_str)
                 pprint(msg_str)
             except:
                 sys.stdout.write(start_new_line+msg_str+new_line)
                 sys.stdout.flush()
         else:
             sys.stdout.write(start_new_line+msg_str+new_line)
             sys.stdout.flush()
    if 'e' in dsp:
         sys.stderr.write(start_new_line+msg_str+new_line)
         sys.stderr.flush()
    if 'r' in dsp:
         if form:
             try:
                 return ast.literal_eval(msg_str)
             except:
                 return start_new_line+msg_str+new_line
         else:
             return start_new_line+msg_str+new_line

def sprintf(string,*inps,**opts):
    if not isinstance(string,str): return False,string
    #"""ipmitool -H %(ipmi_ip)s -U %(ipmi_user)s -P '%(ipmi_pass)s' """%(**opts)
    #"""{app} -H {ipmi_ip} -U {ipmi_user} -P '{ipmi_pass}' """.format(**opts)
    #"""{} -H {} -U {} -P '{}' """.format(*inps)
    #"""{0} -H {1} -U {2} -P '{3}' """.format(*inps)
    ffall=[re.compile('\{(\d*)\}').findall(string),re.compile('\{(\w*)\}').findall(string),re.compile('\%\((\w*)\)s').findall(string),re.compile('\{\}').findall(string)]
    i=0
    for tmp in ffall:
        if i in [0,1]: tmp=[ j  for j in tmp if len(j) ]
        if tmp:
            if i == 0:
                mx=0
                for z in tmp:
                    if int(z) > mx: mx=int(z)
                if inp:
                    if len(inp) > mx: return string.format(*inp)
                elif opts:
                    if len(opts) > mx: return string.format(*opts.values())
                return False,"Need more input (tuple/list) parameters(require {})".format(mx)
            elif 0< i < 2:
                new_str=''
                string_a=string.split()
                oidx=0
                for ii in tmp:
                    idx=None
                    if '{%s}'%(ii) in string_a:
                        idx=string_a.index('{%s}'%(ii))
                    elif "'{%s}'"%(ii) in string_a:
                        idx=string_a.index("'{%s}'"%(ii))
                    if isinstance(idx,int):
                        if ii in opts:
                            string_a[idx]=string_a[idx].format(**opts)
                    elif ii in opts:
                        for jj in range(0,len(string_a)):
                           if '{%s}'%(ii) in string_a[jj]:
                               string_a[jj]=string_a[jj].format(**opts)
                #return True,' '.join(string_a)
                return True,Join(string_a,symbol=' ')
            elif i == 2:
                new_str=''
                string_a=string.split()
                oidx=0
                for ii in tmp:
                    idx=None
                    if '%({})s'.format(ii) in string_a:
                        idx=string_a.index('%({})s'.format(ii))
                    elif "'%({})'".format(ii) in string_a:
                        idx=string_a.index("'%({})s'".format(ii))
                    if isinstance(idx,int):
                        if ii in opts:
                            string_a[idx]=string_a[idx]%(opts)
                    elif ii in opts:
                        for jj in range(0,len(string_a)):
                           if '%({})s'.format(ii) in string_a[jj]:
                               string_a[jj]=string_a[jj]%(opts)
                #return True,' '.join(string_a)
                return True,Join(string_a,symbol=' ')
            elif i == 3:
                if inp:
                    if len(tmp) == len(inp): return string.format(*inp)
                    return False,"Mismatched input (tuple/list) number (require:{}, input:{})".format(len(tmp),len(inp))
                elif opts:
                    if len(tmp) == len(opts): return string.format(*opts.values())
                    return False,"Mismatched input (tuple/list) number (require:{}, input:{})".format(len(tmp),len(opts))
        i+=1
    return True,string


def format_print(string,rc=False,num=0,bstr=None,NFLT=False):
    string_type=type(string)
    rc_str=''
    chk=None
    bspace=space(num)

    # Start Symbol
    if string_type is tuple:
        if bstr is None:
            if NFLT:
                rc_str='%s('%(rc_str)
            else:
                rc_str='%s%s('%(bspace,rc_str)
        else:
            rc_str='%s,\n%s%s('%(bstr,bspace,rc_str)
    elif string_type is list:
        if bstr is None:
            if NFLT:
                rc_str='%s['%(rc_str)
            else:
                rc_str='%s%s['%(bspace,rc_str)
        else:
            rc_str='%s,\n%s%s['%(bstr,bspace,rc_str)
    elif string_type is dict:
        if bstr is None:
            rc_str='%s{'%(rc_str)
        else:
            rc_str='%s,\n%s %s{'%(bstr,bspace,rc_str)
    rc_str='%s\n%s '%(rc_str,bspace)

    # Print string
    if string_type is list or string_type is tuple:
       for ii in list(string):
           ii_type=type(ii)
           if ii_type is tuple or ii_type is list or ii_type is dict:
               if not ii_type is dict:
                  num=num+1
               rc_str=format_print(ii,num=num,bstr=rc_str,rc=True)
           else:
               if chk == None:
                  rc_str='%s%s'%(rc_str,STR(str_format_print(ii,rc=True)).Tap())
                  chk='a'
               else:
                  rc_str='%s,\n%s'%(rc_str,STR(str_format_print(ii,rc=True)).Tap(space=bspace+' '))
    elif string_type is dict:
       for ii in string.keys():
           ii_type=type(string[ii])
           if ii_type is dict or ii_type is tuple or ii_type is list:
               num=num+1
               if ii_type is dict:
                   tmp=format_print(string[ii],num=num,rc=True)
               else:
                   tmp=format_print(string[ii],num=num,rc=True,NFLT=True)
               rc_str="%s,\n%s %s:%s"%(rc_str,bspace,str_format_print(ii,rc=True),tmp)
           else:
               if chk == None:
                  rc_str='%s%s'%(rc_str,STR("{0}:{1}".format(str_format_print(ii,rc=True),str_format_print(string[ii],rc=True))).Tap())
                  chk='a'
               else:
                  rc_str='%s,\n%s'%(rc_str,STR("{0}:{1}".format(str_format_print(ii,rc=True),str_format_print(string[ii],rc=True))).Tap(space=bspace+' '))

    # End symbol
    if string_type is tuple:
        rc_str='%s\n%s)'%(rc_str,bspace)
    elif string_type is list:
        rc_str='%s\n%s]'%(rc_str,bspace)
    elif string_type is dict:
        if bstr is None:
            rc_str='%s\n%s}'%(rc_str,bspace)
        else:
            rc_str='%s\n%s }'%(rc_str,bspace)

    else:
       rc_str=string

    # Output
    if rc:
       return rc_str
    else:
       print(rc_str)

def format_string(string,inps):
    cmd=''
    if isinstance(string,dict):
        cmd=string['cmd']
        string=string['base']
    type_inps=type(inps)
    if type_inps is dict:
        if '%(' in string:
            if '%s' in string:
                return False,"name placehoder can't get %s format"
            try:
                return True,string % inps + ' '+cmd
            except:
                return False,"""string:{} input:{}""".format(string,inps)
        elif re.compile('{(\w.*)}').findall(string):
            if re.compile('{\d*}').findall(string):
                return False,"name placehoder can't get {} format"
            return True,string.format(**inps) + ' '+cmd
    else:
        if '%s' in string and type_inps in [tuple,list]:
            if '%(' in string:
                return False,"%s format string can't get name placeholder format"
            return True,string % tuple(inps) + ' '+cmd
        elif re.compile('{\d*}').findall(string) and type_inps in [tuple,list]:
            if re.compile('{(\w.*)}').findall(string):
                return False,"{} format string can't get name placeholder format"
            return True,string.format(*tuple(inps)) + ' '+cmd
        else:
            return None,string+' '+cmd

def format_string_dict(string):
    if isinstance(string,dict):
        string='''{}'''.format(string['base'])
    if '%(' in string or re.compile('{(\w.*)}').findall(string):
        return True
    return False



def Sort(src,reverse=False,func=None,order=None,field=None,base='key',sym=None):
    if isinstance(src,str) and sym is not None: src=src.split(sym)
    if isinstance(src,dict) and base == 'data':
        field=1
    def _cint_(e):
        try:
            if isinstance(field,int):
                if isinstance(e,(list,tuple)) and len(e) > field:
                    return int(e[field])
                else:
                    return 9999999
            return int(e)
        except:
            return e
    def _cstr_(e):
        if isinstance(field,int):
            if isinstance(e,(list,tuple)) and len(e) > field:
                return '''{}'''.format(e[field])
            else:
                return 'zzzzzzzzz'
        return '''{}'''.format(e)
    if isinstance(src,(list,tuple)):
        if order in [int,'int','digit','number']:
            #def _cint_(e):
            #    try:
            #        if isinstance(field,int):
            #            if isinstance(e,(list,tuple)) and len(e) > field:
            #                return int(e[field])
            #            else:
            #                return 9999999
            #        return int(e)
            #    except:
            #        return e
            return self.root.sort(reverse=reverse,key=_cint_)
        elif order in [str,'str']:
            #def _cint_(e):
            #    if isinstance(field,int):
            #        if isinstance(e,(list,tuple)) and len(e) > field:
            #            return '''{}'''.format(e[field])
            #        else:
            #            return 'zzzzzzzzz'
            #    return '''{}'''.format(e)
            #return self.root.sort(reverse=reverse,key=_cint_)
            return self.root.sort(reverse=reverse,key=_cstr_)
        else:
            if isinstance(field,int):
                #def _cint_(e):
                #    if isinstance(e,(list,tuple)) and len(e) > field:
                #        return e[field]
                return self.root.sort(reverse=reverse,key=_cint_)
            else:
                return self.root.sort(reverse=reverse,key=func)
    elif isinstance(src,dict):
        lst=[]
        if base == 'key':
            lst=list(self.keys())
            if order in [int,'int','digit','number']:
                #def _cint_(e):
                #    try:
                #        return int(e)
                #    except:
                #        return e
                return lst.sort(reverse=reverse,key=_cint_)
            elif order in [str,'str']:
                #def _cint_(e):
                #    return '''{}'''.format(e)
                #return lst.sort(reverse=reverse,key=_cint_)
                return lst.sort(reverse=reverse,key=_cstr_)
            else:
                return lst.sort(reverse=reverse,func=func)
        elif base == 'value':
            lst=self.items()
            if order in [int,'int','digit','number']:
                #def _cint_(e):
                #    try:
                #        return int(e[1])
                #    except:
                #        return e[1]
                lst.sort(reverse=reverse,key=_cint_)
            elif order in [str,'str']:
                #def _cint_(e):
                #    return '''{}'''.format(e[1])
                #lst.sort(reverse=reverse,key=_cint_)
                lst.sort(reverse=reverse,key=_cstr_)
            else:
                lst.sort(reverse=reverse,func=func)
            return [i[0] for i in lst]


def Update(src,*inps,**opts):
    at=opts.pop('at',0)
    err=opts.pop('err',False)
    default=opts.pop('default',False)
    force=opts.pop('force',False)
    sym=opts.pop('sym',None)
    if isinstance(src,(list,tuple,str)):
        if isinstance(src,str) and sym: src=src.split(sym)
        tuple_out=False
        if isinstance(src,tuple) and force:
            src=list(src)
            tuple_out=True
        n=len(src)
        if n == 0:
            if err is True:
                return default
            else:
                src=list(inps)
        elif isinstance(at,int) and n > at:
            for i in range(0,len(inps)):
                if n > at+i:
                    src[at+i]=inps[i]
                elif err is True:
                    return default
                else:
                    src=src+list(inps)[i:]
                    break
        elif isinstance(at,(tuple,list)):
            if len(inps) == len(at):
                for i in range(0,len(at)):
                    if isinstance(at[i],int) and n > at[i]:
                        src[at[i]]=inps[i]
                    elif err is True:
                        return default
                    else:
                        src.append(inps[i])
        if tuple_out: return tuple(src)
        return src
    elif isinstance(src,dict):
        for ii in inps:
           if isinstance(ii,dict):
               src.update(ii)
        if opts:
           src.update(opts)
    return src

def Random(length=8,strs=None,mode='*',letter='*',default=1):
    if mode in [int,'int','num','number']:
        if isinstance(strs,(list,tuple)) and len(strs) == 2:
            try:
                s=int(strs[0])
                n=int(strs[1])
                return random.randint(s,n)
            except:
                pass
        s=0
        n=''
        for i in range(0,length):
            n=n+'9'
        if n:
            return random.randint(s,int(n))
        return default
    new=''
#    if mode in [int,'int','num']:
#        for i in range(0,length):
#            new='{0}{1}'.format(new,random.randint(0,9))
#        return int(num)
    if not isinstance(strs,str) or not strs:
        strs=''
        if 'alpha' in mode or mode in ['all','*']:
            if letter == 'upper':
                strs=string.ascii_uppercase
            elif letter == 'lower':
                strs=string.ascii_lowercase
            elif letter in ['*','all']:
                strs=string.ascii_letters
        if 'num' in mode or mode in ['all','*']:
            strs=strs+string.digits
        if 'char' in mode or 'sym' in mode or mode in ['all','*']:
            strs=strs+string.punctuation
#        if mode in ['all','*','alphanumchar']:
#            strs='0aA-1b+2Bc=C3d_D,4.eE?5"fF6g7G!h8H@i9#Ij$JkK%lLmMn^N&oO*p(Pq)Q/r\Rs:St;TuUv{V<wW}x[Xy>Y]z|Z'
#        elif mode in ['alphachar']:
#            strs='aA-b+Bc=Cd_D,.eE?"fFgG!hH@i#Ij$JkK%lLmMn^N&oO*p(Pq)Q/r\Rs:St;TuUv{V<wW}x[Xy>Y]z|Z'
#        elif mode in ['alphanum']:
#            strs='aA1b2BcC3dD4eE5fF6g7Gh8Hi9IjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'
#        elif mode in ['char']:
#            strs='-+=_,.?"!@#$%^&*()/\:;{<}x[>]|'
#        else:
#            strs='aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'
    if not strs: strs=string.ascii_letters
    strn=len(strs)-1
    for i in range(0,length):
        new='{0}{1}'.format(new,strs[random.randint(0,strn)])
    return new

def Keys(src,find=None,start=None,end=None,sym='\n',default=[],word=False,pattern=False,findall=False,out=None):
    rt=[]
    if isinstance(src,str,list,tuple) and find:
        if isinstance(src,str): src=src.split(sym)

        for row in range(0,len(src)):
            for ff in FIND().Find(find,src=src[row],pattern=pattern,word=word,findall=findall,default=[],out=list):
                if findall:
                    rt=rt+[(row,[m.start() for m in re.finditer(ff,src[row])])]
                else:
                    idx=src[row].index(ff,start,end)
                    if idx >= 0:
                        rt.append((row,idx))
    elif isinstance(src,dict):
        if find is None:
            if out in ['raw',None] and len(src.keys()) == 1 : return list(src.keys())[0]
            if out in ['tuple',tuple]: return tuple(list(src.keys()))
            return list(src.keys())
        # if it has found need code for recurring search at each all data and path of keys
        # return [ (keypath,[found data]), .... ]
    #elif Type(src,'instance','classobj'):
    # if src is instance or classobj then search in description and made function name at key
    if rt:
        if out in ['tuple',tuple]: return tuple(rt)
        if out not in ['list',list] and len(rt) == 1 and rt[0][0] == 0:
            if len(rt[0][1]) == 1:return rt[0][1][0]
            return rt[0][1]
        return rt
    return default

def findXML(xmlfile,find_name=None,find_path=None):
    tree=ET.parse(xmlfile)
    #root=ET.fromstring(data)
    root=tree.getroot()
    def find(tr,find_name):
        for x in tr:
            if x.attrib.get('name') == find_name:
                return x,x.tag
            rt,pp=find(x,find_name)
            if rt:
                return rt,'{}/{}'.format(x.tag,pp)
        return None,None
    found_root=None
    if find_name:
        found=find(root,find_name)
        if found[0]:
             found_root=found[0]
    if find_path and isinstance(find_path,str):
        #ex: root.findall('./Menu/Setting/[@name="Administrator Password"]/Information/HasPassword'):
        if not found_root: found_root=root
        return found_root.findall(find_path)
        # <element>.tag: name, .text: data, .attrib: dict

def Compress(data,mode='lz4'):
    if mode == 'lz4':
        return frame.compress(data)
    elif mode == 'bz2':
        return bz2.compress(data)

def Decompress(data,mode='lz4',work_path='/tmp',del_org_file=False,file_info={}):
    def FileName(filename):
        if isinstance(filename,str):
            filename_info=os.path.basename(filename).split('.')
            if 'tar' in filename_info:
                idx=filename_info.index('tar')
            else:
                idx=-1
            #return '.'.join(filename_info[:idx]),'.'.join(filename_info[idx:])
            return Join(filename_info[:idx],symbol='.'),Join(filename_info[idx:],symbol='.')
        return None,None

    def FileType(filename,default=False):
        if not isinstance(filename,str) or not os.path.isfile(filename): return default
        aa=magic.from_buffer(open(filename,'rb').read(2048))
        if aa: return aa.split()[0].lower()
        return 'unknown'

    if mode == 'lz4':
        return frame.decompress(data)
    elif mode == 'bz2':
        return bz2.BZ2Decompressor().decompress(data)
    elif mode == 'file' and isinstance(data,str) and os.path.isfile(data):
        filename,fileextfile_info=FileName(data)
        filetype=FileType(data)
        if filetype and fileext:
            # Tar stuff
            if fileext in ['tgz','tar','tar.gz','tar.bz2','tar.xz'] and filetype in ['gzip','tar','bzip2','lzma','xz','bz2']:
                tf=tarfile.open(data)
                tf.extractall(work_path)
                tf.close()
            elif fileext in ['zip'] and filetype in ['compress']:
                with zipfile.ZipFile(data,'r') as zf:
                    zf.extractall(work_path)
            if del_org_file: os.unline(data)
            return True

def cat(filename,no_end_newline=False,no_edge=False,byte=False,newline='\n',no_first_newline=False,no_all_newline=False,file_only=True,default={'err'}):
    tmp=FILE().Rw(filename,file_only=file_only,default=default)
    tmp=Get(tmp,1)
    if no_edge:
        return STR(tmp).RemoveNewline(mode='edge',byte=byte,newline=newline)
    elif no_end_newline:
        return STR(tmp).RemoveNewline(mode='end',byte=byte,newline=newline)
    elif no_first_newline:
        return STR(tmp).RemoveNewline(mode='first',byte=byte,newline=newline)
    elif no_all_newline:
        return STR(tmp).RemoveNewline(mode='all',byte=byte,newline=newline)
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

def ping(host,**opts):
    count=opts.get('count',0)
    interval=opts.get('interval',1)
    keep_good=opts.get('keep_good',0)
    timeout=opts.get('timeout',opts.get('timeout_sec',5))
    lost_mon=opts.get('lost_mon',False)
    log=opts.get('log',None)
    stop_func=opts.get('stop_func',None)
    log_format=opts.get('log_format','.')
    cancel_func=opts.get('cancel_func',None)
    return IP().Ping(host=host,count=count,interval=interval,keep_good=keep_good, timeout=timeout,lost_mon=lost_mon,log=log,stop_func=stop_func,log_format=log_format,cancel_func=cancel_func)
##########################################################################################

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
    run_time=TIME().Int()
    if keep == 0 or keep is None:
        return True,'N/A(Missing keep parameter data)'
    if log:
        log('[',direct=True,log_level=1)
    time=TIME()
    while True:
        if time.Out(timeout):
            if log:
                log(']\n',direct=True,log_level=1)
            return False,'Timeout monitor'
        if is_cancel(cancel_func) or stop_func is True:
            if log:
                log(']\n',direct=True,log_level=1)
            return True,'Stopped monitor by Custom'
        if ping(ip,cancel_func=cancel_func):
            if (TIME().Int() - run_time) > keep:
                if log:
                    log(']\n',direct=True,log_level=1)
                return True,'OK'
            if log:
                log('-',direct=True,log_level=1)
        else:
            run_time=TIME().Int()
            if log:
                log('.',direct=True,log_level=1)
        TIME().Sleep(interval)
    if log:
        log(']\n',direct=True,log_level=1)
    return False,'Timeout/Unknown issue'

def file_mode(val):
    #return FILE().Mode(val)
    if isinstance(val,int):
        if val > 511:
            return oct(val)[-4:]
        elif val > 63:
            return oct(val)
    else:
        val=_u_bytes2str(val)
        if val:
            cnt=len(val)
            num=int(val)
            if cnt >=3 and cnt <=4 and num >= 100 and num <= 777:
                return int(val,8)

def get_file(filename,**opts):
    #return FILE(filename,**opts)
    md5sum=opts.get('md5sum',False)
    data=opts.get('data',False)
    include_dir=opts.get('include_dir',False)
    include_sub_dir=opts.get('include_sub_dir',False)

    def get_file_data(filename,root_path=None):
        rc={'name':os.path.basename(filename),'path':os.path.dirname(filename),'exist':False,'dir':False,'link':False}
        if root_path:
            in_filename=os.path.join(root_path,filename)
        else:
            in_filename=filename
        if os.path.exists(in_filename):
            fstat=os.stat(in_filename)
            rc['uid']=fstat.st_uid
            rc['gid']=fstat.st_gid
            rc['size']=fstat.st_size
            rc['atime']=fstat.st_atime
            rc['mtime']=fstat.st_mtime
            rc['ctime']=fstat.st_ctime
            rc['inod']=fstat.st_ino
            rc['mode']=oct(fstat.st_mode)[-4:]
            rc['exist']=True
            if os.path.islink(in_filename):
                rc['link']=True
            else:
                rc['link']=False
                if os.path.isdir(in_filename):
                    rc['dir']=True
                    rc['path']=in_filename
                    rc['name']=''
                else:
                    rc['dir']=False
                    if md5sum or data:
                        with open(in_filename,'rb') as f:
                            fdata=f.read()
                        if md5sum:
                            rc['md5']=md5(fdata)
                        if data:
                            rc['data']=fdata
        return rc

    rc={'exist':False,'includes':[]}
    if type(filename) is str:
        rc.update(get_file_data(filename))
        if rc['dir']:
            root_path=filename
            real_filename=None
        else:
            root_path=os.path.dirname(filename)
            real_filename=os.path.basename(filename)
        if include_dir:
            pwd=os.getcwd()
            os.chdir(root_path)
            for dirPath, subDirs, fileList in os.walk('.'):
                for sfile in fileList:
                    curFile=os.path.join(dirPath.replace('./',''),sfile)
                    if curFile != real_filename:
                        rc['includes'].append(get_file_data(curFile,root_path))
                if include_sub_dir is False:
                    break
            os.chdir(pwd)
    return rc

def save_file(data,dest):
#    return data.Extract(dest=dest,sub_dir=True)
    if not isinstance(data,dict) or not isinstance(dest,str) : return False
    if os.path.isdir(dest) is False: os.system('mkdir -p {0}'.format(dest))
    if data.get('dir'):
        fmode=file_mode(data.get('mode'))
        if fmode:
            os.chmod(dest,fmode)
    else:
        # if file then save
        new_file=os.path.join(dest,data['name'])
        if 'data' in data:
            with open(new_file,'wb') as f:
                f.write(data['data'])
        chmod_mode=file_mode(data.get('mode'))
        if chmod_mode:
            os.chmod(new_file,chmod_mode)
    if 'includes' in data and data['includes']: # If include directory or files 
        for ii in data['includes']:
            if ii['path']:
                sub_dir=os.path.join(dest,ii['path'])
            else:
                sub_dir='{}'.format(dest)
            if os.path.isdir(sub_dir) is False: os.system('mkdir -p {}'.format(sub_dir))
            sub_file=os.path.join(sub_dir,ii['name'])
            with open(sub_file,'wb') as f:
                f.write(ii['data'])
            chmod_mode=file_mode(ii.get('mode'))
            if chmod_mode:
                os.chmod(sub_file,chmod_mode)

#########################################################################
def is_cancel(func):
    ttt=type(func).__name__
    if ttt in ['function','instancemethod','method']:
        if func():
            return True
    elif ttt in ['bool','str'] and func in [True,'cancel']:
        return True
    return False

def log_file_info(name):
    log_file_str=''
    if name and len(name) > 0:
        if type(name) is str:
            if name.split(':')[0] == 'log_file':
                return name
            name=name.split(',')
        for nn in name:
            if nn and nn != 'None':
                if log_file_str:
                    log_file_str='{}:{}'.format(log_file_str,nn)
                else:
                    log_file_str='{}'.format(nn)
        if log_file_str:
            return 'log_file:{}'.format(log_file_str)

def error_exit(msg=None):
    if msg is not None:
       print(msg)
    sys.exit(-1)


def std_err(msg,direct=False):
    if direct:
        sys.stderr.write(msg)
    else:
        sys.stderr.write('{}\n'.format(msg))
    sys.stderr.flush()
    
def log_format(*msg,**opts):
    log_date_format=opts.get('date_format','[%m/%d/%Y %H:%M:%S]')
    func_name=opts.get('func_name',False)
    log_intro=opts.get('log_intro',3)
    end_new_line=opts.get('end_new_line','')
    start_new_line=opts.get('start_new_line','\n')
    if len(msg) > 0:
        m_str=None
        intro=''
        intro_space=''
        if log_date_format:
            intro=TIME().Format(tformat=log_date_format)+' '
        if func_name or log_intro > 3:
            if type(func_name) is str:
                intro=intro+'{0} '.format(func_name)
            else:
                intro=intro+'{0}() '.format(get_caller_fcuntion_name())
        if intro:
           for i in range(0,len(intro)+1):
               intro_space=intro_space+' '
        for m in list(msg):
            if m_str is None:
                m_str='{0}{1}{2}{3}'.format(start_new_line,intro,m,end_new_line)
            else:
                m_str='{0}{1}{2}{3}{4}'.format(start_new_line,m_str,intro_space,m,end_new_line)
        return m_str

def dget(dict=None,keys=None):
    if dict is None or keys is None:
        return False
    tmp=dict.copy()
    for ii in keys.split('/'):
        if ii in tmp:
           dtmp=tmp[ii]
        else:
           return False
        tmp=dtmp
    return tmp

def dput(dic=None,keys=None,val=None,force=False,safe=True):
    if dic is not None and keys:
        tmp=dic
        keys_arr=keys.split('/')
        keys_num=len(keys_arr)
        for ii in keys_arr[:(keys_num-1)]:
            if ii in tmp:
                if type(tmp[ii]) == type({}):
                    dtmp=tmp[ii]
                else:
                    if tmp[ii] == None:
                        tmp[ii]={}
                        dtmp=tmp[ii]
                    else:
                        if force:
                            vtmp=tmp[ii]
                            tmp[ii]={vtmp:None}
                            dtmp=tmp[ii]
                        else:
                            return False
            else:
                if force:
                    tmp[ii]={}
                    dtmp=tmp[ii]
                else:
                    return False
            tmp=dtmp
        if val == '_blank_':
            val={}
        if keys_arr[keys_num-1] in tmp.keys():
            if safe:
                if tmp[keys_arr[keys_num-1]]:
                    return False
            tmp.update({keys_arr[keys_num-1]:val})
            return True
        else:
            if force:
                tmp.update({keys_arr[keys_num-1]:val})
                return True
    return False

def sreplace(pattern,sub,string):
    return re.sub('^%s' % pattern, sub, string)

def ereplace(pattern,sub,string):
    return re.sub('%s$' % pattern, sub, string)

def md5(string):
    return hashlib.md5(_u_bytes(string)).hexdigest()

def ipmi_cmd(cmd,ipmi_ip=None,ipmi_user='ADMIN',ipmi_pass='ADMIN',log=None):
    if ipmi_ip is None:
        ipmi_str=""" ipmitool {0} """.format(cmd)
    else:
        ipmi_str=""" ipmitool -I lanplus -H {0} -U {1} -P '{2}' {3} """.format(ipmi_ip,ipmi_user,ipmi_pass,cmd)
    if log:
        log(' ipmi_cmd():{}'.format(ipmi_str),log_level=7)
    return rshell(ipmi_str)

    
def get_ipmi_mac(ipmi_ip=None,ipmi_user='ADMIN',ipmi_pass='ADMIN',loop=0):
    ipmi_mac_str=None
    if ipmi_ip is None:
        ipmi_mac_str=""" ipmitool lan print 2>/dev/null | grep "MAC Address" | awk """
    elif is_ipv4(ipmi_ip):
        ipmi_mac_str=""" ipmitool -I lanplus -H {0} -U {1} -P {2} lan print 2>/dev/null | grep "MAC Address" | awk """.format(ipmi_ip,ipmi_user,ipmi_pass)
    if ipmi_mac_str is not None:
        ipmi_mac_str=ipmi_mac_str + """ '{print $4}' """
        if not loop:
            return rshell(ipmi_mac_str)
        else:
            for i in range(0,int(loop)):
                mm=rshell(ipmi_mac_str)
                if mm[1]:
                    return mm
                time.sleep(3)
    return False,''

def get_ipmi_ip():
    return rshell('''ipmitool lan print 2>/dev/null| grep "IP Address" | grep -v Source | awk '{print $4}' ''')

def make_tar(filename,filelist,ctype='gz',ignore_file=[]):
    def ignore_files(filename,ignore_files):
        if isinstance(ignore_files,(list,tuple)):
            for ii in ignore_files:
                if isinstance(ii,str) and (ii == filename or filename.startswith(ii)): return True
        elif isinstance(ignore_files,str):
            if ignore_files == filename or filename.startswith(ignore_files): return True
        return False

    if ctype == 'bz2':
        tar = tarfile.open(filename,"w:bz2")
    elif ctype in ['stream',None,'tar']:
        tar = tarfile.open(filename,"w:")
    if ctype == 'xz':
        tar = tarfile.open(filename,"w:xz")
    else:
        tar = tarfile.open(filename,"w:gz")
    ig_dupl=[]
    filelist_tmp=[]
    filelist_type=type(filelist)
    if filelist_type is list:
       filelist_tmp=filelist
    elif filelist_type is str:
       filelist_tmp=filelist.split(',')
    for ii in filelist_tmp:
        if os.path.isfile(ii):
            if ignore_files(ii,ignore_file): continue
            ig_dupl.append(ii)
            tar.add(ii)
        elif os.path.isdir(ii):
            for r,d,f in os.walk(ii):
                if r in ignore_file or (len(d) == 1 and d[0] in ignore_file):
                    continue
                for ff in f:
                    aa=os.path.join(r,ff)
                    if ignore_files(aa,ignore_file) or aa in ig_dupl: continue
                    ig_dupl.append(aa)
                    tar.add(aa)
        else:
            print('{} not found'.format(ii))
    tar.close()

def is_tempfile(filepath,tmp_dir='/tmp'):
   filepath_arr=filepath.split('/')
   if len(filepath_arr) == 1:
      return False
   tmp_dir_arr=tmp_dir.split('/')
   
   for ii in range(0,len(tmp_dir_arr)):
      if filepath_arr[ii] != tmp_dir_arr[ii]:
          return False
   return True


def isfile(filename=None):
   if filename is None:
      return False
   if len(filename) == 0:
      return False
   if os.path.isfile(filename):
      return True
   return False

def space(space_num=0,_space_='   '):
    space_str=''
    for ii in range(space_num):
        space_str='{0}{1}'.format(space_str,_space_)
    return space_str

def tap_print(string,bspace='',rc=False,NFLT=False):
    rc_str=None
    if type(string) is str:
        for ii in string.split('\n'):
            if NFLT:
               line='%s'%(ii)
               NFLT=False
            else:
               line='%s%s'%(bspace,ii)
            if rc_str is None:
               rc_str='%s'%(line)
            else:
               rc_str='%s\n%s'%(rc_str,line)
    else:
        rc_str='%s%s'%(bspace,string)

    if rc:
        return rc_str
    else:
        print(rc_str)

def str_format_print(string,rc=False):
    if type(string) is str:
        if len(string.split("'")) > 1:
            rc_str='"%s"'%(string)
        else:
            rc_str="'%s'"%(string)
    else:
        rc_str=string
    if rc:
        return rc_str
    else:
        print(rc_str)

def clear_version(string,sym='.'):
    if isinstance(string,(int,str)):
        if isinstance(string,str): string=string.strip()
        string='{}'.format(string)
    else:
        return False
    arr=string.split(sym)
    for ii in range(len(arr)-1,0,-1):
        if arr[ii].replace('0','') == '':
            arr.pop(-1)
        else:
            break
    #return sym.join(arr)
    return Join(arr,symbol=sym)

def get_key(dic=None,find=None):
    return find_key_from_value(dic=dic,find=find)

def find_key_from_value(dic=None,find=None):
    if isinstance(dic,dict):
        if find is None:
            return list(dic.keys())
        else:
            for key,val in dic.items():
                if val == find:
                    return key
    elif isinstance(dic,list) or isinstance(dic,tuple):
        if find is None:
            return len(dic)
        else:
            if find in dic:
                return dic.index(find)
         
def git_ver(git_dir=None):
    if git_dir is not None and os.path.isdir('{0}/.git'.format(git_dir)):
        gver=rshell('''cd {0} && git describe --tags'''.format(git_dir))
        if gver[0] == 0:
            return gver[1]

def load_kmod(modules,re_load=False):
    if type(modules) is str:
        modules=modules.split(',')
    for ii in modules:
        if re_load:
            os.system('lsmod | grep {0} >& /dev/null && modprobe -r {0}'.format(ii.replace('-','_')))
        os.system('lsmod | grep {0} >& /dev/null || modprobe --ignore-install {1} || modprobe {1} || modprobe -ib {1}'.format(ii.replace('-','_'),ii))
        #os.system('lsmod | grep {0} >& /dev/null || modprobe -i -f {1}'.format(ii.split('-')[0],ii))

def reduce_string(string,symbol=' ',snum=0,enum=None):
    if type(string) is str:
        arr=string.split(symbol)
    strs=None
    if enum is None:
        enum=len(arr)
    for ii in range(snum,enum):
        if strs is None:
            strs='{0}'.format(arr[ii])
        else:
            strs='{0} {1}'.format(strs,arr[ii])
    return strs

def findstr(string,find,prs=None,split_symbol='\n',patern=True):
    # Patern return selection (^: First(0), $: End(-1), <int>: found item index)
    found=[]
    if not isinstance(string,str): return []
    if split_symbol:
        string_a=string.split(split_symbol)
    else:
        string_a=[string]
    for nn in string_a:
        if isinstance(find,(list,tuple)):
            find=list(find)
        else:
            find=[find]
        for ff in find:
            if patern:
                aa=re.compile(ff).findall(nn)
                for mm in aa:
                    if isinstance(mm,tuple):
                        if prs == '^':
                            found.append(mm[0])
                        elif prs == '$':
                            found.append(mm[-1])
                        elif isinstance(prs,int):
                            found.append(mm[prs])
                        else:
                            found.append(mm)
                    else:
                        found.append(mm)
            else:
                find_a=ff.split('*')
                if len(find_a[0]) > 0:
                    if find_a[0] != nn[:len(find_a[0])]:
                        chk=False
                if len(find_a[-1]) > 0:
                    if find_a[-1] != nn[-len(find_a[-1]):]:
                        chk=False
                for ii in find_a[1:-1]:
                    if ii not in nn:
                        chk=False
                if chk:
                    found.append(nn)
    return found

def find_cdrom_dev(size=None):
    load_kmod(['sr_mod','cdrom','libata','ata_piix','ata_generic','usb-storage'])
    if os.path.isdir('/sys/block') is False:
        return
    for r, d, f in os.walk('/sys/block'):
        for dd in d:
            for rrr,ddd,fff in os.walk(os.path.join(r,dd)):
                if 'removable' in fff:
                    with open('{0}/removable'.format(rrr),'r') as fp:
                        removable=fp.read()
                    if '1' in removable:
                        if os.path.isfile('{0}/device/model'.format(rrr)):
                            with open('{0}/device/model'.format(rrr),'r') as fpp:
                                model=fpp.read()
                            for ii in ['CDROM','DVD-ROM','DVD-RW']:
                                if ii in model:
                                    if size is None:
                                        return '/dev/{0}'.format(dd)
                                    else:
                                        if os.path.exists('{}/size'.format(rrr)):
                                            with open('{}/size'.format(rrr),'r') as fss:
                                                block_size=fss.read()
                                                dev_size=int(block_size) * 512
                                                if dev_size == int(size):
                                                    return '/dev/{0}'.format(dd)

def find_usb_dev(size=None,max_size=None):
    rc=[]
    load_kmod(modules=['usb-storage'])
    if os.path.isdir('/sys/block') is False:
        return
    for r, d, f in os.walk('/sys/block'):
        for dd in d:
            for rrr,ddd,fff in os.walk(os.path.join(r,dd)):
                if 'removable' in fff:
                    removable=cat('{0}/removable'.format(rrr),no_edge=True)
                    if removable:
                        if IsSame('1',removable):
                            if size is None:
                                if max_size:
                                    file_size=cat('{0}/size'.format(rrr),no_edge=True)
                                    if file_size:
                                        dev_size=int(file_size) * 512
                                        if dev_size <= int(max_size):
                                            rc.append('/dev/{0}'.format(dd))
                                else:
                                    rc.append('/dev/{0}'.format(dd))
                            else:
                                file_size=cat('{0}/size'.format(rrr),no_edge=True)
                                if file_size:
                                    dev_size=int(file_size) * 512
                                    if dev_size == int(size):
                                        rc.append('/dev/{0}'.format(dd))
    return rc

#def ipmi_sol(ipmi_ip,ipmi_user,ipmi_pass):
#    if is_ipv4(ipmi_ip):
#        rshell('''ipmitool -I lanplus -H {} -U {} -P {} sol info'''.format(ipmi_ip,ipmi_user,ipmi_pass))
#Set in progress                 : set-complete
#Enabled                         : true
#Force Encryption                : false
#Force Authentication            : false
#Privilege Level                 : OPERATOR
#Character Accumulate Level (ms) : 0
#Character Send Threshold        : 0
#Retry Count                     : 0
#Retry Interval (ms)             : 0
#Volatile Bit Rate (kbps)        : 115.2
#Non-Volatile Bit Rate (kbps)    : 115.2
#Payload Channel                 : 1 (0x01)
#Payload Port                    : 623

def net_send_data(sock,data,key='kg',enc=False,timeout=0):
    if type(sock).__name__ in ['socket','_socketobject','SSLSocket'] and data and type(key) is str and len(key) > 0 and len(key) < 7:
        start_time=TIME().Int()
        # encode code here
        if timeout > 0:
            sock.settimeout(timeout)
        nkey=_u_str2int(key)
        pdata=pickle.dumps(data,protocol=2) # common 2.x & 3.x version : protocol=2
        data_type=_u_bytes(type(data).__name__[0])
        if enc and key:
            # encode code here
            #enc_tf=_u_bytes('t') # Now not code here. So, everything to 'f'
            #pdata=encode(key,pdata)
            enc_tf=_u_bytes('f')
        else:
            enc_tf=_u_bytes('f')
        ndata=struct.pack('>IssI',len(pdata),data_type,enc_tf,nkey)+pdata
        try:
            sock.sendall(ndata)
            return True,'OK'
        except:
            if timeout > 0:
                #timeout=sock.gettimeout()
                if TIME().Int() - start_time > timeout-1:
                    #Timeout
                    return False,'Sending Socket Timeout'
    return False,'Sending Fail'

def net_receive_data(sock,key='kg',progress=None,retry=0,retry_timeout=30):
    # decode code here
    def recvall(sock,count,progress=False): # Packet
        buf = b''
        file_size_d=int('{0}'.format(count))
        if progress: print('\n')
        tn=0
        newbuf=None
        while count:
            if progress:
                sys.stdout.write('\rDownloading... [ {} % ]'.format(int((file_size_d-count) / file_size_d * 100)))
                sys.stdout.flush()
            try:
                newbuf = sock.recv(count)
            except socket.error as e:
                if tn < retry:
                    print("[ERROR] timeout value:{} retry: {}/{}\n{}".format(sock.gettimeout(),tn,retry,e))
                    tn+=1
                    TIME().Sleep(1)
                    sock.settimeout(retry_timeout)
                    continue
                if e == 'timed out':
                    return 'timeout',e
            if not newbuf: return True,None #maybe something socket issue.
            buf += newbuf
            count -= len(newbuf)
        if progress: 
            sys.stdout.write('\rDownloading... [ 100 % ]\n')
            sys.stdout.flush()
        return True,buf
    ok,head=recvall(sock,10)
    if krc(ok,chk=True):
        if head:
            try:
                st_head=struct.unpack('>IssI',_u_bytes(head))
            except:
                return [False,'Fail for read header({})'.format(head)]
            if st_head[3] == _u_str2int(key):
                ok,data=recvall(sock,st_head[0],progress=progress)
                if krc(ok,chk=True):
                    if st_head[2] == 't':
                        # decode code here
                        # data=decode(data)
                        pass
                    if data: return [st_head[1],pickle.loads(data)]
                    return [True,None]
                else:
                    return [ok,data]
            else:
                return [False,'Wrong key']
        return ['lost','Connection lost']
    return ok,head

def net_put_and_get_data(IP,data,PORT=8805,key='kg',timeout=3,try_num=1,try_wait=[0,5],progress=None,enc=False,upacket=None,SSLC=False,log=True):
    sent=False,'Unknown issue'
    for ii in range(0,try_num):
        if upacket: # Update packet function for number of try information ([#/<total #>])
            data=upacket('ntry',[ii+1,try_num],data)
        start_time=TIME().Int()
        sock=net_get_socket(IP,PORT,timeout=timeout,SSLC=SSLC)
        if try_num > 0: 
            rtry_wait=(timeout//try_num)+1
        else:
            rtry_wait=try_wait
        sent=False,'Unknown issue'
        try:
            sent=net_send_data(sock,data,key=key,enc=enc)
        except:
            os.system("""[ -f /tmp/.{0}.{1}.crt ] && rm -f /tmp/.{0}.{1}.crt""".format(host,port))
        if sent[0]:
            nrcd=net_receive_data(sock,key=key,progress=progress)
            return nrcd
        else:
            if timeout >0:
                if TIME().Int() - start_time >= timeout-1:
                    return [False,'Socket Send Timeout']
                #return [False,'Data protocol version mismatch']
        if sock: sock.close()
        if try_num > 1:
            if log:
                print('try send data ... [{}/{}]'.format(ii+1,try_num))
            TIME().Sleep(try_wait)
    return [False,'Send fail({}) :\n{}'.format(sent[1],data)]

def net_get_socket(host,port,timeout=3,dbg=0,SSLC=False): # host : Host name or IP
    try:
        af, socktype, proto, canonname, sa = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)[0]
    except:
        print('Can not get network informatin of {}:{}'.format(host,port))
        return False
    try:
        soc = socket.socket(af, socktype, proto)
        if timeout > 0:
            soc.settimeout(timeout)
    except socket.error as msg:
        print('could not open socket of {0}:{1}\n{2}'.format(host,port,msg))
        return False
    ###### SSL Wrap ######
    if SSLC:
        for i in range(0,5):
            icertfile='/tmp/.{}.{}.crt'.format(host,port)
            try:
                cert=ssl.get_server_certificate((host,port))
            except:
                os.system('rm -f /tmp/.{}.{}.crt'.format(host,port))
                TIME().Sleep(1)
                continue
            f=open(icertfile,'w')
            f.write(cert)
            f.close()
            TIME().Sleep(0.3)
            try:
                soc=ssl.wrap_socket(soc,ca_certs=icertfile,cert_reqs=ssl.CERT_REQUIRED)
                soc.connect((host,port))
                return soc
            except socket.error as msg:
                if dbg > 3:
                    print(msg)
                TIME().Sleep(1)
    ########################
    else:
        try:
            soc.connect(sa)
            return soc
        except socket.error as msg:
            if dbg > 3:
                print('can not connect at {0}:{1}\n{2}'.format(host,port,msg))
    return False

def net_start_server(server_port,main_func_name,server_ip='',timeout=0,max_connection=10,log_file=None,certfile=None,keyfile=None):
    ssoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if timeout > 0:
        ssoc.settimeout(timeout)
    try:
        ssoc.bind((server_ip, server_port))
    except socket.error as msg:
        print('Bind failed. Error : {0}'.format(msg))
        os._exit(1)
    ssoc.listen(max_connection)
    print('Start server for {0}:{1}'.format(server_ip,server_port))
    # for handling task in separate jobs we need threading
    while True:
        conn, addr = ssoc.accept()
        ip, port = str(addr[0]), str(addr[1])
        try:
            if certfile and keyfile:
                ssl_conn=ssl_wrap(conn,certfile,keyfile=keyfile)
                Thread(target=main_func_name, args=(ssl_conn, ip, port, log_file)).start()
            else:
                Thread(target=main_func_name, args=(conn, ip, port, log_file)).start()
        except:
            print('No more generate thread for client from {0}:{1}'.format(ip,port))
    ssoc.close()

def net_start_single_server(server_port,main_func_name,server_ip='',timeout=0,max_connection=10,log_file=None,certfile=None,keyfile=None):
    ssoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if timeout > 0:
        ssoc.settimeout(timeout)
    try:
        ssoc.bind((server_ip, server_port))
    except socket.error as msg:
        print('Bind failed. Error : {0}'.format(msg))
        os._exit(1)
    ssoc.listen(max_connection)
    print('Start server for {0}:{1}'.format(server_ip,server_port))
    # for handling task in separate jobs we need threading
    conn, addr = ssoc.accept()
    ip, port = str(addr[0]), str(addr[1])
    if certfile and keyfile:
        ssl_conn=ssl_wrap(conn,certfile,keyfile=keyfile)
        rc=main_func_name(ssl_conn, ip, port, log_file)
    else:
        rc=main_func_name(conn, ip, port, log_file)
    ssoc.close()
    return rc

def kmp(mp={},func=None,name=None,timeout=0,quit=False,log_file=None,log_screen=True,log_raw=False, argv=[],queue=None):
    # Clean
    for n in [k for k in mp]:
        if quit is True:
            if n != 'log':
                mp[n]['mp'].terminate()
                if 'log' in mp:
                    mp['log']['queue'].put('\nterminate function {}'.format(n))
        else:
            if mp[n]['timeout'] > 0 and TIME().Int() > mp[n]['timeout']:
                mp[n]['mp'].terminate()
                if 'log' in mp:
                    mp['log']['queue'].put('\ntimeout function {}'.format(n))
        if not mp[n]['mp'].is_alive():
            del mp[n]
    if quit is True and 'log' in mp:
        mp['log']['queue'].put('\nterminate function log')
        TIME().Sleep(2)
        mp['log']['mp'].terminate()
        return

    # LOG
    def logging(ql,log_file=None,log_screen=True,raw=False):
        while True:
            #if not ql.empty():
            if ql.empty():
                TIME().Sleep(0.01)
            else:
                ll=ql.get()
                if raw:
                    log_msg=ll
                else:
                    log_msg='{} : {}\n'.format(TIME().Now().strftime('%m-%d-%Y %H:%M:%S'),ll)
                if type(log_msg) is not str:
                    log_msg='{}'.format(log_msg)
                if log_file and os.path.isdir(os.path.dirname(log_file)):
                    with open(log_file,'a') as f:
                        f.write('{}'.format(log_msg))
                if log_screen:
                    sys.stdout.write(log_msg)
                    sys.stdout.flush()

    if 'log' not in mp or not mp['log']['mp'].is_alive():
        #log=multiprocessing.Queue()
        log=Queue()
        #lqp=multiprocessing.Process(name='log',target=logging,args=(log,log_file,log_screen,log_raw,))
        lqp=Process(name='log',target=logging,args=(log,log_file,log_screen,log_raw,))
        lqp.daemon = True
        mp.update({'log':{'mp':lqp,'start':TIME().Int(),'timeout':0,'queue':log}})
        lqp.start()

    # Functions
    if func:
        if name is None:
            name=func.__name__
        if name not in mp:
            if argv:
                #mf=multiprocessing.Process(name=name,target=func,args=tuple(argv))
                mf=Process(name=name,target=func,args=tuple(argv))
            else:
                #mf=multiprocessing.Process(name=name,target=func)
                mf=Process(name=name,target=func)
            if timeout > 0:
                timeout=TIME().Int()+timeout
            
#            for aa in argv:
#                if type(aa).__name__ == 'Queue':
#                    mp.update({name:{'mp':mf,'timeout':timeout,'start':now(),'queue':aa}})
            if name not in mp:
                if queue and type(queue).__name__ == 'Queue':
                    mp.update({name:{'mp':mf,'timeout':timeout,'start':TIME().Int(),'queue':queue}})
                else:
                    mp.update({name:{'mp':mf,'timeout':timeout,'start':TIME().Int()}})
            mf.start()
    return mp

def key_remove_pass(filename):
    rshell('openssl rsa -in {0}.key -out {0}.nopass.key'.format(filename))

def cert_file(keyfile,certfile,C='US',ST='CA',L='San Jose',O='KGC',OU='KG',CN=None,EMAIL=None,days=365,passwd=None,mode='gen'):
    if keyfile is None and certfile is None:
        return None,None
    if mode == 'remove':
        rc=rshell('openssl rsa -in {0} -out {0}.nopass'.format(keyfile))
        if rc[0] == 0:
            if os.path.isfile('{}'.format(certfile)):
                return '{}.nopass'.format(keyfile),certfile
            else:
                return '{}.nopass.key'.format(keyfile),None
    elif mode == 'gen' or (mode == 'auto' and (os.path.isfile(keyfile) is False or os.path.isfile(certfile) is False)):
        if mode == 'gen':
            os.system('''rm -f {}'''.format(certfile))
            os.system('''rm -f {}'''.format(keyfile))
            os.system('''rm -f {}.csr'''.format(keyfile))
        subj=''
        if C:
            subj='{}/C={}'.format(subj,C)
        if ST:
            subj='{}/ST={}'.format(subj,ST)
        if L:
            subj='{}/L={}'.format(subj,L)
        if O:
            subj='{}/O={}'.format(subj,O)
        if OU:
            subj='{}/OU={}'.format(subj,OU)
        if CN:
            subj='{}/CN={}'.format(subj,CN)
        if EMAIL:
            subj='{}/emailAddress={}'.format(subj,EMAIL)
        if subj:
            subj=' -subj "{}"'.format(subj)
        # gen 
        rc=(1,'error','error',0,0,'','')
        if os.path.isfile(keyfile) is False:
            if passwd:
                # gen KEY
                rc=rshell('openssl genrsa -aes256 -out {0} 2048'.format(keyfile))
            else:
                #print('openssl genrsa -out {0} 2048'.format(keyfile))
                rc=rshell('openssl genrsa -out {0} 2048'.format(keyfile))
        if (os.path.isfile(keyfile) and os.path.isfile(certfile) is False) or rc[0] == 0:
            # gen CSR
            os.system('''rm -f {}'''.format(certfile))
            os.system('''rm -f {}.csr'''.format(keyfile))
            rrc=rshell('openssl req -new -key {0} -out {0}.csr {1}'.format(keyfile,subj))
            if rrc[0] == 0:
                # gen cert
                #print('openssl x509 -req -days {1} -in {0}.csr -signkey {0} -out {2}'.format(keyfile,days,certfile))
                rrrc=rshell('openssl x509 -req -days {1} -in {0}.csr -signkey {0} -out {2}'.format(keyfile,days,certfile))
                if rrrc[0] == 0:
                    # check
#                    print(rshell('openssl x509 -text -noout -in {}'.format(certfile))[1])
                    return keyfile,certfile
    else:
        key_file=None
        crt_file=None
        if os.path.isfile(keyfile):
            key_file=keyfile
        if os.path.isfile(certfile):
            crt_file=certfile
        return key_file,crt_file
    return None,None

def net_put_data(IP,data,PORT=8805,key='kg',timeout=3,try_num=1,try_wait=[1,10],progress=None,enc=False,upacket=None,dbg=0,wait_time=3,SSLC=False):
    sent=False,'Unknown issue'
    for ii in range(0,try_num):
        if upacket: # Update packet function for number of try information ([#/<total #>])
            data=upacket('ntry',[ii+1,try_num],data)
        sock=net_get_socket(IP,PORT,timeout=timeout,dbg=dbg,SSLC=SSLC)
        
        if sock is False:
            if dbg >= 3:
                print('Can not get socket data [{}/{}], wait {}s'.format(ii+1,try_num,wait_time))
            else:
                sys.stdout.write('.')
                sys.stdout.flush()
            TIME().Sleep(wait_time)
            continue
        sent=False,'Unknown issue'
        try:
            sent=net_send_data(sock,data,key=key,enc=enc)
        except:
            print('send fail, try again ... [{}/{}]'.format(ii+1,try_num))
        if sent[0]:
            if sock:
                sock.close()
            return [True,'sent']
        if try_num > 1:
            wait_time=Random(length=0,strs=try_wait,mode='int')
            if dbg >= 3:
                print('try send data ... [{}/{}], wait {}s'.format(ii+1,try_num,wait_time))
            TIME().Sleep(wait_time)
    return [False,'Send fail({}) :\n{}'.format(sent[1],data)]


def encode(string):
    enc='{0}'.format(string)
    tmp=zlib.compress(enc.encode("utf-8"))
    return '{0}'.format(base64.b64encode(tmp).decode('utf-8'))

def decode(string):
    if type(string) is str:
        dd=zlib.decompress(base64.b64decode(string))
        return '{0}'.format(dd.decode("utf-8"))
    return string

def check_work_dir(work_dir,make=False,ntry=1,try_wait=[1,3]):
    for ii in range(0,ntry):
        if os.path.isdir(work_dir):
            return True
        else:
            if make:
                try:
                    os.makedirs(work_dir)
                    return True
                except:
                    TIME().Sleep(try_wait)
    return False

def get_node_info(loop=0):
    host_ip=get_host_ip()
    return {
         'host_name':get_host_name(),
         'host_ip':host_ip,
         'host_mac':get_host_mac(ip=host_ip),
         'ipmi_mac':get_ipmi_mac(loop=loop)[1],
         'ipmi_ip':get_ipmi_ip()[1],
         }

def rreplace(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

def mount_samba(url,user,passwd,mount_point):
    if os.path.isdir(mount_point) is False:
        os.system('sudo mkdir -p {0}'.format(mount_point))
        TIME().Sleep(1)
    if os.path.isdir(mount_point) is False:
        return False,'can not make a {} directory'.format(mount_point),'can not make a {} directory'.format(mount_point),0,0,None,None
    if 'smb://' in url:
        url_a=url.split('/')
        url_m=len(url_a)
        iso_file=url_a[-1]
        new_url=''
        for i in url_a[2:url_m-1]:
            new_url='{0}/{1}'.format(new_url,i)
        rc=rshell('''sudo mount -t cifs -o user={0} -o password={1} /{2} {3}'''.format(user,passwd,new_url,mount_point))
        if rc[0] == 0:
            return True,rc[1]
    else:
        url_a=url.split('\\')
        url_m=len(url_a)
        iso_file=url_a[-1]
        new_url=''
        for i in url_a[1:url_m-1]:
            new_url='{0}/{1}'.format(new_url,i)
        rc=rshell('''sudo mount -t cifs -o user={0} -o password={1} {2} {3}'''.format(user,passwd,new_url,mount_point))
        if rc[0] == 0:
            return True,rc[1]

def umount(mount_point,del_dir=False):
    rc=rshell('''[ -d {0} ] && sudo mountpoint {0} && sleep 1 && sudo umount {0} && sleep 1'''.format(mount_point))
    if rc[0] == 0 and del_dir:
        os.system('[ -d {0} ] && sudo rmdir {0}'.format(mount_point))
    return rc

def is_xml(filename):
    firstLine_i=FILE().Rw(filename,out='string',read='firstline')
    if krc(firstLine_i,chk=True):
        firstLine=get_value(firstLine_i,1)
    else:
        filename_str=_u_byte2str(filename)
        if isinstance(filename_str,str):
            firstLine=filename_str.split('\n')[0]
    if isinstance(firstLine,str) and firstLine.split(' ')[0] == '<?xml':
        return True
    return False

def krc(rt,chk='_',rtd={'GOOD':[True,'True','Good','Ok','Pass',{'OK'},0],'FAIL':[False,'False','Fail',{'FAL'}],'NONE':[None,'None','N/A',{'NA'}],'IGNO':['IGNO','Ignore',{'IGN'}],'ERRO':['ERR','Error','error','erro','ERRO',{'ERR'}],'WARN':['Warn','warn',{'WAR'}],'UNKN':['Unknown','UNKN',{'UNK'}],'JUMP':['Jump',{'JUMP'}],'TOUT':['timeout','TimeOut','time out','Time Out','TMOUT','TOUT',{'TOUT'}],'REVD':['cancel','Cancel','CANCEL','REV','REVD','Revoked','revoked','revoke','Revoke',{'REVD'}],'LOST':['lost','connection lost','Connection Lost','Connection lost','CONNECTION LOST',{'LOST'}]},default=False):
    def trans(irt):
        type_irt=type(irt)
        for ii in rtd:
            for jj in rtd[ii]:
                if type(jj) == type_irt and ((type_irt is str and jj.lower() == irt.lower()) or jj == irt):
                    return ii
        return 'UNKN'
    rtc=Get(rt,'0|rc',out='raw',err='ignore',check=(list,tuple,dict))
    nrtc=trans(rtc)
    if chk != '_':
        if not isinstance(chk,list): chk=[chk]
        for cc in chk:
            if trans(cc) == nrtc:
                return True
            if nrtc == 'UNKN' and default == 'org':
                return rtc
        if default == 'org': return rt
        return default
    return nrtc

def replacestr(data,org,new):
    if isinstance(data,str):
        if not isinstance(org,str): org=_u_bytes2str(org)
        if not isinstance(new,str): new=_u_bytes2str(new)
    elif isinstance(data,bytes):
        if not isinstance(org,bytes): org=_u_bytes(org)
        if not isinstance(new,bytes): new=_u_bytes(new)
#    if not isinstance(data,bytes):
#        data=_u_bytes(data)
#    if not isinstance(org,bytes):
#        org=_u_bytes(org)
#    if not isinstance(new,bytes):
#        new=_u_bytes(new)
    return data.replace(org,new)

def get_iso_uid(filename):
    if type(filename) is not str:
        return False,None,None
    if os.path.exists(filename):
        uid_cmd='''sudo /usr/sbin/blkid {}'''.format(filename)
        rc=rshell(uid_cmd)
        if rc[0] == 0:
            uid_str='{0}_{1}'.format(findstr(rc[1],'UUID="(\w.*)" L')[0],findstr(rc[1],'LABEL="(\w.*)" T')[0]).replace(' ','_')
            file_info=get_file(filename)
            file_size=file_info.get('size',None)
            return True,uid_str,file_size
        return False,rc[1],None
    return False,'{} not found'.format(filename),None

def alive(out=None):
    aa=rshell('uptime')
    if aa[0] == 0:
        aa_a=aa[1].split()
        if len(aa_a) > 2: 
            if ':' in aa_a[2]:
                if out in ['sec','second','seconds',int]:
                    bb_a=aa_a[2][:-1].split(':')
                    return int(bb_a[0])*3600+int(bb_a[1])*60
                else:
                    return aa_a[2][:-1]+'h'
            elif aa_a[3] == 'min,':
                if out in ['sec','second','seconds',int]:
                    return int(aa_a[2])*60
                else:
                    return aa_a[2]+'m'
            else:
                if out in ['sec','second','seconds',int]:
                    if ':' in aa_a[4]:
                        bb_a=aa_a[4][:-1].split(':')
                        return int(aa_a[2])*(24*3600)+int(bb_a[0])*3600+int(bb_a[1])*60
                    else:
                        if aa_a[5] == 'min,':
                            return int(aa_a[2])*(24*3600)+int(aa_a[4])*60
                        else:
                            return int(aa_a[2])*(24*3600)+int(aa_a[4])
                else:
                    return aa_a[2]+'d'
    if out in ['sec','second','seconds',int]:
        return -1
    else:
        return 'unknown'

def ddict(*inps,**opts):
    out={}
    for ii in inps:
        if isinstance(ii,dict):
            out.update(ii)
    if opts:
        out.update(opts)
    return out

def fdict(src,keys):
    if isinstance(src,dict) and isinstance(keys,list):
        new_out={}
        for kk in keys:
            new_out[kk]=src.get(kk)
        return new_out

def pipe_msg(**opts):
    m={}
    if not pipe_file: return False
    if os.path.isfile(pipe_file):
        with open(pipe_file,'rb') as f:
            m=pickle.load(f)
    if opts:
        m.update(opts)
        with open(pipe_file,'wb') as f:
            pickle.dump(m,f, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        return m

def Try(cmd):
    try:
        return True,cmd
    except:
        e=sys.exc_info()[0]
        return False,{'err':e}

def Timeout(timeout_sec,init_time=None,default=(24*3600)):
    if timeout_sec == 0: return True,0
    init_time=integer(init_time,default=0)
    timeout_sec=integer(timeout_sec,default=default)
    if init_time == 0:
        init_time=TIME().Int()
    if timeout_sec == 0:
        return False,init_time
    if timeout_sec < 3:
       timeout_sec=3
    if TIME().Int() - init_time >  timeout_sec:
        return True,init_time
    return False,init_time

#################################################################
def Wrap(src,space='',space_mode='space',sym='\n',default=None,NFLT=False,out=str):
    return STR(src).Wrap(space=space,space_mode=space_mode,sym=sym,default=default,NFLT=NFLT,out=out)

def Split(src,sym,default=None):
    return STR(src).Split(sym,default=default)

def screen_kill(self,title):
    return SCREEN().Kill(title)

def screen_monitor(title,ip,ipmi_user,ipmi_pass,find=[],timeout_sec=600):
    return SCREEN().Monitor(title,ip,ipmi_user,ipmi_pass,find=find,timeout=timeout_sec)

def screen_id(title=None):
    return SCREEN().Id(title)

def screen_logging(title,cmd):
    return SCREEN().Log(title,cmd)

def mac2str(mac,case='lower'):
    return MAC(mac).ToStr(case=case)

def str2mac(mac,sym=':',case='lower',chk=False):
    return MAC(mac).FromStr(case=case,sym=sym,chk=chk)

def is_mac4(mac=None,symbol=':',convert=True):
    return MAC(mac).IsV4(symbol=symbol)

def rshell(cmd,timeout=None,ansi=True,path=None,progress=False,progress_pre_new_line=False,progress_post_new_line=False,log=None,progress_interval=5,cd=False):
    return SHELL().Run(cmd,timeout=timeout,ansi=ansi,path=path,progress=progress,progress_pre_new_line=progress_pre_new_line,progress_post_new_line=progress_post_new_line,log=log,progress_interval=progress_interval,cd=cd)

def gen_random_string(length=8,letter='*',digits=True,symbols=True,custom=''):
    mode='alpha'
    if digits:mode=mode+'num'
    if symbols:mode=mode+'char'
    return Random(length=length,strs=custom,mode=mode,letter=letter)

def string2data(string,default='org',want_type=None):
    return CONVERT(string).Ast(default=default,want_type=want_type)

def str2url(string):
    return WEB().str2url(string)

def is_bmc_ipv4(ipaddr,port=(623,664,443)):
    return IP(ipaddr).IsBmcIp(port=port)

def is_port_ip(ipaddr,port):
    return IP(ipaddr).IsOpenPort(port)

def ipv4(ipaddr=None,chk=False):
    return IP(ipaddr).V4(out='str',default=False)

def ip_in_range(ip,start,end):
    return IP(ip).InRange(start,end)

def is_ipv4(ipaddr=None):
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

def logging(*msg,**opts):
    return printf(*msg,**opts)

def is_py3():
    return PyVer(3)

def get_value(src,key=None,default=None,check=[str,list,tuple,dict],err=False):
    return Get(src,key,default=default,check=check,err=err)

def file_rw(name,data=None,out='string',append=False,read=None,overwrite=True):
    return FILE().Rw(name,data=data,out=out,append=append,read=read,overwrite=overwrite,finfo={})

def rm_file(filelist):
    return FILE().Rm(filelist)

def append2list(*inps,**opts):
    return LIST(inps[0]).Append(*inps[1:],**opts)

def sizeConvert(sz=None,unit='b:g'):
    return CONVERT(sz).Size(unit=unit)

def list2str(arr):
    return Join(arr,symbol=' ')

def _u_str2int(val,encode='utf-8'):
    return BYTES(val).Str2Int(encode)

def _u_bytes(val,encode='utf-8'):
    return BYTES(encode=encode).From(val)

def _u_bytes2str(val,encode='latin1'):
    return BYTES(val).Str(encode=encode)

def _u_byte2str(val,encode='latin1'):
    return _u_bytes2str(val,encode=encode)

def CompVersion(src,compare_symbol,dest,compare_range='dest',version_symbol='.'):
    return VERSION().Compare(src,compare_symbol,dest,compare_range=compare_range,version_symbol=version_symbol)

def Int(i,default={'org'}):
    return CONVERT(i).Int(default=default)

def integer(a,default=0):
    return CONVERT(a).Int(default=default)

def Lower(src):
    if isinstance(src,str): return src.lower()
    return src

def sendanmail(to,subj,msg,html=True):
    Email=EMAIL()
    Email.Send(to,sender='root@sumtester.supermicro.com',title=subj,msg=msg,html=html)

def mktemp(filename=None,suffix='-XXXXXXXX',opt='dry',base_dir='/tmp'):
    return FILE().MkTemp(filename=filename,suffix=suffix,opt=opt,base_dir=base_dir)

def check_version(a,sym,b):
    return VERSION().Check(a,sym,b)
    
def Pwd(cwd=None):
    return FILE().Path(cwd)

def get_my_directory(cwd=None):
    return FILE().Path(cwd)

def IsSame(src,chk_val,sense=False):
    return IS().Same(src,chk_val,sense=sense)

def move2first(item,pool):
    return LIST(pool).Move2first(item)

def now():
    return TIME().Int()

def int_sec():
    return TIME().Int()

def clean_ansi(src):
    return ANSI().Clean(src)

def _dict(pk={},add=False,**var):
    for key in var.keys():
        if key in pk:
            pk.update({key:var[key]})
        else:
            if add:
                pk[key]=var[key]
            else:
                return False
    return pk

def get_function_name():
    return FUNCTION().Name(sub=True)

def get_pfunction_name():
    return FUNCTION().ParentName(sub=True)

def get_function_list(objName=None,obj=None):
    return FUNCTION(obj).List(objName)

def get_caller_fcuntion_name(detail=False):
    return FUNCTION().CallerName(detail=detail)

def is_function(find,src=None):
    return FUNCTION().Is(find=find,src=src)

def get_data(data,key=None,ekey=None,default=None,method=None,strip=True,find=[],out_form=None):
    return GET(data).Value(key=key,ekey=ekey,default=default,method=method,strip=strip,find=find,out_form=out_form,peel=True)

def check_value(src,find,idx=None):
    return IS(find).In(src,idx=idx)

def get_host_name():
    return HOST().Name()

def get_host_ip(ifname=None,mac=None):
    return HOST().Ip(ifname,mac)

def get_default_route_dev():
    return HOST().DefaultRouteDev()

def get_dev_name_from_mac(mac=None):
    return HOST().DevName(mac)

def get_dev_mac(ifname):
    return HOST().Mac(dev=ifname)

def get_host_iface():
    return HOST().DefaultRouteDev()

def get_host_mac(ip=None,dev=None):
    return HOST().Mac(ip=ip,dev=dev)

def get_net_dev_ip(ifname):
    return HOST().Ip(ifname=ifname)

def get_net_device(name=None):
    return HOST().NetDevice(name)

def argtype(arg,want='_',get_data=['_']):
    return GET().ArgType(arg,want=want,get_data=get_data)

def get_function_args(func,mode='defaults'):
    return FUNCTION().Args(func=func,mode=mode)

