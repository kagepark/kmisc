import re
from kmisc.Import import *
Import('from kmisc.Type import Type')

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
