# Kage Park
from klib.MODULE import *
MODULE().Import('from klib.Get import Get')

def Crc(rt,chk='_',rc={'GOOD':[True,'True','Good','Ok','Pass',{'OK'},0],'FAIL':[False,'False','Fail',{'FAL'},1],'NONE':[None,'None','N/A',{'NA'}],'IGNO':['IGNO','Ignore',{'IGN'}],'ERRO':['ERR','Error',{'ERR'},-1],'WARN':['Warn',{'WAR'}],'UNKN':['Unknown','UNKN',{'UNK'}],'JUMP':['Jump',{'JUMP'}]},rt_true=True,rt_false=False):
    def Trans(irt):
        type_irt=type(irt)
        for ii in rc:
            for jj in rc[ii]:
                if type(jj) == type_irt and ((type_irt is str and jj.lower() == irt.lower()) or jj == irt):
                    return ii
        return 'UNKN'

    nrtc=Trans(Get(rt,'0|rc',out='raw',err='ignore',check=(list,tuple,dict)))
    if chk == '_': return nrtc
    if Trans(chk) == nrtc:return rt_true
    return rt_false
