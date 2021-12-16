#!/bin/python
# -*- coding: utf-8 -*-
# Kage personal stuff
#
from __future__ import print_function
import sys
import re
import ast
from pprint import pprint
from kmisc.Import import *
Import('from kmisc.Type import Type')
Import('from kmisc.COLOR import COLOR')
Import('from kmisc.STR import STR')
#Import('from kmisc.Misc import *')

def printf(*msg,**opts):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    color_db=opts.get('color_db',{'blue': 34, 'grey': 30, 'yellow': 33, 'green': 32, 'cyan': 36, 'magenta': 35, 'white': 37, 'red': 31})
    bg_color_db=opts.get('bg_color_db',{'cyan': 46, 'white': 47, 'grey': 40, 'yellow': 43, 'blue': 44, 'magenta': 45, 'red': 41, 'green': 42})
    attr_db=opts.get('attr_db',{'reverse': 7, 'blink': 5,'concealed': 8, 'underline': 4, 'bold': 1})
    dsp=opts.get('dsp','s')
    limit=opts.get('limit',None)
    if isinstance(limit,int):
        level=opts.get('level',1)
        if limit < level:
            return
    if not isinstance(dsp,str):
        dsp='s'
    filename=opts.get('filename',None)
    color=opts.get('color',None)
    bgcolor=opts.get('bgcolor',None)
    color_mode=opts.get('color_mode','shell')
    wrap=opts.get('wrap',None)
    length=opts.get('length',None)
    form=opts.get('form',False)

    if opts.get('direct',False):
        new_line=''
        start_new_line=''
    else:
        start_new_line=opts.get('start_new_line','')
        new_line=opts.get('new_line','\n')
    filename=opts.get('filename',None)

    msg_str=''
    for ii in msg:
        if msg_str:
            msg_str='''{}{}{}'''.format(msg_str,new_line,ii)
        else:
            msg_str='''{}'''.format(ii)

    #New line
    if new_line:
        msg_str=msg_str.split(new_line)
    # Cut each line
    if isinstance(length,int):
        length=(length,)
    if isinstance(length,(tuple,list)):
        new_msg_str=[]
        if len(length) == 1:
            for mm in range(0,len(msg_str)):
                new_msg_str=new_msg_str+STR(msg_str[mm]).Cut(head_len=length[0])
        elif  len(length) == 2 and len(msg_str):
            new_msg_str=new_msg_str+STR(msg_str[0]).Cut(head_len=length[0],body_len=length[1])
            if len(msg_str) > 1:
                for mm in range(1,len(msg_str)):
                    new_msg_str=new_msg_str+STR(msg_str[mm]).Cut(head_len=length[1])
        msg_str=new_msg_str
    # wrap each line
    if isinstance(wrap,int):
        wrap=(wrap,)
    if isinstance(wrap,(tuple,list)):
        if len(wrap) == 1:
            for mm in range(0,len(msg_str)):
                msg_str[mm]=tap[0]+msg_str[mm]
        elif  len(wrap) == 2 and len(msg_str):
            msg_str[0]=tap[0]+msg_str[0]
            if len(msg_str) > 1:
                for mm in range(1,len(msg_str)):
                    msg_str[mm]=tap[1]+msg_str[mm]
    msg_str=new_line.join(msg_str)
    if color in ['clear','clean','remove','del','delete','mono']:
        if color_mode == 'shell':
            msg_str=ansi_escape.sub('',msg_str)
    elif color:
        msg_str=COLOR().String(msg_str,color,bg=False,attr=False,mode=color_mode)
    elif bgcolor:
        msg_str=COLOR().String(msg_str,bgcolor,bg=True,mode=color_mode)
    # return msg
    if 'f' in dsp:
        if isinstance(filename,(str,list,tuple)):
             if isinstance(filename,str):filename=filename.split(',')
             for ff in filename:
                 if GET(ff).Dirname():
                     with open(ff,filemode) as f:
                         f.write(msg_str+new_line)
        else:
            dsp=dsp+'s' # if nothing filename then display it on screen
    if 's' in dsp or 'a' in dsp:
         if form:
             try:
                 msg_str=ast.literal_eval(msg_str)
                 pprint(msg_str)
             except:
                 sys.stdout.write(start_new_line+msg_str+new_line)
                 sys.stdout.flush()
         else:
             sys.stdout.write(start_new_line+msg_str+new_line)
             sys.stdout.flush()
    if 'e' in dsp:
         sys.stderr.write(start_new_line+msg_str+new_line)
         sys.stderr.flush()
    if 'r' in dsp:
         if form:
             try:
                 return ast.literal_eval(msg_str)
             except:
                 return start_new_line+msg_str+new_line
         else:
             return start_new_line+msg_str+new_line

def sprintf(string,*inps,**opts):
    if not isinstance(string,str): return False,string
    #"""ipmitool -H %(ipmi_ip)s -U %(ipmi_user)s -P '%(ipmi_pass)s' """%(**opts)
    #"""{app} -H {ipmi_ip} -U {ipmi_user} -P '{ipmi_pass}' """.format(**opts)
    #"""{} -H {} -U {} -P '{}' """.format(*inps)
    #"""{0} -H {1} -U {2} -P '{3}' """.format(*inps)
    ffall=[re.compile('\{(\d*)\}').findall(string),re.compile('\{(\w*)\}').findall(string),re.compile('\%\((\w*)\)s').findall(string),re.compile('\{\}').findall(string)]
    i=0
    for tmp in ffall:
        if i in [0,1]: tmp=[ j  for j in tmp if len(j) ]
        if tmp:
            if i == 0:
                mx=0
                for z in tmp:
                    if int(z) > mx: mx=int(z)
                if inp:
                    if len(inp) > mx: return string.format(*inp)
                elif opts:
                    if len(opts) > mx: return string.format(*opts.values())
                return False,"Need more input (tuple/list) parameters(require {})".format(mx)
            elif 0< i < 2:
                new_str=''
                string_a=string.split()
                oidx=0
                for ii in tmp:
                    idx=None
                    if '{%s}'%(ii) in string_a:
                        idx=string_a.index('{%s}'%(ii))
                    elif "'{%s}'"%(ii) in string_a:
                        idx=string_a.index("'{%s}'"%(ii))
                    if isinstance(idx,int):
                        if ii in opts:
                            string_a[idx]=string_a[idx].format(**opts)
                    elif ii in opts:
                        for jj in range(0,len(string_a)):
                           if '{%s}'%(ii) in string_a[jj]:
                               string_a[jj]=string_a[jj].format(**opts)
                return True,' '.join(string_a)
            elif i == 2:
                new_str=''
                string_a=string.split()
                oidx=0
                for ii in tmp:
                    idx=None
                    if '%({})s'.format(ii) in string_a:
                        idx=string_a.index('%({})s'.format(ii))
                    elif "'%({})'".format(ii) in string_a:
                        idx=string_a.index("'%({})s'".format(ii))
                    if isinstance(idx,int):
                        if ii in opts:
                            string_a[idx]=string_a[idx]%(opts)
                    elif ii in opts:
                        for jj in range(0,len(string_a)):
                           if '%({})s'.format(ii) in string_a[jj]:
                               string_a[jj]=string_a[jj]%(opts)
                return True,' '.join(string_a)
            elif i == 3:
                if inp:
                    if len(tmp) == len(inp): return string.format(*inp)
                    return False,"Mismatched input (tuple/list) number (require:{}, input:{})".format(len(tmp),len(inp))
                elif opts:
                    if len(tmp) == len(opts): return string.format(*opts.values())
                    return False,"Mismatched input (tuple/list) number (require:{}, input:{})".format(len(tmp),len(opts))
        i+=1
    return True,string


def format_print(string,rc=False,num=0,bstr=None,NFLT=False):
    string_type=type(string)
    rc_str=''
    chk=None
    bspace=space(num)

    # Start Symbol
    if string_type is tuple:
        if bstr is None:
            if NFLT:
                rc_str='%s('%(rc_str)
            else:
                rc_str='%s%s('%(bspace,rc_str)
        else:
            rc_str='%s,\n%s%s('%(bstr,bspace,rc_str)
    elif string_type is list:
        if bstr is None:
            if NFLT:
                rc_str='%s['%(rc_str)
            else:
                rc_str='%s%s['%(bspace,rc_str)
        else:
            rc_str='%s,\n%s%s['%(bstr,bspace,rc_str)
    elif string_type is dict:
        if bstr is None:
            rc_str='%s{'%(rc_str)
        else:
            rc_str='%s,\n%s %s{'%(bstr,bspace,rc_str)
    rc_str='%s\n%s '%(rc_str,bspace)

    # Print string
    if string_type is list or string_type is tuple:
       for ii in list(string):
           ii_type=type(ii)
           if ii_type is tuple or ii_type is list or ii_type is dict:
               if not ii_type is dict:
                  num=num+1
               rc_str=format_print(ii,num=num,bstr=rc_str,rc=True)
           else:
               if chk == None:
                  rc_str='%s%s'%(rc_str,STR(str_format_print(ii,rc=True)).Tap())
                  chk='a'
               else:
                  rc_str='%s,\n%s'%(rc_str,STR(str_format_print(ii,rc=True)).Tap(space=bspace+' '))
    elif string_type is dict:
       for ii in string.keys():
           ii_type=type(string[ii])
           if ii_type is dict or ii_type is tuple or ii_type is list:
               num=num+1
               if ii_type is dict:
                   tmp=format_print(string[ii],num=num,rc=True)
               else:
                   tmp=format_print(string[ii],num=num,rc=True,NFLT=True)
               rc_str="%s,\n%s %s:%s"%(rc_str,bspace,str_format_print(ii,rc=True),tmp)
           else:
               if chk == None:
                  rc_str='%s%s'%(rc_str,STR("{0}:{1}".format(str_format_print(ii,rc=True),str_format_print(string[ii],rc=True))).Tap())
                  chk='a'
               else:
                  rc_str='%s,\n%s'%(rc_str,STR("{0}:{1}".format(str_format_print(ii,rc=True),str_format_print(string[ii],rc=True))).Tap(space=bspace+' '))

    # End symbol
    if string_type is tuple:
        rc_str='%s\n%s)'%(rc_str,bspace)
    elif string_type is list:
        rc_str='%s\n%s]'%(rc_str,bspace)
    elif string_type is dict:
        if bstr is None:
            rc_str='%s\n%s}'%(rc_str,bspace)
        else:
            rc_str='%s\n%s }'%(rc_str,bspace)

    else:
       rc_str=string

    # Output
    if rc:
       return rc_str
    else:
       print(rc_str)

def format_string(string,inps):
    cmd=''
    if isinstance(string,dict):
        cmd=string['cmd']
        string=string['base']
    type_inps=type(inps)
    if type_inps is dict:
        if '%(' in string:
            if '%s' in string:
                return False,"name placehoder can't get %s format"
            try:
                return True,string % inps + ' '+cmd
            except:
                return False,"""string:{} input:{}""".format(string,inps)
        elif re.compile('{(\w.*)}').findall(string):
            if re.compile('{\d*}').findall(string):
                return False,"name placehoder can't get {} format"
            return True,string.format(**inps) + ' '+cmd
    else:
        if '%s' in string and type_inps in [tuple,list]:
            if '%(' in string:
                return False,"%s format string can't get name placeholder format"
            return True,string % tuple(inps) + ' '+cmd
        elif re.compile('{\d*}').findall(string) and type_inps in [tuple,list]:
            if re.compile('{(\w.*)}').findall(string):
                return False,"{} format string can't get name placeholder format"
            return True,string.format(*tuple(inps)) + ' '+cmd
        else:
            return None,string+' '+cmd

def format_string_dict(string):
    if isinstance(string,dict):
        string='''{}'''.format(string['base'])
    if '%(' in string or re.compile('{(\w.*)}').findall(string):
        return True
    return False

