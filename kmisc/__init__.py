#Kage park

#######################################
# Load All files
#######################################
import os
from kmisc.Import import *
from kmisc.Misc import *
for iii in os.listdir(os.path.dirname(__file__)):
    ii_a=iii.split('.')
    if len(ii_a) == 2 and ii_a[-1] == 'py':
        if ii_a[0] in ['__init__','MODULE','test','setup','kmisc','Misc']: continue
        Import('from kmisc.{0} import {0}'.format(ii_a[0]))
