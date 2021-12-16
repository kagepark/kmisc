#Kage Park
import socket,os
from kmisc.Import import Import
Import('from kmisc.Type import Type')
Import('from kmisc.DEV import *')
Import('from kmisc.SHELL import SHELL')
Import('from kmisc.IP import IP')
Import('from kmisc.CONVERT import CONVERT')
Import('import uuid')

class HOST:
    def __init__(self):
        pass

    def Name(self):
        return socket.gethostname()

    def NetIp(self,ifname):
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

    def Ip(self,ifname=None,mac=None,default=None):
        if mac is None : mac=self.Mac()
        if ifname is None: ifname=get_dev_name_from_mac(mac)
        ip=self.NetIp(ifname)
        if ip: return ip
        return socket.gethostbyname(socket.gethostname())

    def IpmiIp(self,default=None):
        rt=SHELL().Run('''ipmitool lan print 2>/dev/null| grep "IP Address" | grep -v Source | awk '{print $4}' ''')
        if rt[0]:return rt[1]
        return default

    def IpmiMac(self,default=None):
        rt=SHELL().Run(""" ipmitool lan print 2>/dev/null | grep "MAC Address" | awk """ + """ '{print $4}' """)
        if rt[0]:return rt[1]
        return default

    def DevMac(self,ifname,default=None):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
            return ':'.join(['%02x' % ord(char) for char in info[18:24]])
        except:
            return default

    def Mac(self,ip=None,dev=None,default=None):
        if IP(ip).IsV4():
            dev_info=self.NetDevice()
            for dev in dev_info.keys():
                if self.NetIp(dev) == ip:
                    return dev_info[dev]['mac']
        elif dev:
            return self.DevMac(dev)
        else:
            #return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
            return CONVERT('%012x' % uuid.getnode()).Str2Mac()
        return default

    def DevName(self,mac=None,default=None):
        if mac is None:
            mac=self.Mac()
        net_dir='/sys/class/net'
        if isinstance(mac,str) and os.path.isdir(net_dir):
            dirpath,dirnames,filenames = list(os.walk(net_dir))[0]
            for dev in dirnames:
                fmac=cat('{}/{}/address'.format(dirpath,dev),no_end_newline=True)
                if isinstance(fmac,str) and fmac.strip().lower() == mac.lower():
                    return dev
        return default

    def NetIP(ifname,default=None):
        if not os.path.isdir('/sys/class/net/{}'.format(ifname)):
            return default
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
                pass
        return default

    def Info(self):
        return {
         'host_name':self.Name(),
         'host_ip':self.Ip(),
         'host_mac':self.Mac(),
         'ipmi_ip':self.IpmiIp(),
         'ipmi_mac':self.IpmiMac(),
         }

    def NetDevice(self,name=None):
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

    def Alive(self,ip,keep=20,interval=3,timeout=1800,default=False,log=None,cancel_func=None):
        return IP(ip).Online(keep=keep,interval=interval,timeout=timeout,default=default,log=log,cancel_func=cancel_func)[1]

    def Ping(self,ip):
        return IP(ip).Ping()
