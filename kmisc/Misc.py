#!/bin/python
# -*- coding: utf-8 -*-
# Kage personal stuff
#
from __future__ import print_function
import sys,os,re,copy
import tarfile
import tempfile
from os import close, remove
import random
import hashlib
from kmisc.Import import *
Import('from kmisc.Type import Type')
Import('from kmisc.OutFormat import OutFormat')
Import('from kmisc.Abs import Abs')
Import('from kmisc.Crc import Crc')

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
url_group = re.compile('^(https|http|ftp)://([^/\r\n]+)(/[^\r\n]*)?')
log_intro=3
log_new_line='\n'

cdrom_ko=['sr_mod','cdrom','libata','ata_piix','ata_generic','usb-storage']

def is_cancel(func):
    if func:
        ttt=type(func).__name__
        if ttt in ['function','instancemethod','method']:
            if func():
                return True
        elif ttt in ['bool','str'] and func:
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

def sendanmail(to,subj,msg,html=True):
    if html:
        email_msg='''To: {0}
Subject: {1}
Content-Type: text/html
<html>
<body>
<pre>
{2}
</pre>
</body>
</html>'''.format(to,subj,msg)
    else:
        email_msg=''
    cmd='''echo "{0}" | sendmail -t'''.format(email_msg)
    return rshell(cmd)

def md5(string,encode='utf-8'):
    if PyVer(3):
        if isinstance(string,bytes):
            return hashlib.md5(string).hexdigest()
        else:
            return hashlib.md5(bytes(string,encode)).hexdigest()
    return hashlib.md5(bytes(string)).hexdigest()

def cat(filename,no_end_newline=False):
    tmp=FILE(filename).Rw()
    if tmp[0]:
        tmp_data=GET(tmp).Value(1)
        if isinstance(tmp_data,str) and no_end_newline:
            tmp_a=tmp_data.split('\n')
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

def make_tar(filename,filelist,ctype='gz',ignore_file=[]):
    if ctype == 'bz2':
        tar = tarfile.open(filename,"w:bz2")
    elif ctype == 'stream':
        tar = tarfile.open(filename,"w:")
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
            if ii in ignore_file or ii in ig_dupl:
                continue
            ig_dupl.append(ii)
            tar.add(ii)
        elif os.path.isdir(ii):
            for r,d,f in os.walk(ii):
                if r in ignore_file or (len(d) == 1 and d[0] in ignore_file):
                    continue
                for ff in f:
                    aa=os.path.join(r,ff)
                    if aa in ignore_file or aa in ig_dupl:
                        continue
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


def mktemp(filename=None,suffix='-XXXXXXXX',opt='dry',base_dir='/tmp'):
   if filename is None:
       filename=os.path.join(base_dir,random_str(length=len(suffix)-1,mode='str'))
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
                   rnd_str='.{}'.format(random_str(length=len(suffix)-1,mode='str'))
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
                    sleep(try_wait)
    return False

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

def get_value(src,key=None,default=None,check=[list,tuple,dict]):
    return Get(src,key,default=default,check=check)

def krc(rt,chk='_',rtd={'GOOD':[True,'True','Good','Ok','Pass',{'OK'},0],'FAIL':[False,'False','Fail',{'FAL'}],'NONE':[None,'None','N/A',{'NA'}],'IGNO':['IGNO','Ignore',{'IGN'}],'ERRO':['ERR','Error',{'ERR'}],'WARN':['Warn',{'WAR'}],'UNKN':['Unknown','UNKN',{'UNK'}],'JUMP':['Jump',{'JUMP'}]}):
    if chk != '_':return Crc(rt,rc=rtd)
    return Crc(rt,chk=chk,rc=rtd)

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
            if rc in find:
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

if __name__ == "__main__":
    class ABC:
        uu=3
        def __init__(self):
            self.a=1
            self.b=2
    print(get_value(ABC(),'b',default=None))
    print(get_value(ABC(),'uu',default=None))
    print(get_value(ABC(),'ux',default=None))

    a=[0,1,2,3]
    print(get(a,1,-8,3,-2))
