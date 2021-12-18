#Kage park
import re
from kmisc.Import import *
Import('requests')
#Import('kmisc.Misc import *')

class WEB:
    def __init__(self,request=None):
        if request:
            self.requests=request
        else:
            self.requests=requests

    def Session(self):
        return self.requests.session._get_or_create_session_key()

    def ClietIp(self):
        x_forwarded_for = self.requests.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.requests.META.get('REMOTE_ADDR')
        return ip

    def ServerIp(self):
        return self.requests.get_host().split(':')

    def Request(self,host_url,**opts):
        # remove SSL waring error message (test)
        self.requests.packages.urllib3.disable_warnings()

        mode=opts.get('mode','get')
        max_try=opts.get('max_try',3)
        auth=opts.get('auth',None)
        user=opts.get('user',None)
        ip=opts.get('ip',None)
        port=opts.get('port',None)
        passwd=opts.get('passwd',None)
        timeout=opts.get('timeout',None)
        https=opts.get('https',False)
        verify=opts.get('verify',True)
        request_url=opts.get('request_url',None)
        log=opts.get('log',None)
        log_level=opts.get('log_level',8)
        logfile=opts.get('logfile',None)
        ping=opts.get('ping',False)
        if https:
            verify=False
        if auth is None and user and passwd:
            if type(user) is not str or type(passwd) is not str:
                printf("user='<user>',passwd='<pass>' : format(each string)",dsp='e',log=log,log_level=log_level,logfile=logfile)
                return False,"user='<user>',passwd='<pass>' : format(each string)"
            auth=(user,passwd)
        if auth and type(auth) is not tuple:
            printf("auth=('<user>','<pass>') : format(tuple)",dsp='e',log=log,log_level=log_level,logfile=logfile)
            return False,"auth=('<user>','<pass>') : format(tuple)"
        data=opts.get('data',None) # dictionary format
        if data and type(data) is not dict:
            printf("data={'<key>':'<val>',...} : format(dict)",dsp='e',log=log,log_level=log_level,logfile=logfile)
            return False,"data={'<key>':'<val>',...} : format(dict)"
        json_data=opts.get('json',None) # dictionary format
        if json_data and type(json_data) is not dict:
            printf("data={'<key>':'<val>',...} : format(dict)",dsp='e',log=log,log_level=log_level,logfile=logfile)
            return False,"json={'<key>':'<val>',...} : format(dict)"
        files=opts.get('files',None) # dictionary format
        if files and type(files) is not dict:
            printf("files = { '<file parameter name>': (<filename>, open(<filename>,'rb'))} : format(dict)",dsp='e',log=log,log_level=log_level,logfile=logfile)
            return False,"files = { '<file parameter name>': (<filename>, open(<filename>,'rb'))} : format(dict)"
        if type(host_url) is str:
            chk_dest=re.compile('http[s]://([a-zA-Z0-9.]*)[:/]').findall(host_url)
            if len(chk_dest): chk_dest=chk_dest[0]
            if host_url.find('https://') == 0:
                verify=False
        elif ip:
            chk_dest='{}'.format(ip)
            if verify:
                host_url='http://{}'.format(ip)
            else:
                host_url='https://{}'.format(ip)
            if port:
                host_url='{}:{}'.format(host_url,port)
            if request_url:
                host_url='{}/{}'.format(host_url,request_url)
        else:
            return False,'host_url or ip not found'
        if ping and chk_dest:
            if not ping(chk_dest,timeout_sec=3):
                return False,'Can not access to destination({})'.format(chk_dest)
        ss = self.requests.Session()
        for j in range(0,max_try):
            if mode == 'post':
                try:
                    r =ss.post(host_url,verify=verify,auth=auth,data=data,files=files,timeout=timeout,json=json_data)
                    return True,r
                except:
                    pass
            else:
                try:
                    r =ss.get(host_url,verify=verify,auth=auth,data=data,files=files,timeout=timeout,json=json_data)
                    return True,r
                except:
                    pass
            #except requests.exceptions.RequestException as e:
            host_url_a=host_url.split('/')[2]
            server_a=host_url_a.split(':')
            if len(server_a) == 1:
                printf("Server({}) has no response (wait {}/{} (10s))".format(server_a[0],j,max_try),dsp='e',log=log,log_level=log_level,logfile=logfile)
            else:
                printf("Server({}:{}) has no response (wait {}/{} (10s))".format(server_a[0],server_a[1],j,max_try),dsp='e',log=log,log_level=log_level,logfile=logfile)
            time.sleep(10)
        return False,'TimeOut'

    def str2url(self,string):
        if string is None: return ''
        if type(string) is str:
            return string.replace('+','%2B').replace('?','%3F').replace('/','%2F').replace(':','%3A').replace('=','%3D').replace(' ','+')
        return string
