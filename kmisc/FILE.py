#Kage Park
from distutils.spawn import find_executable
import sys
import os
import fnmatch
import stat
import pickle
import tarfile
import zipfile
import inspect
from kmisc.Import import *
Import('from kmisc.CONVERT import CONVERT')
Import('from kmisc.Path import Path')
Import('from kmisc.Compress import *')
Import('from kmisc.Type import Type')
Import('import magic')

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
            return '.'.join(filename_info[:idx]),'.'.join(filename_info[idx:])
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

    def Rw(self,name,data=None,out='byte',append=False,read=None,overwrite=True,finfo={}):
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
                        if out in ['string','str']:
                            return True,CONVERT(data).Str()
                        else:
                            return True,data
                    except:
                        pass
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
                            #mode=self.Mode(mode)
                            #if mode: os.chmod(name,int(mode,base=8))
                            #if uid and gid: os.chown(name,uid,gid)
                            #if mtime and atime: os.utime(name,(atime,mtime))# Time update must be at last order
                            self.SetIdentity(name,**finfo)
                        return True,None
                    except:
                        pass
                return False,'Directory({}) not found'.format(file_path)
        return False,'Unknown type({}) filename'.format(name)

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
                    remain_path='/'.join(filename_a[ii+1:])
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
                if self.Mkdir(mydest,force=True) is False: return False
                if rtype == 'link':
                    os.symlink(rinfo['dest'],os.path.join(mydest,myname))
                    self.SetIdentity(os.path.join(mydest,myname),**rinfo)
                else: # File
                    if 'data' in rt: self.Rw(Path(mydest,myname),data=rt['data'],finfo=rinfo)
                    else: print('{} file have no data'.format(dirpath))
                self.SetIdentity(os.path.join(mydest,myname),**rinfo)
            else: # directory or root DB
                for ii in rt:
                    if ii == ' i ': continue
                    finfo=rt[ii].get(' i ',{})
                    ftype=finfo.get('type')
                    if ftype == 'dir': 
                        mydir=os.path.join(new_dest,ii)
                        self.Mkdir(mydir,force=True)
                        # Sub directory
                        if sub_dir: self.ExtractRoot(dirpath=os.path.join(dirpath,ii),root_path=rp,dest=os.path.join(new_dest,ii),sub_dir=sub_dir)
                        #if dmtime and datime: os.utime(mydir,(datime,dmtime)) # Time update must be at last order
                        self.SetIdentity(mydir,**finfo)
                    elif ftype == 'link':
                        iimm=os.path.join(new_dest,ii)
                        if not os.path.exists(iimm):
                            os.symlink(finfo['dest'],iimm)
                            self.SetIdentity(iimm,**finfo)
                    else: # File
                        if 'data' in rt[ii]: self.Rw(os.path.join(new_dest,ii),data=rt[ii]['data'],finfo=finfo)
                        else: print('{} file have no data'.format(ii))

    def Mkdir(self,path,force=False):
        if not isinstance(path,str): return None
        if os.path.exists(path): return None
        if force:
            try:
                os.makedirs(path)
            except:
                return False
        else:
            try:
                os.mkdir(path)
            except:
                return False
        return True

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



if __name__ == "__main__":
    from pprint import pprint
    f=FILE
    #data=f('/tmp/test') # Read File information from directory
    #data=f('/tmp/test',sub_dir=True,md5sum=True,data=True) # Read file data and recuring directory
    #data=f('/tmp/test',sub_dir=True,md5sum=True,data=True,link2file=True) #make a real file instead sym-link file
    #pprint(data.__dict__) # print FILE class data structure
    #print(f().FileList('/tmp/test')) # Get File List from the directory
    #print(f(root_path='/tmp/test').FileList('../test2')) # Get File List from the root_path directory

    #print(data.FindRoot('/tmp/test/a/b/README.md')) # Find root_path for the filename
    #print(data.FindRoot('/tmp/test/a/b'))           # Find root_path for the directory
    #print(data.GetInfoFile('a/b/README.md','/tmp/test'))  # Get File Information
    #data.Extract('/tmp/test/a/b/README.md',dest='/tmp/d') # Extract single file at /tmp/a
    #data.Extract('/tmp/test/a/b',dest='/tmp/d')           # Extract sub directory at /tmp/a
    #data.Extract('/tmp/test',dest='/tmp/d',sub_dir=True)  # Extract whole directory of /tmp/test at /tmp/d
    #data.Save('/tmp/a.kf') # Save /tmp/test directory at /tmp/a.kf file

    # Extract /tmp/a.kf file to /tmp/d directory for all of them
    data=f()
    data.Open('/tmp/a.kf')
    data.Extract(dest='/tmp/d',sub_dir=True) 

