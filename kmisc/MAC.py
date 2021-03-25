#Kage Park
import uuid
from kmisc.Import import *
Import('from kmisc.Type import Type')

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
                self.src=symbol.join(self.src[i:i+2] for i in range(0,12,2))
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
                    self.src=sym.join(self.src[i:i+2] for i in range(0,12,2))
                if case == 'lower':
                    self.src=self.src.lower()
                else:
                    self.src=self.src.upper()
        if chk:
            if not IS(self.src).Mac4():
                return  default
        return self.src

    def ToStr(self,case='lower',default=False):
        if IS(self.src).Mac4():
            if case == 'lower':
                self.src=self.src.strip().replace(':','').replace('-','').lower()
            else:
                self.src=self.src.strip().replace(':','').replace('-','').upper()
            return self.src
        return default

