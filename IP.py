#Kage Park
import socket
import struct
from klib.MODULE import MODULE
MODULE().Import('from klib.kmisc import *')
MODULE().Import('from klib.PING import ping')
MODULE().Import('from klib.TIME import TIME')

class IP:
    def __init__(self,src):
        self.src=src
#        if isinstance(src,str):
#            self.src=src.strip()
#        elif isinstance(src,int):
#            self.src=src
#        elif isinstance(src,hex):
#            self.src=src

    def IsV4(self,ip=None):
        if ip is not None:
            self.src=ip
        if self.V4(default=False) is False: return False
        return True
#        if ip is None:
#            ip=self.src
#        if isinstance(ip,str):
#            ipa = ip.strip().split(".")
#            if len(ipa) != 4: return False
#            for ipn in ipa:
#                if not ipn.isdigit() or not 0 <= int(ipn) <= 255: return False
#            return True
#        return False

    def WithPort(self,port,**opts):
        default=opts.get('default',False)
        tcp_sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_sk.settimeout(1)
        if self.IsV4(self.src) is False or not isinstance(port,(str,int,list,tuple)):
            return default
        if isinstance(port,(str,int)):
            try:
                port=[int(port)]
            except:
                return default
        for pt in port:
            try:
                tcp_sk.connect((self.src,pt))
                return True
            except:
                pass
        return False

    def Ip2Num(self,ip=None,default=False):
        if ip is not None:
            self.src=ip
        return self.V4(out=int,default=default)
#        if ip is None:
#            ip=self.src
#        if isinstance(ip,int):
#            return ip
#        if self.IsV4(ip):
#            return struct.unpack("!L", socket.inet_aton(ip))[0]
#        return default

    def Ip2Str(self,ip=None,default=False):
        if ip is not None:
            self.src=ip
        return self.V4(out=str,default=default)

    def Ip2hex(self,ip=None,default=False):
        if ip is not None:
            self.src=ip
        return self.V4(out=hex,default=default)

    def InRange(self,start_ip,end_ip,**opts):
        default=opts.get('default',False)
        startip=self.Ip2Num(start_ip)
        myip=self.Ip2Num(self.src)
        endip=self.Ip2Num(end_ip)
        if isinstance(startip,int) and isinstance(myip,int) and isinstance(endip,int):
            if startip <= myip <= endip: return True
            return False
        return default

    def LostNetwork(self,**opts):
        default=opts.get('default',False)
        timeout_sec=opts.get('timeout',1800)
        interval=opts.get('interval',2)
        keep_good=opts.get('keep_good',30)
        cancel_func=opts.get('cancel_func',None)
        log=opts.get('log',None)
        init_time=None
        if self.IsV4():
            if not ping(self.src,count=3):
                if not ping(self.src,count=0,timeout=timeout_sec,keep_good=keep_good,interval=interval,cancel_func=cancel_func,log=log):
                    return True
            return False
        return default

    def V4(self,out='str',default=False):
        ip_int=None
        if isinstance(self.src,str):
            ipstr=self.src.strip()
            if '0x' in ipstr:
                ip_int=int(ipstr,16)
            elif ipstr.isdigit():
                ip_int=int(ipstr)
            elif '.' in ipstr:
                try:
                    ip_int=struct.unpack("!I", socket.inet_aton(ipstr))[0] # convert Int IP
                except:
                    return default
        elif isinstance(self.src,int):
            try:
                socket.inet_ntoa(struct.pack("!I", ipaddr)) # check int is IP or not
                ip_int=self.src
            except:
                return default
        elif isinstance(self.src,hex):
            ip_int=int(ipaddr,16)

        if ip_int is not None:
            if out in ['str',str]:
                return socket.inet_ntoa(struct.pack("!I", ip_int))
            elif out in ['int',int]:
                return ip_int
            elif out in ['hex',hex]:
                return hex(ip_int)
        return default

    def Online(self,**opts):
        default=opts.get('default',False)
        timeout_sec=opts.get('timeout',1800)
        interval=opts.get('interval',3)
        keep=opts.get('keep',20)
        cancel_func=opts.get('cancel_func',None)
        log=opts.get('log',None)
        init_time=None
        run_time=int_sec()
        if self.IsV4(self.src):
            if log:
                log('[',direct=True,log_level=1)
            while True:
                ttt,init_time=timeout(timeout_sec,init_time)
                if ttt:
                    if log:
                        log(']\n',direct=True,log_level=1)
                    return False,'Timeout monitor'
                if self.cancel(cancel_func):
                    if log:
                        log(']\n',direct=True,log_level=1)
                    return True,'Stopped monitor by Custom'
                if ping(self.src,cancel_func=cancel_func):
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
                TIME().Sleep(interval)
            if log:
                log(']\n',direct=True,log_level=1)
            return False,'Timeout/Unknown issue'
        return default,'IP format error'

    def Host(self,ifname=None,mac=None):
        if ifname or mac:
            if mac:
                ifname=get_dev_name_from_mac(mac)
            return get_net_dev_ip(ifname)
        else:
            ifname=get_dev_name_from_mac()
            if ifname:
                ip=get_net_dev_ip(ifname)
                if self.IsV4(ip):
                    return ip
            return socket.gethostbyname(socket.gethostname())

    def Dev(ifname):
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
