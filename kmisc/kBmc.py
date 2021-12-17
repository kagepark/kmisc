# Kage Park
# Inteligent BMC Tool
# Version 2

import os
from distutils.spawn import find_executable
import time
import sys
from kmisc.Import import *
Import('from kmisc.SHELL import SHELL')
Import('from kmisc.Misc import *')
rshell=SHELL().Run
#import kmisc as km
import json
ats_version='2.1.101'

class Ipmitool:
    def __init__(self,**opts):
        self.__name__='ipmitool'
        self.tool_path=None
        self.log=opts.get('log',None)
        self.power_mode=opts.get('power_mode',{'on':['chassis power on'],'off':['chassis power off'],'reset':['chassis power reset'],'off_on':['chassis power off','chassis power on'],'on_off':['chassis power on','chassis power off'],'cycle':['chassis power cycle'],'status':['chassis power status'],'shutdown':['chassis power soft']})
        self.ipmitool=True
        if find_executable('ipmitool') is False:
            self.ipmitool=False

    def cmd_str(self,cmd,**opts):
        if not self.ipmitool:
            km.logging('Install ipmitool package(yum install ipmitool)',log=self.log,log_level=1,dsp='e')
            return False,'ipmitool file not found',{}
        cmd_a=cmd.split()
        option=opts.get('option','lanplus')
        if km.check_value(cmd_a,'ipmi',0) and km.check_value(cmd_a,'power',1) and km.get_value(cmd_a,2) in self.power_mode:
            cmd_a[0] = 'chassis'
        elif km.check_value(cmd_a,'ipmi',0) and km.check_value(cmd_a,'reset',1):
            cmd_a=['mc','reset','cold']
        elif km.check_value(cmd_a,'ipmi',0) and km.check_value(cmd_a,'lan',1):
            if len(cmd_a) == 3 and cmd_a[2] in ['mac','dhcp','gateway','netmask']:
                cmd_a=['lan','print']
        elif km.check_value(cmd_a,'ipmi',0) and km.check_value(cmd_a,'sensor',1):
            cmd_a=['sdr','type','Temperature']
        return True,{'base':'''ipmitool -I %s -H {ip} -U {user} -P '{passwd}' '''%(option),'cmd':'''%s'''%(' '.join(cmd_a))},None,{'ok':[0],'fail':[1]},None


class Smcipmitool:
    def __init__(self,**opts):
        self.__name__='smc'
        self.smc_file=opts.get('smc_file',None)
        if self.smc_file and not os.path.isfile(self.smc_file):
            self.smc_file=None
        self.log=opts.get('log',None)
        self.power_mode=opts.get('power_mode',{'on':['ipmi power up'],'off':['ipmi power down'],'reset':['ipmi power reset'],'off_on':['ipmi power down','ipmi power up'],'on_off':['ipmi power up','ipmi power down'],'cycle':['ipmi power cycle'],'status':['ipmi power status'],'shutdown':['ipmi power softshutdown']})

    def cmd_str(self,cmd,**opts):
        cmd_a=cmd.split()
        if not self.smc_file:
            km.logging('- SMCIPMITool({}) not found'.format(self.smc_file),log=self.log,log_level=1,dsp='e')
            return False,'SMCIPMITool file not found',{}
        if km.check_value(cmd_a,'chassis',0) and km.check_value(cmd_a,'power',1):
            cmd_a[0] == 'ipmi'
        elif km.check_value(cmd_a,'mc',0) and km.check_value(cmd_a,'reset',1) and km.check_value(cmd_a,'cold',2):
            cmd_a=['ipmi','reset']
        elif km.check_value(cmd_a,'lan',0) and km.check_value(cmd_a,'print',1):
            cmd_a=['ipmi','lan','mac']
        elif km.check_value(cmd_a,'sdr',0) and km.check_value(cmd_a,'Temperature',2):
            cmd_a=['ipmi','sensor']
        return True,{'base':'''sudo java -jar %s {ip} {user} '{passwd}' '''%(self.smc_file),'cmd':'''%s'''%(' '.join(cmd_a))},None,{'ok':[0,144],'error':[180],'err_bmc_user':[146],'err_connection':[145]},None

class Redfish:
    def __init__(self,**opts):
        self.__name__='redfish'
        self.log=opts.get('log',None)
        self.dcmd={
            'EthernetCount':'Systems/1/EthernetInterfaces',
            'PsuCount':'Chassis/1/Power',
            'Marvell':'Systems/1/Storage/MRVL.HA-RAID/Volumes/Controller.0.Volume.0',
            'LSI3108':'Systems/1/Storage/HA-RAID',
            'BootOption':'Systems/1/BootOptions',
        }

    def cmd_str(self,cmd,**opts):
        sub_cmd=[]
        cmd_a=cmd.strip().split()
        mode='get'
        if len(cmd_a) == 1 and '/' in cmd:
            cmd_a=cmd.strip().split('/')
            cmd_t=[]
            if not cmd_a[0]: cmd_a=cmd_a[1:]
            for i in range(0,len(cmd_a)):
               if i <= 1 and cmd_a[i] in ['redfish','v1']: continue
               cmd_t.append(cmd_a[i])
            cmd='/'.join(cmd_t)
        elif cmd_a[0] == 'power' and cmd_a[1] in ['on','off','off_on','on_ff']:
            mode='post'
            cmd='Systems/1/Actions/ComputerSystem.Reset'
            if cmd_a[1] == 'on':
                sub_cmd=[{'Action': 'Reset', 'ResetType': 'On'}]
            elif cmd_a[1] == 'off':
                sub_cmd=[{'Action': 'Reset', 'ResetType': 'ForceOff'}]
            elif cmd_a[1] == 'off_on':
                sub_cmd=[{'Action': 'Reset', 'ResetType': 'ForceOff'},{'Action': 'Reset', 'ResetType': 'On'}]
            elif cmd_a[1] == 'on_off':
                sub_cmd=[{'Action': 'Reset', 'ResetType': 'On'},{'Action': 'Reset', 'ResetType': 'ForceOff'}]
        elif cmd_a[0] in self.dcmd:
            cmd=self.dcmd[cmd_a[0]]
        return True,{'base':'''https://{ip}/redfish/v1/%s'''%(cmd),'cmd':sub_cmd,'mode':mode},None,{'ok':[0,144],'error':[180],'err_bmc_user':[146],'err_connection':[145]},None

    def get_cmd(self,dic):
       if type(dic) is dict and '@odata.id' in dic and len(dic) == 1:
           return True,dic['@odata.id']
       return False,dic

    def get_data(data=None,sub=False,rec=False):
       if data is None:
           data=do_redfish(cmd,'get')
       if sub:
           for key in data:
               if type(data[key]) is list:
                   for ii in range(0,len(data[key])):
                       zz=get_cmd(data[key][ii])
                       if zz[0] is True:
                           zz_sub_data=do_redfish(zz[1],'get')
                           if rec:
                               data[key][ii]=get_data(data=zz_sub_data,sub=True,rec=True)
                           else:
                               data[key][ii]=zz_sub_data
               else:
                   s_cmd=get_cmd(data[key])
                   if s_cmd[0] is True:
                       sub_data=do_redfish(s_cmd[1],'get')
                       if rec:
                           data[key]=get_data(data=sub_data,sub=True,rec=True)
                       else:
                           data[key]=sub_data
       return data

    def run_cmd(self,cmd_str,**opts):
        start_time=km.int_sec()
        cmd_str=self.cmd_str(cmd_str)
        if cmd_str[0]:
            base_cmd=km.sprintf(cmd_str[1].get('base'),ip=opts.get('ip'))
            if cmd_str[1].get('cmd'):
                for ii in cmd_str[1].get('cmd'):
                    rc=km.web_req(base_cmd[1],user=opts.get('user'),passwd=opts.get('passwd'),json=ii,mode=cmd_str[1].get('mode'))
                    if rc[0] is False  or rc[1].status_code == 404:
                        return False,rc[1].text
            else:
                rc=km.web_req(base_cmd[1],user=opts.get('user'),passwd=opts.get('passwd'),mode='get')

            end_time=km.int_sec()
            if rc[0] is False  or rc[1].status_code == 404:
                return False,rc[1].text
            else:
                return True,json.loads(rc[1].text)

def move2first(item,pool):
    if item: 
        if type(pool) is list and item in pool:
            pool.remove(item)
        return [item]+pool
    return pool

class kBmc:
    def __init__(self,*inps,**opts):
        self.ip=opts.get('ipmi_ip')
        if not self.ip: self.ip=opts.get('ip')
        self.port=opts.get('ipmi_port',(623,664,443))
        self.mac=opts.get('mac')
        if not self.mac: self.mac=opts.get('bmc_mac')
        if not self.mac: self.mac=opts.get('ipmi_mac')
        self.eth_mac=opts.get('eth_mac')
        self.user=opts.get('ipmi_user')
        if not self.user: self.user=opts.get('user','ADMIN')
        self.passwd=opts.get('ipmi_pass')
        if not self.passwd:  self.passwd=opts.get('passwd','ADMIN') # current password
        self.upasswd=opts.get('ipmi_upass')
        if not self.upasswd: self.upasswd=opts.get('upasswd')
        self.redfish_hi=opts.get('redfish_hi')
        self.err={}
        self.warning={}
        self.canceling={}
        self.cancel_func=opts.get('cancel_func',None)
        self.mac2ip=opts.get('mac2ip',None)
        self.log=opts.get('log',None)
        self.org_user='{}'.format(self.user)
        self.default_passwd=opts.get('default_passwd')
        self.org_passwd='{}'.format(self.passwd)
        self.test_user=opts.get('test_user')
        if not self.test_user: self.test_user=['ADMIN','Admin','admin','root','Administrator']
        self.test_passwd=opts.get('test_pass')
        if not self.test_passwd: self.test_passwd=opts.get('test_passwd')
        if not self.test_passwd: self.test_passwd=['ADMIN','Admin','admin','root','Administrator']
        for ii in ['ADMIN','Admin','admin','root','Administrator']:
            if ii not in self.test_passwd: self.test_passwd.append(ii)
        if self.user in self.test_user: self.test_user.remove(self.user)
        if self.passwd in self.test_passwd: self.test_passwd.remove(self.passwd)
        self.mode=opts.get('mode',[Ipmitool()])
        self.log_level=opts.get('log_level',5)
        self.timeout=opts.get('timeout',1800)
        self.checked_ip=False
        self.checked_port=False
        self.org_ip='{}'.format(self.ip)

    def check(self,mac2ip=None,cancel_func=None):
        if cancel_func is None: cancel_func=self.cancel_func
        chk=False
        ip='{}'.format(self.ip)
        for i in range(0,2):
            if self.checked_ip is False:
                if mac2ip and self.mac:
                    ip=mac2ip(self.mac)
                    chk=True
                    self.checked_port=False
            if km.ping(ip,count=0,timeout_sec=self.timeout,log=self.log):
                if self.checked_port is False:
                    if km.is_port_ip(ip,self.port):
                        self.checked_port=True
                    else:
                        self.error(_type='ip',msg="{} is not IPMI IP".format(ip))
                        km.logging(ip,log=self.log,log_level=1,dsp='e')
                        return False,self.ip,self.user,self.passwd
                self.checked_ip=True
                ok,user,passwd=self.find_user_pass(ip)
                if ok:
                    if chk:
                        mac=self.get_mac(ip,user=user,passwd=passwd)
                        if mac != self.mac:
                            self.error(_type='net',msg='Can not find correct IPMI IP')
                            return False,self.ip,self.user,self.passwd
                    self.ip=ip
                    self.user=user
                    self.passwd=passwd
                    return True,ip,user,passwd
            self.checked_ip=False
        self.checked_ip=True
        self.error(_type='net',msg='Destination Host({}) Unreachable/Network problem'.format(ip))
        km.logging(ip,log=self.log,log_level=1,dsp='e')
        return False,self.ip,self.user,self.passwd
        

    def get_mode(self,name):
        for mm in self.mode:
            if mm.__name__ == name:
                return mm

    def find_user_pass(self,ip=None,default_range=4,check_cmd='ipmi power status',cancel_func=None):
        if cancel_func is None: cancel_func=self.cancel_func
        if ip is None: ip=self.ip
        test_user=move2first(self.user,self.test_user[:])
        tt=1
        if len(self.test_passwd) > default_range: tt=2
        tested_user_pass=[]
        for mm in self.mode:
            cmd_str=mm.cmd_str(check_cmd)
            for t in range(0,tt):
                if t == 0:
                    test_pass_sample=self.test_passwd[:default_range]
                else:
                    test_pass_sample=self.test_passwd[default_range:]
                # Two times check for uniq,current,temporary password
                if self.upasswd: test_pass_sample=move2first(self.upasswd,test_pass_sample[:])
                if self.org_passwd: test_pass_sample=move2first(self.org_passwd,test_pass_sample[:])
                test_pass_sample=move2first(self.passwd,test_pass_sample)
                if self.default_passwd not in test_pass_sample: test_pass_sample.append(self.default_passwd)
                for uu in test_user:
                    for pp in test_pass_sample:
                        if km.ping(ip,count=1,keep_good=0,timeout_sec=300): # Timeout :5min, count:2, just pass when pinging
                            tested_user_pass.append((uu,pp))
                            km.logging("""Try BMC User({}) and password({})""".format(uu,pp),log=self.log,log_level=7)
                            full_str=cmd_str[1]['base'].format(ip=ip,user=uu,passwd=pp)+' '+cmd_str[1]['cmd']
                            rc=km.rshell(full_str)
                            if rc[0] in cmd_str[3]['ok']:
                                if self.user != uu:
                                    km.logging("""[BMC]Found New User({})""".format(uu),log=self.log,log_level=3)
                                    self.user=uu
                                if self.passwd != pp:
                                    km.logging("""[BMC]Found New Password({})""".format(pp),log=self.log,log_level=3)
                                    self.passwd=pp
                                return True,uu,pp
                            if self.log_level < 7:
                                km.logging("""p""",log=self.log,direct=True,log_level=3)
                        else:
                            km.logging("""x""",log=self.log,direct=True,log_level=3)
        km.logging("""Can not find working BMC User or password from POOL""",log=self.log,log_level=1,dsp='e')
        self.error(_type='user_pass',msg="Can not find working BMC User or password from POOL\n{}".format(tested_user_pass))
        return False,None,None

    def recover_user_pass(self):
        mm=self.get_mode('smc')
        if not mm:
            km.logging("""SMCIPMITool module not found""",log=self.log,log_level=1)
            return False,'SMCIPMITool module not found'
        if self.user == self.org_user:
            if self.passwd == self.org_passwd:
                km.logging("""Same user and passwrd. Do not need recover""",log=self.log,log_level=6)
                return True,self.user,self.passwd
            else:
                #SMCIPMITool.jar IP ID PASS user setpwd 2 <New Pass>
                #rc=self.run_cmd(mm.cmd_str("""user setpwd 2 '{}'""".format(self.org_passwd)))
                recover_cmd=mm.cmd_str("""user setpwd 2 '{}'""".format(self.org_passwd))
        else:
            #SMCIPMITool.jar IP ID PASS user add 2 <New User> <New Pass> 4
            #rc=self.run_cmd(mm.cmd_str("""user add 2 {} '{}' 4""".format(self.org_user,self.org_passwd)))
            recover_cmd=mm.cmd_str("""user add 2 {} '{}' 4""".format(self.org_user,self.org_passwd))
        #print('\n*kBMC: {}'.format(recover_cmd))
        km.logging("""Recover command: {}""".format(recover_cmd),log_level=7)
        rc=self.run_cmd(recover_cmd)
        
        if km.krc(rc[0],chk='error'):
            km.logging("""BMC Password: Recover fail""",log=self.log,log_level=1)
            self.warn(_type='ipmi_user',msg="BMC Password: Recover fail")
            return 'error',self.ipmi_user,self.ipmi_passwd
        if km.krc(rc[0],chk=True):
            km.logging("""Recovered BMC: from User({}) and Password({}) to User({}) and Password({})""".format(self.user,self.passwd,self.org_user,self.org_passwd),log=self.log,log_level=6)
            self.user='{}'.format(self.org_user)
            self.passwd='{}'.format(self.org_passwd)
            return True,self.user,self.passwd
        else:
            km.logging("""Not support {}. Looks need more length. So Try again with {}""".format(self.org_passwd,self.default_passwd),log=self.log,log_level=6)
            if self.user == self.org_user:
                #SMCIPMITool.jar IP ID PASS user setpwd 2 <New Pass>
                recover_cmd=mm.cmd_str("""user setpwd 2 '{}'""".format(self.default_passwd))
            else:
                #SMCIPMITool.jar IP ID PASS user add 2 <New User> <New Pass> 4
                recover_cmd=mm.cmd_str("""user add 2 {} '{}' 4""".format(self.org_user,self.default_passwd))
        #    print('\n*kBMC2: {}'.format(recover_cmd))
            km.logging("""Recover command: {}""".format(recover_cmd),log_level=7)
            rrc=self.run_cmd(recover_cmd)
            if km.krc(rrc[0],chk=True):
                km.logging("""Recovered BMC: from User({}) and Password({}) to User({}) and Password({})""".format(self.user,self.passwd,self.org_user,self.default_passwd),log=self.log,log_level=6)
                self.user='{}'.format(self.org_user)
                self.passwd='{}'.format(self.default_passwd)
                return True,self.user,self.passwd
            else:
                self.warn(_type='ipmi_user',msg="Recover ERROR!! Please checkup user-lock-mode on the BMC Configure.")
                km.logging("""BMC Password: Recover ERROR!! Please checkup user-lock-mode on the BMC Configure.""",log=self.log,log_level=1)
                return False,self.user,self.passwd
                
    def run_cmd(self,cmd,append=None,path=None,retry=0,timeout=None,return_code={'ok':[0,True],'fail':[]},show_str=False,dbg=False,mode='app',cancel_func=None,peeling=False,progress=False,ip=None,user=None,passwd=None):
        if cancel_func is None: cancel_func=self.cancel_func
        error=self.error()
        if error[0]:
            return 'error','''{}'''.format(error[1])
        while peeling:
            if type(cmd)is tuple and len(cmd) == 1:
                cmd=cmd[0]
            else:
                break
        if isinstance(cmd, (tuple,list)) and len(cmd) >= 2 and type(cmd[0]) is bool:
            ok,cmd,path,return_code,timeout=tuple(km.get_value(cmd,[0,1,2,3,4]))
            if not ok:
                self.warn(_type='cmd',msg="command({}) format error".format(cmd))
                return False,(-1,'command format error(2)','command format error',0,0,cmd,path),'command({}) format error'.format(cmd)
        elif not isinstance(cmd,str):
            self.warn(_type='cmd',msg="command({}) format error".format(cmd))
            return False,(-1,'command format error(3)','command format error',0,0,cmd,path),'command({}) format error'.format(cmd)
        if not isinstance(return_code,dict):
            return_code={}
        rc_ok=return_code.get('ok',[0,True])
        rc_ignore=return_code.get('ignore',[])
        rc_fail=return_code.get('fail',[])
        rc_error=return_code.get('error',[127])
        rc_err_connection=return_code.get('err_connection',[])
        rc_err_key=return_code.get('err_key',[])
        rc_err_bmc_user=return_code.get('err_bmc_user',[])
        if ip is None: ip=self.ip
        if user is None: user=self.user
        if passwd is None: passwd=self.passwd
        if type(append) is not str:
            append=''
        for i in range(0,2+retry):
            if i > 1:
                km.logging('Re-try command [{}/{}]'.format(i,retry+1),log=self.log,log_level=1,dsp='d')
            if isinstance(cmd,dict):
                base_cmd=km.sprintf(cmd['base'],**{'ip':ip,'user':user,'passwd':passwd})
                cmd_str='{} {} {}'.format(base_cmd[1],cmd.get('cmd'),append)
            else:
                base_cmd=km.sprintf(cmd,**{'ip':ip,'user':user,'passwd':passwd})
                cmd_str='{} {}'.format(base_cmd[1],append)
            if not base_cmd[0]:
                return False,(-1,'Wrong commnd format','Wrong command format',0,0,cmd_str,path),'Command format is wrong'
            if dbg or show_str:
                km.logging('** Do CMD   : {}'.format(cmd_str),log=self.log,log_level=1,dsp='d')
                km.logging(' - Timeout  : %-15s  - PATH     : %s'%(timeout,path),log=self.log,log_level=1,dsp='d')
                km.logging(' - CHK_CODE : {}\n'.format(return_code),log=self.log,log_level=1,dsp='d')
            if self.cancel(cancel_func=cancel_func):
                km.logging(' !! Canceling Job',log=self.log,log_level=1,dsp='d')
                self.warn(_type='cancel',msg="Canceling")
                return False,(-1,'canceling','canceling',0,0,cmd_str,path),'canceling'
            try:
                if mode == 'redfish':
                    return Redfish().run_cmd(cmd_str,**self.__dict__)
                else:
                    rc=km.rshell(cmd_str,path=path,timeout=timeout,progress=progress,log=self.log,progress_pre_new_line=True,progress_post_new_line=True)
                if rc[0] != 0:
                    ok,ip,user,passwd=self.check(mac2ip=self.mac2ip,cancel_func=cancel_func)
            except:
                e = sys.exc_info()[0]
                self.warn(_type='cmd',msg="Your command got error\n{}".format(e))
                return 'error',(-1,'{}'.format(e),'unknown',0,0,cmd_str,path),'Your command got error'
            if show_str:
                km.logging(' - RT_CODE : {}'.format(rc[0]),log=self.log,log_level=1,dsp='d')
            if dbg:
                km.logging(' - Output  : {}'.format(rc),log=self.log,log_level=1,dsp='d')
            if rc[0] == 1:
                return False,rc,'Command file not found'
            elif (not rc_ok and rc[0] == 0) or km.check_value(rc_ok,rc[0]):
                return True,rc,'ok'
            elif km.check_value(rc_err_connection,rc[0]): # retry condition1
                msg='err_connection'
                km.logging('Connection error condition:{}, return:{}'.format(rc_err_connection,rc[0]),log=self.log,log_level=7)
                km.logging('Connection Error:',log=self.log,log_level=1,dsp='d',direct=True)
                #Check connection
                if km.is_lost(self.ip,log=self.log,stop_func=self.error(_type='break')[0],cancel_func=self.cancel(cancel_func=cancel_func))[0]:
                    km.logging('Lost Network',log=self.log,log_level=1,dsp='d')
                    self.error(_type='net',msg="{} lost network(over 30min)".format(self.ip))
                    return False,rc,'Lost Network, Please check your server network(1)'
            elif km.check_value(rc_err_bmc_user,rc[0]): # retry condition1
                #Check connection
                if km.is_lost(self.ip,log=self.log,stop_func=self.error(_type='break')[0],cancel_func=self.cancel(cancel_func=cancel_func))[0]:
                    km.logging('Lost Network',log=self.log,log_level=1,dsp='d')
                    self.error(_type='net',msg="{} lost network".format(self.ip))
                    return False,rc,'Lost Network, Please check your server network(2)'
                # Find Password
                ok,ipmi_user,ipmi_pass=self.find_user_pass()
                if not ok:
                    self.error(_type='ipmi_user',msg="Can not find working IPMI USER and PASSWORD")
                    return False,'Can not find working IPMI USER and PASSWORD','user error'
                if dbg:
                    km.logging('Check IPMI User and Password: Found ({}/{})'.format(ipmi_user,ipmi_pass),log=self.log,log_level=1,dsp='d')
                time.sleep(1)
            else:
                if 'ipmitool' in cmd_str and i < 1:
                    #Check connection
                    if km.is_lost(self.ip,log=self.log,stop_func=self.error(_type='break')[0],cancel_func=self.cancel(cancel_func=cancel_func))[0]:
                        km.logging('Lost Network',log=self.log,log_level=1,dsp='d')
                        self.error(_type='net',msg="{} lost network".format(self.ip))
                        return False,rc,'Lost Network, Please check your server network(3)'
                    # Find Password
                    ok,ipmi_user,ipmi_pass=self.find_user_pass()
                    if not ok:
                        self.error(_type='ipmi_user',msg="Can not find working IPMI USER and PASSWORD")
                        return False,'Can not find working IPMI USER and PASSWORD','user error'
                    if dbg:
                        km.logging('Check IPMI User and Password: Found ({}/{})'.format(ipmi_user,ipmi_pass),log=self.log,log_level=1,dsp='d')
                    time.sleep(1)
                else:
                    try:
                        if km.check_value(rc_ignore,rc[0]):
                            return 'ignore',rc,'return code({}) is in ignore condition({})'.format(rc[0],rc_ignore)
                        elif km.check_value(rc_fail,rc[0]):
                            return 'fail',rc,'return code({}) is in fail condition({})'.format(rc[0],rc_fail)
                        elif km.check_value([127],rc[0]):
                            return False,rc,'no command'
                        elif km.check_value(rc_error,rc[0]):
                            return 'error',rc,'return code({}) is in error condition({})'.format(rc[0],rc_error)
                        elif km.check_value(rc_err_key,rc[0]):
                            return 'error',rc,'return code({}) is in key error condition({})'.format(rc[0],rc_err_key)
                        elif isinstance(rc,tuple) and rc[0] > 0:
                            return 'fail',rc,'Not defined return-condition, So it will be fail'
                    except:
                        return 'unknown',rc,'Unknown result'
        return False,(-1,'timeout','timeout',0,0,cmd_str,path),'Time out the running command'

    def reset(self,retry=0,post_keep_up=20,pre_keep_up=0):
        rc=False,'Something issue'
        for i in range(0,1+retry):
            for mm in self.mode:
                if km.is_comeback(self.ip,keep=pre_keep_up,log=self.log,stop_func=self.error(_type='break')[0]):
                    km.logging('R',log=self.log,log_level=1,direct=True)
                    rc=self.run_cmd(mm.cmd_str('ipmi reset'))
                    if km.krc(rc[0],chk='error'):
                        return rc
                    if km.krc(rc[0],chk=True):
                        if km.is_comeback(self.ip,keep=post_keep_up,log=self.log,stop_func=self.error(_type='break')[0]):
                            return True,'Pinging to BMC after reset BMC'
                        else:
                            return False,'Can not Pinging to BMC after reset BMC'
                else:
                    return False,'Can not Pinging to BMC. I am not reset the BMC. please check the network first!'
                time.sleep(5)
        return rc
            

    def get_mac(self,ip=None,user=None,passwd=None):
        if self.mac:
            return True,self.mac
        if ip is None: ip=self.ip
        ok,user,passwd=self.find_user_pass()
        #if user is None: user=self.user
        #if passwd is None: passwd=self.passwd
        for mm in self.mode:
            name=mm.__name__
            cmd_str=mm.cmd_str('ipmi lan mac')
            full_str=cmd_str[1]['base'].format(ip=ip,user=user,passwd=passwd)+' '+cmd_str[1]['cmd']
            rc=km.rshell(full_str,log=self.log,progress_pre_new_line=True,progress_post_new_line=True)
            if km.krc(rc[0],chk=True):
              if name == 'smc':
                  self.mac=rc[1].lower()
                  return True,self.mac
              elif name == 'ipmitool':
                  for ii in rc[1].split('\n'):
                      ii_a=ii.split()
                      if km.check_value(ii_a,'MAC',0) and km.check_value(ii_a,'Address',1) and km.check_value(ii_a,':',2):
                          self.mac=ii_a[-1].lower()
                          return True,self.mac
        return False,None

    def dhcp(self):
        for mm in self.mode:
            name=mm.__name__
            rc=self.run_cmd(mm.cmd_str('ipmi lan dhcp'))
            if km.krc(rc[0],chk='error'):
                return rc
            if km.krc(rc[0],chk=True):
                if name == 'smc':
                    return True,rc[1]
                elif name == 'ipmitool':
                    for ii in rc[1][1].split('\n'):
                        ii_a=ii.split()
                        if km.check_value(ii_a,'IP',0) and km.check_value(ii_a,'Address',1) and km.check_value(ii_a,'Source',2):
                            return True,ii_a[-2]
        return False,None

    def gateway(self):
        for mm in self.mode:
            name=mm.__name__
            rc=self.run_cmd(mm.cmd_str('ipmi lan gateway'))
            if km.krc(rc[0],chk='error'):
                return rc
            if km.krc(rc[0],chk=True):
                if name == 'smc':
                    return True,rc[1]
                elif name == 'ipmitool':
                    for ii in rc[1][1].split('\n'):
                        ii_a=ii.split()
                        if km.check_value(ii_a,'Default',0) and km.check_value(ii_a,'Gateway',1) and km.check_value(ii_a,'IP',2):
                            return True,ii_a[-1]
        return False,None

    def netmask(self):
        for mm in self.mode:
            name=mm.__name__
            rc=self.run_cmd(mm.cmd_str('ipmi lan netmask'))
            if km.krc(rc[0],chk='error'):
                return rc
            if km.krc(rc[0],chk=True):
                if name == 'smc':
                    return True,rc[1]
                elif name == 'ipmitool':
                    for ii in rc[1][1].split('\n'):
                        ii_a=ii.split()
                        if km.check_value(ii_a,'Subnet',0) and km.check_value(ii_a,'Mask',1):
                            return True,ii_a[-1]
        return km.krc(rc[0]),None

    def bootorder(self,mode=None,ipxe=False,persistent=False,force=False,boot_mode={'smc':['pxe','bios','hdd','cd','usb'],'ipmitool':['pxe','ipxe','bios','hdd']}):
        rc=False,"Unknown boot mode({})".format(mode)
        for mm in self.mode:
            name=mm.__name__
            chk_boot_mode=boot_mode.get(name,{})
            if name == 'smc' and mode in chk_boot_mode:
                if mode == 'pxe':
                    rc=self.run_cmd(mm.cmd_str('ipmi power bootoption 1'))
                elif mode == 'hdd':
                    rc=self.run_cmd(mm.cmd_str('ipmi power bootoption 2'))
                elif mode == 'cd':
                    rc=self.run_cmd(mm.cmd_str('ipmi power bootoption 3'))
                elif mode == 'bios':
                    rc=self.run_cmd(mm.cmd_str('ipmi power bootoption 4'))
                elif mode == 'usb':
                    rc=self.run_cmd(mm.cmd_str('ipmi power bootoption 6'))
                if km.krc(rc[0],chk=True):
                    return True,rc[1][1]
            elif name == 'ipmitool':
                if mode in [None,'order']:
                    rc=self.run_cmd(mm.cmd_str('chassis bootparam get 5'))
                    if mode == 'order':
                        if rc[0]:
                            rc=True,km.findstr(rc[1],'- Boot Device Selector : (\w.*)')[0]
                elif mode not in chk_boot_mode:
                    self.warn(_type='boot',msg="Unknown boot mode({}) at {}".format(mode,name))
                    return False,'Unknown boot mode({}) at {}'.format(mode,name)
                else:
                    if persistent:
                        if mode == 'pxe' and ipxe in ['on','ON','On',True,'True']:
                            rc=self.run_cmd(mm.cmd_str('raw 0x00 0x08 0x05 0xe0 0x04 0x00 0x00 0x00'))
                        else:
                            rc=self.run_cmd(mm.cmd_str('chassis bootdev {0} options=persistent'.format(mode)))
                    else:
                        if mode == 'pxe' and ipxe in ['on','ON','On',True,'True']:
                            rc=self.run_cmd(mm.cmd_str('chassis bootdev {0} options=efiboot'.format(mode)))
                        else:
                            if force and chk_boot_mode == 'pxe':
                                rc=self.run_cmd(mm.cmd_str('chassis bootparam set bootflag force_pxe'.format(mode)))
                            else:
                                rc=self.run_cmd(mm.cmd_str('chassis bootdev {0}'.format(mode)))
                if km.krc(rc[0],chk=True):
                    return True,rc[1][1]
            if km.krc(rc[0],chk='error'):
               return rc
        return False,rc[-1]

    def get_eth_mac(self):
        if self.eth_mac:
            return True,self.eth_mac
        rc=False,[]
        for mm in self.mode:
            name=mm.__name__
            if name == 'ipmitool':
                aaa=mm.cmd_str('''raw 0x30 0x21''')
                rc=self.run_cmd(aaa)
                if km.krc(rc[0],chk=True) and rc[1][1]:
                    mac_source=rc[1][1].split('\n')[0].strip()
                    if mac_source:
                        if len(mac_source.split()) == 10:  
                            self.eth_mac=':'.join(mac_source.split()[-6:]).lower()
                        elif len(mac_source.split()) == 16:
                            self.eth_mac=':'.join(mac_source.split()[-12:-6]).lower()
                        return True,self.eth_mac
            elif name == 'smc':
                rc=self.run_cmd(mm.cmd_str('ipmi oem summary | grep "System LAN"'))
                if km.krc(rc[0],chk=True):
                    #rrc=[]
                    #for ii in rc[1].split('\n'):
                    #    rrc.append(ii.split()[-1].lower())
                    #self.eth_mac=rrc
                    self.eth_mac=rc[1].split('\n')[0].strip().lower()
                    return True,self.eth_mac
            if km.krc(rc[0],chk='error'):
               return rc
        return False,None

    def ping(self,ip=None,test_num=3,retry=1,wait=1,keep=0,timeout=30): # BMC is on (pinging)
        if ip is None: ip=self.ip
        return km.ping(ip,count=retry,interval=wait,keep_good=keep,log=self.log,timeout_sec=timeout)

    def summary(self): # BMC is ready(hardware is ready)
        if self.ping() is False:
            print('%10s : %s'%("Ping","Fail"))
            return False
        print('%10s : %s'%("Ping","OK"))
        self.check(mac2ip=self.mac2ip,cancel_func=self.cancel_func)
        print('%10s : %s'%("User",self.user))
        print('%10s : %s'%("Password",self.passwd))
        ok,mac=self.get_mac()
        print('%10s : %s'%("Bmc Mac",'{}'.format(mac)))
        ok,eth_mac=self.get_eth_mac()
        if ok:
            print('%10s : %s'%("Eth Mac",'{}'.format(eth_mac)))
        print('%10s : %s'%("Power",'{}'.format(self.power('status'))))
        print('%10s : %s'%("DHCP",'{}'.format(self.dhcp()[1])))
        print('%10s : %s'%("Gateway",'{}'.format(self.gateway()[1])))
        print('%10s : %s'%("Netmask",'{}'.format(self.netmask()[1])))
        print('%10s : %s'%("LanMode",'{}'.format(self.lanmode()[1])))
        print('%10s : %s'%("BootOrder",'{}'.format(self.bootorder()[1])))

    def node_state(self,state='up',**opts): # Node state
        timeout=km.integer(opts.get('timeout'),default=600)
        keep_up=km.integer(opts.get('keep_up'),default=0)
        keep_down=km.integer(opts.get('keep_down'),default=0)
        power_down=km.integer(opts.get('power_down'),default=0)
        keep_unknown=km.integer(opts.get('keep_unknown'),default=180)
        interval=km.integer(opts.get('interval'),default=0)
        check_down=opts.get('check_down',False)
        if km.compare(keep_up,'>=',timeout,ignore=0):
            timeout=int(keep_up) + 30
        if km.compare(keep_down,'>=',timeout,ignore=0):
            timeout=int(keep_down) + 30
        stop_func=opts.get('stop_func',False)
        cancel_func=opts.get('cancel_func',self.cancel_func)
        km.logging('Node state: timeout:{}, keep_up:{}, keep_down:{} power_down:{}, keep_unknown:{}, check_down:{}'.format(timeout,keep_up,keep_down,power_down,keep_unknown,check_down),log=self.log,log_level=7)
        # _: Down, -: Up, .: Unknown sensor data, !: ipmi sensor command error
        def sensor_data(cmd_str,name):
            krc=self.run_cmd(cmd_str)
            if km.krc(krc[0],chk='error'):
               return 'error'
            if km.krc(krc[0],chk=True):
                sensor_stat='unknown'
                for ii in krc[1][1].split('\n'):
                    ii_a=ii.split('|')
                    find=''
                    if name == 'smc' and len(ii_a) > 2:
                        find=ii_a[1].strip().upper()
                        tmp=ii_a[2].strip()
                    elif len(ii_a) > 4:
                        find=ii_a[0].strip().upper()
                        tmp=ii_a[4].strip()
                    if '_' not in find and ('CPU' in find or 'SYSTEM ' in find) and 'TEMP' in find:
                        if sensor_stat =='unknown' and tmp == 'No Reading':
                            self.warn(_type='sensor',msg="Can not read sensor data")
                            #return 'unknown'
                        elif tmp in ['N/A','Disabled','0C/32F']:
                            sensor_stat='down'
                            #return 'down'
                        else: # Up state
                            return 'up'
                return sensor_stat
            return 'error'

        def power_data():
            pwr_info=self.power(cmd='status')
            return pwr_info.split()[-1]

        bmc_modules_num=len(self.mode)
        bmc_modules_chk=0
        system_down=False
        tmp=''
        ping_out_init=None
        for mm in self.mode:
            init_time=0
            up_time=0
            down_time=0
            no_read=0
            no_read_try=0
            power_down_time=0
            unknown_time=0
            bmc_modules_chk+=1
            name=mm.__name__
            cmd_str=mm.cmd_str('ipmi sensor')
            while True:
                if self.cancel(cancel_func=stop_func):
                    km.logging('Got STOP Signal',log=self.log,log_level=1,dsp='e')
                    return True,'Got STOP Signal'            
                if self.cancel(cancel_func=cancel_func):
                    km.logging('Got Cancel Signal',log=self.log,log_level=1,dsp='e')
                    return False,'Got Cancel Signal'            

                if not km.ping(self.ip,timeout_sec=4,log=self.log):
                    km.logging('*',log=self.log,direct=True,log_level=2)
                    time.sleep(2)
                    ping_out,ping_out_init=km.timeout(timeout,ping_out_init)
                    if ping_out:
                        return False,'Ping Timeout over {} seconds at the Node state'.format(timeout)
                    continue
                ping_out_init=km.now()

                if up_time > 0:
                    out,init_time=km.timeout(timeout+(keep_up*3),init_time)
                else:
                    out,init_time=km.timeout(timeout,init_time)
                if out:
                    if bmc_modules_chk >= bmc_modules_num:
                        self.warn(_type='timeout',msg="node_state()")
                        km.logging('Node state Timeout',log=self.log,log_level=1,dsp='e')
                        if sensor_state == 'unknown':
                            self.error(_type='sensor',msg="Unknown Sensor state")
                        return False,'Node state Timeout over {} seconds'.format(timeout)
                    else:
                        # Change to Next checkup module
                        km.logging('{} state Timeout'.format(name),log=self.log,log_level=1,dsp='e')
                        break
                sensor_state=sensor_data(cmd_str,name)
                pwr_state=power_data()
                km.logging('Module:{}, Sensor state:{}, power_state:{}'.format(name,sensor_state,pwr_state),log=self.log,log_level=8)
                if state == 'up':
                    if sensor_state == 'up':
                        down_time=0
                        up_ok,up_time=km.timeout(keep_up,up_time)
                        if up_ok:
                            if check_down:
                                if system_down:
                                    km.logging('Good, Node is UP after down',log=self.log,log_level=7)
                                    return True,'up'
                                else:
                                    km.logging('Bad, Still UP',log=self.log,log_level=7)
                                    return False,'up'
                            else:
                                km.logging('Good, Node is UP',log=self.log,log_level=7)
                                return True,'up'
                    else:
                        up_time=0
                        if pwr_state == 'off':
                            system_down=True
                            dn_pw_ok,power_down_time=km.timeout(power_down,power_down_time)
                            if dn_pw_ok:
                                km.logging('Bad, Power is off (power_down over {}s)'.format(power_down),log=self.log,log_level=7)
                                return False,'down'
                        else:
                            power_down_time=0
                        up_pw_ok,down_time=km.timeout(keep_down,down_time)
                        if up_pw_ok:
                            if pwr_state == 'on':
                                km.logging('Bad, Power is on',log=self.log,log_level=7)
                                return False,'init'
                            else:
                                km.logging('Bad, Power is off (keep down over {}s)'.format(keep_down),log=self.log,log_level=7)
                                return False,'down'
                elif state == 'down':
                    if sensor_state == 'up':
                        power_down_time=0
                        down_time=0
                        dn_ok,up_time=km.timeout(keep_up,up_time)
                        if dn_ok:
                            km.logging('Bad, Node still up',log=self.log,log_level=7)
                            return False,'up'
                    elif pwr_state == 'off':
                        system_down=True
                        if power_down == 0: return True,'down'
                        dn_pw_ok,power_down_time=km.timeout(power_down,power_down_time)
                        if dn_pw_ok:
                            km.logging('Good, Node is down',log=self.log,log_level=7)
                            return True,'down'
                    else:
                        if keep_down == 0: return True,'down'
                        dn_pw_ok,down_time=km.timeout(keep_down,down_time)
                        if dn_pw_ok:
                            if pwr_state == 'on' and not system_down:
                                km.logging('Bad, Power is up',log=self.log,log_level=7)
                                return False,'up' # Not real down
                            else:
                                km.logging('Good, Power is down',log=self.log,log_level=7)
                                return True,'down' # Real down

                if sensor_state == 'unknown': # No reading data
                    km.logging('Unknown state : keep check : {} < {}, no_read_try: {}, unknown_time:{} '.format(keep_unknown,km.int_sec()-unknown_time,no_read_try,unknown_time),log=self.log,log_level=7)
                    if keep_unknown > 0 and no_read_try < 2:
                        unknown_ok,unknown_time=km.timeout(keep_unknown,unknown_time)
                        km.logging('Unknown Timeout: {} < {} : {}'.format(keep_unknown,km.int_sec()-unknown_time,unknown_ok),log=self.log,log_level=7)
                        if unknown_ok:
                             km.logging('[',log=self.log,direct=True,log_level=2)
                             rrst=self.reset()
                             km.logging(']',log=self.log,direct=True,log_level=2)
                             unknown_time=0
                             timeout=timeout+200
                             no_read_try+=1
                             if km.krc(rrst[0],chk=True):
                                 km.logging('O',log=self.log,direct=True,log_level=2)
                             else:
                                 km.logging('X',log=self.log,direct=True,log_level=2)
                    up_time=0
                    down_time=0
                    km.logging('.',log=self.log,direct=True,log_level=2)
                else:
                    km.logging('sensor_state: {}, unknown_time: {}'.format(sensor_state,unknown_time),log=self.log,log_level=7)
                    unknown_time=0
                    if sensor_state == 'up':
                        km.logging('-',log=self.log,direct=True,log_level=2)
                    elif sensor_state == 'down':
                        km.logging('_',log=self.log,direct=True,log_level=2)
                    else: # error
                        up_time=0
                        down_time=0
                        km.logging('!',log=self.log,direct=True,log_level=2)
                time.sleep(interval)
            time.sleep(interval)

    def is_up(self,timeout=1200,keep_up=60,keep_down=240,power_down=30,interval=8,check_down=False,keep_unknown=300,**opts): # Node state
        return self.node_state(state='up',timeout=km.integer(timeout,default=1200),keep_up=km.integer(keep_up,default=60),keep_down=km.integer(keep_down,default=240),power_down=km.integer(power_down,default=60),interval=km.integer(interval,default=8),check_down=check_down,keep_unknown=km.integer(keep_unknown,default=300),**opts) # Node state

    def is_down(self,timeout=1200,keep_up=240,keep_down=30,interval=8,power_down=30,**opts): # Node state
        return self.node_state(state='down',timeout=km.integer(timeout,default=1200),keep_up=km.integer(keep_up,default=240),interval=km.integer(interval,default=8),power_down=km.integer(power_down,default=60),**opts) # Node state

    def get_boot_mode(self):
        return km.get_boot_mode(self.ip,self.user,self.passwd,log=self.log)

    def power(self,cmd='status',retry=0,boot_mode=None,order=False,ipxe=False,log_file=None,log=None,force=False,mode=None,verify=True,post_keep_up=20,pre_keep_up=0,timeout=3600,lanmode=None,fail_down_time=240):
        retry=km.integer(retry,default=0)
        timeout=km.integer(timeout,default=1200)
        pre_keep_up=km.integer(pre_keep_up,default=0)
        post_keep_up=km.integer(post_keep_up,default=20)
        if cmd == 'status':
            return self.do_power('status',verify=verify)[1]
        if boot_mode:
            km.logging('Set Boot mode to {} with iPXE({})\n'.format(boot_mode,ipxe),log=self.log,log_level=3)
            if ipxe in ['on','On',True,'True']:
                ipxe=True
            else:
                ipxe=False
            if boot_mode == 'ipxe':
                ipxe=True
                boot_mode='pxe'
            for ii in range(0,retry+1):
                # Find ipmi information
                ok,ip,user,passwd=self.check(mac2ip=self.mac2ip,cancel_func=self.cancel_func)
                km.set_boot_mode(self.ip,self.user,self.passwd,boot_mode,persistent=order,ipxe=ipxe,log_file=log_file,log=self.log,force=force)
                boot_mode_state=km.get_boot_mode(self.ip,self.user,self.passwd,log_file=log_file,log=log)
                if (boot_mode == 'pxe' and boot_mode_state[0] is not False and 'PXE' in boot_mode_state[0]) and ipxe == boot_mode_state[1] and order == boot_mode_state[2]:
                    break
                km.logging(' retry boot mode set {} (ipxe:{},force:{})[{}/5]'.format(boot_mode,ipxe,order,ii),log=self.log,log_level=6)
                time.sleep(2)
        return self.do_power(cmd,retry=retry,verify=verify,timeout=timeout,post_keep_up=post_keep_up,lanmode=lanmode,fail_down_time=fail_down_time)

    def do_power(self,cmd,retry=0,verify=False,timeout=1200,post_keep_up=40,pre_keep_up=0,lanmode=None,cancel_func=None,fail_down_time=300):
        timeout=km.integer(timeout,default=1200)
        def lanmode_check(mode):
            # BMC Lan mode Checkup
            cur_lan_mode=self.lanmode()
            if cur_lan_mode[0]:
                if mode.lower() in cur_lan_mode[1].lower():
                    return mode
                else:
                    if mode == 'onboard':
                        rc=self.lanmode(mode=1)
                    elif mode == 'failover':
                        rc=self.lanmode(mode=2)
                    else:
                        rc=self.lanmode(mode=0)
                    if rc[0]:
                        return mode

        chkd=False
        for mm in self.mode:
            name=mm.__name__
            if cmd not in ['status','off_on'] + list(mm.power_mode):
                self.warn(_type='power',msg="Unknown command({})".format(cmd))
                return False,'Unknown command({})'.format(cmd)

            power_step=len(mm.power_mode[cmd])-1
            for ii in range(1,int(retry)+2):
                checked_lanmode=None
                if verify or cmd == 'status':
                    init_rc=self.run_cmd(mm.cmd_str('ipmi power status'))
                    if km.krc(init_rc[0],chk='error'):
                        return init_rc[0],init_rc[1],ii
                    if init_rc[0] is False:
                        if init_rc[-1] == 'canceling':
                            return True,'canceling',ii
                        else:
                            self.warn(_type='power',msg="Power status got some error ({})".format(init_rc[-1]))
                            km.logging('Power status got some error ({})'.format(init_rc[-1]),log=self.log,log_level=3)
                            time.sleep(3)
                            continue
                    if cmd == 'status':
                        if init_rc[0]:
                            if cmd == 'status':
                                return True,init_rc[1][1],ii
                        time.sleep(3)
                        continue
                    init_status=km.get_value(km.get_value(km.get_value(init_rc,1,[]),1,'').split(),-1)
                    if init_status == 'off' and cmd in ['reset','cycle']:
                        cmd='on'
                    # keep command
                    if pre_keep_up > 0 and self.is_up(timeout=timeout,keep_up=pre_keep_up,cancel_func=cancel_func,keep_down=fail_down_time)[0] is False:
                        time.sleep(3)
                        continue
                km.logging('Power {} at {} (try:{}/{}) (limit:{} sec)'.format(cmd,self.ip,ii,retry+1,timeout),log=self.log,log_level=3)
                chk=1
                for rr in list(mm.power_mode[cmd]):
                    verify_status=rr.split(' ')[-1]
                    km.logging(' + Verify Status: "{}" from "{}"'.format(verify_status,rr),log=self.log,log_level=8)
                    if verify:
                        if chk == 1 and init_rc[0] and init_status == verify_status:
                            if chk == len(mm.power_mode[cmd]):
                                return True,verify_status,ii
                            chk+=1
                            continue
                        # BMC Lan mode Checkup before power on/cycle/reset
                        if checked_lanmode is None and lanmode and verify_status in ['on','reset','cycle']:
                           checked_lanmode=lanmode_check(lanmode)

                        if verify_status in ['reset','cycle']:
                             if init_status == 'off':
                                 self.warn(_type='power',msg="Can not set {} on the off mode".format(verify_status))
                                 km.logging(' ! can not {} the power'.format(verify_status),log=self.log,log_level=6)
                                 return False,'can not {} the power'.format(verify_status)
                    rc=self.run_cmd(mm.cmd_str(rr),retry=retry)
                    km.logging('rr:{} cmd:{} rc:{}'.format(rr,mm.cmd_str(rr),rc),log=self.log,log_level=8)
                    if km.krc(rc,chk='error'):
                        return rc
                    if km.krc(rc,chk=True):
                        km.logging(' + Do power {}'.format(verify_status),log=self.log,log_level=3)
                        if verify_status in ['reset','cycle']:
                            verify_status='on'
                            if verify:
                                time.sleep(10)
                    else:
                        self.warn(_type='power',msg="power {} fail".format(verify_status))
                        km.logging(' ! power {} fail'.format(verify_status),log=self.log,log_level=3)
                        time.sleep(5)
                        break
                    if verify:
                        if verify_status in ['on','up']:
                            is_up=self.is_up(timeout=timeout,keep_up=post_keep_up,cancel_func=cancel_func,keep_down=fail_down_time)
                            km.logging('is_up:{}'.format(is_up),log=self.log,log_level=7)
                            if is_up[0]:
                                if chk == len(mm.power_mode[cmd]):
                                    return True,'on',ii
                            elif is_up[1] == 'down' and not chkd:
                                chkd=True
                                self.warn(_type='power',msg="Something weird. Looks BMC issue")
                                km.logging(' Something weird. Try again',log=self.log,log_level=1)
                                retry=retry+1 
                                time.sleep(20)
                            time.sleep(3)
                        elif verify_status in ['off','down']:
                            is_down=self.is_down(cancel_func=cancel_func)
                            km.logging('is_down:{}'.format(is_down),log=self.log,log_level=7)
                            if is_down[0]:
                                if chk == len(mm.power_mode[cmd]):
                                    return True,'off',ii
                            elif is_down[1] == 'up' and not chkd:
                                chkd=True
                                self.warn(_type='power',msg="Something weird. Looks BMC issue")
                                km.logging(' Something weird. Try again',log=self.log,log_level=1)
                                retry=retry+1 
                                time.sleep(20)
                            time.sleep(3)
                        chk+=1
                    else:
                        return True,km.get_value(km.get_value(rc,1),1),ii
                time.sleep(3)
        if chkd:
            km.logging(' It looks BMC issue. (Need reset the physical power)',log=self.log,log_level=1)
            self.error(_type='power',msg="It looks BMC issue. (Need reset the physical power)")
            return False,'It looks BMC issue. (Need reset the physical power)',ii
        return False,'time out',ii

    def lanmode(self,mode=None):
        mm=self.get_mode('smc')
        if not mm:
            km.logging(' - SMCIPMITool not found',log=self.log,log_level=1,dsp='e')
            return False,'SMCIPMITool not found'
        if mode in [0,1,2,'0','1','2']:
            rc=self.run_cmd(mm.cmd_str("""ipmi oem lani {}""".format(mode)))
        else:
            rc=self.run_cmd(mm.cmd_str("""ipmi oem lani"""))
        if km.krc(rc[0],chk='error'):
            return rc
        if km.krc(rc[0],chk=True):
            a=km.findstr(rc[1][1],'Current LAN interface is \[ (\w.*) \]')
            if len(a) == 1:
                return True,a[0]
        return False,None

    def error(self,_type=None,msg=None):
        if _type and msg:
            self.err.update({_type:{km.int_sec():msg}})
        else:
            if not _type:
                if self.err: return True,self.err
                return False,'OK'
            else:
                get_msg=self.err.get(_type,None)
                if get_msg: return True,get_msg
                return False,None

    def warn(self,_type=None,msg=None):
        if _type and msg:
            self.warning.update({_type:{km.int_sec():msg}})
        else:
            if not _type:
                if self.warning: return True,self.warning
                return False,None
            else:
                get_msg=self.warning.get(_type,None)
                if get_msg: return True,get_msg
                return False,None

    def cancel(self,cancel_func=None,msg=None,log_level=1):
        if cancel_func is None: cancel_func=self.cancel_func
        if self.canceling:
            return self.canceling
        else:
            if km.is_cancel(cancel_func):
                if msg :
                    km.logging(msg,log=self.log,log_level=log_level)
                    self.canceling.update({km.int_sec():msg})
                else:
                    self.canceling.update({km.int_sec():km.get_pfunction_name()})
                return 'canceling'
        return False

    def is_admin_user(self,**opts):
        admin_id=opts.get('admin_id',2)
        defined_user=self.__dict__.get('user')
        for mm in self.mode:
            #name=mm.__name__
            for j in range(0,2):
                rc=self.run_cmd(mm.cmd_str("""user list"""))
                if km.krc(rc,chk=True):
                    for i in km.get_value(km.get_value(rc,1),1).split('\n'):
                        i_a=i.strip().split()
                        if str(admin_id) in i_a:
                            if km.get_value(i_a,-1) == 'ADMINISTRATOR':
                                if defined_user == km.get_value(i_a,1):
                                    return True
                else:
                    ok,user,passwd=self.find_user_pass()
                    if not ok: break
        return False
        
if __name__ == "__main__":
    import SysArg
    import sys
    import os
    import pprint
    def KLog(msg,**agc):
        direct=agc.get('direct',False)
        log_level=agc.get('log_level',6)
        ll=agc.get('log_level',5)
        if direct:
            sys.stdout.write(msg)
            sys.stdout.flush()
        elif log_level < ll:
            print(msg)

    arg=SysArg.SysArg(program='kBmc',desc='Inteligent BMC Tool',version=ats_version,cmd_id=1)
    arg.define('ip',short='-i',long='--ip',desc='BMC IP Address',params_name='BMC_IP',required=True)
    arg.define('ipmi_user',short='-u',long='--user',desc='BMC User',params_name='BMC_USER',default='ADMIN')
    arg.define('ipmi_pass',short='-p',long='--passwd',desc='BMC Password',params_name='BMC_PW',default='ADMIN')
    arg.define('tool_path',short='-t',desc='misc tool path',default=km.get_my_directory())
    arg.define('smc_file',short='-si',desc='SMC IPMITOOL file')
    arg.define(group_desc='Is node UP?',group='is_up',command=True)
    arg.define(group_desc='Show summary',group='summary',command=True)
    arg.define(group_desc='Show bootorder',group='bootorder',command=True)
    arg.define('bootorder_pxe',long='--pxe',group_desc='Set PXE boot mode',group='bootorder')
    arg.define('bootorder_ipxe',long='--ipxe',group_desc='Set iPXE boot mode',group='bootorder')
    arg.define('bootorder_bios',long='--bios',group_desc='Set BIOS setup mode',group='bootorder')
    arg.define('bootorder_hdd',long='--hdd',group_desc='Set HDD boot mode',group='bootorder')
    arg.define(group_desc='Check current user is ADMINISTRATOR user',group='is_admin_user',command=True)
    arg.define(group_desc='Get current lanmode',group='lanmode',command=True)
    arg.define(group_desc='Show info',group='info',command=True)
    arg.define(group_desc='Get BMC Mac Address',group='mac',command=True)
    arg.define(group_desc='Get Ethernet Mac Address',group='eth_mac',command=True)
    arg.define(group_desc='Reset BMC',group='reset',command=True)
    arg.define(group_desc='Send power signal',group='power',command=True)
    arg.define('power_status',short='-r',long='--reset',desc='Send reset signal',group='power')
    arg.define('power_off',short='-f',long='--off',desc='Send reset signal',group='power')
    arg.define('power_on',short='-o',long='--on',desc='Send on signal',group='power')
    arg.define('power_shutdown',short='-s',long='--shutdown',desc='Send shutdown signal',group='power')
    arg.define('power_cycle',short='-c',long='--cycle',desc='Send cycle signal',group='power')
    arg.define(group_desc='Send power signal and verify status',group='vpower',command=True)
    arg.define('vpower_reset',short='-vr',long='--vreset',desc='Send reset signal',group='power')
    arg.define('vpower_off',short='-vf',long='--voff',desc='Send off signal',group='power')
    arg.define('vpower_on',short='-vo',long='--von',desc='Send on signal',group='power')
    arg.define('vpower_off_on',short='-vfo',long='--voff_on',desc='Send off and on signal',group='power')
    arg.define('vpower_shutdown',short='-vs',long='--vshutdown',desc='Send shutdown signal',group='power')
    arg.define('vpower_cycle',short='-vc',long='--vcycle',desc='Send cycle signal',group='power')
    arg.define(group_desc='Redfish Command',group='redfish',command=True)
    arg.define('redfish_power',short='-rp',long='--rpower',desc='Send power signal(on/off)',params_name='PW',group='redfish')
    arg.define('redfish_info',short='-ri',long='--rinfo',desc='Get System Information', group='redfish')
    arg.define('redfish_reset_bmc',short='-rrb',long='--reset_bmc',desc='Reset BMC', group='redfish')
    arg.define('redfish_net_info',short='-rni',long='--net_info',desc='Show Network Interface', group='redfish')
    arg.Version()
    arg.Help()
    ipmi_ip=arg.Get('ipmi_ip') 
    ipmi_user=arg.Get('ipmi_user')
    ipmi_pass=arg.Get('ipmi_pass')
    ipxe=arg.Get('bootorder_ipxe')
    smc_file=arg.Get('smc_file')
    if arg.Get('redfish_info',group='redfish'):
        redfish_cmd='Systems/1'
    elif arg.Get('redfish_reset_bmc',group='redfish'):
        redfish_cmd='Managers/1/Actions/Manager.Reset'
    elif arg.Get('redfish_net_info',group='redfish'):
        redfish_cmd='Systems/1/EthernetInterfaces'
    elif arg.Get('redfish_power',group='redfish'):
        redfish_power=arg.Get('redfish_power',group='redfish')



    if km.is_ipv4(ipmi_ip) is False or km.get_value(sys.argv,1) in ['help','-h','--help']:
        help()

    elif km.is_port_ip(ipmi_ip,(623,664,443)):
        print('Test at {}'.format(ipmi_ip))
        if smc_file and os.path.isfile('{}/{}'.format(tool_path,smc_file)):
            bmc=kBmc(ipmi_ip=ipmi_ip,ipmi_user=ipmi_user,ipmi_pass=ipmi_pass,test_pass=['ADMIN','Admin'],test_user=['ADMIN','Admin'],timeout=1800,log=KLog,tool_path=tool_path,ipmi_mode=[Ipmitool(),Smcipmitool(tool_path=tool_path,smc_file=smc_file)])
        elif smc_file and os.path.isfile(smc_file):
            bmc=kBmc(ipmi_ip=ipmi_ip,ipmi_user=ipmi_user,ipmi_pass=ipmi_pass,test_pass=['ADMIN','Admin'],test_user=['ADMIN','Admin'],timeout=1800,log=KLog,tool_path=tool_path,ipmi_mode=[Ipmitool(),Smcipmitool(tool_path=smc_path,smc_file=smc_file)])
        else:
            bmc=kBmc(ipmi_ip=ipmi_ip,ipmi_user=ipmi_user,ipmi_pass=ipmi_pass,test_pass=['ADMIN','Admin'],test_user=['ADMIN','Admin'],timeout=1800,log=KLog,tool_path=tool_path,ipmi_mode=[Ipmitool()])

        cmd_2=km.get_value(sys.argv,-2)
        if cmd_2 == 'power':
            sub_cmd = km.get_value(sys.argv,-1)
            if sub_cmd == 'status':
                print(km.get_value(bmc.do_power(cmd=sub_cmd),1))
            elif sub_cmd in ['on','off','reset','cycle','shutdown']:
                print(km.get_value(bmc.do_power(cmd=sub_cmd),1))
            else:
                print('Unknown command "{}"'.format(sub_cmd))
        elif cmd_2 == 'vpower':
            sub_cmd = km.get_value(sys.argv,-1)
            if sub_cmd == 'status':
                print(bmc.power(cmd=sub_cmd))
            elif sub_cmd in ['on','off','off_on','reset','cycle','shutdown']:
                print(km.get_value(bmc.power(cmd=sub_cmd),1))
            else:
                print('Unknown command "{}"'.format(sub_cmd))
        elif cmd_2 == 'redfish':
            redfish_out=bmc.run_cmd(km.get_value(sys.argv,-1),mode='redfish')
            if km.krc(redfish_out,chk=True):
                pprint.pprint(km.get_value(redfish_out,1))
        elif cmd_2 == 'bootorder':
            mode=km.get_value(sys.argv,-1)
            if mode == 'ipxe':
                print(km.get_value(bmc.bootorder(mode='pxe',ipxe=True,persistent=True,force=True),1))
            else:
                print(km.get_value(bmc.bootorder(mode=mode,persistent=True,force=True),1))
        else:
            cmd=km.get_value(sys.argv,-1)
            if cmd == 'is_up':
                print(km.get_value(bmc.is_up(),1))
            elif cmd == 'bootorder':
                print(km.get_value(bmc.bootorder(),1))
            elif cmd == 'summary':
                print(bmc.summary())
            elif cmd == 'is_admin_user':
                print(bmc.is_admin_user())
            elif cmd == 'lanmode':
                print(bmc.lanmode())
            elif cmd == 'info':
                pprint.pprint(bmc.__dict__)
            elif cmd == 'mac':
                print(km.get_value(bmc.get_mac(),1,default=['Can not get'])[0])
            elif cmd == 'eth_mac':
                print(km.get_value(bmc.get_eth_mac(),1,default=['Can not get'])[0])
            elif cmd == 'reset':
                print(km.get_value(bmc.reset(),1))
            else:
                print('Unknown command "{}"'.format(cmd))
                help()
    else:
        print('Looks the IP({}) is not BMC/IPMI IP or the BMC is not ready on network'.format(ipmi_ip))
