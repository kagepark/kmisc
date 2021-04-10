#Kage Park
import os
import sys
from kmisc.Import import *
Import('import syslog')
Import('from kmisc.TIME import TIME')

class LOG:
    def __init__(self,**opts):
        self.limit=opts.get('limit',3)
        self.dbg_level=opts.get('dbg_level',None)
        self.path=opts.get('path','/tmp')
        self.log_file=opts.get('log_file',None)
        self.info_file=opts.get('info_file',None)
        self.error_file=opts.get('error_file',None)
        self.dbg_file=opts.get('dbg_file',None)
        self.screen=opts.get('screen',False)
        self.date_format=opts.get('date_format','[%m/%d/%Y %H:%M:%S]')

    def Format(self,*msg,**opts):
        log_date_format=opts.get('date_format',self.date_format)
        func_name=opts.get('func_name',None)
        end_new_line=opts.get('end_new_line','')
        start_new_line=opts.get('start_new_line','\n')
        if len(msg) > 0:
            m_str=None
            intro=''
            intro_space=''
            if log_date_format:
                intro=TIME().Format(tformat=log_date_format)+' '
            func_name_name=type(func_name).__name__
            if func_name_name == 'str':
                intro=intro+'{0} '.format(func_name)
            elif func_name is True:
                intro=intro+'{0}() '.format(get_caller_fcuntion_name())
            elif func_name_name in ['function','instancemethod']:
                intro=intro+'{0}() '.format(func_name.__name__)
            if intro:
               for i in range(0,len(intro)):
                   intro_space=intro_space+' '
            for m in list(msg):
                n=m.split('\n')
                if m_str is None:
                    m_str='{0}{1}{2}{3}'.format(start_new_line,intro,n[0],end_new_line)
                else:
                    m_str='{0}{1}{2}{3}{4}'.format(m_str,start_new_line,intro_space,n[0],end_new_line)
                for nn in n[1:]:
                    m_str='{0}{1}{2}{3}{4}'.format(m_str,start_new_line,intro_space,nn,end_new_line)
            return m_str

    def Syslogd(self,*msg,**opts):
        syslogd=opts.get('syslogd',None)
        if syslogd:
            syslog_msg=' '.join(msg)
            if syslogd in ['INFO','info']:
                syslog.syslog(syslog.LOG_INFO,syslog_msg)
            elif syslogd in ['KERN','kern']:
                syslog.syslog(syslog.LOG_KERN,syslog_msg)
            elif syslogd in ['ERR','err']:
                syslog.syslog(syslog.LOG_ERR,syslog_msg)
            elif syslogd in ['CRIT','crit']:
                syslog.syslog(syslog.LOG_CRIT,syslog_msg)
            elif syslogd in ['WARN','warn']:
                syslog.syslog(syslog.LOG_WARNING,syslog_msg)
            elif syslogd in ['DBG','DEBUG','dbg','debug']:
                syslog.syslog(syslog.LOG_DEBUG,syslog_msg)
            else:
                syslog.syslog(syslog_msg)


    def File(self,log_str,log_level,special_file=None):
        log_file=None
        if os.path.isdir(self.path):
            if (log_level in ['dbg','debug'] or (isinstance(log_level,int) and isinstance(self.dbg_level,int) and self.dbg_level <= log_level <= self.limit)) and isinstance(self.dbg_file,str):
                log_file=os.path.join(self.path,self.dbg_file)
            elif log_level in ['info'] and isinstance(self.info_file,str):
                log_file=os.path.join(self.path,self.info_file)
            elif log_level in ['error'] and isinstance(self.error_file,str):
                log_file=os.path.join(self.path,self.error_file)
            elif isinstance(self.log_file,str) or isinstance(special_file,str):
                if special_file:
                    log_file=os.path.join(self.path,special_file)
                elif log_level in ['dbg','debug','info','error'] or (isinstance(log_level,int) and log_level <= self.limit):
                    log_file=os.path.join(self.path,self.log_file)
            if log_file:
                with open(log_file,'a+') as f:
                    f.write(log_str)
        return log_file

    def Screen(self,log_str,log_level):
        if log_level in ['error']:
            sys.stderr.write(log_str)
            sys.stderr.flush()
        elif log_level <= self.limit:
            sys.stdout.write(log_str)
            sys.stdout.flush()


    def Log(self,*msg,**opts):
        direct=opts.get('direct',False)
        func_name=opts.get('func_name',None)
        date_format=opts.get('date_format','[%m/%d/%Y %H:%M:%S]')
        start_new_line=opts.get('start_new_line','\n')
        end_new_line=opts.get('end_new_line','')
        log_level=opts.get('log_level',3)
        special_file=opts.get('filename',None)
        screen=opts.get('screen',None)
        syslogd=opts.get('syslogd',None)
        if msg:
            # send log at syslogd
            self.Syslogd(*msg,syslogd=syslogd)

            if date_format in [False,None,'','no','ignore']:
                date_format=None
            if func_name in [False,None,'','no','ignore']:
                func_name=None
            if direct:
                log_str=' '.join(msg)
            else:
                log_str=self.Format(*msg,func_name=func_name,date_format=date_format,end_new_line=end_new_line,start_new_line=start_new_line)

            # Saving log at file
            log_file=self.File(log_str,log_level,special_file=special_file)

            # print at screen
            if screen is True or (screen is None and self.screen is True):
                self.Screen(log_str,log_level)
 
            # Send Log Data to logging function (self.log_file)
            if log_file is None:
                self.Function(log_str)

    def Function(self,*msg,**opts):
        if type(self.log_file).__name__ == 'function': 
            log_func_arg=get_function_args(self.log_file,mode='all')
            if 'args' in log_func_arg or 'varargs' in log_func_arg:
                log_p=True
                args=log_func_arg.get('args',[])
                if args and len(args) <= 4 and ('direct' in args or 'log_level' in args or 'func_name' in args):
                    tmp=[]
                    for i in range(0,len(args)):
                        tmp.append(i)
                    if 'direct' in args:
                        didx=args.index('direct')
                        del tmp[didx]
                        args[didx]=direct
                    if 'log_level' in args:
                        lidx=args.index('log_level')
                        del tmp[lidx]
                        args[lidx]=log_level
                    if 'func_name' in args:
                        lidx=args.index('func_name')
                        del tmp[lidx]
                        args[lidx]=func_name
                    if 'date_format' in args:
                        lidx=args.index('date_format')
                        del tmp[lidx]
                        args[lidx]=date_format
                    args[tmp[0]]=log_str
                    self.log_file(*args)
                elif 'keywards' in log_func_arg:
                    self.log_file(log_str,direct=direct,log_level=log_level,func_name=func_name,date_format=date_format)
                elif 'defaults' in log_func_arg:
                    if 'direct' in log_func_arg['defaults'] and 'log_level' in log_func_arg['defaults']:
                        self.log_file(log_str,direct=direct,log_level=log_level)
                    elif 'log_level' in log_func_arg['defaults']:
                        self.log_file(log_str,log_level=log_level)
                    elif 'direct' in log_func_arg['defaults']:
                        self.log_file(log_str,direct=direct)
                    else:
                        self.log_file(log_str)
                else:
                    self.log_file(log_str)

