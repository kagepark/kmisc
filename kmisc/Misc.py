# -*- coding: utf-8 -*-
#Kage park
# Kage personal stuff

#######################################
# Load All files
#######################################
from __future__ import print_function
from distutils.spawn import find_executable
import sys,os,re,subprocess,copy
import tarfile
import tempfile
import traceback,inspect
import time
from datetime import datetime
from os import close, remove
import random
import string
import fcntl,socket, struct
import pickle
from threading import Thread
import base64
import hashlib
from multiprocessing import Process, Queue

import json
import uuid
import ast
import base64
import ssl
from distutils.version import LooseVersion
import xml.etree.ElementTree as ET

from kmisc.Import import *
Import('zlib')
#Import('from kmisc import Print')

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
url_group = re.compile('^(https|http|ftp)://([^/\r\n]+)(/[^\r\n]*)?')
#log_file=None
log_intro=3
log_new_line='\n'
pipe_file=None

cdrom_ko=['sr_mod','cdrom','libata','ata_piix','ata_generic','usb-storage']
def clean_ansi(data):
    if data:
        if isinstance(data,str):
            return ansi_escape.sub('',data)
        elif isinstance(data,list):
            new_data=[]
            for ii in data:
                new_data.append(ansi_escape.sub('',ii))
            return new_data
    return data

def is_cancel(func):
    if func:
        ttt=type(func).__name__
        if ttt in ['function','instancemethod','method']:
            if func(): return True
        elif ttt  == 'bool':
            if func : return True
    return False

def log_file_info(name):
    log_file_str=''
    if name and len(name) > 0:
        if type(name) is str:
            if name.split(':')[0] == 'log_file':
                return name
            name=name.split(',')
        for nn in name:
            if nn and nn != 'None':
                if log_file_str:
                    log_file_str='{}:{}'.format(log_file_str,nn)
                else:
                    log_file_str='{}'.format(nn)
        if log_file_str:
            return 'log_file:{}'.format(log_file_str)

def error_exit(msg=None):
    if msg is not None:
       print(msg)
    sys.exit(-1)


def std_err(msg,direct=False):
    if direct:
        sys.stderr.write(msg)
    else:
        sys.stderr.write('{}\n'.format(msg))
    sys.stderr.flush()
    
def format_time(time=0,tformat='%s',time_format='%S'):
    if time in [0,'0',None]:
        return datetime.now().strftime(tformat)
    elif isinstance(time,int) or (isinstance(time,str) and time.isdigit()):
        #if type(time) is int or (type(time) is str and time.isdigit()):
        if time_format == '%S':
            return datetime.fromtimestamp(int(time)).strftime(tformat)
        else:
            return datetime.strptime(str(time),time_format).strftime(tformat)

def get_caller_fcuntion_name(detail=False):
    try:
        dep=len(inspect.stack())-2
        if detail:
            return sys._getframe(dep).f_code.co_name,sys._getframe(dep).f_lineno,sys._getframe(dep).f_code.co_filename
        else:
            name=sys._getframe(dep).f_code.co_name
            if name == '_bootstrap_inner' or name == '_run_code':
                return sys._getframe(3).f_code.co_name
            return name
    except:
        return False

def log_format(*msg,**opts):
    log_date_format=opts.get('date_format','[%m/%d/%Y %H:%M:%S]')
    func_name=opts.get('func_name',False)
    log_intro=opts.get('log_intro',3)
    end_new_line=opts.get('end_new_line','')
    start_new_line=opts.get('start_new_line','\n')
    if len(msg) > 0:
        m_str=None
        intro=''
        intro_space=''
        if log_date_format:
            intro=format_time(tformat=log_date_format)+' '
        if func_name or log_intro > 3:
            if type(func_name) is str:
                intro=intro+'{0} '.format(func_name)
            else:
                intro=intro+'{0}() '.format(get_caller_fcuntion_name())
        if intro:
           for i in range(0,len(intro)+1):
               intro_space=intro_space+' '
        for m in list(msg):
            if m_str is None:
                m_str='{0}{1}{2}{3}'.format(start_new_line,intro,m,end_new_line)
            else:
                m_str='{0}{1}{2}{3}{4}'.format(start_new_line,m_str,intro_space,m,end_new_line)
        return m_str

#def printf(*msg,**opts):
#    log_p=False
#    log=opts.get('log',None)
#    log_level=opts.get('log_level',8)
#    dsp=opts.get('dsp','a')
#    func_name=opts.get('func_name',None)
#    date=opts.get('date',False)
#    date_format=opts.get('date_format','[%m/%d/%Y %H:%M:%S]')
#    intro=opts.get('intro',None)
#    caller=opts.get('caller',False)
#    caller_detail=opts.get('caller_detail',False)
#    msg=list(msg)
#    direct=opts.get('direct',False)
#    color=opts.get('color',None)
#    color_db=opts.get('color_db',{'blue': 34, 'grey': 30, 'yellow': 33, 'green': 32, 'cyan': 36, 'magenta': 35, 'white': 37, 'red': 31})
#    bg_color=opts.get('bg_color',None)
#    bg_color_db=opts.get('bg_color_db',{'cyan': 46, 'white': 47, 'grey': 40, 'yellow': 43, 'blue': 44, 'magenta': 45, 'red': 41, 'green': 42})
#    attr=opts.get('attr',None)
#    attr_db=opts.get('attr_db',{'reverse': 7, 'blink': 5,'concealed': 8, 'underline': 4, 'bold': 1})
#    syslogd=opts.get('syslogd',None)
# 
#    if direct:
#        new_line=opts.get('new_line','')
#    else:
#        new_line=opts.get('new_line','\n')
#    logfile=opts.get('logfile',None)
#    logfile_type=type(logfile)
#    if logfile_type is str:
#        logfile=logfile.split(',')
#    elif logfile_type in [list,tuple]:
#        logfile=list(logfile)
#    else:
#        logfile=[]
#    for ii in msg:
#        if type(ii) is str and ':' in ii:
#            logfile_list=ii.split(':')
#            if logfile_list[0] in ['log_file','logfile']:
#                if len(logfile_list) > 2:
#                    for jj in logfile_list[1:]:
#                        logfile.append(jj)
#                else:
#                    logfile=logfile+logfile_list[1].split(',')
#                msg.remove(ii)
# 
#    if os.getenv('ANSI_COLORS_DISABLED') is None and (color or bg_color or attr):
#        reset='''\033[0m'''
#        fmt_msg='''\033[%dm%s'''
#        if color and color in color_db:
#            msg=fmt_msg % (color_db[color],msg)
#        if bg_color and bg_color in bg_color_db:
#            msg=fmt_msg % (color_db[bg_color],msg)
#        if attr and attr in attr_db:
#            msg=fmt_msg % (attr_db[attr],msg)
#        msg=msg+reset
# 
#    # Make a Intro
#    intro_msg=''
#    if date and syslogd is False:
#        intro_msg='[{0}] '.format(datetime.now().strftime(date_format))
#    if caller:
#        call_name=get_caller_fcuntion_name(detail=caller_detail)
#        if call_name:
#            if len(call_name) == 3:
#                intro_msg=intro_msg+'{}({}:{}): '.format(call_name[0],call_name[1],call_name[2])
#            else:
#                intro_msg=intro_msg+'{}(): '.format(call_name)
#    if intro is not None:
#        intro_msg=intro_msg+intro+': '
# 
#    # Make a Tap
#    tap=''
#    for ii in range(0,len(intro_msg)):
#        tap=tap+' '
# 
#    # Make a msg
#    msg_str=''
#    for ii in msg:
#        if msg_str:
#            if new_line:
#                msg_str=msg_str+new_line+tap+'{}'.format(ii)
#            else:
#                msg_str=msg_str+'{}'.format(ii)
#        else:
#            msg_str=intro_msg+'{}'.format(ii)
# 
#    # save msg to syslogd
#    if syslogd:
#        if syslogd in ['INFO','info']:
#            syslog.syslog(syslog.LOG_INFO,msg)
#        elif syslogd in ['KERN','kern']:
#            syslog.syslog(syslog.LOG_KERN,msg)
#        elif syslogd in ['ERR','err']:
#            syslog.syslog(syslog.LOG_ERR,msg)
#        elif syslogd in ['CRIT','crit']:
#            syslog.syslog(syslog.LOG_CRIT,msg)
#        elif syslogd in ['WARN','warn']:
#            syslog.syslog(syslog.LOG_WARNING,msg)
#        elif syslogd in ['DBG','DEBUG','dbg','debug']:
#            syslog.syslog(syslog.LOG_DEBUG,msg)
#        else:
#            syslog.syslog(msg)
# 
#    # Save msg to file
#    if type(logfile) is str:
#        logfile=logfile.split(',')
#    if type(logfile) in [list,tuple] and ('f' in dsp or 'a' in dsp):
#        for ii in logfile:
#            if ii and os.path.isdir(os.path.dirname(ii)):
#                log_p=True
#                with open(ii,'a+') as f:
#                    f.write(msg_str+new_line)
#    if type(log).__name__ == 'function':
#         log_func_arg=get_function_args(log,mode='all')
#         if 'args' in log_func_arg or 'varargs' in log_func_arg:
#             log_p=True
#             args=log_func_arg.get('args',[])
#             if args and len(args) <= 4 and ('direct' in args or 'log_level' in args or 'func_name' in args):
#                 tmp=[]
#                 for i in range(0,len(args)):
#                     tmp.append(i)
#                 if 'direct' in args:
#                     didx=args.index('direct')
#                     del tmp[didx]
#                     args[didx]=direct
#                 if 'log_level' in args:
#                     lidx=args.index('log_level')
#                     del tmp[lidx]
#                     args[lidx]=log_level
#                 if 'func_name' in args:
#                     lidx=args.index('func_name')
#                     del tmp[lidx]
#                     args[lidx]=func_name
#                 if 'date_format' in args:
#                     lidx=args.index('date_format')
#                     del tmp[lidx]
#                     args[lidx]=date_format
#                 args[tmp[0]]=msg_str
#                 log(*args)
#             elif 'keywards' in log_func_arg:
#                 log(msg_str,direct=direct,log_level=log_level,func_name=func_name,date_format=date_format)
#             elif 'defaults' in log_func_arg:
#                 if 'direct' in log_func_arg['defaults'] and 'log_level' in log_func_arg['defaults']:
#                     log(msg_str,direct=direct,log_level=log_level)
#                 elif 'log_level' in log_func_arg['defaults']:
#                     log(msg_str,log_level=log_level)
#                 elif 'direct' in log_func_arg['defaults']:
#                     log(msg_str,direct=direct)
#                 else:
#                     log(msg_str)
#             else:
#                 log(msg_str)
#    # print msg to screen
#    if (log_p is False and 'a' in dsp) or 's' in dsp or 'e' in dsp:
#         if 'e' in dsp:
#             sys.stderr.write(msg_str+new_line)
#             sys.stderr.flush()
#         else:
#             sys.stdout.write(msg_str+new_line)
#             sys.stdout.flush()
#    # return msg
#    if 'r' in dsp:
#         return msg_str


def dget(dict=None,keys=None):
    if dict is None or keys is None:
        return False
    tmp=dict.copy()
    for ii in keys.split('/'):
        if ii in tmp:
           dtmp=tmp[ii]
        else:
           return False
        tmp=dtmp
    return tmp

def dput(dic=None,keys=None,val=None,force=False,safe=True):
    if dic is not None and keys:
        tmp=dic
        keys_arr=keys.split('/')
        keys_num=len(keys_arr)
        for ii in keys_arr[:(keys_num-1)]:
            if ii in tmp:
                if type(tmp[ii]) == type({}):
                    dtmp=tmp[ii]
                else:
                    if tmp[ii] == None:
                        tmp[ii]={}
                        dtmp=tmp[ii]
                    else:
                        if force:
                            vtmp=tmp[ii]
                            tmp[ii]={vtmp:None}
                            dtmp=tmp[ii]
                        else:
                            return False
            else:
                if force:
                    tmp[ii]={}
                    dtmp=tmp[ii]
                else:
                    return False
            tmp=dtmp
        if val == '_blank_':
            val={}
        if keys_arr[keys_num-1] in tmp.keys():
            if safe:
                if tmp[keys_arr[keys_num-1]]:
                    return False
            tmp.update({keys_arr[keys_num-1]:val})
            return True
        else:
            if force:
                tmp.update({keys_arr[keys_num-1]:val})
                return True
    return False

#def is_py3():
#    if sys.version_info[0] >= 3:
#        return True
#    return False


#def rshell(cmd,timeout=None,ansi=True,path=None,progress=False,progress_pre_new_line=False,progress_post_new_line=False,log=None):
#    if isinstance(timeout,int) or (isinstance(timeout,str) and timeout.isdigit()):
#        try:
#            timeout=int(timeout)
#        except:
#            timeout=600
#        if timeout < 3:
#            timeout=3
#    else:
#        timeout=None
# 
#    def pprog(stop,progress_pre_new_line=False,progress_post_new_line=False,log=None):
#        time.sleep(5)
#        if stop():
#            return
#        if progress_pre_new_line:
#            if log:
#                log('\n',direct=True,log_level=1)
#            else:
#                sys.stdout.write('\n')
#                sys.stdout.flush()
#        post_chk=False
#        while True:
#            if stop():
#                break
#            if log:
#                log('>',direct=True,log_level=1)
#            else:
#                sys.stdout.write('>')
#                sys.stdout.flush()
#            post_chk=True
#            time.sleep(5)
#        if post_chk and progress_post_new_line:
#            if log:
#                log('\n',direct=True,log_level=1)
#            else:
#                sys.stdout.write('\n')
#                sys.stdout.flush()
#    start_time=datetime.now().strftime('%s')
#    if not isinstance(cmd,str):
#        return -1,'wrong command information :{0}'.format(cmd),'',start_time,start_time,datetime.now().strftime('%s'),cmd,path
#    Popen=subprocess.Popen
#    PIPE=subprocess.PIPE
# 
#    cmd_env=''
#    cmd_a=cmd.split()
#    cmd_file=cmd_a[0]
#    if cmd_a[0] == 'sudo': cmd_file=cmd_a[1]
#    if isinstance(path,str) and path and os.path.isdir(path):
#        cmd_env='''export PATH=%s:${PATH}; '''%(path)
#        if os.path.join(path,cmd_file):
#            cmd_env=cmd_env+'''cd %s && '''%(path)
#    else:
#        if os.path.isfile(os.path.basename(cmd_file)):
#            cmd_env='''./'''
#    p = Popen(cmd_env+cmd , shell=True, stdout=PIPE, stderr=PIPE)
#    out=None
#    err=None
#    if progress:
#        stop_threads=False
#        ppth=Thread(target=pprog,args=(lambda:stop_threads,progress_pre_new_line,progress_post_new_line,log,))
#        ppth.start()
#    if is_py3():
#        try:
#            out, err = p.communicate(timeout=timeout)
#        except subprocess.TimeoutExpired:
#            p.kill()
#            if progress:
#                stop_threads=True
#                ppth.join()
#            return -1, 'Kill process after timeout ({0} sec)'.format(timeout), 'Error: Kill process after Timeout {0}'.format(timeout),start_time,datetime.now().strftime('%s'),cmd,path
#    else:
#        if timeout:
#            countdown=int('{}'.format(timeout))
#            while p.poll() is None and countdown > 0:
#                time.sleep(2)
#                countdown -= 2
#            if countdown < 1:
#                p.kill()
#                if progress:
#                    stop_threads=True
#                    ppth.join()
#                return -1, 'Kill process after timeout ({0} sec)'.format(timeout), 'Error: Kill process after Timeout {0}'.format(timeout),start_time,datetime.now().strftime('%s'),cmd,path
#        out, err = p.communicate()
# 
#    if progress:
#        stop_threads=True
#        ppth.join()
#        time.sleep(1)
#    if is_py3():
#        out=out.decode("ISO-8859-1")
#        err=err.decode("ISO-8859-1")
#    if ansi:
#        return p.returncode, out.rstrip(), err.rstrip(),start_time,datetime.now().strftime('%s'),cmd,path
#    else:
#        return p.returncode, ansi_escape.sub('',out).rstrip(), ansi_escape.sub('',err).rstrip(),start_time,datetime.now().strftime('%s'),cmd,path

def sendanmail(to,subj,msg,html=True):
    msg='''{}'''.format(msg)
    msg=msg.replace('"','\\"')
    if html:
        email_msg='''To: {0}
Subject: {1}  
Content-Type: text/html
<html>
<body>
<pre>
{2}
</pre>
</body>
</html>'''.format(to,subj,msg)
    else:
        email_msg=''
    cmd='''echo "{0}" | sendmail -t'''.format(email_msg)
    return rshell(cmd)

def mac2str(mac,case='lower'):
    if is_mac4(mac):
        if case == 'lower':
            mac=mac.strip().replace(':','').replace('-','').lower()
        else:
            mac=mac.strip().replace(':','').replace('-','').upper()
        return mac
    return False

def str2mac(mac,sym=':',case='lower',chk=False):
    if type(mac) is str:
        cmac=mac.strip()
        if len(cmac) in [12,17]:
            cmac=cmac.replace(':','').replace('-','')
            if len(cmac) == 12:
                cmac=sym.join(cmac[i:i+2] for i in range(0,12,2))
            if case == 'lower':
                mac=cmac.lower()
            else:
                mac=cmac.upper()
    if chk:
        if is_mac4(mac,convert=False):
            return mac
        else:
            return False
    return mac

def is_mac4(mac=None,symbol=':',convert=True):
    if convert:
        mac=str2mac(mac,sym=symbol)
    if mac is None or type(mac) is not str:
        return False
    octets = mac.split(symbol)
    if len(octets) != 6:
        return False
    for i in octets:
        try:
           if len(i) != 2 or int(i, 16) > 255:
               return False
        except:
           return False
    return True

def sreplace(pattern,sub,string):
    return re.sub('^%s' % pattern, sub, string)

def ereplace(pattern,sub,string):
    return re.sub('%s$' % pattern, sub, string)

def md5(string):
    return hashlib.md5(_u_bytes(string)).hexdigest()

def is_bmc_ipv4(ipaddr,port=(623,664,443)):
    if ipv4(ipaddr):
        if is_port_ip(ipaddr,port):
            return True
    return False

def ipv4(ipaddr=None,chk=False):
    if type(ipaddr) is str:
        ipaddr_a=ipaddr.strip().split('.')
        new_ip=''
        for i in ipaddr_a:
            for j in range(0,10):
                if len(i) <= 1:
                    break
                i=sreplace('^0','',i)
            if new_ip:
                new_ip+='.{}'.format(i)
            else:
                new_ip=i
        if len(new_ip.split('.')) == 4:
            if chk:
                if is_ipv4(new_ip):
                    return new_ip
                else:
                    return False
            return new_ip
    return False

def is_port_ip(ipadd,port):
    tcp_sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sk.settimeout(1)
    if isinstance(port,(str,int)):
        port=[int(port)]
    if isinstance(port,(list,tuple)):
        for pt in port:
            try:
                tcp_sk.connect((ipadd,pt))
                return True
            except:
                pass
    return False

def is_ipv4(ipadd=None):
    if ipadd is None or type(ipadd) is not str or len(ipadd) == 0:
        return False
    ipa = ipadd.split(".")
    if len(ipa) != 4:
        return False
    for ip in ipa:
        if not ip.isdigit():
            return False
        if not 0 <= int(ip) <= 255:
            return False
    return True

def ip2num(ip):
    if is_ipv4(ip):
        return struct.unpack("!L", socket.inet_aton(ip))[0]
    return False

def ip_in_range(ip,start,end):
    if type(ip) is str and type(start) is str and type(end) is str:
        ip=ip2num(ip)
        start=ip2num(start)
        end=ip2num(end)
        if start <= ip and ip <= end:
            return True
    return False

def get_function_name():
    return traceback.extract_stack(None, 2)[0][2]

def get_pfunction_name():
    return traceback.extract_stack(None, 3)[0][2]

def ipmi_cmd(cmd,ipmi_ip=None,ipmi_user='ADMIN',ipmi_pass='ADMIN',log=None):
    if ipmi_ip is None:
        ipmi_str=""" ipmitool {0} """.format(cmd)
    else:
        ipmi_str=""" ipmitool -I lanplus -H {0} -U {1} -P '{2}' {3} """.format(ipmi_ip,ipmi_user,ipmi_pass,cmd)
    if log:
        log(' ipmi_cmd():{}'.format(ipmi_str),log_level=7)
    return rshell(ipmi_str)

def get_ipmi_mac(ipmi_ip=None,ipmi_user='ADMIN',ipmi_pass='ADMIN'):
    ipmi_mac_str=None
    if ipmi_ip is None:
        ipmi_mac_str=""" ipmitool lan print 2>/dev/null | grep "MAC Address" | awk """
    elif is_ipv4(ipmi_ip):
        ipmi_mac_str=""" ipmitool -I lanplus -H {0} -U {1} -P {2} lan print 2>/dev/null | grep "MAC Address" | awk """.format(ipmi_ip,ipmi_user,ipmi_pass)
    if ipmi_mac_str is not None:
        ipmi_mac_str=ipmi_mac_str + """ '{print $4}' """
        return rshell(ipmi_mac_str)

def get_ipmi_ip():
    return rshell('''ipmitool lan print 2>/dev/null| grep "IP Address" | grep -v Source | awk '{print $4}' ''')

def get_host_name():
    return socket.gethostname()

def get_host_ip(ifname=None,mac=None):
    if ifname or mac:
        if mac:
            ifname=get_dev_name_from_mac(mac)
        return get_net_dev_ip(ifname)
    else:
        ifname=get_default_route_dev()
        if not ifname:
            ifname=get_dev_name_from_mac()
        if not ifname: ifname=get_dev_name_from_mac()
        if ifname:
            ip=get_net_dev_ip(ifname)
            if ip:
                return ip
        return socket.gethostbyname(socket.gethostname())

def get_default_route_dev():
    for ii in cat('/proc/net/route').split('\n'):
        ii_a=ii.split()
        if len(ii_a) > 8 and '00000000' == ii_a[1] and '00000000' == ii_a[7]: return ii_a[0]

def get_dev_name_from_mac(mac=None):
    if mac is None:
        mac=get_host_mac()
    net_dir='/sys/class/net'
    if type(mac) is str and os.path.isdir(net_dir):
        dirpath,dirnames,filenames = list(os.walk(net_dir))[0]
        for dev in dirnames:
            fmac=cat('{}/{}/address'.format(dirpath,dev),no_end_newline=True)
            if type(fmac) is str and fmac.strip().lower() == mac.lower():
                return dev

def get_dev_mac(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
        return ':'.join(['%02x' % ord(char) for char in info[18:24]])
    except:
        return

def get_host_iface():
    if os.path.isfile('/proc/net/route'):
        routes=cat('/proc/net/route')
        for ii in routes.split('\n'):
            ii_a=ii.split()
            if ii_a[2] == '030010AC':
                return ii_a[0]
    
def get_host_mac(ip=None,dev=None):
    if is_ipv4(ip):
        dev_info=get_net_device()
        if isinstance(dev_info,dict):
            for dev in dev_info.keys():
                if get_net_dev_ip(dev) == ip:
                    return dev_info[dev]['mac']
    elif dev:
        return get_dev_mac(dev)
    else:
        #return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
        return str2mac('%012x' % uuid.getnode())

def get_net_dev_ip(ifname):
    if os.path.isdir('/sys/class/net/{}'.format(ifname)) is False:
        return False
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
    except:
        try:
            return os.popen('ip addr show {}'.format(ifname)).read().split("inet ")[1].split("/")[0]
        except:
            return

def cat(filename,no_end_newline=False):
    tmp=file_rw(filename)
    tmp=Get(tmp,1)
    if isinstance(tmp,str) and no_end_newline:
        tmp_a=tmp.split('\n')
        ntmp=''
        for ii in tmp_a[:-1]:
            if ntmp:
                ntmp='{}\n{}'.format(ntmp,ii)
            else:
                ntmp='{}'.format(ii)
        if len(tmp_a[-1]) > 0:
            ntmp='{}\n{}'.format(ntmp,tmp_a[-1])
        tmp=ntmp
    return tmp

def ls(dirname,opt=''):
    if os.path.isdir(dirname):
        dirlist=[]
        dirinfo=list(os.walk(dirname))[0]
        if opt == 'd':
            dirlist=dirinfo[1]
        elif opt == 'f':
            dirlist=dirinfo[2]
        else:
            dirlist=dirinfo[1]+dirinfo[2]
        return dirlist
    return False

def get_net_device(name=None):
    net_dev={}
    net_dir='/sys/class/net'
    if os.path.isdir(net_dir):
        dirpath,dirnames,filenames = list(os.walk(net_dir))[0]
        if name:
            if name in dirnames:
                drv=ls('{}/{}/device/driver/module/drivers'.format(dirpath,name))
                if drv is False:
                    drv='unknown'
                else:
                    drv=drv[0].split(':')[1]
                net_dev[name]={
                    'mac':cat('{}/{}/address'.format(dirpath,name),no_end_newline=True),
                    'duplex':cat('{}/{}/duplex'.format(dirpath,name),no_end_newline=True),
                    'mtu':cat('{}/{}/mtu'.format(dirpath,name),no_end_newline=True),
                    'state':cat('{}/{}/operstate'.format(dirpath,name),no_end_newline=True),
                    'speed':cat('{}/{}/speed'.format(dirpath,name),no_end_newline=True),
                    'id':cat('{}/{}/ifindex'.format(dirpath,name),no_end_newline=True),
                    'driver':drv,
                    'drv_ver':cat('{}/{}/device/driver/module/version'.format(dirpath,name),no_end_newline=True),
                    }
        else:
            for dev in dirnames:
                drv=ls('{}/{}/device/driver/module/drivers'.format(dirpath,dev))
                if drv is False:
                    drv='unknown'
                else:
                    drv=drv[0].split(':')[1]
                net_dev[dev]={
                    'mac':cat('{}/{}/address'.format(dirpath,dev),no_end_newline=True),
                    'duplex':cat('{}/{}/duplex'.format(dirpath,dev),no_end_newline=True),
                    'mtu':cat('{}/{}/mtu'.format(dirpath,dev),no_end_newline=True),
                    'state':cat('{}/{}/operstate'.format(dirpath,dev),no_end_newline=True),
                    'speed':cat('{}/{}/speed'.format(dirpath,dev),no_end_newline=True),
                    'id':cat('{}/{}/ifindex'.format(dirpath,dev),no_end_newline=True),
                    'driver':drv,
                    'drv_ver':cat('{}/{}/device/driver/module/version'.format(dirpath,dev),no_end_newline=True),
                    }
        return net_dev
    else:
        return False

def rm_file(filelist):
    if type(filelist) == type([]):
       filelist_tmp=filelist
    else:
       filelist_tmp=filelist.split(',')
    for ii in list(filelist_tmp):
        if os.path.isfile(ii):
            os.unlink(ii)
        else:
            print('not found {0}'.format(ii))

def make_tar(filename,filelist,ctype='gz',ignore_file=[]):
    def ignore_files(filename,ignore_files):
        if isinstance(ignore_files,(list,tuple)):
            for ii in ignore_files:
                if isinstance(ii,str) and (ii == filename or filename.startswith(ii)): return True
        elif isinstance(ignore_files,str):
            if ignore_files == filename or filename.startswith(ignore_files): return True
        return False

    if ctype == 'bz2':
        tar = tarfile.open(filename,"w:bz2")
    elif ctype in ['stream',None,'tar']:
        tar = tarfile.open(filename,"w:")
    if ctype == 'xz':
        tar = tarfile.open(filename,"w:xz")
    else:
        tar = tarfile.open(filename,"w:gz")
    ig_dupl=[]
    filelist_tmp=[]
    filelist_type=type(filelist)
    if filelist_type is list:
       filelist_tmp=filelist
    elif filelist_type is str:
       filelist_tmp=filelist.split(',')
    for ii in filelist_tmp:
        if os.path.isfile(ii):
            if ignore_files(ii,ignore_file): continue
            ig_dupl.append(ii)
            tar.add(ii)
        elif os.path.isdir(ii):
            for r,d,f in os.walk(ii):
                if r in ignore_file or (len(d) == 1 and d[0] in ignore_file):
                    continue
                for ff in f:
                    aa=os.path.join(r,ff)
                    if ignore_files(aa,ignore_file) or aa in ig_dupl: continue
                    ig_dupl.append(aa)
                    tar.add(aa)
        else:
            print('{} not found'.format(ii))
    tar.close()

def cut_string(string,max_len=None,sub_len=None,new_line='\n',front_space=False,out_format=list):
    rc=[]
    if not isinstance(string,str):
        string='{0}'.format(string)
    if new_line:
        string_a=string.split(new_line)
    else:
        string_a=[string]
    if max_len is None or (max_len is None and sub_len is None):
        if new_line and out_format in [str,'str','string']:
            return string
        return [string]
    max_num=len(string_a)
    space=''
    if sub_len and front_space:
        for ii in range(0,max_len-sub_len):
            space=space+' '
    elif sub_len is None:
        sub_len=max_len
    for ii in range(0,max_num):
        str_len=len(string_a[ii])
        if max_num == 1:
            if max_len is None or max_len >= str_len:
                if new_line and out_format in [str,'str','string']:
                    return string_a[ii]
                return [string_a[ii]]
            if sub_len is None:
                rc=[string_a[i:i + max_len] for i in range(0, str_len, max_len)]
                if new_line and out_format in [str,'str','string']:
                    return new_line.join(rc)
                return rc
        rc.append(string_a[ii][0:max_len])
        string_tmp=string_a[ii][max_len:]
        string_tmp_len=len(string_tmp)
        if string_tmp_len > 0:
            for i in range(0, (string_tmp_len//sub_len)+1):
                if (i+1)*sub_len > string_tmp_len:
                    rc.append(space+string_tmp[sub_len*i:])
                else:
                    rc.append(space+string_tmp[sub_len*i:(i+1)*sub_len])
#        else:
#            rc.append('')
    if new_line and out_format in [str,'str','string']:
        return new_line.join(rc)
    return rc

def is_tempfile(filepath,tmp_dir='/tmp'):
   filepath_arr=filepath.split('/')
   if len(filepath_arr) == 1:
      return False
   tmp_dir_arr=tmp_dir.split('/')
   
   for ii in range(0,len(tmp_dir_arr)):
      if filepath_arr[ii] != tmp_dir_arr[ii]:
          return False
   return True


def mktemp(filename=None,suffix='-XXXXXXXX',opt='dry',base_dir='/tmp'):
   if filename is None:
       filename=os.path.join(base_dir,random_str(length=len(suffix)-1,mode='str'))
   dir_name=os.path.dirname(filename)
   file_name=os.path.basename(filename)
   name, ext = os.path.splitext(file_name)
   if type(suffix) is not str:
       suffix='-XXXXXXXX'
   num_type='.%0{}d'.format(len(suffix)-1)
   if dir_name == '.':
       dir_name=os.path.dirname(os.path.realpath(__file__))
   elif dir_name == '':
       dir_name=base_dir
   def new_name(name,ext=None,ext2=None):
       if ext:
           if ext2:
               return '{}{}{}'.format(name,ext,ext2)
           return '{}{}'.format(name,ext)
       if ext2:
           return '{}{}'.format(name,ext2)
       return name
   def new_dest(dest_dir,name,ext=None):
       if os.path.isdir(dest_dir) is False:
           return False
       i=0
       new_file=new_name(name,ext)
       while True:
           rfile=os.path.join(dest_dir,new_file)
           if os.path.exists(rfile) is False:
               return rfile
           if suffix:
               if '0' in suffix or 'n' in suffix or 'N' in suffix:
                   if suffix[-1] not in ['0','n']:
                       new_file=new_name(name,num_type%i,ext)
                   else:
                       new_file=new_name(name,ext,num_type%i)
               elif 'x' in suffix or 'X' in suffix:
                   rnd_str='.{}'.format(random_str(length=len(suffix)-1,mode='str'))
                   if suffix[-1] not in ['X','x']:
                       new_file=new_name(name,rnd_str,ext)
                   else:
                       new_file=new_name(name,ext,rnd_str)
               else:
                   if i == 0:
                       new_file=new_name(name,ext,'.{}'.format(suffix))
                   else:
                       new_file=new_name(name,ext,'.{}.{}'.format(suffix,i))
           else:
               new_file=new_name(name,ext,'.{}'.format(i))
           i+=1
   new_dest_file=new_dest(dir_name,name,ext)
   if opt in ['file','f']:
      os.mknode(new_dest_file)
   elif opt in ['dir','d','directory']:
      os.mkdir(new_dest_file)
   else:
      return new_dest_file

def append2list(*inp,**cond):
   org=[]
   add_num=len(inp)
   uniq=cond.get('uniq',False)
   if add_num == 0:
       return []
   src=inp[0]
   src_type=type(inp)
   if add_num == 1:
       if src_type in [list,tuple,str]:
           return list(src)
       else:
           org.append(src)
           return org
   add=inp[1:]
   if src_type is str:
      for jj in src.split(','):
         if uniq and jj in org: continue
         org.append(jj)
   elif src_type in [list,tuple]:
      for jj in src:
          if uniq and jj in org: continue
          org.append(jj)
   else:
      org.append(src)

   for ii in add:
      ii_type=type(ii)
      if ii_type in [list,tuple]:
         for jj in ii:
             if uniq and jj in org: continue
             org.append(jj)
      elif ii_type is str:
         for jj in ii.split(','):
            if uniq and jj in org: continue
            org.append(jj)
      else:
         if uniq and ii in org: continue
         org.append(ii)
   return org


def isfile(filename=None):
   if filename is None:
      return False
   if len(filename) == 0:
      return False
   if os.path.isfile(filename):
      return True
   return False


def ping(host,count=3,interval=1,keep_good=0, timeout_sec=5,lost_mon=False,log=None,stop_func=None,log_format='.',cancel_func=None):
    ICMP_ECHO_REQUEST = 8 # Seems to be the same on Solaris. From /usr/include/linux/icmp.h;
    ICMP_CODE = socket.getprotobyname('icmp')
    ERROR_DESCR = {
        1: ' - Note that ICMP messages can only be '
           'sent from processes running as root.',
        10013: ' - Note that ICMP messages can only be sent by'
               ' users or processes with administrator rights.'
        }

    def checksum(msg):
        sum = 0
        size = (len(msg) // 2) * 2
        for c in range(0,size, 2):
            sum = (sum + ord(msg[c + 1])*256+ord(msg[c])) & 0xffffffff
        if size < len(msg):
            sum = (sum+ord(msg[len(msg) - 1])) & 0xffffffff
        ra = ~((sum >> 16) + (sum & 0xffff) + (sum >> 16)) & 0xffff
        ra = ra >> 8 | (ra << 8 & 0xff00)
        return ra

    def mk_packet(size):
        """Make a new echo request packet according to size"""
        # Header is type (8), code (8), checksum (16), id (16), sequence (16)
        header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, size, 1)
        #data = struct.calcsize('bbHHh') * 'Q'
        data = size * 'Q'
        my_checksum = checksum(_u_bytes2str(header) + data)
        header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,
                             socket.htons(my_checksum), size, 1)
        return header + _u_bytes(data)

    def receive(my_socket, ssize, stime, timeout_sec):
        while True:
            if timeout_sec <= 0:
                return
            ready = select.select([my_socket], [], [], timeout_sec)
            if ready[0] == []: # Timeout
                return
            received_time = time.time()
            packet, addr = my_socket.recvfrom(1024)
            type, code, checksum, gsize, seq = struct.unpack('bbHHh', packet[20:28]) # Get Header
            if gsize == ssize:
                return received_time - stime
            timeout_sec -= received_time - stime

    def pinging(ip,timeout_sec=1,size=64):
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
        except socket.error as e:
            if e.errno in ERROR_DESCR:
                raise socket.error(''.join((e.args[1], ERROR_DESCR[e.errno])))
            raise
        if size in ['rnd','random']:
            # Maximum size for an unsigned short int c object(65535)
            size = int((id(timeout_sec) * random.random()) % 65535)
        packet = mk_packet(size)
        while packet:
            sent = my_socket.sendto(packet, (ip, 1)) # ICMP have no port, So just put dummy port 1
            packet = packet[sent:]
        delay = receive(my_socket, size, time.time(), timeout_sec)
        my_socket.close()
        if delay:
            return delay,size

    def do_ping(ip,timeout_sec=1,size=64,count=None,interval=0.7,log_format='ping',cancel_func=None,timeout_ping=1):
        ok=1
        i=1
        init_time=None
        while True:
            out,init_time=timeout(timeout_sec,init_time)
            if out:
                return -1,'Timeout'
            if is_cancel(cancel_func):
                return -1,'canceled'
            delay=pinging(ip,timeout_ping,size)
            if delay:
                ok=0
                if log_format == '.':
                    sys.stdout.write('.')
                    sys.stdout.flush()
                elif log_format == 'ping':
                    sys.stdout.write('{} bytes from {}: icmp_seq={} ttl={} time={} ms\n'.format(delay[1],ip,i,size,round(delay[0]*1000.0,4)))
                    sys.stdout.flush()
            else:
                ok=1
                if log_format == '.':
                    sys.stdout.write('x')
                    sys.stdout.flush()
                elif log_format == 'ping':
                    sys.stdout.write('{} icmp_seq={} timeout ({} second)\n'.format(ip,i,timeout_sec))
                    sys.stdout.flush()
            if count:
                count-=1
                if count < 1:
                    return ok,'{} is alive'.format(ip)
            i+=1
            time.sleep(interval)


    if log_format=='ping':
        if find_executable('ping'):
            os.system("ping -c {0} {1}".format(count,host))
        else:
            do_ping(host,timeout_sec=timeout_sec,size=64,count=count,log_format='ping',cancel_func=cancel_func)
    else:
        chk_sec=int_sec()
        log_type=type(log).__name__
        found_lost=False
        if keep_good > 0 or not count:
           try:
               timeout_sec=int(timeout_sec)
           except:
               timeout_sec=1
           if timeout_sec < keep_good:
               count=keep_good+(2*interval)
               timeout_sec=keep_good+5
           elif not count:
               count=timeout_sec//interval + 3
           elif count * interval > timeout_sec:
               timeout_sec=count*interval+timeout_sec
        good=False
        timeoutini=None
        while True:
           out,timeoutini=timeout(timeout_sec,init_time=timeoutini)
           if out:
               return False
           if is_cancel(cancel_func):
               log(' - Canceled ping')
               return False
           if stop_func:
               if log_type == 'function':
                   log(' - Stopped ping')
               return False
           if find_executable('ping'):
               rc=rshell("ping -c 1 {}".format(host))
           else:
               rc=do_ping(host,timeout_sec=1,size=64,count=count,log_format=None)
           if rc[0] == 0:
              good=True
              if keep_good:
                  if good and keep_good and int_sec() - chk_sec >= keep_good:
                      return True
              else:
                  return True
              if log_type == 'function':
                  log('.',direct=True,log_level=1)
           else:
              good=False
              chk_sec=int_sec()
              if log_type == 'function':
                  log('x',direct=True,log_level=1)
           time.sleep(interval)
           count-=1
        return good

def is_lost(ip,**opts):
    timeout_sec=opts.get('timeout',1800)
    interval=opts.get('interval',5)
    stop_func=opts.get('stop_func',None)
    cancel_func=opts.get('cancel_func',None)
    log=opts.get('log',None)
    init_time=None
    if not ping(ip,count=3):
        if not ping(ip,count=0,timeout_sec=timeout_sec,keep_good=30,interval=2,stop_func=stop_func,log=log,cancel_func=cancel_func):
            return True,'Lost network'
    return False,'OK'

def is_comeback(ip,**opts):
    timeout_sec=opts.get('timeout',1800)
    interval=opts.get('interval',3)
    keep=opts.get('keep',20)
    stop_func=opts.get('stop_func',None)
    cancel_func=opts.get('cancel_func',None)
    log=opts.get('log',None)
    init_time=None
    run_time=int_sec()
    if keep == 0 or keep is None:
        return True,'N/A(Missing keep parameter data)'
    if log:
        log('[',direct=True,log_level=1)
    while True:
        ttt,init_time=timeout(timeout_sec,init_time)
        if ttt:
            if log:
                log(']\n',direct=True,log_level=1)
            return False,'Timeout monitor'
        if is_cancel(cancel_func) or stop_func is True:
            if log:
                log(']\n',direct=True,log_level=1)
            return True,'Stopped monitor by Custom'
        if ping(ip,cancel_func=cancel_func):
            if (int_sec() - run_time) > keep:
                if log:
                    log(']\n',direct=True,log_level=1)
                return True,'OK'
            if log:
                log('-',direct=True,log_level=1)
        else:
            run_time=int_sec()
            if log:
                log('.',direct=True,log_level=1)
        time.sleep(interval)
    if log:
        log(']\n',direct=True,log_level=1)
    return False,'Timeout/Unknown issue'

def get_function_args(func,mode='defaults'):
    rc={}
    args, varargs, keywords, defaults = inspect.getargspec(func)
    if defaults is not None:
        defaults=dict(zip(args[-len(defaults):], defaults))
        del args[-len(defaults):]
        rc['defaults']=defaults
    if args:
        rc['args']=args
    if varargs:
        rc['varargs']=varargs
    if keywords:
        rc['keywards']=keywords
    if mode in ['*','all']:
        return rc
    if mode in rc:
        return rc[mode]

def get_function_list(objName=None,obj=None):
    aa={}
    if obj is None and objName is not None:
       obj=sys.modules[objName]
    if obj is not None:
        for name,fobj in inspect.getmembers(obj):
            if inspect.isfunction(fobj): # inspect.ismodule(obj) check the obj is module or not
                aa.update({name:fobj})
    return aa

def space(space_num=0,_space_='   '):
    space_str=''
    for ii in range(space_num):
        space_str='{0}{1}'.format(space_str,_space_)
    return space_str

def tap_print(string,bspace='',rc=False,NFLT=False):
    rc_str=None
    if type(string) is str:
        for ii in string.split('\n'):
            if NFLT:
               line='%s'%(ii)
               NFLT=False
            else:
               line='%s%s'%(bspace,ii)
            if rc_str is None:
               rc_str='%s'%(line)
            else:
               rc_str='%s\n%s'%(rc_str,line)
    else:
        rc_str='%s%s'%(bspace,string)

    if rc:
        return rc_str
    else:
        print(rc_str)

def str_format_print(string,rc=False):
    if type(string) is str:
        if len(string.split("'")) > 1:
            rc_str='"%s"'%(string)
        else:
            rc_str="'%s'"%(string)
    else:
        rc_str=string
    if rc:
        return rc_str
    else:
        print(rc_str)

#def format_print(string,rc=False,num=0,bstr=None,NFLT=False):
#    string_type=type(string)
#    rc_str=''
#    chk=None
#    bspace=space(num)
# 
#    # Start Symbol
#    if string_type is tuple:
#        if bstr is None:
#            if NFLT:
#                rc_str='%s('%(rc_str)
#            else:
#                rc_str='%s%s('%(bspace,rc_str)
#        else:
#            rc_str='%s,\n%s%s('%(bstr,bspace,rc_str)
#    elif string_type is list:
#        if bstr is None:
#            if NFLT:
#                rc_str='%s['%(rc_str)
#            else:
#                rc_str='%s%s['%(bspace,rc_str)
#        else:
#            rc_str='%s,\n%s%s['%(bstr,bspace,rc_str)
#    elif string_type is dict:
#        if bstr is None:
#            rc_str='%s{'%(rc_str)
#        else:
#            rc_str='%s,\n%s %s{'%(bstr,bspace,rc_str)
#    rc_str='%s\n%s '%(rc_str,bspace)
# 
#    # Print string
#    if string_type is list or string_type is tuple:
#       for ii in list(string):
#           ii_type=type(ii)
#           if ii_type is tuple or ii_type is list or ii_type is dict:
#               if not ii_type is dict:
#                  num=num+1
#               rc_str=format_print(ii,num=num,bstr=rc_str,rc=True)
#           else:
#               if chk == None:
#                  rc_str='%s%s'%(rc_str,tap_print(str_format_print(ii,rc=True),rc=True))
#                  chk='a'
#               else:
#                  rc_str='%s,\n%s'%(rc_str,tap_print(str_format_print(ii,rc=True),bspace=bspace+' ',rc=True))
#    elif string_type is dict:
#       for ii in string.keys():
#           ii_type=type(string[ii])
#           if ii_type is dict or ii_type is tuple or ii_type is list:
#               num=num+1
#               if ii_type is dict:
#                   tmp=format_print(string[ii],num=num,rc=True)
#               else:
#                   tmp=format_print(string[ii],num=num,rc=True,NFLT=True)
#               rc_str="%s,\n%s %s:%s"%(rc_str,bspace,str_format_print(ii,rc=True),tmp)
#           else:
#               if chk == None:
#                  rc_str='%s%s'%(rc_str,tap_print("{0}:{1}".format(str_format_print(ii,rc=True),str_format_print(string[ii],rc=True)),rc=True))
#                  chk='a'
#               else:
#                  rc_str='%s,\n%s'%(rc_str,tap_print("{0}:{1}".format(str_format_print(ii,rc=True),str_format_print(string[ii],rc=True)),bspace=bspace+' ',rc=True))
# 
#    # End symbol
#    if string_type is tuple:
#        rc_str='%s\n%s)'%(rc_str,bspace)
#    elif string_type is list:
#        rc_str='%s\n%s]'%(rc_str,bspace)
#    elif string_type is dict:
#        if bstr is None:
#            rc_str='%s\n%s}'%(rc_str,bspace)
#        else:
#            rc_str='%s\n%s }'%(rc_str,bspace)
# 
#    else:
#       rc_str=string
# 
#    # Output
#    if rc:
#       return rc_str    
#    else:
#       print(rc_str)


#def str2url(string):
#    if string is None: return ''
#    if type(string) is str:
#        return string.replace('+','%2B').replace('?','%3F').replace('/','%2F').replace(':','%3A').replace('=','%3D').replace(' ','+')
#    return string

def clear_version(string,sym='.'):
    if isinstance(string,(int,str)):
        if isinstance(string,str): string=string.strip()
        string='{}'.format(string)
    else:
        return False
    arr=string.split(sym)
    for ii in range(len(arr)-1,0,-1):
        if arr[ii].replace('0','') == '':
            arr.pop(-1)
        else:
            break
    return sym.join(arr)

def get_key(dic=None,find=None):
    return find_key_from_value(dic=dic,find=find)

def find_key_from_value(dic=None,find=None):
    if isinstance(dic,dict):
        if find is None:
            return list(dic.keys())
        else:
            for key,val in dic.items():
                if val == find:
                    return key
    elif isinstance(dic,list) or isinstance(dic,tuple):
        if find is None:
            return len(dic)
        else:
            if find in dic:
                return dic.index(find)
         

def random_str(length=8,strs=None,mode='*'):
    if strs is None:
        if mode in ['all','*','alphanumchar']:
            strs='0aA-1b+2Bc=C3d_D,4.eE?5"fF6g7G!h8H@i9#Ij$JkK%lLmMn^N&oO*p(Pq)Q/r\Rs:St;TuUv{V<wW}x[Xy>Y]z|Z'
        elif mode in ['alphanum']:
            strs='aA1b2BcC3dD4eE5fF6g7Gh8Hi9IjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'
        else:
            strs='aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'
    new=''
    strn=len(strs)-1
    for i in range(0,length):
        new='{0}{1}'.format(new,strs[random.randint(0,strn)])
    return new

def power_state(ipmi_ip,ipmi_user='ADMIN',ipmi_pass='ADMIN',wait_time=60,check_status=None,monitor_time=3,log_file=None,log=None):
    sys_status='unknown'
    if check_status is None:
        wait_time=3
    for ii in range(0,wait_time):
        power_status=ipmi_cmd(cmd='chassis power status',ipmi_ip=ipmi_ip,ipmi_user=ipmi_user,ipmi_pass=ipmi_pass,log=log)
        if power_status[0] == 0:
            if power_status[1] == 'Chassis Power is on':
                sys_status='on'
            elif power_status[1] == 'Chassis Power is off':
                sys_status='off'
            if (check_status and check_status == sys_status) or (check_status is None and sys_status in ['on','off']):
                if check_status:
                    logging("   * confirm state : {} => {}".format(sys_status,check_status),log_file=log_file,date=True,log=log,log_level=6)
                return [True,sys_status]
            else:
                if check_status:
                    logging("   - wait {}sec : {} => {}".format((wait_time - ii)*monitor_time,sys_status,check_status),log_file=log_file,date=True,log=log,log_level=6)
        else:
            logging("   - wait {}sec for check power state with {}:{}".format(monitor_time,ipmi_user,ipmi_pass),log_file=log_file,date=True,log=log,log_level=6)
        sleep(monitor_time)
    return [False,'time out']

def get_boot_mode(ipmi_ip,ipmi_user,ipmi_pass,log_file=None,log=None):
    status='No override'
    rc=ipmi_cmd(cmd='chassis bootparam get 5',ipmi_ip=ipmi_ip,ipmi_user=ipmi_user,ipmi_pass=ipmi_pass,log=log)
    if rc[0] == 0:
        efi=False
        persistent=False
        for ii in rc[1].split('\n'):
            if 'Options apply to all future boots' in ii:
                persistent=True
            elif 'BIOS EFI boot' in ii:
                efi=True
            elif 'Boot Device Selector :' in ii:
                status=ii.split(':')[1]
                break
        if log:
            log("Boot mode Status:{}, EFI:{}, Persistent:{}".format(status,efi,persistent),log_level=7)
        return [status,efi,persistent]
    else:
        return [False,False,False]

def set_boot_mode(ipmi_ip,ipmi_user,ipmi_pass,boot_mode,ipxe=False,persistent=False,log_file=None,log=None,force=False):
    boot_mode_d=['pxe','ipxe','bios','hdd']
    if not boot_mode in boot_mode_d:
        return
    if persistent:
        if boot_mode == 'pxe' and ipxe in ['on','ON','On',True,'True']:
            # ipmitool -I lanplus -H 172.16.105.74 -U ADMIN -P 'ADMIN' raw 0x00 0x08 0x05 0xe0 0x04 0x00 0x00 0x00
            ipmi_cmd(cmd='raw 0x00 0x08 0x05 0xe0 0x04 0x00 0x00 0x00',ipmi_ip=ipmi_ip,ipmi_user=ipmi_user,ipmi_pass=ipmi_pass,log=log)
            logging("Persistently Boot mode set to i{0} at {1}".format(boot_mode,ipmi_ip),log_file=log_file,date=True,log=log,log_level=7)
        else:
            ipmi_cmd(cmd='chassis bootdev {0} options=persistent'.format(boot_mode),ipmi_ip=ipmi_ip,ipmi_user=ipmi_user,ipmi_pass=ipmi_pass,log=log)
            logging("Persistently Boot mode set to {0} at {1}".format(boot_mode,ipmi_ip),log_file=log_file,date=True,log=log,log_level=7)
    else:
        if boot_mode == 'pxe' and ipxe in ['on','ON','On',True,'True']:
                ipmi_cmd(cmd='chassis bootdev {0} options=efiboot'.format(boot_mode),ipmi_ip=ipmi_ip,ipmi_user=ipmi_user,ipmi_pass=ipmi_pass,log=log)
        else:
            if force and boot_mode == 'pxe':
                ipmi_cmd(cmd='chassis bootparam set bootflag force_pxe'.format(boot_mode),ipmi_ip=ipmi_ip,ipmi_user=ipmi_user,ipmi_pass=ipmi_pass,log=log)
            else:
                ipmi_cmd(cmd='chassis bootdev {0}'.format(boot_mode),ipmi_ip=ipmi_ip,ipmi_user=ipmi_user,ipmi_pass=ipmi_pass,log=log)
        logging("Temporary Boot mode set to {0} at {1}".format(boot_mode,ipmi_ip),log_file=log_file,date=True,log=log,log_level=7)


def do_power(ipmi_ip,ipmi_user,ipmi_pass,mode,num=2,log_file=None,log=None):
    power_mode={'on':['chassis power on'],'off':['chassis power off'],'reset':['chassis power reset'],'off_on':['chassis power off','chassis power on'],'cycle':['chassis power cycle']}
    if not mode in power_mode:
        return [False,'Unknown power mode']
    power_step=len(power_mode[mode])-1
    for ii in range(1,int(num)+1):
        logging("Power {} at {} (try:{}/{})".format(mode,ipmi_ip,ii,num),log_file=log_file,date=True,log=log,log_level=6)
        for rr in list(power_mode[mode]):
            verify_status=rr.split(' ')[-1]
            if verify_status in ['reset','cycle']:
                 sys_status=power_state(ipmi_ip,ipmi_user,ipmi_pass,log_file=log_file,log=log)
                 if sys_status[0] and sys_status[1] == 'off':
                     logging(" ! can not {} the power at {} status".format(verify_status,sys_status[1]),log_file=log_file,date=True,log=log,log_level=3)
                     return [False,'can not {} at {} status'.format(verify_status,sys_status[1])]
            rc=ipmi_cmd(cmd=rr,ipmi_ip=ipmi_ip,ipmi_user=ipmi_user,ipmi_pass=ipmi_pass,log=log)
            if rc[0] == 0:
                logging(" + Do power {}".format(verify_status),log_file=log_file,date=True,log=log,log_level=5)
                if verify_status in ['reset','cycle']:
                    verify_status='on'
                    sleep(10)
            else:
                logging(" ! power {} fail".format(verify_status),log_file=log_file,date=True,log=log,log_level=3)
                break
            sys_status=power_state(ipmi_ip,ipmi_user,ipmi_pass,check_status=verify_status,log_file=log_file,log=log)
            if sys_status[0]:
                if sys_status[1] == verify_status:
                    if power_step == power_mode[mode].index(rr):
                        return sys_status + [ii]
                sleep(5)
            else:
                break
        sleep(3)
    return [False,'time out',ii]

def power_handle(ipmi_ip,mode='status',num=2,ipmi_user='ADMIN',ipmi_pass='ADMIN',boot_mode=None,order=False,ipxe=False,log_file=None,log=None,force=False):
    # Power handle
    if mode == 'status':
        return power_state(ipmi_ip,ipmi_user,ipmi_pass,log_file=log_file,log=log)
    if boot_mode:
        if ipxe in ['on','On',True,'True']:
            ipxe=True
        else:
            ipxe=False
        if boot_mode == 'ipxe':
            ipxe=True
            boot_mode='pxe'
        for ii in range(0,5):
            aa=set_boot_mode(ipmi_ip,ipmi_user,ipmi_pass,boot_mode,persistent=order,ipxe=ipxe,log_file=log_file,log=log,force=force)
            boot_mode_state=get_boot_mode(ipmi_ip,ipmi_user,ipmi_pass,log_file=log_file,log=log)
            if (boot_mode == 'pxe' and boot_mode_state[0] is not False and 'PXE' in boot_mode_state[0]) and ipxe == boot_mode_state[1] and order == boot_mode_state[2]:
                break
            logging(" retry boot mode set {} (ipxe:{},force:{})[{}/5]".format(boot_mode,ipxe,order,ii),log_file=log_file,date=True,log=log,log_level=3)
            time.sleep(2)
    rc=do_power(ipmi_ip,ipmi_user,ipmi_pass,mode,num=num,log_file=log_file,log=log)
#    if ipxe in ['on','On',True,'True']:
#        ipxe=True
#    if rc[0]:
#        if boot_mode:
#            for ii in range(0,5):
#                set_boot_mode(ipmi_ip,ipmi_user,ipmi_pass,boot_mode,persistent=order,ipxe=ipxe,log_file=log_file,log=log)
#                boot_mode_state=get_boot_mode(ipmi_ip,ipmi_user,ipmi_pass,log_file=log_file,log=log)
#                if (boot_mode == 'pxe' and 'PXE' in boot_mode_state[0]) and ipxe == boot_mode_state[1] and order == boot_mode_state[2]:
#                    break
#                logging(" retry boot mode set {} (ipxe:{},force:{})[{}/5]".format(boot_mode,ipxe,order,ii),log_file=log_file,date=True,log=log)
#                time.sleep(2)
    return rc

def wait_ready_system(ipmi_ip,ipmi_user='ADMIN',ipmi_pass='ADMIN',timeout_sec=1800,keep_up=45,down_monitor=300,interval=3,stop_func=None,stop_arg={},log_file=None,log=None):
    aa="""ipmitool -I lanplus -H {0} -U {1} -P {2} sdr type Temperature 2>/dev/null""".format(ipmi_ip,ipmi_user,ipmi_pass)
    chk=0
    if keep_up >= timeout_sec:
       timeout_sec=int('{}'.format(keep_up)) + 30
    if down_monitor >= timeout_sec:
       timeout_sec=int('{}'.format(down_monitor)) + 30
    log_type=type(log).__name__
    init_sec=int(datetime.now().strftime('%s'))
    do_sec=int('{}'.format(init_sec))
    wait_count=0
    count_down=(down_monitor//interval)
    max_wait=keep_up//interval
    node_state=None
    node_old=None
    node_change=False
    node_change_count=0

    if count_down > 0:
        logging("Wait until the system({}) is ready(keep {}sec)".format(ipmi_ip,keep_up),log_file=log_file,date=True,log=log,log_level=6)
    else:
        logging("Wait until the system({}) is ready(keep {}sec) after down(check time: {} sec)".format(ipmi_ip,keep_up,down_monitor),log_file=log_file,date=True,log=log,log_level=6)
    while True:
        if stop_func and type(stop_arg) is dict:
            if stop_func(**stop_arg) is True:
                if log_type=='function':
                    logging("Got STOP signal",log_file=log_file,date=True,log=log,log_level=3)
#                    log("Got STOP signal",log_level=6)
                return [False,'Got STOP signal']
        if do_sec - init_sec > timeout_sec and node_state == node_old:
            if log_type=='function':
                logging("TIme Out, node state is {}".format(node_state),log_file=log_file,date=True,log=log,log_level=3)
#                log("Time Out, node state is {}".format(node_state),log_level=6)
            return [False,'Time Out, node state is {}'.format(node_state)]
        if ping(ipmi_ip,2):
            tempc=[]
            wrc=rshell(aa)
            if wrc[0] == 0:
                 for ii in wrc[1].split('\n'):
                      if re.findall('CPU?[0-9]?.Temp',ii) or re.findall('System.Temp',ii):
                          tempc=re.findall('(\d+) degrees',ii.split('|')[-1])
                          if tempc:
                              break
                 if tempc and int(tempc[0]) > 0:
                     node_state='up'
                 else:
                     node_state='down'
                 if node_state and node_old and node_state != node_old:
                     if node_change_count < 4:
                         init_sec=int(datetime.now().strftime('%s'))
                     wait_count=0
                     count_down=(down_monitor//interval)
                     node_change=True 
                     node_change_count=node_change_count+1
                 if (down_monitor == 0 or node_change) and node_state == 'up':
                     wait_count=wait_count+1
                     if wait_count > max_wait:
                         logging("System ready",log_file=log_file,date=True,log=log,log_level=6)
                         #if log_type=='function':
                         #    log("The system ready",log_level=6)
                         return [True,'System ready']
                 elif down_monitor > 0 and node_change is False and node_state in ['up','down']:
                     count_down=count_down-1
                     if count_down < 0:
                         logging("It did not changed state. still {}".format(node_state),log_file=log_file,date=True,log=log,log_level=3)
                         #if log_type=='function':
                         #    log("It did not changed state. still {}".format(node_state),log_level=6)
                         return [False,'It did not changed state. still {}'.format(node_state)]
                 if chk % 5 == 0:
                     if node_state != node_old:
                         mark='+'
                     else:
                         mark='-'
                     if count_down > 0:
                         logging(" {2} wait {1}sec for ready system({3}:{4}) at {0}".format(ipmi_ip, (timeout_sec - (do_sec - init_sec)),mark,ipmi_user,ipmi_pass),log_file=log_file,date=True,log=log,log_level=6)
                     else:
                         logging(" {2} wait {1}sec for ready system({3}:{4}) at {0} after down".format(ipmi_ip, (timeout_sec - (do_sec - init_sec)),mark,ipmi_user,ipmi_pass),log_file=log_file,date=True,log=log,log_level=6)
                 node_old='{}'.format(node_state)
            else:
                if chk % 5 == 0:
                    if count_down > 0:
                        logging("Wait {1}sec for readable sensor data from the system({2}:{3}) at {0}".format(ipmi_ip, (timeout_sec - (do_sec - init_sec)),ipmi_user,ipmi_pass),log_file=log_file,date=True,log=log,log_level=6)
                    else:
                        logging("Wait {1}sec for readable sensor data from the system({2}:{3}) at {0} after down".format(ipmi_ip, (timeout_sec - (do_sec - init_sec)),ipmi_user,ipmi_pass),log_file=log_file,date=True,log=log,log_level=6)
        else:
            if chk % 5 == 0:
                logging(" - can't ping to {0}".format(ipmi_ip),log_file=log_file,date=True,log=log,log_level=3)
        chk=chk+1
        sleep(interval)
        do_sec=int(datetime.now().strftime('%s'))
    if log_type=='function':
        logging("Unknown status",log_file=log_file,date=True,log=log,log_level=6)
#        log("Unknown status",log_level=6)
    return [None,'Unknown status']

#def get_lanmode(smcipmitool_file,smcipmitool_opt):
#    if smcipmitool_file is not None and smcipmitool_opt is not None:
#        lanmode_info=rshell('''java -jar {0}/{1} {2}'''.format(tool_path,os.path.basename(smcipmitool_file),smcipmitool_opt))
#        if lanmode_info[0] == 144:
#            a=re.compile('Current LAN interface is \[ (\w.*) \]').findall(lanmode_info[1])
#            if len(a) == 1:
#                return a[0]
#    return

def sizeConvert(sz=None,unit='b:g'):
    if sz is None:
        return False
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
            sz=inc(sz)
        else:
            sz=dec(sz)
    return sz

def git_ver(git_dir=None):
    if git_dir is not None and os.path.isdir('{0}/.git'.format(git_dir)):
        gver=rshell('''cd {0} && git describe --tags'''.format(git_dir))
        if gver[0] == 0:
            return gver[1]

def load_kmod(modules,re_load=False):
    if type(modules) is str:
        modules=modules.split(',')
    for ii in modules:
        if re_load:
            os.system('lsmod | grep {0} >& /dev/null && modprobe -r {0}'.format(ii.replace('-','_')))
        os.system('lsmod | grep {0} >& /dev/null || modprobe --ignore-install {1} || modprobe {1} || modprobe -ib {1}'.format(ii.replace('-','_'),ii))
        #os.system('lsmod | grep {0} >& /dev/null || modprobe -i -f {1}'.format(ii.split('-')[0],ii))

def reduce_string(string,symbol=' ',snum=0,enum=None):
    if type(string) is str:
        arr=string.split(symbol)
    strs=None
    if enum is None:
        enum=len(arr)
    for ii in range(snum,enum):
        if strs is None:
            strs='{0}'.format(arr[ii])
        else:
            strs='{0} {1}'.format(strs,arr[ii])
    return strs

def list2str(arr):
    rc=None
    for i in arr:
        if rc:
            rc='{0} {1}'.format(rc,i)
        else:
            rc='{0}'.format(i)
    return rc


def findstr(string,find,prs=None,split_symbol='\n',patern=True):
    # Patern return selection (^: First(0), $: End(-1), <int>: found item index)
    found=[]
    if not isinstance(string,str): return []
    if split_symbol:
        string_a=string.split(split_symbol)
    else:
        string_a=[string]
    for nn in string_a:
        if isinstance(find,(list,tuple)):
            find=list(find)
        else:
            find=[find]
        for ff in find:
            if patern:
                aa=re.compile(ff).findall(nn)
                for mm in aa:
                    if isinstance(mm,tuple):
                        if prs == '^':
                            found.append(mm[0])
                        elif prs == '$':
                            found.append(mm[-1])
                        elif isinstance(prs,int):
                            found.append(mm[prs])
                        else:
                            found.append(mm)
                    else:
                        found.append(mm)
            else:
                find_a=ff.split('*')
                if len(find_a[0]) > 0:
                    if find_a[0] != nn[:len(find_a[0])]:
                        chk=False
                if len(find_a[-1]) > 0:
                    if find_a[-1] != nn[-len(find_a[-1]):]:
                        chk=False
                for ii in find_a[1:-1]:
                    if ii not in nn:
                        chk=False
                if chk:
                    found.append(nn)
    return found

def find_cdrom_dev(size=None):
    load_kmod(['sr_mod','cdrom','libata','ata_piix','ata_generic','usb-storage'])
    if os.path.isdir('/sys/block') is False:
        return
    for r, d, f in os.walk('/sys/block'):
        for dd in d:
            for rrr,ddd,fff in os.walk(os.path.join(r,dd)):
                if 'removable' in fff:
                    with open('{0}/removable'.format(rrr),'r') as fp:
                        removable=fp.read()
                    if '1' in removable:
                        if os.path.isfile('{0}/device/model'.format(rrr)):
                            with open('{0}/device/model'.format(rrr),'r') as fpp:
                                model=fpp.read()
                            for ii in ['CDROM','DVD-ROM','DVD-RW']:
                                if ii in model:
                                    if size is None:
                                        return '/dev/{0}'.format(dd)
                                    else:
                                        if os.path.exists('{}/size'.format(rrr)):
                                            with open('{}/size'.format(rrr),'r') as fss:
                                                block_size=fss.read()
                                                dev_size=int(block_size) * 512
                                                if dev_size == int(size):
                                                    return '/dev/{0}'.format(dd)

#def ipmi_sol(ipmi_ip,ipmi_user,ipmi_pass):
#    if is_ipv4(ipmi_ip):
#        rshell('''ipmitool -I lanplus -H {} -U {} -P {} sol info'''.format(ipmi_ip,ipmi_user,ipmi_pass))
#Set in progress                 : set-complete
#Enabled                         : true
#Force Encryption                : false
#Force Authentication            : false
#Privilege Level                 : OPERATOR
#Character Accumulate Level (ms) : 0
#Character Send Threshold        : 0
#Retry Count                     : 0
#Retry Interval (ms)             : 0
#Volatile Bit Rate (kbps)        : 115.2
#Non-Volatile Bit Rate (kbps)    : 115.2
#Payload Channel                 : 1 (0x01)
#Payload Port                    : 623

def _u_str2int(val,encode='utf-8'):
    if is_py3():
        if type(val) is bytes:
            return int(val.hex(),16)
        else:
            return int(_u_bytes(val,encode=encode).hex(),16)
    return int(val.encode('hex'),16)

def _u_bytes(val,encode='utf-8'):
    def _bytes_(val,encode):
        try:
            if is_py3():
                if type(val) is bytes:
                    return val
                else:
                    return bytes(val,encode)
            return bytes(val) # if change to decode then network packet broken
        except:
            return val
    tuple_data=False
    if isinstance(val,tuple):
        val=list(val)
        tuple_data=True
    if isinstance(val,list):
        for i in range(0,len(val)):
            val[i]=_bytes_(val[i],encode)
        if tuple_data:
            return tuple(val)
        else:
            return val
    else:
        return _bytes_(val,encode)

def _u_bytes2str(val,encode='latin1'):
    return _u_byte2str(val,encode=encode)

#def _u_byte2str(val,encode='windows-1252'):
def _u_byte2str(val,encode='latin1'):
    #return val.decode(encode) # this is original
    def _byte2str_(val,encode):
        type_val=type(val)
        if is_py3() and type_val is bytes:
            return val.decode(encode)
        elif type_val.__name__ == 'unicode':
            return val.encode(encode)
        return val
    tuple_data=False
    if isinstance(val,tuple):
        val=list(val)
        tuple_data=True
    if isinstance(val,list):
        for i in range(0,len(val)):
            val[i]=_byte2str_(val[i],encode)
        if tuple_data:
            return tuple(val)
        else:
            return val
    else:
        return _byte2str_(val,encode)

def net_send_data(sock,data,key='kg',enc=False,timeout=0):
    if type(sock).__name__ in ['socket','_socketobject','SSLSocket'] and data and type(key) is str and len(key) > 0 and len(key) < 7:
        start_time=now()
        # encode code here
        if timeout > 0:
            sock.settimeout(timeout)
        nkey=_u_str2int(key)
        pdata=pickle.dumps(data,protocol=2) # common 2.x & 3.x version : protocol=2
        data_type=_u_bytes(type(data).__name__[0])
        if enc and key:
            # encode code here
            #enc_tf=_u_bytes('t') # Now not code here. So, everything to 'f'
            #pdata=encode(key,pdata)
            enc_tf=_u_bytes('f')
        else:
            enc_tf=_u_bytes('f')
        ndata=struct.pack('>IssI',len(pdata),data_type,enc_tf,nkey)+pdata
        try:
            sock.sendall(ndata)
            return True,'OK'
        except:
            if timeout > 0:
                #timeout=sock.gettimeout()
                if now() - start_time > timeout-1:
                    #Timeout
                    return False,'Sending Socket Timeout'
    return False,'Sending Fail'

def _dict(pk={},add=False,**var):
    for key in var.keys():
        if key in pk:
            pk.update({key:var[key]})
        else:
            if add:
                pk[key]=var[key]
            else:
                return False
    return pk

def net_receive_data(sock,key='kg',progress=None,retry=0,retry_timeout=30):
    # decode code here
    def recvall(sock,count,progress=False): # Packet
        buf = b''
        file_size_d=int('{0}'.format(count))
        if progress: print('\n')
        tn=0
        newbuf=None
        while count:
            if progress:
                sys.stdout.write('\rDownloading... [ {} % ]'.format(int((file_size_d-count) / file_size_d * 100)))
                sys.stdout.flush()
            try:
                newbuf = sock.recv(count)
            except socket.error as e:
                if tn < retry:
                    print("[ERROR] timeout value:{} retry: {}/{}\n{}".format(sock.gettimeout(),tn,retry,e))
                    tn+=1
                    time.sleep(1)
                    sock.settimeout(retry_timeout)
                    continue
                if e == 'timed out':
                    return 'timeout',e
            if not newbuf: return True,None #maybe something socket issue.
            buf += newbuf
            count -= len(newbuf)
        if progress: 
            sys.stdout.write('\rDownloading... [ 100 % ]\n')
            sys.stdout.flush()
        return True,buf
    ok,head=recvall(sock,10)
    if krc(ok,chk=True):
        if head:
            try:
                st_head=struct.unpack('>IssI',_u_bytes(head))
            except:
                return [False,'Fail for read header({})'.format(head)]
            if st_head[3] == _u_str2int(key):
                ok,data=recvall(sock,st_head[0],progress=progress)
                if krc(ok,chk=True):
                    if st_head[2] == 't':
                        # decode code here
                        # data=decode(data)
                        pass
                    if data: return [st_head[1],pickle.loads(data)]
                    return [True,None]
                else:
                    return [ok,data]
            else:
                return [False,'Wrong key']
        return ['lost','Connection lost']
    return ok,head

def net_put_and_get_data(IP,data,PORT=8805,key='kg',timeout=3,try_num=1,try_wait=[0,5],progress=None,enc=False,upacket=None,SSLC=False,log=True):
    sent=False,'Unknown issue'
    for ii in range(0,try_num):
        if upacket: # Update packet function for number of try information ([#/<total #>])
            data=upacket('ntry',[ii+1,try_num],data)
        start_time=now()
        sock=net_get_socket(IP,PORT,timeout=timeout,SSLC=SSLC)
        if try_num > 0: 
            rtry_wait=(timeout//try_num)+1
        else:
            rtry_wait=try_wait
        sent=False,'Unknown issue'
        try:
            sent=net_send_data(sock,data,key=key,enc=enc)
        except:
            os.system("""[ -f /tmp/.{0}.{1}.crt ] && rm -f /tmp/.{0}.{1}.crt""".format(host,port))
        if sent[0]:
            nrcd=net_receive_data(sock,key=key,progress=progress)
            return nrcd
        else:
            if timeout >0:
                if now() - start_time >= timeout-1:
                    return [False,'Socket Send Timeout']
                #return [False,'Data protocol version mismatch']
        if sock: sock.close()
        if try_num > 1:
            if log:
                print('try send data ... [{}/{}]'.format(ii+1,try_num))
            sleep(try_wait)
    return [False,'Send fail({}) :\n{}'.format(sent[1],data)]

def net_get_socket(host,port,timeout=3,dbg=0,SSLC=False): # host : Host name or IP
    try:
        af, socktype, proto, canonname, sa = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)[0]
    except:
        print('Can not get network informatin of {}:{}'.format(host,port))
        return False
    try:
        soc = socket.socket(af, socktype, proto)
        if timeout > 0:
            soc.settimeout(timeout)
    except socket.error as msg:
        print('could not open socket of {0}:{1}\n{2}'.format(host,port,msg))
        return False
    ###### SSL Wrap ######
    if SSLC:
        for i in range(0,5):
            icertfile='/tmp/.{}.{}.crt'.format(host,port)
            try:
                cert=ssl.get_server_certificate((host,port))
            except:
                os.system('rm -f /tmp/.{}.{}.crt'.format(host,port))
                time.sleep(1)
                continue
            f=open(icertfile,'w')
            f.write(cert)
            f.close()
            time.sleep(0.3)
            try:
                soc=ssl.wrap_socket(soc,ca_certs=icertfile,cert_reqs=ssl.CERT_REQUIRED)
                soc.connect((host,port))
                return soc
            except socket.error as msg:
                if dbg > 3:
                    print(msg)
                time.sleep(1)
    ########################
    else:
        try:
            soc.connect(sa)
            return soc
        except socket.error as msg:
            if dbg > 3:
                print('can not connect at {0}:{1}\n{2}'.format(host,port,msg))
    return False

def net_start_server(server_port,main_func_name,server_ip='',timeout=0,max_connection=10,log_file=None,certfile=None,keyfile=None):
    ssoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if timeout > 0:
        ssoc.settimeout(timeout)
    try:
        ssoc.bind((server_ip, server_port))
    except socket.error as msg:
        print('Bind failed. Error : {0}'.format(msg))
        os._exit(1)
    ssoc.listen(max_connection)
    print('Start server for {0}:{1}'.format(server_ip,server_port))
    # for handling task in separate jobs we need threading
    while True:
        conn, addr = ssoc.accept()
        ip, port = str(addr[0]), str(addr[1])
        try:
            if certfile and keyfile:
                ssl_conn=ssl_wrap(conn,certfile,keyfile=keyfile)
                Thread(target=main_func_name, args=(ssl_conn, ip, port, log_file)).start()
            else:
                Thread(target=main_func_name, args=(conn, ip, port, log_file)).start()
        except:
            print('No more generate thread for client from {0}:{1}'.format(ip,port))
    ssoc.close()

def net_start_single_server(server_port,main_func_name,server_ip='',timeout=0,max_connection=10,log_file=None,certfile=None,keyfile=None):
    ssoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if timeout > 0:
        ssoc.settimeout(timeout)
    try:
        ssoc.bind((server_ip, server_port))
    except socket.error as msg:
        print('Bind failed. Error : {0}'.format(msg))
        os._exit(1)
    ssoc.listen(max_connection)
    print('Start server for {0}:{1}'.format(server_ip,server_port))
    # for handling task in separate jobs we need threading
    conn, addr = ssoc.accept()
    ip, port = str(addr[0]), str(addr[1])
    if certfile and keyfile:
        ssl_conn=ssl_wrap(conn,certfile,keyfile=keyfile)
        rc=main_func_name(ssl_conn, ip, port, log_file)
    else:
        rc=main_func_name(conn, ip, port, log_file)
    ssoc.close()
    return rc

def sleep(try_wait=None):
    try_wait_type=type(try_wait)
    if try_wait in [None,True]:
        time.sleep(1)
    elif try_wait_type is list:
        if len(try_wait) == 2:
            try:
                time.sleep(random.randint(int(try_wait[0]),int(try_wait[1])))
            except:
                time.sleep(1)
        else:
            try:
                time.sleep(int(try_wait[0]))
            except:
                time.sleep(1)
    elif try_wait_type is str:
        if try_wait.isdigit():
            time.sleep(int(try_wait))
    else:
        try:
            time.sleep(try_wait)
        except:
            time.sleep(1)

def check_work_dir(work_dir,make=False,ntry=1,try_wait=[1,3]):
    for ii in range(0,ntry):
        if os.path.isdir(work_dir):
            return True
        else:
            if make:
                try:
                    os.makedirs(work_dir)
                    return True
                except:
                    sleep(try_wait)
    return False

def file_mode(val):
    if isinstance(val,int):
        if val > 511:
            return oct(val)[-4:]
        elif val > 63:
            return oct(val)
    else:
        val=_u_bytes2str(val)
        if val:
            cnt=len(val)
            num=int(val)
            if cnt >=3 and cnt <=4 and num >= 100 and num <= 777:
                return int(val,8)

def get_file(filename,**opts):
    md5sum=opts.get('md5sum',False)
    data=opts.get('data',False)
    include_dir=opts.get('include_dir',False)
    include_sub_dir=opts.get('include_sub_dir',False)

    def get_file_data(filename,root_path=None):
        rc={'name':os.path.basename(filename),'path':os.path.dirname(filename),'exist':False,'dir':False,'link':False}
        if root_path:
            in_filename=os.path.join(root_path,filename)
        else:
            in_filename=filename
        if os.path.exists(in_filename):
            fstat=os.stat(in_filename)
            rc['uid']=fstat.st_uid
            rc['gid']=fstat.st_gid
            rc['size']=fstat.st_size
            rc['atime']=fstat.st_atime
            rc['mtime']=fstat.st_mtime
            rc['ctime']=fstat.st_ctime
            rc['inod']=fstat.st_ino
            rc['mode']=oct(fstat.st_mode)[-4:]
            rc['exist']=True
            if os.path.islink(in_filename):
                rc['link']=True
            else:
                rc['link']=False
                if os.path.isdir(in_filename):
                    rc['dir']=True
                    rc['path']=in_filename
                    rc['name']=''
                else:
                    rc['dir']=False
                    if md5sum or data:
                        with open(in_filename,'rb') as f:
                            fdata=f.read()
                        if md5sum:
                            rc['md5']=md5(fdata)
                        if data:
                            rc['data']=fdata
        return rc

    rc={'exist':False,'includes':[]}
    if type(filename) is str:
        rc.update(get_file_data(filename))
        if rc['dir']:
            root_path=filename
            real_filename=None
        else:
            root_path=os.path.dirname(filename)
            real_filename=os.path.basename(filename)
        if include_dir:
            pwd=os.getcwd()
            os.chdir(root_path)
            for dirPath, subDirs, fileList in os.walk('.'):
                for sfile in fileList:
                    curFile=os.path.join(dirPath.replace('./',''),sfile)
                    if curFile != real_filename:
                        rc['includes'].append(get_file_data(curFile,root_path))
                if include_sub_dir is False:
                    break
            os.chdir(pwd)
    return rc
        
def save_file(data,dest):
    if not isinstance(data,dict) or not isinstance(dest,str) : return False
    if os.path.isdir(dest) is False: os.system('mkdir -p {0}'.format(dest))
    if data.get('dir'):
        fmode=file_mode(data.get('mode'))
        if fmode:
            os.chmod(dest,fmode)
    else:
        # if file then save
        new_file=os.path.join(dest,data['name'])
        if 'data' in data:
            with open(new_file,'wb') as f:
                f.write(data['data'])
        chmod_mode=file_mode(data.get('mode'))
        if chmod_mode:
            os.chmod(new_file,chmod_mode)
    if 'includes' in data and data['includes']: # If include directory or files 
        for ii in data['includes']:
            if ii['path']:
                sub_dir=os.path.join(dest,ii['path'])
            else:
                sub_dir='{}'.format(dest)
            if os.path.isdir(sub_dir) is False: os.system('mkdir -p {}'.format(sub_dir))
            sub_file=os.path.join(sub_dir,ii['name'])
            with open(sub_file,'wb') as f:
                f.write(ii['data'])
            chmod_mode=file_mode(ii.get('mode'))
            if chmod_mode:
                os.chmod(sub_file,chmod_mode)


def get_node_info():
    host_ip=get_host_ip()
    return {
         'host_name':get_host_name(),
         'host_ip':host_ip,
         'host_mac':get_host_mac(ip=host_ip),
         'ipmi_ip':get_ipmi_ip()[1],
         'ipmi_mac':get_ipmi_mac()[1],
         }

def int_sec():
    return int(datetime.now().strftime('%s'))

def now():
    return int_sec()

def timeout(timeout_sec,init_time=None,default=(24*3600)):
    if timeout_sec == 0: return True,0
    init_time=integer(init_time,default=0)
    timeout_sec=integer(timeout_sec,default=default)
    if init_time == 0:
        init_time=int_sec()
    if timeout_sec == 0:
        return False,init_time
    if timeout_sec < 3:
       timeout_sec=3
    if int_sec() - init_time >  timeout_sec:
        return True,init_time
    return False,init_time

def kmp(mp={},func=None,name=None,timeout=0,quit=False,log_file=None,log_screen=True,log_raw=False, argv=[],queue=None):
    # Clean
    for n in [k for k in mp]:
        if quit is True:
            if n != 'log':
                mp[n]['mp'].terminate()
                if 'log' in mp:
                    mp['log']['queue'].put('\nterminate function {}'.format(n))
        else:
            if mp[n]['timeout'] > 0 and int_sec() > mp[n]['timeout']:
                mp[n]['mp'].terminate()
                if 'log' in mp:
                    mp['log']['queue'].put('\ntimeout function {}'.format(n))
        if not mp[n]['mp'].is_alive():
            del mp[n]
    if quit is True and 'log' in mp:
        mp['log']['queue'].put('\nterminate function log')
        time.sleep(2)
        mp['log']['mp'].terminate()
        return

    # LOG
    def logging(ql,log_file=None,log_screen=True,raw=False):
        while True:
            #if not ql.empty():
            if ql.empty():
                time.sleep(0.01)
            else:
                ll=ql.get()
                if raw:
                    log_msg=ll
                else:
                    log_msg='{} : {}\n'.format(datetime.now().strftime('%m-%d-%Y %H:%M:%S'),ll)
                if type(log_msg) is not str:
                    log_msg='{}'.format(log_msg)
                if log_file and os.path.isdir(os.path.dirname(log_file)):
                    with open(log_file,'a') as f:
                        f.write('{}'.format(log_msg))
                if log_screen:
                    sys.stdout.write(log_msg)
                    sys.stdout.flush()

    if 'log' not in mp or not mp['log']['mp'].is_alive():
        #log=multiprocessing.Queue()
        log=Queue()
        #lqp=multiprocessing.Process(name='log',target=logging,args=(log,log_file,log_screen,log_raw,))
        lqp=Process(name='log',target=logging,args=(log,log_file,log_screen,log_raw,))
        lqp.daemon = True
        mp.update({'log':{'mp':lqp,'start':int_sec(),'timeout':0,'queue':log}})
        lqp.start()

    # Functions
    if func:
        if name is None:
            name=func.__name__
        if name not in mp:
            if argv:
                #mf=multiprocessing.Process(name=name,target=func,args=tuple(argv))
                mf=Process(name=name,target=func,args=tuple(argv))
            else:
                #mf=multiprocessing.Process(name=name,target=func)
                mf=Process(name=name,target=func)
            if timeout > 0:
                timeout=int_sec()+timeout
            
#            for aa in argv:
#                if type(aa).__name__ == 'Queue':
#                    mp.update({name:{'mp':mf,'timeout':timeout,'start':now(),'queue':aa}})
            if name not in mp:
                if queue and type(queue).__name__ == 'Queue':
                    mp.update({name:{'mp':mf,'timeout':timeout,'start':int_sec(),'queue':queue}})
                else:
                    mp.update({name:{'mp':mf,'timeout':timeout,'start':int_sec()}})
            mf.start()
    return mp

def key_remove_pass(filename):
    rshell('openssl rsa -in {0}.key -out {0}.nopass.key'.format(filename))

def cert_file(keyfile,certfile,C='US',ST='CA',L='San Jose',O='KGC',OU='KG',CN=None,EMAIL=None,days=365,passwd=None,mode='gen'):
    if keyfile is None and certfile is None:
        return None,None
    if mode == 'remove':
        rc=rshell('openssl rsa -in {0} -out {0}.nopass'.format(keyfile))
        if rc[0] == 0:
            if os.path.isfile('{}'.format(certfile)):
                return '{}.nopass'.format(keyfile),certfile
            else:
                return '{}.nopass.key'.format(keyfile),None
    elif mode == 'gen' or (mode == 'auto' and (os.path.isfile(keyfile) is False or os.path.isfile(certfile) is False)):
        if mode == 'gen':
            os.system('''rm -f {}'''.format(certfile))
            os.system('''rm -f {}'''.format(keyfile))
            os.system('''rm -f {}.csr'''.format(keyfile))
        subj=''
        if C:
            subj='{}/C={}'.format(subj,C)
        if ST:
            subj='{}/ST={}'.format(subj,ST)
        if L:
            subj='{}/L={}'.format(subj,L)
        if O:
            subj='{}/O={}'.format(subj,O)
        if OU:
            subj='{}/OU={}'.format(subj,OU)
        if CN:
            subj='{}/CN={}'.format(subj,CN)
        if EMAIL:
            subj='{}/emailAddress={}'.format(subj,EMAIL)
        if subj:
            subj=' -subj "{}"'.format(subj)
        # gen 
        rc=(1,'error','error',0,0,'','')
        if os.path.isfile(keyfile) is False:
            if passwd:
                # gen KEY
                rc=rshell('openssl genrsa -aes256 -out {0} 2048'.format(keyfile))
            else:
                #print('openssl genrsa -out {0} 2048'.format(keyfile))
                rc=rshell('openssl genrsa -out {0} 2048'.format(keyfile))
        if (os.path.isfile(keyfile) and os.path.isfile(certfile) is False) or rc[0] == 0:
            # gen CSR
    #        time.sleep(0.1)
            os.system('''rm -f {}'''.format(certfile))
            os.system('''rm -f {}.csr'''.format(keyfile))
            rrc=rshell('openssl req -new -key {0} -out {0}.csr {1}'.format(keyfile,subj))
            if rrc[0] == 0:
                # gen cert
                #print('openssl x509 -req -days {1} -in {0}.csr -signkey {0} -out {2}'.format(keyfile,days,certfile))
#                time.sleep(0.1)
                rrrc=rshell('openssl x509 -req -days {1} -in {0}.csr -signkey {0} -out {2}'.format(keyfile,days,certfile))
                if rrrc[0] == 0:
                    # check
#                    print(rshell('openssl x509 -text -noout -in {}'.format(certfile))[1])
#                    time.sleep(3)
                    return keyfile,certfile
    else:
        key_file=None
        crt_file=None
        if os.path.isfile(keyfile):
            key_file=keyfile
        if os.path.isfile(certfile):
            crt_file=certfile
        return key_file,crt_file
    return None,None

def rreplace(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

def net_put_data(IP,data,PORT=8805,key='kg',timeout=3,try_num=1,try_wait=[1,10],progress=None,enc=False,upacket=None,dbg=0,wait_time=3,SSLC=False):
    sent=False,'Unknown issue'
    for ii in range(0,try_num):
        if upacket: # Update packet function for number of try information ([#/<total #>])
            data=upacket('ntry',[ii+1,try_num],data)
        sock=net_get_socket(IP,PORT,timeout=timeout,dbg=dbg,SSLC=SSLC)
        
        if sock is False:
            if dbg >= 3:
                print('Can not get socket data [{}/{}], wait {}s'.format(ii+1,try_num,wait_time))
            else:
                sys.stdout.write('.')
                sys.stdout.flush()
            time.sleep(wait_time)
            continue
        sent=False,'Unknown issue'
        try:
            sent=net_send_data(sock,data,key=key,enc=enc)
        except:
            print('send fail, try again ... [{}/{}]'.format(ii+1,try_num))
        if sent[0]:
            if sock:
                sock.close()
            return [True,'sent']
        if try_num > 1:
            wait_time=make_second(try_wait)
            if dbg >= 3:
                print('try send data ... [{}/{}], wait {}s'.format(ii+1,try_num,wait_time))
            time.sleep(wait_time)
    return [False,'Send fail({}) :\n{}'.format(sent[1],data)]


def make_second(try_wait=None):
    wait_time=1
    if try_wait:
        try_wait_type=type(try_wait)
        if try_wait_type is list:
            if len(try_wait) == 1:
                wait_time=int(try_wait[0])
            else:
                wait_time=random.randint(int(try_wait[0]),int(try_wait[-1]))
        elif try_wait_type is str:
            if try_wait.isdigit():
                wait_time=int(try_wait)
        elif try_wait_type is int:
            wait_time=try_wait
    return wait_time

#def web_server_ip(request):
#    return request.get_host().split(':')

#def web_client_ip(request):
#    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#    if x_forwarded_for:
#        ip = x_forwarded_for.split(',')[0]
#    else:
#        ip = request.META.get('REMOTE_ADDR')
#    return ip

#def web_session(request):
#    return request.session._get_or_create_session_key()

#def web_req(host_url=None,**opts):
# 
#    # remove SSL waring error message (test)
#    requests.packages.urllib3.disable_warnings() 
# 
#    mode=opts.get('mode','get')
#    max_try=opts.get('max_try',3)
#    auth=opts.get('auth',None)
#    user=opts.get('user',None)
#    ip=opts.get('ip',None)
#    port=opts.get('port',None)
#    passwd=opts.get('passwd',None)
#    timeout_sec=opts.get('timeout',None)
#    https=opts.get('https',False)
#    verify=opts.get('verify',True)
#    request_url=opts.get('request_url',None)
#    log=opts.get('log',None)
#    log_level=opts.get('log_level',8)
#    logfile=opts.get('logfile',None)
#    if https:
#        verify=False
#    if auth is None and user and passwd:
#        if type(user) is not str or type(passwd) is not str:
#            printf("user='<user>',passwd='<pass>' : format(each string)",dsp='e',log=log,log_level=log_level,logfile=logfile)
#            return False,"user='<user>',passwd='<pass>' : format(each string)"
#        auth=(user,passwd)
#    if auth and type(auth) is not tuple:
#        printf("auth=('<user>','<pass>') : format(tuple)",dsp='e',log=log,log_level=log_level,logfile=logfile)
#        return False,"auth=('<user>','<pass>') : format(tuple)"
#    data=opts.get('data',None) # dictionary format
#    if data and type(data) is not dict:
#        printf("data={'<key>':'<val>',...} : format(dict)",dsp='e',log=log,log_level=log_level,logfile=logfile)
#        return False,"data={'<key>':'<val>',...} : format(dict)"
#    json_data=opts.get('json',None) # dictionary format
#    if json_data and type(json_data) is not dict:
#        printf("data={'<key>':'<val>',...} : format(dict)",dsp='e',log=log,log_level=log_level,logfile=logfile)
#        return False,"json={'<key>':'<val>',...} : format(dict)"
#    files=opts.get('files',None) # dictionary format
#    if files and type(files) is not dict:
#        printf("files = { '<file parameter name>': (<filename>, open(<filename>,'rb'))} : format(dict)",dsp='e',log=log,log_level=log_level,logfile=logfile)
#        return False,"files = { '<file parameter name>': (<filename>, open(<filename>,'rb'))} : format(dict)"
#    if isinstance(host_url,str):
#        chk_dest=re.compile('http[s]://([a-zA-Z0-9.]*)[:/]').findall(host_url)
#        if len(chk_dest): chk_dest=chk_dest[0]
#        if host_url.find('https://') == 0:
#            verify=False
#    elif ip:
#        chk_dest='{}'.format(ip)
#        if verify:
#            host_url='http://{}'.format(ip)
#        else:
#            host_url='https://{}'.format(ip)
#        if port:
#            host_url='{}:{}'.format(host_url,port)
#        if request_url:
#            host_url='{}/{}'.format(host_url,request_url)
#    else:
#        return False,'host_url or ip not found'    
#    if chk_dest:
#        if not ping(chk_dest,timeout_sec=3):
#            return False,'Can not access to destination({})'.format(chk_dest)
#    ss = requests.Session()
#    for j in range(0,max_try):
#        if mode == 'post':
#            try:
#                r =ss.post(host_url,verify=verify,auth=auth,data=data,files=files,timeout=timeout_sec,json=json_data)
#                return True,r
#            except:
#                pass
#        else:
#            try:
#                r =ss.get(host_url,verify=verify,auth=auth,data=data,files=files,timeout=timeout_sec,json=json_data)
#                return True,r
#            except:
#                pass
#        #except requests.exceptions.RequestException as e:
#        host_url_a=host_url.split('/')[2]
#        server_a=host_url_a.split(':')
#        if len(server_a) == 1:
#            printf("Server({}) has no response (wait {}/{} (10s))".format(server_a[0],j,max_try),dsp='e',log=log,log_level=log_level,logfile=logfile)
#        else:
#            printf("Server({}:{}) has no response (wait {}/{} (10s))".format(server_a[0],server_a[1],j,max_try),dsp='e',log=log,log_level=log_level,logfile=logfile)
#        time.sleep(10)
#    return False,'TimeOut'

def screen_logging(title,cmd):
    # ipmitool -I lanplus -H 172.16.114.80 -U ADMIN -P ADMIN sol activate
    pid=os.getpid()
    tmp_file=mktemp('/tmp/.slc.{}_{}.cfg'.format(title,pid))
    log_file=mktemp('/tmp/.screen_ck_{}_{}.log'.format(title,pid))
    if os.path.isfile(log_file):
        log_file=''
    with open(tmp_file,'w') as f:
        f.write('''logfile {}\nlogfile flush 0\nlog on\n'''.format(log_file))
    if os.path.isfile(tmp_file):
        rc=rshell('''screen -c {} -dmSL "{}" {}'''.format(tmp_file,title,cmd))
        if rc[0] == 0:
            for ii in range(0,50):
                if os.path.isfile(log_file):
                    os.unlink(tmp_file)
                    return log_file
                time.sleep(0.1)

def screen_id(title=None):
    scs=[]
    rc=rshell('''screen -ls''')
    if rc[0] == 1:
        for ii in rc[1].split('\n')[1:]:
            jj=ii.split()
            if len(jj) == 2:
                if title:
                    zz=jj[0].split('.')
                    if zz[1] == title:
                        scs.append(jj[0])
                else:
                    scs.append(jj[0])
    return scs

def screen_kill(title):
    ids=screen_id(title)
    if len(ids) == 1:
        rc=rshell('''screen -X -S {} quit'''.format(ids[0]))
        if rc[0] == 0:
            return True
        return False

def screen_monitor(title,ip,ipmi_user,ipmi_pass,find=[],timeout_sec=600):
    if type(title) is not str or not title:
        print('no title')
        return False
    scr_id=screen_id(title)
    if scr_id:
        print('Already has the title at {}'.format(scr_id))
        return False
    cmd="ipmitool -I lanplus -H {} -U {} -P {} sol activate".format(ip,ipmi_user,ipmi_pass)
    # Linux OS Boot (Completely kernel loaded): find=['initrd0.img','\xff']
    # PXE Boot prompt: find=['boot:']
    # PXE initial : find=['PXE ']
    # DHCP initial : find=['DHCP'] 
    # ex: aa=screen_monitor('test','ipmitool -I lanplus -H <bmc ip> -U ADMIN -P ADMIN sol activate',find=['initrd0.img','\xff'],timeout=300)
    log_file=screen_logging(title,cmd)
    init_time=int_sec()
    if log_file:
        mon_line=0
        old_mon_line=-1
        found=0
        find_num=len(find)
        cnt=0
        while True:
            if int_sec() - init_time > timeout_sec :
                print('Monitoring timeout({} sec)'.format(timeout_sec))
                if screen_kill(title):
                    os.unlink(log_file)
                break
            with open(log_file,'rb') as f:
                tmp=f.read()
            tmp=_u_byte2str(tmp)
            if '\x1b' in tmp:
                tmp_a=tmp.split('\x1b')
            elif '\r\n' in tmp:
                tmp_a=tmp.split('\r\n')
            elif '\r' in tmp:
                tmp_a=tmp.split('\r')
            else:
                tmp_a=tmp.split('\n')
            tmp_n=len(tmp_a)
            for ss in tmp_a[tmp_n-2:]:
                if 'SOL Session operational' in ss:
                    # control+c : "^C", Enter: "^M", any command "<linux command> ^M"
                    rshell('screen -S {} -p 0 -X stuff "^M"'.format(title))
                    cnt+=1
                    if cnt > 5:
                        print('maybe not activated SOL or BMC issue')
                        if screen_kill(title):
                            os.unlink(log_file)
                        return False
                    continue
            if find:
                for ii in tmp_a[mon_line:]:
                    if find_num == 0:
                        print(ii)
                    else:
                        for ff in range(0,find_num):
                            find_i=find[found]
                            if ii.find(find_i) < 0:
                                break
                            found=found+1
                            if found >= find_num:
                                if screen_kill(title):
                                    os.unlink(log_file)
                                return True
                if tmp_n > 1:
                    mon_line=tmp_n -1
                else:
                    mon_line=tmp_n
            else:
                if screen_kill(title):
                    os.unlink(log_file)
                return True
            time.sleep(1)
    return False

def check_value(src,find,idx=None):
    '''Check key or value in the dict, list or tuple then True, not then False'''
    if isinstance(src, (list,tuple,str,dict)):
        if idx is None:
            for i in src:
                if IsSame(i,find): return True
        else:
            if isinstance(src,str):
                if idx < 0:
                    if src[idx-len(find):idx] == find:
                        return True
                else:
                    if src[idx:idx+len(find)] == find:
                        return True
            else:
                if Get(src,idx,out='raw') == find:
                    return True
    return False

def OutFormat(data,out=None):
    if out in [tuple,'tuple']:
        if not isinstance(data,tuple):
            return (data,)
        elif not isinstance(data,list):
            return tuple(data)
    elif out in [list,'list']:
        if not isinstance(data,list):
            return [data]
        elif not isinstance(data,tuple):
            return list(data)
    elif out in ['raw',None]:
        if isinstance(data,(list,tuple)) and len(data) == 1:
            return data[0]
        elif isinstance(data,dict) and len(data) == 1:
            return data.values()[0]
    elif out in ['str',str]:
        return '''{}'''.format(data)
    elif out in ['int',int]:
        try:
            return int(data)
        except:
            pass
    return data

def Get(*inps,**opts):
    default=opts.get('default',None)
    out=opts.get('out',None)
    err=opts.get('err',True)
    check=opts.get('check',(str,list,tuple,dict))
    key=None
    if len(inps) >= 2:
        src=inps[0]
        key=inps[1:]
    elif len(inps) == 1:
        src=inps[0]
        key=opts.get('key',None)
        if isinstance(key,list):
            key=tuple(key)
        elif key is not None:
            key=(key,)
    rc=[]
    if key is None:
        if err in [True,'err','True']:
            return OutFormat(default,out=out)
        return OutFormat(src,out=out)
    if isinstance(src,tuple(check)):
        if isinstance(src,(str,list,tuple)) and len(src)>0:
            for kk in Abs(*key,obj=src,out=list,default=[None],err=False):
                if kk is None:
                    if err != 'ignore':
                        rc.append(default)
                else:
                    rc.append(src[kk])
            if not rc and err in [True,'err','True']:
                return OutFormat(default,out=out)
            return OutFormat(rc,out=out)
        elif isinstance(src,dict) and len(src) > 0:
            nkeys=Abs(*key,obj=src,out=list,default=[None],err=False)
            if nkeys:
                for kk in Abs(*key,obj=src,out=list,default=[None],err=False):
                    rr=src.get(kk,default)
                    if rr == default:
                        if err != 'ignore':
                            rc.append(rr)
                    else:
                        rc.append(rr)
                if not rc and err in [True,'err','True']:
                    return OutFormat(default,out=out)
                return OutFormat(rc,out=out)
            return src.get(key[0],default)
    elif type(src).__name__ in ['instance','classobj']:
        if isinstance(key,(list,tuple,dict)):
            for kk in key:
                rc.append(getattr(src,kk,default))
            if not rc and err in [True,'err','True']:
                return OutFormat(default,out=out)
            return OutFormat(rc,out=out)
        return getattr(src,key,default)
    if err in [True,'err','True']:
        return OutFormat(default,out=out)
    return OutFormat(src,out=out)


def get_value(src,key=None,default=None,check=[str,list,tuple,dict]):
    return Get(src,key,default=default,check=check)

def encode(string):
    enc='{0}'.format(string)
    tmp=zlib.compress(enc.encode("utf-8"))
    return '{0}'.format(base64.b64encode(tmp).decode('utf-8'))

def decode(string):
    if type(string) is str:
        dd=zlib.decompress(base64.b64decode(string))
        return '{0}'.format(dd.decode("utf-8"))
    return string

def string2data(string,default='org',want_type=None):
    if isinstance(string,str):
        try:
            return ast.literal_eval(string)
        except:
            pass
    if want_type:
        if isinstance(string,want_type):
            return string
    if default == 'org':
        return string
    return default

def mount_samba(url,user,passwd,mount_point):
    if os.path.isdir(mount_point) is False:
        os.system('sudo mkdir -p {0}'.format(mount_point))
        time.sleep(1)
    if os.path.isdir(mount_point) is False:
        return False,'can not make a {} directory'.format(mount_point),'can not make a {} directory'.format(mount_point),0,0,None,None
    if 'smb://' in url:
        url_a=url.split('/')
        url_m=len(url_a)
        iso_file=url_a[-1]
        new_url=''
        for i in url_a[2:url_m-1]:
            new_url='{0}/{1}'.format(new_url,i)
        rc=rshell('''sudo mount -t cifs -o user={0} -o password={1} /{2} {3}'''.format(user,passwd,new_url,mount_point))
        if rc[0] == 0:
            return True,rc[1]
    else:
        url_a=url.split('\\')
        url_m=len(url_a)
        iso_file=url_a[-1]
        new_url=''
        for i in url_a[1:url_m-1]:
            new_url='{0}/{1}'.format(new_url,i)
        rc=rshell('''sudo mount -t cifs -o user={0} -o password={1} {2} {3}'''.format(user,passwd,new_url,mount_point))
        if rc[0] == 0:
            return True,rc[1]

def umount(mount_point,del_dir=False):
    rc=rshell('''[ -d {0} ] && sudo mountpoint {0} && sleep 1 && sudo umount {0} && sleep 1'''.format(mount_point))
    if rc[0] == 0 and del_dir:
        os.system('[ -d {0} ] && sudo rmdir {0}'.format(mount_point))
    return rc

def append(src,addendum):
    type_src=type(src)
    type_data=type(addendum)
    if src is None:
        if type_data is str:
            src=''
        elif type_data is dict:
            src={}
        elif type_data is list:
            src=[]
        elif type_data is tuple:
            src=()
        type_src=type(src)
    if addendum is None:
        return src
    if type_src == type_data:
        if type_src is dict:
            return src.update(addendum)
        elif type_src in [list,tuple]:
            src=list(src)
            for ii in addendum:
                if ii not in src:
                    src.append(ii)
            if type_src is tuple:
                src=tuple(src)
            return src
        elif type_src is str:
            return src+addendum
    return False

def is_xml(filename):
    firstLine_i=file_rw(filename,out='string',read='firstline')
    if krc(firstLine_i,chk=True):
        firstLine=get_value(firstLine_i,1)
    else:
        filename_str=_u_byte2str(filename)
        if isinstance(filename_str,str):
            firstLine=filename_str.split('\n')[0]
    if isinstance(firstLine,str) and firstLine.split(' ')[0] == '<?xml':
        return True
    return False

def krc(rt,chk='_',rtd={'GOOD':[True,'True','Good','Ok','Pass',{'OK'},0],'FAIL':[False,'False','Fail',{'FAL'}],'NONE':[None,'None','N/A',{'NA'}],'IGNO':['IGNO','Ignore',{'IGN'}],'ERRO':['ERR','Error','error','erro','ERRO',{'ERR'}],'WARN':['Warn','warn',{'WAR'}],'UNKN':['Unknown','UNKN',{'UNK'}],'JUMP':['Jump',{'JUMP'}],'TOUT':['timeout','TimeOut','time out','Time Out','TMOUT','TOUT',{'TOUT'}],'REVD':['cancel','Cancel','CANCEL','REV','REVD','Revoked','revoked','revoke','Revoke',{'REVD'}],'LOST':['lost','connection lost','Connection Lost','Connection lost','CONNECTION LOST',{'LOST'}]},default=False):
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

def get_data(data,key=None,ekey=None,default=None,method=None,strip=True,find=[],out_form=str):
    if argtype(data,'Request'):
        if key:
            if method is None:
                method=data.method
            if method.upper() == 'GET':
                rc=data.GET.get(key,default)
            elif method == 'FILE':
                if out_form is list:
                    rc=data.FILES.getlist(key,default)
                else:
                    rc=data.FILES.get(key,default)
            else:
                if out_form is list:
                    rc=data.POST.getlist(key,default)
                else:
                    rc=data.POST.get(key,default)
            if argtype(rc,str) and strip:
                rc=rc.strip()
            if find and rc in find:
                return True
            if rc == 'true':
                return True
            elif rc == '':
                return default
            return rc
        else:
            if data.method == 'GET':
                return data.GET
            else:
                return data.data
    else:
        type_data=type(data)
        if type_data in [tuple,list]:
            if len(data) > key:
                if ekey and len(data) > ekey:
                    return data[key:ekey]
                else:
                    return data[key]
        elif type_data is dict:
            return data.get(key,default)
    return default

def compare(a,sym,b,ignore=None):
    if type(a) is not int or type(b) is not int:
        return False
    if ignore is not None:
        if eval('{} == {}'.format(a,ignore)) or eval('{} == {}'.format(b,ignore)):
            return False
    return eval('{} {} {}'.format(a,sym,b))

def integer(a,default=0):
    if isinstance(a,int):
        return a
    try:
        a=int(a)
    except:
        return default

def file_rw(name,data=None,out='string',append=False,read=None,overwrite=True):
    if isinstance(name,str):
        if data is None:
            if os.path.isfile(name):
                try:
                    if read in ['firstread','firstline','first_line','head','readline']:
                        with open(name,'rb') as f:
                            data=f.readline()
                    else:
                        with open(name,'rb') as f:
                            data=f.read()
                except:
                    pass
                if data is not None:
                    if out in ['string','str']:
                        return True,_u_bytes2str(data)
                    else:
                        return True,data
            return False,'File({}) not found'.format(name)
        else:
            file_path=os.path.dirname(name)
            if not file_path or os.path.isdir(file_path): # current dir or correct directory
                try:
                    if append:
                        with open(name,'ab') as f:
                            f.write(_u_bytes(data))
                    else:
                        with open(name,'wb') as f:
                            f.write(_u_bytes(data))
                    return True,None
                except:
                    pass
            return False,'Directory({}) not found'.format(file_path)
    return False,'Unknown type({}) filename'.format(name)

def argtype(arg,want='_',get_data=['_']):
    type_arg=type(arg)
    if want in get_data:
        if type_arg.__name__ == 'Request':
            return arg.method.lower()
        return type_arg.__name__.lower()
    if type(want) is str:
        if type_arg.__name__ == 'Request':
            if want.upper() == 'REQUEST' or want.upper() == arg.method:
                return True
            return False
        else:
            if type_arg.__name__.lower() == want.lower():
                return True
    else:
        if type_arg == want:
            return True
    return False        

def replacestr(data,org,new):
    if isinstance(data,str):
        if not isinstance(org,str): org=_u_bytes2str(org)
        if not isinstance(new,str): new=_u_bytes2str(new)
    elif isinstance(data,bytes):
        if not isinstance(org,bytes): org=_u_bytes(org)
        if not isinstance(new,bytes): new=_u_bytes(new)
#    if not isinstance(data,bytes):
#        data=_u_bytes(data)
#    if not isinstance(org,bytes):
#        org=_u_bytes(org)
#    if not isinstance(new,bytes):
#        new=_u_bytes(new)
    return data.replace(org,new)

def check_version(a,sym,b):
    a=clear_version(a)
    b=clear_version(b)
    if a is False or b is False:
        return False
    if sym == '>':
        if LooseVersion(a) > LooseVersion(b):
            return True
    elif sym == '>=':
        if LooseVersion(a) >= LooseVersion(b):
            return True
    elif sym == '==':
        if LooseVersion(a) == LooseVersion(b):
            return True
    elif sym == '<=':
        if LooseVersion(a) <= LooseVersion(b):
            return True
    elif sym == '<':
        if LooseVersion(a) < LooseVersion(b):
            return True
    return False
    
def get_iso_uid(filename):
    if type(filename) is not str:
        return False,None,None
    if os.path.exists(filename):
        uid_cmd='''sudo /usr/sbin/blkid {}'''.format(filename)
        rc=rshell(uid_cmd)
        if rc[0] == 0:
            uid_str='{0}_{1}'.format(findstr(rc[1],'UUID="(\w.*)" L')[0],findstr(rc[1],'LABEL="(\w.*)" T')[0]).replace(' ','_')
            file_info=get_file(filename)
            file_size=file_info.get('size',None)
            return True,uid_str,file_size
        return False,rc[1],None
    return False,'{} not found'.format(filename),None

def find_usb_dev(size=None,max_size=None):
    rc=[]
    load_kmod(modules=['usb-storage'])
    if os.path.isdir('/sys/block') is False:
        return
    for r, d, f in os.walk('/sys/block'):
        for dd in d:
            for rrr,ddd,fff in os.walk(os.path.join(r,dd)):
                if 'removable' in fff:
                    removable=cat('{0}/removable'.format(rrr))
                    if removable:
                        if '1' in removable:
                            if size is None:
                                if max_size:
                                    file_size=cat('{0}/size'.format(rrr))
                                    if file_size:
                                        dev_size=int(file_size) * 512
                                        if dev_size <= int(max_size):
                                            rc.append('/dev/{0}'.format(dd))
                                else:
                                    rc.append('/dev/{0}'.format(dd))
                            else:
                                file_size=cat('{0}/size'.format(rrr))
                                if file_size:
                                    dev_size=int(file_size) * 512
                                    if dev_size == int(size):
                                        rc.append('/dev/{0}'.format(dd))
    return rc

def get_my_directory():
    return os.path.dirname(os.path.realpath(__file__))

def is_json_format(data):
    try:
        json.loads(data)
        return True
    except:
        return False

def Abs(*inps,**opts):
    default=opts.get('default',None)
    out=opts.get('out','auto')
    obj=opts.get('obj',None)
    err=opts.get('err',True)
 
    def int_idx(idx,nobj,default,err,out='auto'):
        if idx < 0:
            if abs(idx) <= nobj:
                if out in ['list',list]:
                    return [nobj+idx]
                elif out in ['tuple',tuple]:
                    return (nobj+idx,)
                return nobj+idx
            elif err not in [True,'err','True']:
                return 0
        else:
            if nobj > idx:
                if out in ['list',list]:
                    return [idx]
                elif out in ['tuple',tuple]:
                    return (idx,)
                return idx
            elif err not in [True,'err','True']:
                return nobj-1
        return default
    if len(inps) > 0:
        ss=None
        ee=None
        rt=[]
        if obj is None:
            for i in inps:
                if isinstance(i,int):
                    rt.append(abs(i))
                elif err in [True,'err','True']:
                    rt.append(default)
        elif isinstance(obj,dict):
            keys=list(obj)
            for idx in inps:
                if isinstance(idx,int):
                    rt.append(keys[int_idx(idx,len(keys),default,err)])
                elif isinstance(idx,tuple) and len(idx) == 2:
                    ss=Abs(idx[0],**opts)
                    ee=Abs(idx[1],**opts)
                    for i in range(ss,ee+1):
                        rt.append(keys[i])
                elif isinstance(idx,str):
                    try:
                        idx=int(idx)
                        rt.append(int_idx(idx,len(keys),default,err))
                    except:
                        if len(idx.split(':')) == 2:
                            ss,ee=tuple(idx.split(':'))
                            if isinstance(ss,int) and isinstance(ee,int):
                                for i in range(ss,ee+1):
                                    rt.append(keys[i])
                        elif len(idx.split('-')) == 2:
                            ss,ee=tuple(idx.split('-'))
                            if isinstance(ss,int) and isinstance(ee,int):
                                for i in range(ss,ee+1):
                                    rt.append(keys[i])
                        elif len(idx.split('|')) > 1:
                            rt=rt+idx.split('|')
        elif isinstance(obj,(list,tuple,str)):
            nobj=len(obj)
            for idx in inps:
                if isinstance(idx,list):
                    for ii in idx:
                        if isinstance(ii,int):
                            if nobj > ii:
                                rt.append(ii)
                            else:
                                rt.append(OutFormat(default))
                elif isinstance(idx,int):
                    rt.append(int_idx(idx,nobj,default,err))
                elif isinstance(idx,tuple) and len(idx) == 2:
                    ss=Abs(idx[0],**opts)
                    ee=Abs(idx[1],**opts)
                    rt=rt+list(range(ss,ee+1))
                elif isinstance(idx,str):
                    try:
                        idx=int(idx)
                        rt.append(int_idx(idx,nobj,default,err))
                    except:
                        if len(idx.split(':')) == 2:
                            ss,ee=tuple(idx.split(':'))
                            ss=Abs(ss,**opts)
                            ee=Abs(ee,**opts)
                            if isinstance(ss,int) and isinstance(ee,int):
                                rt=rt+list(range(ss,ee+1))
                        elif len(idx.split('-')) == 2:
                            ss,ee=tuple(idx.split('-'))
                            ss=Abs(ss,**opts)
                            ee=Abs(ee,**opts)
                            if isinstance(ss,int) and isinstance(ee,int):
                                rt=rt+list(range(ss,ee+1))
                        elif len(idx.split('|')) > 1:
                            for i in idx.split('|'):
                                ss=Abs(i,obj=obj,out='raw')
                                if isinstance(ss,int):
                                    rt.append(ss)
                        else:
                            rt.append(OutFormat(default))
        return OutFormat(rt,out=out)
    elif obj:
        if isinstance(obj,(list,tuple,str)):
            return len(obj)
        elif isinstance(obj,dict):
            return list(obj.keys())
    return default

def Delete(*inps,**opts):
    if len(inps) >= 2:
        obj=inps[0]
        keys=inps[1:]
    elif len(inps) == 1:
        obj=inps[0]
        keys=opts.get('key',None)
        if isinstance(keys,list):
            keys=tuple(keys)
        elif keys is not None:
            keys=(keys,)
    default=opts.get('default',None)
    _type=opts.get('type','index')
   
    if isinstance(obj,(list,tuple)):
        nobj=len(obj)
        rt=[]
        if _type == 'index':
            nkeys=Abs(*tuple(keys),obj=obj,out=list)
            for i in range(0,len(obj)):
                if i not in nkeys:
                    rt.append(obj[i])
        else:
            for i in obj:
                if i not in keys:
                    rt.append(i)
        return rt
    elif isinstance(obj,dict):
        if isinstance(keys,(list,tuple,dict)):
            for key in keys:
                obj.pop(key,default)
        else:
            obj.pop(keys,default)
        return obj
    elif isinstance(obj,str):
        nkeys=[]
        for i in keys:
            if isinstance(i,(tuple,str,int)):
                tt=Abs(i,obj=obj,out=list)
                if tt:
                    nkeys=nkeys+tt
        rt=''
        for i in range(0,len(obj)):
            if i in nkeys:
                continue
            rt=rt+obj[i]
        return rt
    return default

def alive(out=None):
    aa=rshell('uptime')
    if aa[0] == 0:
        aa_a=aa[1].split()
        if len(aa_a) > 2: 
            if ':' in aa_a[2]:
                if out in ['sec','second','seconds',int]:
                    bb_a=aa_a[2][:-1].split(':')
                    return int(bb_a[0])*3600+int(bb_a[1])*60
                else:
                    return aa_a[2][:-1]+'h'
            elif aa_a[3] == 'min,':
                if out in ['sec','second','seconds',int]:
                    return int(aa_a[2])*60
                else:
                    return aa_a[2]+'m'
            else:
                if out in ['sec','second','seconds',int]:
                    if ':' in aa_a[4]:
                        bb_a=aa_a[4][:-1].split(':')
                        return int(aa_a[2])*(24*3600)+int(bb_a[0])*3600+int(bb_a[1])*60
                    else:
                        if aa_a[5] == 'min,':
                            return int(aa_a[2])*(24*3600)+int(aa_a[4])*60
                        else:
                            return int(aa_a[2])*(24*3600)+int(aa_a[4])
                else:
                    return aa_a[2]+'d'
    if out in ['sec','second','seconds',int]:
        return -1
    else:
        return 'unknown'


class Multiprocessor():
    def __init__(self):
        self.processes = []
        self.queue = Queue()

    @staticmethod
    def _wrapper(func, queue, args, kwargs):
        ret = func(*args, **kwargs)
        queue.put(ret)

    def run(self, func, *args, **kwargs):
        args2 = [func, self.queue, args, kwargs]
        p = Process(target=self._wrapper, args=args2)
        self.processes.append(p)
        p.start()

    def wait(self):
        rets = []
        for p in self.processes[:]:
            ret = self.queue.get()
            rets.append(ret)
            self.processes.remove(p)
        return rets

def IsSame(src,chk_val,sense=False):
    def _IsSame_(src,chk,sense):
        src_type=type(src).__name__
        chk_type=type(chk).__name__
        if src_type == 'bytes' or chk_type == 'bytes':
            if chk_type=='int': chk='{}'.format(chk)
            if isinstance(chk,str):
                if sense:
                    chk=_u_bytes(chk)
                else:
                    chk=_u_bytes(chk).lower()
            elif not sense:
                chk=chk.lower()
            if src_type=='int': src='{}'.format(src)
            if isinstance(src,str):
                if sense:
                    src=_u_bytes(src)
                else:
                    src=_u_bytes(src).lower()
            elif not sense:
                src=src.lower()
            if src == chk: return True
        else:
            if src_type == 'str' and src.isdigit(): src=int(src)
            if chk_type == 'str' and chk.isdigit(): chk=int(chk)
            if not sense and isinstance(src,str) and isinstance(chk,str):
                if src.lower() == chk.lower(): return True
            elif src == chk:
                return True
        return False
    if isinstance(src,(list,tuple)) and isinstance(chk_val,(list,tuple)):
        for j in src:
            ok=False
            for i in chk_val:
                aa=_IsSame_(j,i,sense)
                if aa is True:
                    ok=True
                    break
            if ok is False: return False
        for j in chk_val:
            ok=False
            for i in src:
                aa=_IsSame_(j,i,sense)
                if aa is True:
                    ok=True
                    break
            if ok is False: return False
        return True
    else:
        if isinstance(chk_val,(list,tuple)):
            for i in chk_val:
                aa=_IsSame_(src,i,sense)
                if aa is True: return True
            return False
        else:
            return _IsSame_(src,chk_val,sense)

def ddict(*inps,**opts):
    out={}
    for ii in inps:
        if isinstance(ii,dict):
            out.update(ii)
    if opts:
        out.update(opts)
    return out

def fdict(src,keys):
    if isinstance(src,dict) and isinstance(keys,list):
        new_out={}
        for kk in keys:
            new_out[kk]=src.get(kk)
        return new_out

def is_function(find,src=None):
    if src is None: 
        if isinstance(find,str):
            find=sys.modules.get(find)
        return inspect.isfunction(find)
    aa=[]
    if not isinstance(find,str): find=find.__name__
    if isinstance(src,str):
        src=sys.modules.get(src)
    if inspect.ismodule(src) or inspect.isclass(src):
        for name,fobj in inspect.getmembers(src):
            if inspect.isfunction(fobj): # inspect.ismodule(obj) check the obj is module or not
                aa.append(name)
    else:
        for name,fobj in inspect.getmembers(src):
            if inspect.ismethod(fobj): # inspect.ismodule(obj) check the obj is module or not
                aa.append(name)
    if find in aa: return True
    return False

def pipe_msg(**opts):
    m={}
    if not pipe_file: return False
    if os.path.isfile(pipe_file):
        with open(pipe_file,'rb') as f:
            m=pickle.load(f)
    if opts:
        m.update(opts)
        with open(pipe_file,'wb') as f:
            pickle.dump(m,f, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        return m

def is_same(a,b,sense=False):
    return IsSame(a,b,sense=sense)
#    if isinstance(a,(list,tuple)) and len(a) == 1:
#        a=a[0]
#    if isinstance(b,(list,tuple)) and len(b) == 1:
#        b=b[0]
#    if isinstance(a,str) and a.isdigit():
#        a=int(a)
#    if isinstance(b,str) and b.isdigit():
#        b=int(b)
#    if sense is False and isinstance(a,str) and isinstance(b,str):
#        if a.lower() == b.lower(): return True
#    elif a == b: 
#        return True
#    return False
    
def gen_random_string(length=8,letter='*',digits=True,symbols=True,custom=''):
    src=''
    if custom:
        src=custom
    else:
        if letter == 'upper':
            src=string.ascii_uppercase
        elif letter == 'lower':
            src=string.ascii_lowercase
        elif letter in ['*','all']:
            src=string.ascii_letters
        if digits:
            src=src+string.digits
        if symbols:
            src=src+string.punctuation
    return ''.join(random.choice(src) for i in range(length))

def Try(cmd):
    try:
        return True,cmd
    except:
        e=sys.exc_info()[0]
        return False,{'err':e}


def list_index(src,step):
    if isinstance(src,(list,tuple,str,dict)) and isinstance(step,int):
        if step < 0:
            if len(src) > abs(step):
                step=len(src)-abs(step)
            else:
                step=0
        else:
            if len(src) <= step: step=len(src)-1
        return step
    return 0

def Next(src,step=0,out=None,default='org'):
    if isinstance(src,(list,tuple,dict)):
        step=list_index(src,step)
        iterator=iter(src)
        for i in range(-1,step):
            rt=next(iterator)
        return OutFormat(rt,out=out)
    elif isinstance(src,str):
        step=list_index(src,step)
        if len(src) == 0:
            return ''
        elif len(src) >= 0 or len(src) <= step:
            return OutFormat(src[step],out=out)

    if default == 'org': return src
    OutFormat(default,out=out)

def code_error(email_func=None,email=None,email_title=None,email_server=None,log=None,log_msg='',default=None):
    e=sys.exc_info()[0]
    er=traceback.format_exc()
    if log_msg:
        log_msg='{}\n\n*SYS ERR:\n{}\n\n*FORM ERR:\n{}'.format(log_msg,e,er)
    else:
        log_msg='*SYS ERR:\n{}\n\n*FORM ERR:\n{}'.format(e,er)
    if log: log('\n!!ERROR!!: {}'.format(log_msg),log_level=1)
    if email_func and email and email_title:
        a=email_func(email,email_title,log_msg,dj_ip=email_server)
    time.sleep(5)
    return default

def findXML(xmlfile,find_name=None,find_path=None):
    tree=ET.parse(xmlfile)
    #root=ET.fromstring(data)
    root=tree.getroot()
    def find(tr,find_name):
        for x in tr:
            if x.attrib.get('name') == find_name:
                return x,x.tag
            rt,pp=find(x,find_name)
            if rt:
                return rt,'{}/{}'.format(x.tag,pp)
        return None,None
    found_root=None
    if find_name:
        found=find(root,find_name)
        if found[0]:
             found_root=found[0]
    if find_path and isinstance(find_path,str):
        #ex: root.findall('./Menu/Setting/[@name="Administrator Password"]/Information/HasPassword'):
        if not found_root: found_root=root
        return found_root.findall(find_path)
        # <element>.tag: name, .text: data, .attrib: dict

