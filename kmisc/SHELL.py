#Kage park
import sys
import os
import subprocess
from threading import Thread
from kmisc.Import import *
Import('from kmisc.TIME import TIME')

class SHELL:
    def __init__(self):
        pass

    def Pprog(self,stop,progress_pre_new_line=False,progress_post_new_line=False,log=None,progress_interval=5):
        TIME().Sleep(progress_interval)
        if stop():
            return
        if progress_pre_new_line:
            if log:
                log('\n',direct=True,log_level=1)
            else:
                sys.stdout.write('\n')
                sys.stdout.flush()
        post_chk=False
        while True:
            if stop():
                break
            if log:
                log('>',direct=True,log_level=1)
            else:
                sys.stdout.write('>')
                sys.stdout.flush()
            post_chk=True
            TIME().Sleep(progress_interval)
        if post_chk and progress_post_new_line:
            if log:
                log('\n',direct=True,log_level=1)
            else:
                sys.stdout.write('\n')
                sys.stdout.flush()

    def Run(self,cmd,timeout=None,ansi=True,path=None,progress=False,progress_pre_new_line=False,progress_post_new_line=False,log=None,progress_interval=5):
        start_time=TIME()
        if not isinstance(cmd,str):
            return -1,'wrong command information :{0}'.format(cmd),'',start_time.Init(),start_time.Init(),start_time.Now(int),cmd,path
        Popen=subprocess.Popen
        PIPE=subprocess.PIPE
        cmd_env=''
        cmd_a=cmd.split()
        cmd_file=cmd_a[0]
        if cmd_a[0] == 'sudo': cmd_file=cmd_a[1]
        if path and isinstance(path,str) and os.path.isdir(path) and os.path.isfile(os.path.join(path,cmd_file)):
            cmd_env='''export PATH=%s:${PATH}; '''%(path)
            if os.path.join(path,cmd_file):
                cmd_env=cmd_env+'''cd %s && '''%(path)
        elif cmd_file[0] != '/' and cmd_file == os.path.basename(cmd_file) and os.path.isfile(cmd_file):
            cmd_env='./'
        p = Popen(cmd_env+cmd , shell=True, stdout=PIPE, stderr=PIPE)
        out=None
        err=None
        if progress:
            stop_threads=False
            ppth=Thread(target=self.Pprog,args=(lambda:stop_threads,progress_pre_new_line,progress_post_new_line,log,progress_interval))
            ppth.start()
        if isinstance(timeout,(int,str)):
            try:
                timeout=int(timeout)
            except:
                timeout=600
            if timeout < 3:
                timeout=3
        if PyVer(3):
            try:
                out, err = p.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                p.kill()
                if progress:
                    stop_threads=True
                    ppth.join()
                return -1, 'Kill process after timeout ({0} sec)'.format(timeout), 'Error: Kill process after Timeout {0}'.format(timeout),start_time.Init(),start_time.Now(int),cmd,path
        else:
            if isinstance(timeout,int):
                countdown=int('{}'.format(timeout))
                while p.poll() is None and countdown > 0:
                    TIME().Sleep(2)
                    countdown -= 2
                if countdown < 1:
                    p.kill()
                    if progress:
                        stop_threads=True
                        ppth.join()
                    return -1, 'Kill process after timeout ({0} sec)'.format(timeout), 'Error: Kill process after Timeout {0}'.format(timeout),start_time.Init(),start_time.Now(int),cmd,path
            out, err = p.communicate()

        if progress:
            stop_threads=True
            ppth.join()
        if PyVer(3):
            out=out.decode("ISO-8859-1")
            err=err.decode("ISO-8859-1")
        if ansi:
            return p.returncode, out.rstrip(), err.rstrip(),start_time.Init(),start_time.Now(int),cmd,path
        else:
            return p.returncode, ansi_escape.sub('',out).rstrip(), ansi_escape.sub('',err).rstrip(),start_time.Init(),start_time.Now(int),cmd,path

