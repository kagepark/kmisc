#Kage park
import time
from datetime import datetime
import random
from kmisc.Import import *
Import('from kmisc.Type import Type')

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
