# Kage Park
import os
import tarfile
import zipfile
from kmisc.Import import *
Import('from lz4 import frame')
Import('import bz2')
Import('import magic')

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
            return '.'.join(filename_info[:idx]),'.'.join(filename_info[idx:])
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
