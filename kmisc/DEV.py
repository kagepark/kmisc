#Kage Park
import os
from kmisc.Import import *
Import('from kmisc.Type import Type')
Import('from kmisc.Misc import *')

def get_dev_name_from_mac(mac):
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


