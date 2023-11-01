#!/bin/python
# -*- coding: utf-8 -*-
# Kage personal stuff
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
import copy
import json
import random
import string
import socket
import pickle
import base64
import hashlib
import fnmatch
import smtplib
import zipfile
import tarfile
import email.utils
from sys import modules
from pprint import pprint
import fcntl,socket,struct
from email import encoders
from threading import Thread
from datetime import datetime
from http.cookies import Morsel # This module for requests when you use build by pyinstaller command
import xml.etree.ElementTree as ET
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from multiprocessing import Process, Queue
from email.mime.multipart import MIMEMultipart
try:
    from kmport import *
except:
    pip_user_install='--user' if os.environ.get('VIRTUAL_ENV') is None else ''
    os.system('''for i in 1 2 3 4 5; do python3 -m pip install pip --upgrade {} 2>&1 | grep "however version" |grep "is available" >& /dev/null || break; done'''.format(pip_user_install))
    os.system('python3 -m pip install kmport {}'.format(pip_user_install))
    try:
        from kmport import *
    except:
        print('Can not install kmport')
        os._exit(1)

Import('import whois',install_name='python-whois')
#Import('import whois') # it print some comment on screen

global krc_define
global printf_log_base
global printf_caller_tree
global printf_caller_detail
log_intro=3
pipe_file=None
log_new_line='\n'
url_group = re.compile('^(https|http|ftp)://([^/\r\n]+)(/[^\r\n]*)?')
cdrom_ko=['sr_mod','cdrom','libata','ata_piix','ata_generic','usb-storage']

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
        if IsNone(obj):
            for i in inps:
                if isinstance(i,int):
                    rt.append(abs(i))
                elif err in [True,'err','True']:
                    rt.append(default)
        elif isinstance(obj,dict):
            keys=list(obj)
            for idx in inps:
                if isinstance(idx,int):
                    int_index=int_idx(idx,len(keys),default,err)
                    if int_index != default: rt.append(keys[int_index])
                elif isinstance(idx,tuple) and len(idx) == 2:
                    ss=Abs(idx[0],**opts)
                    ee=Abs(idx[1],**opts)
                    for i in range(ss,ee+1):
                        rt.append(keys[i])
                elif isinstance(idx,str):
                    if len(idx.split(':')) == 2:
                        ss,ee=tuple(idx.split(':'))
                        if isinstance(ss,int) and isinstance(ee,int):
                            for i in range(ss,ee+1):
                                rt.append(keys[i])
                    elif len(idx.split('-')) == 2:
                        ss,ee=tuple(idx.split('-'))
                        if isinstance(ss,int) and isinstance(ee,int):
                            for i in range(ss,ee+1):
                                rt.append(keys[i])
                    elif len(idx.split('|')) > 1:
                        for i in idx.split('|'): #A|B => A or B
                            if i in keys:
                                rt.append(i)
                    else:
                        rt.append(idx)
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

def Delete(*inps,**opts):
    if len(inps) >= 2:
        obj=inps[0]
        keys=inps[1:]
    elif len(inps) == 1:
        obj=inps[0]
        keys=opts.get('key',None)
        if isinstance(keys,list):
            keys=tuple(keys)
        elif not IsNone(keys):
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

class DIFF:
    def __init__(self):
        pass

    def Data(self,a,sym,b,ignore=None,default=None):
        if isinstance(ignore,(list,tuple)):
            if a in ignore or b in ignore:
                return default
        elif not IsNone(ignore):
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

class CONVERT:
    def __init__(self,src):
        self.src=src

    def Int(self,default=False):
        return Int(self.src,default)

    def Str(self,default='org'):
        return Str(self.src,default=default,mode='force')

    def Ast(self,default=False,want_type=None):
        return TypeData(self.src,default,want_type)

    def Form(self,default=False):
        return self.Ast(default=default)

    def Json(self,src='_#_',default=None):
        if IsNone(src,chk_val=['_#_'],chk_only=True): src=self.src
        try:
            return json.loads(src)
        except:
            return default

    def Mac2Str(self,case='lower',default=False):
        return MacV4(self.src,case=case,default=default)

    def Str2Mac(self,case='lower',default=False,sym=':',chk=False):
        return MacV4(self.src,case=case,default=default,symbol=sym)

    def Size(self,unit='b:g',default=False):
        return sizeConvert(self.src,unit=unit)

    def Url(self):
        return str2url(self.src)

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
        #if self.root_path is None: self.root_path=self.Path()
        if IsNone(self.root_path): self.root_path=self.Path()
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
        Import('import magic')
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
        if IsNone(roots): roots=self.FindRP()
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
        if IsNone(roots): roots=self.FindRP()
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
        if IsNone(roots): roots=self.FindRP()
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
        if IsNone(bin_name): return os.path.dirname(filename)
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
            #if data is None: # Read from file
            if IsNone(data): # Read from file
                if os.path.isfile(name) or (not file_only and os.path.exists(name)):
                    try:
                        if read in ['firstread','firstline','first_line','head','readline']:
                            with open(name,'rb') as f:
                                data=f.readline()
                        elif not file_only:
                            data=os.open(name,os.O_RDONLY)
                            os.close(data)
                        else:
                            with open(name,'rb') as f:
                                data=f.read()
                        if out in ['string','str']:
                            return True,Str(data)
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
                            f.write(Bytes(data))
                    elif not file_only:
                        try:
                            f=os.open(name,os.O_RDWR)
                            os.write(f,data)
                            os.close(f)
                        except:
                            return False,None
                    else:
                        with open(name,'wb') as f:
                            f.write(Bytes(data))
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

    def Mode(self,val,mode='chmod',default=False):
        '''
        convert File Mode to mask
        mode
           'chmod' : default, convert to mask (os.chmod(<file>,<mask>))
           'int'   : return to int number of oct( ex: 755 )
           'oct'   : return oct number (string)
           'str'   : return string (-rwxr--r--)
        default: False
        '''
        def _mode_(oct_data,mode='chmod'):
            #convert to octal to 8bit mask, int, string
            if mode == 'chmod':
                return int(oct_data,base=8)
            elif mode in ['int',int]:
                return int(oct_data.replace('o',''),base=10)
            elif mode in ['str',str]:
                m=[]
                #for i in list(str(int(oct_data,base=10))):
                t=False
                for n,i in enumerate(str(int(oct_data.replace('o',''),base=10))):
                    if n == 0:
                        if i == '1': t=True
                    if n > 0:
                        if i == '7':
                            m.append('rwx')
                        elif i == '6':
                            m.append('rw-')
                        elif i == '5':
                            m.append('r-x')
                        elif i == '4':
                            m.append('r--')
                        elif i == '3':
                            m.append('-wx')
                        elif i == '2':
                            m.append('-w-')
                        elif i == '1':
                            m.append('--x')
                str_mod=Join(m,'')
                if t: return str_mod[:-1]+'t'
                return str_mod
            return oct_data
        if isinstance(val,int):
            #if val > 511:       #stat.st_mode (32768 ~ 33279)
            #stat.st_mode (file: 32768~36863, directory: 16384 ~ 20479)
            if 32768 <= val <= 36863 or 16384 <= val <= 20479:   #stat.st_mode
                #return _mode_(oct(val)[-4:],mode) # to octal number (oct(val)[-4:])
                return _mode_(oct(val & 0o777),mode) # to octal number (oct(val)[-4:])
            elif 511 >= val > 63:      #mask
                return _mode_(oct(val),mode)      # to ocal number(oct(val))
            else:
                return _mode_('%04d'%(val),mode)      # to ocal number(oct(val))
        else:
            val=Str(val,default=None)
            if isinstance(val,str):
                val_len=len(val)
                num=Int(val,default=None)
                if isinstance(num,int):
                    if 3 <= len(val) <=4 and 100 <= num <= 777: #string type of permission number(octal number)
                        return _mode_('%04d'%(num),mode)
                else:
                    val_len=len(val)
                    if 9<= val_len <=10:
                        if val_len == 10 and val[0] in ['-','d','s']:
                            val=val[1:]
                    else:
                        StdErr('Bad permission length')
                        return default
                    if not all(val[k] in 'rw-' for k in [0,1,3,4,6,7]):
                        StdErr('Bad permission format (read-write)')
                        return default
                    if not all(val[k] in 'xs-' for k in [2,5]):
                        StdErr('Bad permission format (execute)')
                        return default
                    if val[8] not in 'xt-':
                        StdErr( 'Bad permission format (execute other)')
                        return default
                    m = 0
                    if val[0] == 'r': m |= stat.S_IRUSR
                    if val[1] == 'w': m |= stat.S_IWUSR
                    if val[2] == 'x': m |= stat.S_IXUSR
                    if val[2] == 's': m |= stat.S_IXUSR | stat.S_ISUID

                    if val[3] == 'r': m |= stat.S_IRGRP
                    if val[4] == 'w': m |= stat.S_IWGRP
        if isinstance(val,int):
            #if val > 511:       #stat.st_mode (32768 ~ 33279)
            #stat.st_mode (file: 32768~36863, directory: 16384 ~ 20479)
            if 32768 <= val <= 36863 or 16384 <= val <= 20479:   #stat.st_mode
                #return _mode_(oct(val)[-4:],mode) # to octal number (oct(val)[-4:])
                return _mode_(oct(val & 0o777),mode) # to octal number (oct(val)[-4:])
            elif 511 >= val > 63:      #mask
                return _mode_(oct(val),mode)      # to ocal number(oct(val))
            else:
                return _mode_('%04d'%(val),mode)      # to ocal number(oct(val))
        else:
            val=Str(val,default=None)
            if isinstance(val,str):
                val_len=len(val)
                num=Int(val,default=None)
                if isinstance(num,int):
                    if 3 <= len(val) <=4 and 100 <= num <= 777: #string type of permission number(octal number)
                        return _mode_('%04d'%(num),mode)
                else:
                    val_len=len(val)
                    if 9<= val_len <=10:
                        if val_len == 10 and val[0] in ['-','d','s']:
                            val=val[1:]
                    else:
                        StdErr('Bad permission length')
                        return default
                    if not all(val[k] in 'rw-' for k in [0,1,3,4,6,7]):
                        StdErr('Bad permission format (read-write)')
                        return default
                    if not all(val[k] in 'xs-' for k in [2,5]):
                        StdErr('Bad permission format (execute)')
                        return default
                    if val[8] not in 'xt-':
                        StdErr( 'Bad permission format (execute other)')
                        return default
                    m = 0
                    if val[0] == 'r': m |= stat.S_IRUSR
                    if val[1] == 'w': m |= stat.S_IWUSR
                    if val[2] == 'x': m |= stat.S_IXUSR
                    if val[2] == 's': m |= stat.S_IXUSR | stat.S_ISUID

                    if val[3] == 'r': m |= stat.S_IRGRP
                    if val[4] == 'w': m |= stat.S_IWGRP
        if isinstance(val,int):
            #if val > 511:       #stat.st_mode (32768 ~ 33279)
            #stat.st_mode (file: 32768~36863, directory: 16384 ~ 20479)
            if 32768 <= val <= 36863 or 16384 <= val <= 20479:   #stat.st_mode
                #return _mode_(oct(val)[-4:],mode) # to octal number (oct(val)[-4:])
                return _mode_(oct(val & 0o777),mode) # to octal number (oct(val)[-4:])
            elif 511 >= val > 63:      #mask
                return _mode_(oct(val),mode)      # to ocal number(oct(val))
            else:
                return _mode_('%04d'%(val),mode)      # to ocal number(oct(val))
        else:
            val=Str(val,default=None)
            if isinstance(val,str):
                val_len=len(val)
                num=Int(val,default=None)
                if isinstance(num,int):
                    if 3 <= len(val) <=4 and 100 <= num <= 777: #string type of permission number(octal number)
                        return _mode_('%04d'%(num),mode)
                else:
                    val_len=len(val)
                    if 9<= val_len <=10:
                        if val_len == 10 and val[0] in ['-','d','s']:
                            val=val[1:]
                    else:
                        StdErr('Bad permission length')
                        return default
                    if not all(val[k] in 'rw-' for k in [0,1,3,4,6,7]):
                        StdErr('Bad permission format (read-write)')
                        return default
                    if not all(val[k] in 'xs-' for k in [2,5]):
                        StdErr('Bad permission format (execute)')
                        return default
                    if val[8] not in 'xt-':
                        StdErr( 'Bad permission format (execute other)')
                        return default
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
                    return _mode_(oct(m),mode)
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
            if not IsNone(rtype,chk_val=['dir',None,'']): # File / Link
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

    def MkTemp(self,filename=None,suffix='-XXXXXXXX',opt='dry',base_dir='/tmp',custom=None,force=False):
        if IsNone(filename):
            filename=os.path.join(base_dir,Random(length=len(suffix)-1,strs=custom,mode='str'))
        dir_name=os.path.dirname(filename)
        file_name=os.path.basename(filename)
        name, ext = os.path.splitext(file_name)
        if type(suffix) is not str or force is True:
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
        def new_dest(dest_dir,name,ext=None,force=False):
            if os.path.isdir(dest_dir) is False:
                return False
            i=0
            new_file=new_name(name,ext)
            while True:
                rfile=os.path.join(dest_dir,new_file)
                if force is False and os.path.exists(rfile) is False:
                    return rfile
                force=False
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
        new_dest_file=new_dest(dir_name,name,ext,force=force)
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
        if IsNone(dest): return False
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

    def Path(self,filename=None):
        if filename:
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

def IsJson(src):
    try:
        json.loads(src)
        return True
    except:
        return False

def IsXml(src):
    firstLine=file_rw(src,out='string',read='firstline')
    if firstLine is False:
        filename_str=Str(src)
        if isinstance(filename_str,str):
            firstLine=filename_str.split('\n')[0]
    if isinstance(firstLine,str) and firstLine.split(' ')[0] == '<?xml': return True
    return False

def IsBin(src):
    return find_executable(src)

def IsPickle(src):
    if isinstance(src,str) and os.path.isfile(src):
        try:
            with open(src,'rb') as f: # Pickle Type
                pickle.load(f)
                return True
        except:
            pass
    return False

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
                intro=intro+'{0}() '.format(CallerName())
            elif func_name_name in ['function','instancemethod']:
                intro=intro+'{0}() '.format(func_name.__name__)
            if intro:
               for i in range(0,len(intro)):
                   intro_space=intro_space+' '
            for m in list(msg):
                n=m.split('\n')
                #if m_str is None:
                if IsNone(m_str):
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

            #if date_format in [False,None,'','no','ignore']:
            if IsNone(date_format,chk_val=[False,None,'','no','ignore']):
                date_format=None
            if IsNone(func_name,chk_val=[False,None,'','no','ignore']):
                func_name=None
            if direct:
                #log_str=' '.join(msg)
                log_str=Join(msg,symbol=' ')
            else:
                log_str=self.Format(*msg,func_name=func_name,date_format=date_format,end_new_line=end_new_line,start_new_line=start_new_line)

            # Saving log at file
            log_file=self.File(log_str,log_level,special_file=special_file)

            # print at screen
            if screen is True or (IsNone(screen) and self.screen is True):
                self.Screen(log_str,log_level)
 
            # Send Log Data to logging function (self.log_file)
            #if log_file is None:
            if IsNone(log_file):
                self.Function(log_str)

    def Function(self,*msg,**opts):
        if type(self.log_file).__name__ == 'function': 
            log_func_arg=FunctionArgs(self.log_file,mode='all')
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
        for ii in Split(cat('/proc/net/route',no_edge=True),'\n',default=[]):
            ii_a=ii.split()
            #if len(ii_a) > 8 and '00000000' == ii_a[1] and '00000000' == ii_a[7]: return ii_a[0]
            if len(ii_a) < 4 or ii_a[1] != '00000000' or not int(ii_a[3], 16) & 2:
                #If not default route or not RTF_GATEWAY, skip it
                continue
            if gw:
                if IsSame(socket.inet_ntoa(struct.pack("<L", int(ii_a[2], 16))),gw):
                    return ii_a[0]
            else:
                return ii_a[0]
        return default

    def DefaultRouteIp(self,default=None):
        for ii in Split(cat('/proc/net/route',no_edge=True),'\n'):
            ii_a=ii.split()
            if len(ii_a) < 4 or ii_a[1] != '00000000' or not int(ii_a[3], 16) & 2:
                #If not default route or not RTF_GATEWAY, skip it
                continue
            return socket.inet_ntoa(struct.pack("<L", int(ii_a[2], 16)))
        return default

    def Ip(self,ifname=None,mac=None,default=None):
        if IsNone(ifname):
            if IsNone(mac) : mac=self.Mac()
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
                    return default
        return socket.gethostbyname(socket.gethostname())

    def IpmiIp(self,default=None):
        rt=rshell('''ipmitool lan print 2>/dev/null| grep "IP Address" | grep -v Source | awk '{print $4}' ''')
        if rt[0]:return rt[1]
        return default

    def IpmiMac(self,default=None):
        rt=rshell(""" ipmitool lan print 2>/dev/null | grep "MAC Address" | awk """ + """ '{print $4}' """)
        if rt[0]:return rt[1]
        return default

    def Mac(self,ip=None,dev=None,default=None,ifname=None):
        #if dev is None and ifname: dev=ifname
        if IsNone(dev) and ifname: dev=ifname
        if IpV4(ip):
            dev_info=self.NetDevice()
            for dev in dev_info.keys():
                if self.Ip(ifname=dev) == ip:
                    return dev_info[dev]['mac']
        #ip or anyother input of device then getting default gw's dev
        if IsNone(dev): dev=self.DefaultRouteDev()
        if dev:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', Bytes(dev[:15])))
                return Join(['%02x' % ord(char) for char in Str(info[18:24])],symbol=':')
            except:
                return default
        #return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
        return MacV4('%012x' % uuid.getnode())

    def DevName(self,mac=None,default=None):
        if IsNone(mac):
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
        time=TIME()
        run_time=time.Int()
        if IpV4(ip):
            if log:
                log('[',direct=True,log_level=1)
            while True:
                if time.Out(timeout_sec):
                    if log:
                        log(']\n',direct=True,log_level=1)
                    return False,'Timeout monitor'
                if IsBreak(cancel_func):
                    if log:
                        log(']\n',direct=True,log_level=1)
                    return True,'Stopped monitor by Custom'
                if ping(ip,cancel_func=cancel_func):
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

    def Ping(self,ip,keep_good=10,timeout=3600):
        if IpV4(ip):
            return ping(ip,keep_good=keep_good,timeout=timeout)

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
           if IsNone(color_code):
               return msg
           if IsNone(os.getenv('ANSI_COLORS_DISABLED')):
               reset='''\033[0m'''
               fmt_msg='''\033[%dm%s'''
               msg=fmt_msg % (color_code,msg)
               return msg+reset

def Domainname(source=None,info=False):
    if source:
        try:
            d=whois.whois(source) # python-whois
#            d=whois.query(source) # use whois
        except Exception:
            return False,source
        else:
#            if info:
#                if d is None: return False,None
#                return True,d.__dict__
#            if d is None: return False,source
#            return d.expiration_date >= datetime.now(),source # whois
            return bool(d.domain_name),source  # python-whois
    else:
        dn=socket.getfqdn().split('.', 1)
        if len(dn) == 1:
            return True,dn[0]
        else:
            return True,dn[1]

def EmailAddress(email,local=False,check_domain=True):
    if isinstance(email,str):
        src_a=email.split('@')
        if not local and len(src_a) == 2:
            if len(src_a[0]) > 1 and len(src_a[1]) > 3 and '.' in src_a[1]:
                if check_domain is True:
                    username=src_a[0]
                    domain=src_a[1]
                    if Domainname(domain)[0]:
                        return True,email
                else:
                    return True,email
        elif local or len(src_a) in [1,2]:
            with open('/etc/passwd','r') as f:
                pwi=f.read()
            user_list=[i.split(':')[0] for i in pwi.split('\n')]
            local_domain=Domainname()[1]
            if len(src_a) == 2 and src_a[1]:
                if local_domain == src_a[1] and src_a[0] in user_list:
                    return True,email
            elif src_a[0] in user_list:
                return True,'{}@{}'.format(src_a[0],local_domain)
    return False,email

class EMAIL:
    ############################
    # GMAIL Information
    # server  : smtp.gmail.com
    # SSL Port: 465
    # user    : email address
    # password: email password
    # ex) email.Send('<to user>@gmail.com',sender='<from user>@<your domain>',title='test2',msg='test body2',filename='test.tgz',html=True,dbg=True)
    ############################
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
            part.add_header('Content-Disposition','attachment; filename="{}"'.format(filename))
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
            if IsNone(self.user): self.user=sender
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
                if IsNone(self.user): self.user=sender
                server.login(self.user, self.password)
        return server

    #def Send(self,sender,receivers,title='Subject',msg='MSG',dbg=False,filename=None,html=False):
    def Send(self,*receivers,**opts):
        sender=opts.get('sender',opts.get('from','{}@{}'.format(os.getlogin(),Domainname()[1])))
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
            return False

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

class SCREEN:
    def Kill(self,title):
        ids=self.Id(title)
        if len(ids) == 1:
            rc=rshell('''screen -X -S {} quit'''.format(ids[0]))
            if rc[0] == 0:
                return True
            return False

    def Monitor(self,title,ip,ipmi_user,ipmi_pass,find=[],timeout=600,session_out=10,stdout=False):
        if type(title) is not str or not title:
            print('no title')
            return False
        scr_id=self.Id(title)
        if scr_id:
            print('Already has the title at {}'.format(scr_id))
            return False
        
        if not IP(ip).IsBmcIp(port=(623,664,443)):
            print('{} is not ipmi ip'.format(ip))
            return False

        # if Not support SOL 
        if self.Info(ip,ipmi_user,ipmi_pass)[0] is False:
            print('The BMC is not support SOL function')
            return False

        cmd="ipmitool -I lanplus -H {} -U {} -P {} sol activate".format(ip,ipmi_user,ipmi_pass)
        # Linux OS Boot (Completely kernel loaded): find=['initrd0.img','\xff']
        # PXE Boot prompt: find=['boot:']
        # PXE initial : find=['PXE ']
        # DHCP initial : find=['DHCP']
        # ex: aa=screen_monitor('test','ipmitool -I lanplus -H <bmc ip> -U ADMIN -P ADMIN sol activate',find=['initrd0.img','\xff'],timeout=300)
        log_file=self.Log(title,cmd)
        if not log_file: 
            return False
        init_time=TIME().Int()
        mon_line=0
        old_mon_line=-1
        found=0
        find_num=len(find)
        time=TIME()
        while True:
            if TIME().Int() - init_time > timeout :
                print('Monitoring timeout({} sec)'.format(timeout))
                if self.Kill(title):
                    os.unlink(log_file)
                break
            with open(log_file,'rb') as f:
                tmp=f.read()
            #tmp=_u_byte2str(tmp)
            tmp=Str(tmp)
            if stdout: print(tmp)
                
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
                    if time.Out(session_out):
                        print('maybe not updated any screen information or SOL issue (over {}seconds)'.format(session_out))
                        if self.Kill(title):
                            os.unlink(log_file)
                        return False
                    TIME().Sleep(2)
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
            elif rc[0] == 127:
                print(rc[2])
                return False

    def Info(self,ip,ipmi_user,ipmi_pass):
        cmd="ipmitool -I lanplus -H {} -U {} -P '{}' sol info".format(ip,ipmi_user,ipmi_pass)
        rc=rshell(cmd)
        enable=False
        channel=1
        rate=9600
        port=623
        if rc[0] == 0:
            for ii in rc[1].split('\n'):
                ii_a=ii.split()
                if ii_a[0] == 'Enabled' and ii_a[-1] == 'true':
                    enable=True
                elif ii_a[0] == 'Volatile':
                    if '.' in ii_a[-1]:
                        try:
                            rate=int(float(ii_a[-1]) * 1000)
                        except:
                            pass
                    else:
                        try:
                            rate=int(ii_a[-1])
                        except:
                            pass
                elif ii_a[0] == 'Payload':
                    if ii_a[1] == 'Channel':
                        try:
                            channel=int(ii_a[-2])
                        except:
                            pass
                    elif ii_a[1] == 'Port':
                        try:
                            port=int(ii_a[-1])
                        except:
                            pass
        return enable,rate,channel,port,'~~~ console=ttyS1,{}'.format(rate)
                
####################################STRING##################################################
def cut_string(string,max_len=None,sub_len=None,new_line='\n',front_space=False,out_format=list):
    front_space=0 if front_space is True else None
    return Cut(string,head_len=max_len,body_len=sub_len,new_line=new_line,front_space=front_space,out=out_format,newline_head=True)

####################################KEYS##################################################
def FirstKey(src,default=None):
    return Next(src,default=default)

def code_error(email_func=None,email=None,email_title=None,email_server=None,log=None,log_msg='',default=None):
    log_msg=ExceptMessage(msg=log_msg,default=default)
    if log_msg != default:
        if log: log('\n!!ERROR!!: {}'.format(log_msg),log_level=1)
        if email_func and email and email_title:
            a=email_func(email,email_title,log_msg,dj_ip=email_server)
            TIME().Sleep(5)
    return default

def DirName(src,default=None):
    dirname=Path(src,default=default)
    if dirname == default: return default
    if dirname == '': return '.'
    return dirname

def Args2Str(args,default='org'):
    if isinstance(args,(tuple,list)):
        args=list(args)
        for i in range(0,len(args)):
            if "'" in args[i]:
                args[i]='''"{}"'''.format(args[i])
            elif '"' in args[i]:
                args[i]="""'{}'""".format(args[i])
            elif ' ' in args[i]:
                args[i]='''"{}"'''.format(args[i])
        return ' '.join(args)
    return args

def check_value(src,find,idx=None):
    '''Check key or value in the dict, list or tuple then True, not then False'''
    if isinstance(src, (list,tuple,str,dict)):
        if idx is None:
            if find in src:
                return True
        else:
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
    return False

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
        #if find is None:
        if IsNone(find):
            #if out in ['raw',None] and len(src.keys()) == 1 : return list(src.keys())[0]
            if IsNone(out,chk_val=['raw',None,'']) and len(src.keys()) == 1 : return list(src.keys())[0]
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

def findXML(xmlfile,find_name=None,find_path=None,default=None,out='xmlobj',get_opt=None):
    #<Menu name="Security">
    #  <Setting name="Administrator Password" type="Password">
    #    <Information>
    #      <HasPassword>False</HasPassword>
    #    </Information>
    #  </Setting>
    #</Menu>
    #findXML(cfg_file,find_name='Administrator Password',find_path='./Information/HasPassword',out='data'))
    # => False
    if os.path.isfile(xmlfile):
        try:
            tree=ET.parse(xmlfile)
            root=tree.getroot()
        except:
            return default
    else:
        try:
            root=ET.fromstring(xmlfile)
        except:
            return default
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
        found_result=found_root.findall(find_path)
        # <element>.tag: name, .text: data, .attrib: dict
        rt=[]
        if out in ['tag','name']:
            for ii in found_result:
                rt.append(ii.tag)
        elif out in ['text','data']:
            for ii in found_result:
                if get_opt:
                    rt.append(ii.get(get_opt,default))
                else:
                    rt.append(ii.text)
        elif out in ['attrib','att']:
            for ii in found_result:
                rt.append(ii.attrib)
        if rt:
            return rt
        else:
            return found_result
    else:
        if found_root:
            if out in ['tag','name']:
                return found_root.tag
            elif out in ['text','data']:
                if get_opt:
                    return found_root.get(get_opt,default)
                else:
                    return found_root.text
            elif out in ['attrib','att']:
                return found_root.attrib
            return found_root
    return default

def Compress(data,mode='lz4'):
    if mode == 'lz4':
        Import('from lz4 import frame')
        return frame.compress(data)
    elif mode == 'bz2':
        Import('import bz2')
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
        Import('import magic')
        aa=magic.from_buffer(open(filename,'rb').read(2048))
        if aa: return aa.split()[0].lower()
        return 'unknown'

    if mode == 'lz4':
        Import('from lz4 import frame')
        return frame.decompress(data)
    elif mode == 'bz2':
        Import('import bz2')
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

def ls(dirname,opt=''):
    if not IsNone(dirname) and os.path.isdir(dirname):
        dirlist=[]
        dirinfo_a=list(os.walk(dirname))
        if not IsNone(dirinfo_a):
            dirinfo=dirinfo_a[0]
            if opt == 'd':
                dirlist=Get(dirinfo,1)
            elif opt == 'f':
                dirlist=Get(dirinfo,2)
            else:
                dirlist=Get(dirinfo,1)+Get(dirinfo,2)
            return dirlist
    return False

def append(src,addendum):
    type_src=type(src)
    type_data=type(addendum)
    if IsNone(src):
        if type_data is str:
            src=''
        elif type_data is dict:
            src={}
        elif type_data is list:
            src=[]
        elif type_data is tuple:
            src=()
        type_src=type(src)
    if IsNone(addendum):
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
    if IsNone(keep,chk_val=[None,'',0]):
        return True,'N/A(Missing keep parameter data)'
    if log:
        log('[',direct=True,log_level=1)
    time=TIME()
    while True:
        if time.Out(timeout):
            if log:
                log(']\n',direct=True,log_level=1)
            return False,'Timeout monitor'
        if IsBreak(cancel_func) or stop_func is True:
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
            file_path=os.path.dirname(in_filename) 
            if file_path != '.': rc['path_mode']=oct(os.stat(file_path).st_mode)[-4:]
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
                        try:
                            with open(in_filename,'rb') as f:
                                fdata=f.read()
                            if md5sum:
                                rc['md5']=md5(fdata)
                            if data:
                                rc['data']=fdata
                        except:
                            print('Permission denied: {}'.format(in_filename))
                            rc['exist']=False
        return rc

    rc={'exist':False,'includes':[]}
    if type(filename) is str:
        rc.update(get_file_data(filename))
        if rc['dir']:
            root_path=filename
            real_filename=None
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

def save_file(data,dest=None,filename=None,force=False):
#    return data.Extract(dest=dest,sub_dir=True)
    if not isinstance(data,dict): return False
    if not data.get('exist'): return False
    if isinstance(dest,str): 
        if os.path.exists(dest) and not os.path.isdir(dest):
            printf('Already exist {}'.format(dest),dsp='e')
            return False
        elif os.path.isdir(dest) is False:
            os.system('mkdir -p {0}'.format(dest))
    else:
        dest=os.getcwd()
    if data.get('dir'):
        if os.path.exists(data['path']) and not os.path.isdir(data['path']):
            printf('Already exist {}'.format(dest),dsp='e')
            return False
        elif not os.path.isdir(data['path']):
            os.system('mkdir -p {0}'.format(data['path']))
            if data.get('mode'): os.chmod(data['path'],file_mode(data.get('mode')))
        # If include directory or files 
        for ii in data.get('includes',[]):
            if ii['path']:
                sub_dir=os.path.join(dest,ii['path'])
            else:
                sub_dir='{}'.format(dest)
            if not os.path.isdir(sub_dir):
                os.system('mkdir -p {}'.format(sub_dir))
                if ii.get('path_mode'): os.chmod(sub_dir,file_mode(ii.get('path_mode')))
            sub_file=os.path.join(sub_dir,ii['name'])
            with open(sub_file,'wb') as f:
                f.write(Bytes(ii['data']))
            if ii.get('mode'): os.chmod(sub_file,file_mode(ii.get('mode')))
    else:
        # if file then save
        if force is False and os.path.exists(dest) and not os.path.isdir(dest):
            printf('Already exist {}'.format(dest),dsp='e')
            return False
        if os.path.isdir(dest):
            new_file=os.path.join(dest,data['name'])
        else:
            new_file=dest
        with open(new_file,'wb') as f:
            f.write(Bytes(data.get('data','')))
        chmod_mode=file_mode(data.get('mode'))
        if chmod_mode: os.chmod(new_file,chmod_mode)
    return True

#########################################################################
def error_exit(msg=None):
    if not IsNone(msg):
       print(msg)
    sys.exit(-1)


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
                intro=intro+'{0}() '.format(CallerName())
        if intro:
           for i in range(0,len(intro)+1):
               intro_space=intro_space+' '
        for m in list(msg):
            if IsNone(m_str):
                m_str='{0}{1}{2}{3}'.format(start_new_line,intro,m,end_new_line)
            else:
                m_str='{0}{1}{2}{3}{4}'.format(start_new_line,m_str,intro_space,m,end_new_line)
        return m_str

def md5(string):
    return hashlib.md5(Bytes(string)).hexdigest()

def ipmi_cmd(cmd,ipmi_ip=None,ipmi_user='ADMIN',ipmi_pass='ADMIN',log=None):
    if IsNone(ipmi_ip):
        ipmi_str=""" ipmitool {0} """.format(cmd)
    else:
        ipmi_str=""" ipmitool -I lanplus -H {0} -U {1} -P '{2}' {3} """.format(ipmi_ip,ipmi_user,ipmi_pass,cmd)
    if log:
        log(' ipmi_cmd():{}'.format(ipmi_str),log_level=7)
    return rshell(ipmi_str)

    
def get_ipmi_mac(ipmi_ip=None,ipmi_user='ADMIN',ipmi_pass='ADMIN',loop=0):
    ipmi_mac_str=None
    if IsNone(ipmi_ip):
        ipmi_mac_str=""" ipmitool lan print 2>/dev/null | grep "MAC Address" | awk """
    elif IpV4(ipmi_ip):
        ipmi_mac_str=""" ipmitool -I lanplus -H {0} -U {1} -P {2} lan print 2>/dev/null | grep "MAC Address" | awk """.format(ipmi_ip,ipmi_user,ipmi_pass)
    if not IsNone(ipmi_mac_str):
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

def git_ver(git_dir=None):
    if not IsNone(git_dir) and os.path.isdir('{0}/.git'.format(git_dir)):
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
                                    if IsNone(size):
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
                            if IsNone(size):
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
#    if IpV4(ipmi_ip):
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

def net_send_data(sock,data,key='kg',enc=False,timeout=0,instant=False,log=None,err_scr=True):
    # if close=True then just send data and close socket
    # if close=False then it need close socket code
    # ex)
    #      aa=net_send_data(sock,.....)
    #      if aa[0] is True: sock.close()
    start_time=TIME().Int()
    ok,enc_data=packet_enc(data,key=key,enc=enc)
    if ok:
        try:
            sock.sendall(enc_data)
            if instant is True:
                sock.close()
            return True,'OK'
        except:
            if instant is True:
                if sock: sock.close()
            if timeout > 0:
                #timeout=sock.gettimeout()
                if TIME().Int() - start_time > timeout-1:
                    return False,'Sending Socket Timeout'
    return False,enc_data

def net_receive_data(sock,key='kg',progress=None,retry=0,retry_timeout=30,progress_msg=None,log=None,err_scr=True):
    # decode code here
    ok,size,data_type,enc=packet_head(sock,retry=retry,timeout=retry_timeout)
    if krc(ok,chk=True):
        # File not found Error log size is 57. So if 57 then ignore progress
        if size == 57: progress=False
        data_ok,data=packet_receive_all(sock,size,progress=progress,progress_msg=progress_msg,log=log,retry=retry,retry_timeout=retry_timeout,err_scr=err_scr)
        if krc(data_ok,chk=True):
            real_data=packet_dec(data,enc,key=key)
            if real_data: return [data_type,real_data]
            return [True,None]
        return [data_ok,data]
    return [ok,size]

def net_put_and_get_data(IP,data,PORT=8805,key='kg',timeout=3,try_num=1,try_wait=[0,5],progress=None,enc=False,upacket=None,SSLC=False,progress_msg=None,instant=True,dbg=6,log=None,wait_time=3,err_scr=True):
    sent=False,'Unknown issue'
    for ii in range(0,try_num):
        if upacket: # Update packet function for number of try information ([#/<total #>])
            data=upacket('ntry',[ii+1,try_num],data)
        start_time=TIME().Int()
        ok,sock=net_get_socket(IP,PORT,timeout=timeout,SSLC=SSLC,log=log,err_scr=err_scr)
        if ok is False:
            if ii >= try_num-1:
                return ok,sock,sock
            printf('Can not get socket data [{}/{}], wait {}s'.format(ii+1,try_num,wait_time) if dbg < 4 else '.',log=log)
            TIME().Sleep(wait_time)
            continue
        if try_num > 0: 
            rtry_wait=(timeout//try_num)+1
        else:
            rtry_wait=try_wait
        sent=False,'Unknown issue',sock
        try:
            sent=net_send_data(sock,data,key=key,enc=enc,log=log,err_scr=err_scr,timeout=timeout)
        except:
            if sock:
                sock.close()
            os.system("""[ -f /tmp/.{0}.{1}.crt ] && rm -f /tmp/.{0}.{1}.crt""".format(IP,PORT))
        if sent[0]:
            if ClosedSocket(sock): # Already closed socket after sent
                return [False,'Already closed/lost the socket',sock]
            else:
                nrcd=net_receive_data(sock,key=key,progress=progress,progress_msg=progress_msg,log=log,err_scr=err_scr,retry=2,retry_timeout=timeout)
                return nrcd+[sock]
        else:
            if timeout >0:
                if TIME().Int() - start_time >= timeout-1:
                    return [False,'Socket Send Timeout',sock]
                #return [False,'Data protocol version mismatch']
        if sock and instant is True:
            sock.close()
            sock=None
        if try_num > 1:
            printf('try send data ... [{}/{}]'.format(ii+1,try_num),log=log)
            TIME().Sleep(try_wait)
    return [False,'Send fail({}) :\n{}'.format(sent[1],data),sock]

def net_get_socket(host,port,timeout=3,dbg=6,SSLC=False,log=None,err_scr=True): # host : Host name or IP
    try:
        af, socktype, proto, canonname, sa = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)[0]
    except:
        _e_='Can not get network informatin of {}:{}'.format(host,port)
        return [False,_e_]
    try:
        soc = socket.socket(af, socktype, proto)
        if timeout > 0:
            soc.settimeout(timeout)
    except socket.error as msg:
        _e_='could not open socket of {0}:{1}\n{2}'.format(host,port,msg)
        printf(_e_,log=log,dsp='e' if err_scr else 'd')
        return [False,_e_]
    ###### SSL Wrap ######
    _e_=None
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
                return [True,soc]
            except socket.error as msg:
                printf(msg,log=log,log_level=dbg,mode='e' if err_scr else 'd')
                TIME().Sleep(1)
    ########################
    else:
        try:
            soc.connect(sa)
            return [True,soc]
        except socket.error as msg:
            _e_='can not connect at {0}:{1}\n{2}'.format(host,port,msg)
            printf(_e_,log=log,log_level=dbg,dsp='e' if err_scr else 'd')
    return [False,_e_]

def net_start_server(server_port,main_func_name,server_ip='',timeout=0,max_connection=10,log_file=None,certfile=None,keyfile=None,log=None,err_scr=True):
    ssoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if timeout > 0:
        ssoc.settimeout(timeout)
    try:
        ssoc.bind((server_ip, server_port))
    except socket.error as msg:
        printf('Bind failed. Error : {0}'.format(msg),log=log,mode='e' if err_scr else 'd',logfile=log_file)
        os._exit(1)
    ssoc.listen(max_connection)
    printf('Start server for {0}:{1}'.format(server_ip,server_port),log=log,logfile=log_file,dsp='f')
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
            printf('No more generate thread for client from {0}:{1}'.format(ip,port),dsp='e' if err_scr else 'd',log=log,logfile=log_file)
    ssoc.close()

def net_start_single_server(server_port,main_func_name,server_ip='',timeout=0,max_connection=10,log_file=None,certfile=None,keyfile=None,log=None,err_scr=True):
    ssoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if timeout > 0:
        ssoc.settimeout(timeout)
    try:
        ssoc.bind((server_ip, server_port))
    except socket.error as msg:
        printf('Bind failed. Error : {0}'.format(msg),log=log,dsp='e' if err_scr else 'd',logfile=log_file)
        os._exit(1)
    ssoc.listen(max_connection)
    printf('Start server for {0}:{1}'.format(server_ip,server_port),log=log,dsp='e' if err_scr else 'd',logfile=log_file)
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
        if IsNone(name):
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
    if IsNone(keyfile) and IsNone(certfile):
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

def net_put_data(IP,data,PORT=8805,key='kg',timeout=3,try_num=1,try_wait=[1,10],progress=None,enc=False,upacket=None,dbg=6,wait_time=3,SSLC=False,instant=True,log=None,err_scr=True):
    sent=False,'Unknown issue',None
    for ii in range(0,try_num):
        if upacket: # Update packet function for number of try information ([#/<total #>])
            data=upacket('ntry',[ii+1,try_num],data)
        ok,sock=net_get_socket(IP,PORT,timeout=timeout,dbg=dbg,SSLC=SSLC,log=log,err_scr=err_scr)
        if ok is False:
            if ii >= try_num-1:
                return [ok,sock,sock]
            printf('Can not get socket data [{}/{}], wait {}s'.format(ii+1,try_num,wait_time) if dbg < 4 else '.',log=log)
            TIME().Sleep(wait_time)
            continue
        sent=[False,'Unknown issue',sock]
        try:
            sent=net_send_data(sock,data,key=key,enc=enc,log=log)
        except:
            printf('send fail, try again ... [{}/{}]'.format(ii+1,try_num),log=log)
        if sent[0]:
            if sock and instant:
                sock.close()
                sock=None
            return [True,'sent',sock]
        if try_num > 1:
            wait_time=Random(length=0,strs=try_wait,mode='int')
            printf('try send data ... [{}/{}], wait {}s'.format(ii+1,try_num,wait_time),log=log,log_level=dbg)
            TIME().Sleep(wait_time)
    return [False,'Send fail({}) :\n{}'.format(sent[1],data),sock]


def encode(string):
    enc='{0}'.format(string)
    tmp=zlib.compress(enc.encode("utf-8"))
    return '{0}'.format(base64.b64encode(tmp).decode('utf-8'))

def decode(string):
    if type(string) is str:
        dd=zlib.decompress(base64.b64decode(string))
        return '{0}'.format(dd.decode("utf-8"))
    return string

def get_node_info(loop=0):
    host_ip=get_host_ip()
    return {
         'host_name':get_host_name(),
         'host_ip':host_ip,
         'host_mac':get_host_mac(ip=host_ip),
         'ipmi_mac':get_ipmi_mac(loop=loop)[1],
         'ipmi_ip':get_ipmi_ip()[1],
         }

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
        firstLine=Get(firstLine_i,1)
    else:
        filename_str=_u_byte2str(filename)
        if isinstance(filename_str,str):
            firstLine=filename_str.split('\n')[0]
    if isinstance(firstLine,str) and firstLine.split(' ')[0] == '<?xml':
        return True
    return False

def get_iso_uid(filename):
    if type(filename) is not str:
        return False,None,None
    if os.path.exists(filename):
        uid_cmd='''sudo /usr/sbin/blkid {}'''.format(filename)
        rc=rshell(uid_cmd)
        if rc[0] == 0:
            uid_str='{0}_{1}'.format(FIND(rc[1]).Find('UUID="(\w.*)" L'),FIND(rc[1]).Find('LABEL="(\w.*)" T')).replace(' ','_')
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

def pipe_msg(**opts):
    m={}
    if not pipe_file: return False
    if os.path.isfile(pipe_file):
        with open(pipe_file,'rb') as f:
            buf=f.read()
        try:
            m=pickle.loads(buf)
        except:
            pass
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

#################################################################
def gen_random_string(length=8,letter='*',digits=True,symbols=True,custom=''):
    mode='alpha'
    if digits:mode=mode+'num'
    if symbols:mode=mode+'char'
    return Random(length=length,strs=custom,mode=mode,letter=letter)

def TypeData(src,default='org',want_type=None,spliter=None):
    '''Convert (input)data to want type (ex: str -> list, int, ...), can not convert to type then return False'''
    if want_type is str and spliter and isinstance(src,(list,tuple)):
        return spliter.join(src)
    elif want_type is str and not isinstance(src,str):
        return '''{}'''.format(src)
    elif want_type is int and not isinstance(src,int):
        try:
            return int(src)
        except:
            if default in ['org',{'org'}]: return src
            return default
    elif want_type in [list,tuple] and isinstance(src,str) and isinstance(spliter,str):
        if want_type is tuple:
            return tuple(src.split(spliter))
        return src.split(spliter)
    elif want_type is tuple and isinstance(src,(list,dict)):
        if isinstance(src,dict):
            if spliter == 'key':
                return tuple(src.keys())
            elif spliter == 'value':
                return tuple(src.values())
            else:
                return tuple(src.items())
        return tuple(src)
    elif want_type is list and isinstance(src,(tuple,dict)):
        if isinstance(src,dict):
            if spliter == 'key':
                return list(src.keys())
            elif spliter == 'value':
                return list(src.values())
            else:
                return list(src.items())
        return list(src)
    elif want_type:
        if isinstance(src,want_type):
            return src
    if isinstance(src,str):
        try:
            return ast.literal_eval(src)
        except:
            try:
                return json.loads(src)
            except:
                pass
    if default in ['org',{'org'}]: return src
    return default

def sizeConvert(sz=None,unit='b:g'):
    try:
        sz=int(sz)
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
            sz=inc(sz)
        else:
            sz=dec(sz)
    return sz

############################################
#Temporary function
############################################
def compare(a,sym,b,ignore=None):
    if type(a) is not int or type(b) is not int:
        return False
    if not IsNone(ignore):
        if eval('{} == {}'.format(a,ignore)) or eval('{} == {}'.format(b,ignore)):
            return False
    return eval('{} {} {}'.format(a,sym,b))

def dput(dic=None,keys=None,val=None,force=False,safe=True):
    if not IsNone(dic) and keys:
        tmp=dic
        keys_arr=keys.split('/')
        keys_num=len(keys_arr)
        for ii in keys_arr[:(keys_num-1)]:
            if ii in tmp:
                if type(tmp[ii]) == type({}):
                    dtmp=tmp[ii]
                else:
                    if IsNone(tmp[ii]):
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

def dget(dict=None,keys=None):
    if IsNone(dict) or IsNone(keys):
        return False
    tmp=dict.copy()
    keys_path=keys.split('/')
    if keys_path[0] == '': keys_path=keys_path[1:]
    for ii in keys.split('/'):
        if ii in tmp:
           dtmp=tmp[ii]
        else:
           return False
        tmp=dtmp
    return tmp

def isfile(filename=None):
   if Type(filename,'str',data=True) and os.path.isfile(filename):
      return True
   return False

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

def reduce_string(string,symbol=' ',snum=0,enum=None):
    string_a=Cut(string,symbol=symbol,out=list)
    sidx=FixIndex(string_a,snum)
    eidx=FixIndex(string_a,enum if isinstance(enum,int) else len(string_a))
    return Join(string_a[sidx:edix],' ')

def sreplace(pattern,sub,string):
    return re.sub('^%s' % pattern, sub, string)

def ereplace(pattern,sub,string):
    return re.sub('%s$' % pattern, sub, string)

def rreplace(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

def argtype(arg,want='_',get_data=['_']):
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

def Lower(src,default='org'):
    if isinstance(src,str): return src.lower()
    if default in ['org',{'org'}]: return src
    return default

def Upper(src,default='org'):
    if isinstance(src,str): return src.upper()
    if default in ['org',{'org'}]: return src
    return default
############################################
#Temporary function map for replacement
############################################
def sendanmail(to,subj,msg,html=True):
    Email=EMAIL()
    return Email.Send(to,sender='root@sumtester.supermicro.com',title=subj,msg=msg,html=html)

def mktemp(filename=None,suffix='-XXXXXXXX',opt='dry',base_dir='/tmp',force=False):
    return FILE().MkTemp(filename=filename,suffix=suffix,opt=opt,base_dir=base_dir,force=force)

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

def get_my_directory(cwd=None):
    return FILE().Path(cwd)

def str2url(string):
    return WEB().str2url(string)

def web_server_ip(request):
    return WEB(request).GetIP(mode='server')

def web_client_ip(request):
    return WEB(request).GetIP(mode='client')

def web_req(host_url=None,**opts):
    return WEB().Request(host_url,**opts)

def web_session(request):
    return WEB(request).Session()

def file_rw(name,data=None,out='string',append=False,read=None,overwrite=True):
    return FILE().Rw(name,data=data,out=out,append=append,read=read,overwrite=overwrite,finfo={})

def rm_file(filelist):
    return FILE().Rm(filelist)

def screen_kill(self,title):
    return SCREEN().Kill(title)

def screen_monitor(title,ip,ipmi_user,ipmi_pass,find=[],timeout_sec=600,session_out=10):
    return SCREEN().Monitor(title,ip,ipmi_user,ipmi_pass,find=find,timeout=timeout_sec,session_out=session_out)

def screen_id(title=None):
    return SCREEN().Id(title)

def screen_logging(title,cmd):
    return SCREEN().Log(title,cmd)

def now():
    return TIME().Int()

def int_sec():
    return TIME().Int()

def get_function_args(func,mode='defaults'):
    return FunctionArgs(func,mode=mode)

def Var(src,obj=None,default=None,mode='all',VarType=None):
    return Variable(src=src,obj=obj,parent=0,default=default,mode=mode,VarType=VarType)

def get_data(data,key=None,ekey=None,default=None,method=None,strip=True,find=[],out_form=None):
    return Get(data,key=key,ekey=ekey,default=default,method=method,strip=strip,find=find,out_form=out_form,peel=True)

def is_function(find,src=None):
    return IsFunction(src,find=find)

def get_caller_fcuntion_name(detail=False):
    return CallerName(detail=detail)

def get_function_list(obj=None):
    return FunctionList(obj)

def get_pfunction_name():
    return FunctionName(parent=1)

def get_function_name():
    return FunctionName()

def clean_ansi(src):
    return CleanAnsi(src)

def move2first(item,pool):
    return LIST(pool).Move2first(item)

def Pwd(cwd=None):
    return FILE().Path(cwd)

def check_version(a,sym,b):
    return CompVersion(a,sym,b)

def integer(a,default=0):
    return Int(a,default=default)

def list2str(arr):
    return Join(arr,symbol=' ')

def _u_str2int(val,encode='utf-8'):
    return Bytes2Int(val,encode=encode,default='org')

def _u_bytes(val,encode='utf-8'):
    return Bytes(val,encode=encode)

def _u_bytes2str(val,encode='latin1'):
    return Str(val,encode=encode)

def _u_byte2str(val,encode='latin1'):
    return Str(val,encode=encode)

def append2list(*inps,**opts):
    return LIST(inps[0]).Append(*inps[1:],**opts)

def get_value(src,key=None,default=None,check=[str,list,tuple,dict],err=False):
    return Get(src,key,default=default,_type_=check,err=err)

def logging(*msg,**opts):
    return printf(*msg,**opts)

def is_py3():
    return PyVer(3)

def ip2num(ip):
    return IpV4(ip,out='int')

def is_ipv4(ipaddr=None):
    return True if IpV4(ipaddr) else False

def is_bmc_ipv4(ipaddr,port=(623,664,443)):
    return True if IpV4(ipaddr,port=port) else False

def is_port_ip(ipaddr,port):
    return True if IpV4(ipaddr,port=port) else False

def ipv4(ipaddr=None,chk=False):
    return IpV4(ipaddr)

def ip_in_range(ip,start,end):
    return IpV4(ip,pool=(start,end))

def string2data(src,default='org',want_type=None,spliter=None):
    return TypeData(src,default,want_type,spliter)

def mac2str(mac,case='lower'):
    return MacV4(mac,case=case)

def str2mac(mac,sym=':',case='lower',chk=False):
    return MacV4(mac,symbol=sym,case=case)

def is_mac4(mac=None,symbol=':',convert=True):
    return True if MacV4(mac,symbol=symbol) else False

def Wrap(src,fspace='',nspace='',space_mode='space',sym='\n',default=None,NFLT=False,out=str):
    if isinstance(space,str): space=len(space)
    return STR(src).Tap(fspace=fspace,nspace=nspace,new_line=sym,NFLT=NFLT,mode=space_mode,default=default,out=out)

def ddict(*inps,**opts):
    return Dict(*inps,**opts)

def replacestr(data,org,new):
    return Replace(data,org,new)

def findstr(string,find,prs=None,split_symbol='\n',patern=True):
    return FIND(string).Find(find,sym=split_symbol,prs=prs,peel=False)

def get_key(dic=None,find=None):
    return GetKey(dic,find=find)

def find_key_from_value(dic=None,find=None):
    return GetKey(dic,find=find)

def is_cancel(func):
    return IsBreak(func)

def file_mode(val):
    return FILE().Mode(val)
