# Kage Park
from kmisc.Import import *
Import('from kmisc.GET import *')

def Crc(rt,chk='_',rtd={'GOOD':[True,'True','Good','Ok','Pass',{'OK'},0],'FAIL':[False,'False','Fail',{'FAL'}],'NONE':[None,'None','N/A',{'NA'}],'IGNO':['IGNO','Ignore',{'IGN'}],'ERRO':['ERR','Error','error','erro','ERRO',{'ERR'}],'WARN':['Warn','warn',{'WAR'}],'UNKN':['Unknown','UNKN',{'UNK'}],'JUMP':['Jump',{'JUMP'}],'TOUT':['timeout','TimeOut','time out','Time Out','TMOUT','TOUT',{'TOUT'}],'REVD':['cancel','Cancel','CANCEL','REV','REVD','Revoked','revoked','revoke','Revoke',{'REVD'}],'LOST':['lost','connection lost','Connection Lost','Connection lost','CONNECTION LOST',{'LOST'}]},default=False):
    def trans(irt):
        type_irt=type(irt)
        for ii in rtd:
            for jj in rtd[ii]:
                if type(jj) == type_irt and ((type_irt is str and jj.lower() == irt.lower()) or jj == irt):
                    return ii
        return 'UNKN'
    rtc=Get(rt,'0|rc',out='raw',err='ignore',check=(list,tuple,dict))
    nrtc=trans(rtc)
    if chk != '_':
        if not isinstance(chk,list): chk=[chk]
        for cc in chk:
            if trans(cc) == nrtc:
                return True
            if nrtc == 'UNKN' and default == 'org':
                return rtc
        if default == 'org': return rt
        return default
    return nrtc

