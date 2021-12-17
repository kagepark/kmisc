#Kage Park
from kmisc.Import import *
Import('from kmisc.Type import Type')
Import('from kmisc.SHELL import SHELL')
rshell=SHELL().Run

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

