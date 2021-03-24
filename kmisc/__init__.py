#Kage park

#######################################
# Load All files
#######################################
import os
from klib.MODULE import *
for ii in os.listdir(os.path.dirname(__file__)):
    if ii in ['__init__.py','MODULE.py','test.py','setup.py']: continue
    ii_a=ii.split('.')
    if len(ii_a) == 2 and ii_a[-1] == 'py':
        MODULE().Import('klib.{} import *'.format(ii_a[0]))
#######################################
# Load defined Files
#######################################
# from klib.MODULE import *
# from klib.Type import Type
# from klib.Misc import *
# from klib.IS import IS
# from klib.DICT import DICT
# from klib.LIST import LIST
# from klib.GET import GET
# from klib.CONVERT import CONVERT
# from klib.BMC import *
# from klib.PRINT import *
# from klib.PING import *
# from klib.IP import IP
