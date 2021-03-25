#Kage Park
import inspect
from sys import modules
from sys import path as mod_path
from sys import version_info
import importlib
import pip


if version_info[0] < 3: # Python 2 has built in reload
    Py2=True
    Py3=False
elif version_info[0] == 3 and version_info[1] <= 4:
    Py2=False
    Py3=True
    from imp import reload # Python 3.0 - 3.4 
else:
    Py2=False
    Py3=True
    from importlib import reload # Python 3.5+

def Import(*inps,**opts):
    globalenv=dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"] # Get my parent's globals()
    force=opts.get('force',None)
    err=opts.get('err',False)
    default=opts.get('default',False)
    dbg=opts.get('dbg',False)
    install_account=opts.get('install_account','--user')
    if install_account in ['root','all','*','global','system','os']:
        install_account=''

    def CheckObj(obj):
        obj_dir=dir(obj)
        obj_name=type(obj).__name__
        if obj_name in ['function']: return obj_name
        if '__dict__' in obj_dir:
            if obj_name == 'type': return 'classobj'
            return 'instance'
        return obj_name.lower()

    ninps=[]
    for inp in inps:
        ninps=ninps+inp.split(',')
    for inp in ninps:
        inp_a=inp.split()
        classm=False
        class_name=None
        wildcard=None
        if inp_a[0] in ['from','import']:
            del inp_a[0]
        name=inp_a[-1]
        module=inp_a[0]
        if '*' not in inp and name in globalenv: # already loaded
            if force: self.Reload(name) # if force then reload
            continue
        if 'import' in inp_a:
            import_idx=inp_a.index('import')
            if len(inp_a) > import_idx+1:
                class_name=inp_a[import_idx+1]
                classm=True
            else:
                print('*** Wrong information')
                continue
        try:
            if class_name == '*':
                wildcard=importlib.import_module(module)
            else:
                if classm:
                    globalenv[name]=getattr(importlib.import_module(module),class_name)
                else:
                    globalenv[name]=importlib.import_module(module)
        except AttributeError: # Try Loading looped Module/Class then ignore  or Wrong define
            continue
        except ImportError: # Import error then try install
            pip_main=None
            if hasattr(pip,'main'):
                pip_main=pip.main
            elif hasattr(pip,'_internal'):
                pip_main=pip._internal.main
            if module == 'magic': 
                install_name='python-magic'
            elif module == 'bdist_wheel': 
                install_name='wheel'
            else:
                install_name='{}'.format(module.split('.')[0])
            if pip_main and pip_main(['install',install_name,install_account]) == 0:
                if class_name == '*':
                    wildcard=importlib.import_module(module)
                else:
                    if classm:
                        globalenv[name]=getattr(importlib.import_module(module),name)
                    else:
                        globalenv[name]=importlib.import_module(module)
            else:
                if dbg:
                    print('*** Import Error or Need install with SUDO or ROOT or --user permission')
                continue
        if wildcard: # import wildcard
            for ii in wildcard.__dict__.keys():
                if ii not in ['__name__','__doc__','__package__','__loader__','__spec__','__file__','__cached__','__builtins__']:
                    if ii in globalenv:
                        # swap Same Name between module(my module of the wild card) and class(wild card import class name)
                        if ii in wildcard.__dict__.keys():
                            if CheckObj(globalenv[ii]) == 'module' and CheckObj(wildcard.__dict__[ii]) == 'classobj':
#                                TMP=globalenv[ii] # move to local temporay 
                                globalenv[ii]=wildcard.__dict__[ii]
                                continue
                        if not force: continue # Not force then ignore same name
                    globalenv[ii]=wildcard.__dict__[ii]
