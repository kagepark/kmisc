# Kage Park
from klib.Import import *
Import('from kmisc.Misc import *')

def Tap(num=1,space='',base=4,mode='space'):
    tap=''
    if mode in ['tap','TAP','Tap']: 
        tap='\t'
    else:
        for i in range(0,base):
            tap=tap+' '
    for i in range(0,num):
        space=space+tap
    return space
    

