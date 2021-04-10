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
Import('from kmisc.Tap import Tap')

def Print(*msg,**opts):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    color_db=opts.get('color_db',{'blue': 34, 'grey': 30, 'yellow': 33, 'green': 32, 'cyan': 36, 'magenta': 35, 'white': 37, 'red': 31})
    bg_color_db=opts.get('bg_color_db',{'cyan': 46, 'white': 47, 'grey': 40, 'yellow': 43, 'blue': 44, 'magenta': 45, 'red': 41, 'green': 42})
    attr_db=opts.get('attr_db',{'reverse': 7, 'blink': 5,'concealed': 8, 'underline': 4, 'bold': 1})
    def color_string(color,msg,bg=False,attr=False):
           if bg:
               color_code=bg_color_db.get(color,None)
           elif attr:
               color_code=attr_db.get(color,None)
           else:
               color_code=color_db.get(color,None)
           if color_code is None:
               return msg
           if os.getenv('ANSI_COLORS_DISABLED') is None:
               reset='''\033[0m'''
               fmt_msg='''\033[%dm%s'''
               msg=fmt_msg % (color_code,msg)
               return msg+reset

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
    if opts.get('stderr',False):
        if isinstance(dsp,str) and 'e' not in dsp: dsp=dsp+'e'

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
                new_msg_str=new_msg_str+Cut(msg_str[mm],head_len=length[0])
        elif  len(length) == 2 and len(msg_str):
            new_msg_str=new_msg_str+Cut(msg_str[0],head_len=length[0],body_len=length[1])
            if len(msg_str) > 1:
                for mm in range(1,len(msg_str)):
                    new_msg_str=new_msg_str+Cut(msg_str[mm],head_len=length[1])
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
        msg_str=color_string(color,msg_str,bg=False,attr=False,mode=color_mode)
    elif bgcolor:
        msg_str=color_string(color,msg_str,bg=True,mode=color_mode)
    # return msg
    if 'f' in dsp:
        if isinstance(filename,(str,list,tuple)):
             if isinstance(filename,str):filename=filename.split(',')
             for ff in filename:
                 if GET(ff).Dirname():
                     with open(ff,filemode) as f:
                         f.write(start_new_line+msg_str+new_line)
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


