#Kage Park
import ast
import struct
from kmisc.Import import *
Import('from kmisc.Type import Type')
Import('from kmisc.Misc import *')
Import('from kmisc.MAC import MAC')

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

    def Bytes(self,encode='utf-8'):
        def _bytes_(src,encode):
            try:
                if PyVer(3):
                    if isinstance(src,bytes):
                        return src
                    else:
                        return bytes(src,encode)
                return bytes(src) # if change to decode then network packet broken
            except:
                return src

        tuple_data=False
        if isinstance(self.src,tuple):
            self.src=list(self.src)
            tuple_data=True
        if isinstance(self.src,list):
            for i in range(0,len(self.src)):
                self.src[i]=_bytes_(self.src[i],encode)
            if tuple_data:
                return tuple(self.src)
            else:
                return self.src
        else:
            return _bytes_(self.src,encode)

    def Str(self,encode='latin1'): # or windows-1252
        def _byte2str_(src,encode):
            if PyVer(3) and isinstance(src,bytes):
                return src.decode(encode)
            #elif isinstance(src,unicode): # type(self.src).__name__ == 'unicode':
            elif Type(src,'unicode'):
                return src.encode(encode)
            #return '''{}'''.format(src)
            return src

        tuple_data=False
        if isinstance(self.src,tuple):
            self.src=list(self.src)
            tuple_data=True
        if isinstance(self.src,list):
            for i in range(0,len(self.src)):
                self.src[i]=_byte2str_(self.src[i],encode)
            if tuple_data:
                return tuple(self.src)
            else:
                return self.src
        else:
            return _byte2str_(self.src,encode)

    def Str2Int(self,encode='utf-8'):
        if PyVer(3):
            if isinstance(self.src,bytes):
                return int(self.src.hex(),16)
            else:
                return int(self.Bytes(encode=encode).hex(),16)
        return int(self.src.encode('hex'),16)

    def Ast(self,default=False,want_type=None):
        if isinstance(self.src,str):
            try:
                ast.literal_eval(string)
            except:
                return default
        if want_type:
            if isinstance(string,want_type):
                return self.src
        if default == 'org' or default == {'org'}:
            return self.src
        return default

    def Form(self,default=False):
        return self.Ast(default=default)

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
                    self.src=sym.join(self.src[i:i+2] for i in range(0,12,2))
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

