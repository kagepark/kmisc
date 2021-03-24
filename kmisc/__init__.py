#Kage park

#######################################
# Load All files
#######################################
import os
from kmisc.Import import *
for ii in os.listdir(os.path.dirname(__file__)):
    if ii in ['__init__.py','MODULE.py','test.py','setup.py']: continue
    ii_a=ii.split('.')
    if len(ii_a) == 2 and ii_a[-1] == 'py':
        Import('kmisc.{} import *'.format(ii_a[0]))
