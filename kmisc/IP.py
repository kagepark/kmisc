#Kage Park
import socket
import struct
from distutils.spawn import find_executable
from klib.Import import *
Import('from kmisc.Type import Type')
Import('from kmisc.TIME import TIME')
Import('from kmisc.SHELL import SHELL')

def is_cancel(func):
    ttt=type(func).__name__
    if ttt in ['function','instancemethod','method']:
        if func():
            return True
    elif ttt in ['bool','str'] and func in [True,'cancel']:
        return True
    return False

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
            if not self.Ping(self.src,count=3):
                if not self.Ping(self.src,count=0,timeout=timeout_sec,keep_good=keep_good,interval=interval,cancel_func=cancel_func,log=log):
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
        elif isinstance(self.src,type(hex)):
            ip_int=int(self.src,16)

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
        time=TIME()
        run_time=time.Int()
        if self.IsV4(self.src):
            if log:
                log('[',direct=True,log_level=1)
            while True:
                if time.Out(timeout_sec):
                    if log:
                        log(']\n',direct=True,log_level=1)
                    return False,'Timeout monitor'
                if is_cancel(cancel_func):
                    if log:
                        log(']\n',direct=True,log_level=1)
                    return True,'Stopped monitor by Custom'
                if self.Ping(self.src,cancel_func=cancel_func):
                    if (time.Int() - run_time) > keep:
                        if log:
                            log(']\n',direct=True,log_level=1)
                        return True,'OK'
                    if log:
                        log('-',direct=True,log_level=1)
                else:
                    run_time=time.Int()
                    if log:
                        log('.',direct=True,log_level=1)
                time.Sleep(interval)
            if log:
                log(']\n',direct=True,log_level=1)
            return False,'Timeout/Unknown issue'
        return default,'IP format error'

    def Ping(self,host=None,count=3,interval=1,keep_good=0, timeout=60,lost_mon=False,log=None,stop_func=None,log_format='.',cancel_func=None):
        if host is None: host=self.src
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
            my_checksum = checksum(CONVERT(header).Str() + data)
            header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,
                                 socket.htons(my_checksum), size, 1)
            return header + CONVERT(data).Bytes()

        def receive(my_socket, ssize, stime, timeout):
            while True:
                if timeout <= 0:
                    return
                ready = select.select([my_socket], [], [], timeout)
                if ready[0] == []: # Timeout
                    return
                received_time = time.time()
                packet, addr = my_socket.recvfrom(1024)
                type, code, checksum, gsize, seq = struct.unpack('bbHHh', packet[20:28]) # Get Header
                if gsize == ssize:
                    return received_time - stime
                timeout -= received_time - stime

        def pinging(ip,timeout=1,size=64):
            try:
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
            except socket.error as e:
                if e.errno in ERROR_DESCR:
                    raise socket.error(''.join((e.args[1], ERROR_DESCR[e.errno])))
                raise
            if size in ['rnd','random']:
                # Maximum size for an unsigned short int c object(65535)
                size = int((id(timeout) * random.random()) % 65535)
            packet = mk_packet(size)
            while packet:
                sent = my_socket.sendto(packet, (ip, 1)) # ICMP have no port, So just put dummy port 1
                packet = packet[sent:]
            delay = receive(my_socket, size, TIME().Time(), timeout)
            my_socket.close()
            if delay:
                return delay,size

        def do_ping(ip,timeout=1,size=64,count=None,interval=0.7,log_format='ping',cancel_func=None):
            ok=1
            i=1
            while True:
                if is_cancel(cancel_func):
                    return -1,'canceled'
                delay=pinging(ip,timeout,size)
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
                        sys.stdout.write('{} icmp_seq={} timeout ({} second)\n'.format(ip,i,timeout))
                        sys.stdout.flush()
                if count:
                    count-=1
                    if count < 1:
                        return ok,'{} is alive'.format(ip)
                i+=1
                TIME().Sleep(interval)


        if log_format=='ping':
            if find_executable('ping'):
                os.system("ping -c {0} {1}".format(count,host))
            else:
                do_ping(host,timeout=timeout,size=64,count=count,log_format='ping',cancel_func=cancel_func)
        else:
            Time=TIME()
            init_sec=Time.Init()
            chk_sec=Time.Init()
            log_type=type(log).__name__
            found_lost=False
            if keep_good > 0 or not count:
               try:
                   timeout=int(timeout)
               except:
                   timeout=1
               if timeout < keep_good:
                   count=keep_good+(2*interval)
                   timeout=keep_good+5
               elif not count:
                   count=timeout//interval + 3
               elif count * interval > timeout:
                   timeout=count*interval+timeout
            good=False
            while count > 0:
               if is_cancel(cancel_func):
                   log(' - Canceled ping')
                   return False
               if stop_func:
                   if log_type == 'function':
                       log(' - Stopped ping')
                   return False
               if find_executable('ping'):
                   rc=SHELL().Run("ping -c 1 {}".format(host))
               else:
                   rc=do_ping(host,timeout=1,size=64,count=1,log_format=None)
               if rc[0] == 0:
                  good=True
                  if keep_good:
                      if good and keep_good and TIME().Now(int) - chk_sec >= keep_good:
                          return True
                  else:
                      return True
                  if log_type == 'function':
                      log('.',direct=True,log_level=1)
               else:
                  good=False
                  chk_sec=TIME().Now(int)
                  if log_type == 'function':
                      log('x',direct=True,log_level=1)
               if TIME().Now(int) - init_sec > timeout:
                   return False
               TIME().Sleep(interval)
               count-=1
            return good
