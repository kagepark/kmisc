#Kage Park
import os
from kmisc.Import import *
Import('from kmisc.Type import Type')

def Cd(data,path,sym='/'):
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
