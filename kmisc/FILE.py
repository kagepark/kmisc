#Kage Park
from distutils.spawn import find_executable
import os
import fnmatch
from kmisc.Import import *
Import('from kmisc.CONVERT import CONVERT')
Import('import magic')
Import('import tarfile')
Import('import zipfile')

class FILE:
    def __init__(self,*inp,**opts):
        self.root_path=opts.get('root_path',None)
        if self.root_path is None: self.root_path=os.path.dirname(os.path.abspath(__file__))
        self.info={}
        sub_dir=opts.get('sub_dir',False)
        data=opts.get('data',False)
        md5sum=opts.get('md5sum',False)
        self.filelist=[]
        for filename in inp:
            self.filelist=self.filelist+self.FileList(filename,sub_dir=sub_dir)
        for ff in self.filelist:
            self.Get(ff,data=data,md5sum=md5sum)

    def FileList(self,name,sub_dir=False,default=[]):
        if isinstance(name,str):
            if name[0] == '/': self.root_path='/'
            if os.path.isfile('{}/{}'.format(self.root_path,name)): return [name]
            if os.path.isdir('{}/{}'.format(self.root_path,name)):
                if sub_dir:
                    rt = []
                    pwd=os.getcwd()
                    os.chdir(self.root_path)
                    for base, dirs, files in os.walk(name):
                        rt.extend(os.path.join(base, f) for f in files)
                    os.chdir(pwd)
                    return rt
                else:
                    return [os.path.join(name,f) for f in os.listdir('{}/{}'.format(self.root_path,name))]
        return default

    def PathDir(self,path):
        rt=self.info
        if isinstance(path,str) and path[0] == '/':
            cur_path='/'
        else:
            cur_path='{}'.format(self.root_path)
        if '/' in path:
            for ii in os.path.dirname(path).split('/'):
                if ii:
                    cur_path=os.path.join(cur_path,ii)
                    if os.path.isdir(cur_path):
                        if ii not in rt: rt[ii]={}
                        rt=rt[ii]
        return rt

    def MkInfo(self,rt,filename=None,**opts):
        if isinstance(rt,dict):
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
            if opts:
                rt[' i '].update(opts)

    def GetInfo(self,data,*inps):
        if isinstance(data,dict):
            rt=[]
            for ii in inps:
                if ii == 'data' and ii in data: rt.append(data[ii])
                if ' i ' in data and ii in data[' i ']: rt.append(data[' i '][ii])
            return rt

    def Get(self,filename,default={},data=False,md5sum=False,sub_dir=False):
        if isinstance(filename,str):
            rt=self.PathDir(filename)
            tfilename=os.path.join(self.root_path,filename)
            if os.path.exists(tfilename):
                self.info['root_path']=self.root_path
                if os.path.isdir(tfilename):
                    self.MkInfo(rt,tfilename,type='dir')
                elif os.path.islink(tfilename): # it is Link File
                    file_name=os.path.basename(tfilename)
                    rt[file_name]={}
                    rt=rt[file_name]
                    self.MkInfo(rt,filename=tfilename,type='link',dest=os.path.realpath(tfilename))
#                    rt['exist']=True
#                    rt['type']='link'
#                    rt['dest']=os.path.realpath(tfilename)
                elif os.path.isfile(filename): # it is File
                    file_name=os.path.basename(tfilename)
                    rt[file_name]={}
                    rt=rt[file_name]
#                    rt['exist']=True
                    filename_info=file_name.split('.')
                    if 'tar' in filename_info:
                        idx=filename_info.index('tar')
                    else:
                        idx=-1
#                    rt['name']='.'.join(filename_info[:idx])
#                    rt['ext']='.'.join(filename_info[idx:])
                    aa=magic.from_buffer(open(tfilename,'rb').read(2048))
                    if aa:
                        _type=aa.split()[0].lower()
#                        rt['type']=aa.split()[0].lower()
                    else:
                        _type='unknown'
#                        rt['type']='unknown'
#                   state=os.stat(tfilename)
#                   rt['size']=state.st_size
#                   rt['mode']=oct(state.st_mode)[-4:]
#                   #rt['mode']=state.st_mode
#                   rt['atime']=state.st_atime
#                   rt['mtime']=state.st_mtime
#                   rt['ctime']=state.st_ctime
#                   rt['gid']=state.st_gid
#                   rt['uid']=state.st_uid
                    _md5=None
                    if data or md5sum:
                        filedata=self.Rw(tfilename)
                        if filedata[0]:
                            #if data: rt['data']=filedata[1]
                            #if md5sum: rt['md5']=md5(filedata[1])
                            if data: rt['data']=filedata[1]
                            if md5sum: _md5=md5(filedata[1])
                    if _md5:
                        self.MkInfo(rt,filename=tfilename,type=_type,name='.'.join(filename_info[:idx]),ext='.'.join(filename_info[idx:]),md5=_md5)
                    else:
                        self.MkInfo(rt,filename=tfilename,type=_type,name='.'.join(filename_info[:idx]),ext='.'.join(filename_info[idx:]))
            else:
                self.MkInfo(rt,exist=False)
#                rt[' i ']['exist']=False

    def GetInfoFile(self,name): #get file info dict from Filename path
        if isinstance(name,str):
            rt=self.info
            for ii in name.split('/'):
                if ii not in rt: return False
                rt=rt[ii]
            if rt.get('exist',False): return rt
        return False

    def GetFilename(self): #Get filename path from info dict
        filename=[]
        for ii in self.info:
            filename.append(ii)
            if ii.get('exist',False): break
        return '/'.join(filename)
    
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
        return '/'.join(filename_info[:-bin_n])

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
 
    def Extract(self,filename,work_path='/tmp',info={},del_org_file=False):
        if not info and isinstance(filename,str) and os.path.isfile(filename): info=self.Get(filename)
        filetype=info.get('type',None)
        fileext=info.get('ext',None)
        if filetype and fileext:
            # Tar stuff
            if fileext in ['tgz','tar','tar.gz','tar.bz2','tar.xz'] and filetype in ['gzip','tar','bzip2','lzma','xz','bz2']:
                tf=tarfile.open(filename)
                tf.extractall(work_path)
                tf.close()
            elif fileext in ['zip'] and filetype in ['compress']:
                with zipfile.ZipFile(filename,'r') as zf:
                    zf.extractall(work_path)
            if del_org_file: os.unline(filename)
            return True
        return False

    def Rw(self,name,data=None,out='string',append=False,read=None,overwrite=True):
        if isinstance(name,str):
            if data is None: # Read from file
                if os.path.isfile(name):
                    try:
                        if read in ['firstread','firstline','first_line','head','readline']:
                            with open(name,'rb') as f:
                                data=f.readline()
                        else:
                            with open(name,'rb') as f:
                                data=f.read()
                    except:
                        pass
                    if data is not None:
                        if out in ['string','str']:
                            return True,CONVERT(data).Str()
                        else:
                            return True,data
                return False,'File({}) not found'.format(name)
            else: # Write to file
                file_path=os.path.dirname(name)
                if not file_path or os.path.isdir(file_path): # current dir or correct directory
                    try:
                        if append:
                            with open(name,'ab') as f:
                                f.write(CONVERT(data).Bytes())
                        else:
                            with open(name,'wb') as f:
                                f.write(CONVERT(data).Bytes())
                        return True,None
                    except:
                        pass
                return False,'Directory({}) not found'.format(file_path)
        return False,'Unknown type({}) filename'.format(name)


    def Mode(self,val):
        if isinstance(val,int):
            if val > 511:
                return oct(val)[-4:]
            elif val > 63:
                return oct(val)
        elif isinstance(val,str):
            cnt=len(val)
            num=int(val)
            if cnt >=3 and cnt <=4 and num >= 100 and num <= 777:
                return int(val,8)

