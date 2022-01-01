#Kage Park
# Base size 6.4MB
# pip module size : 21MB
from distutils.version import LooseVersion
from inspect import getmembers, stack
from sys import version_info, executable
from sys import path as mod_path
from os import path as os_path
from importlib import import_module
from pkg_resources import working_set
#import pip
from subprocess import check_call
#import git
from pathlib import Path
'''
if you want requests then you need must pre-loaded below module when you use compiled binary file using pyinstaller

example)
from http.cookies import Morsel
Import('import requests')

Without build then import requests is ok. but if you build it then it need pre-loaded Morsel module for Import('import requests') command
'''

def PyVer(main=None,miner=None,msym=None):
    if isinstance(main,int):
        if main == version_info[0]:
            if isinstance(miner,int):
                if msym:
                    if msym == '>=':
                        if version_info[1] >= miner: return True
                    elif msym == '>':
                        if version_info[1] > miner: return True
                    elif msym == '<=':
                        if version_info[1] <= miner: return True
                    elif msym == '<':
                        if version_info[1] < miner: return True
                if miner == version_info[1]:return True
                return False
            return True
        return False
    else:
        return '{}.{}'.format(version_info[0],version_info[1])

# Python 2 has built in reload
if PyVer(3,4,'<='): 
    from imp import reload # Python 3.0 - 3.4 
elif PyVer(3,4,'>'): 
    from importlib import reload # Python 3.5+

def GlobalEnv(): # Get my parent's globals()
    return dict(getmembers(stack()[1][0]))["f_globals"]

def Install(module,install_account='',mode=None,upgrade=False,version=None,force=False,pkg_map=None,err=False):
    # version 
    #  - same : ==1.0.0
    #  - big  : >1.0.0
    #  - or   : >=1.3.0,<1.4.0
    # pip module)
    #pip_main=None
    #if hasattr(pip,'main'):
    #    pip_main=pip.main
    #elif hasattr(pip,'_internal'):
    #    pip_main=pip._internal.main
    if pkg_map is None:
        pkg_map={
           'magic':'python-magic',
           'bdist_wheel':'wheel',
        }

    pip_main=check_call
    if not pip_main:
        print('!! PIP module not found')
        return False

    pkg_name=module.split('.')[0]
    install_name=pkg_map.get(pkg_name,pkg_name)
    # Check installed package
    # pip module)
    #install_cmd=['install']
    if os_path.basename(executable).startswith('python'):
        install_cmd=[executable,'-m','pip','install']
    else:
        install_cmd=['python3','-m','pip','install']
    ipkgs=working_set
    pkn=ipkgs.__dict__.get('by_key',{}).get(install_name)
    if pkn:
        if version:
            chk_ver=version.replace('>',' ').replace('=',' ').replace('<',' ').split()
            if ('>=' in version and LooseVersion(pkn.version) < LooseVersion(chk_ver[-1])) or ('==' in version and LooseVersion(pkn.version) != LooseVersion(chk_ver[-1])) or ('<=' in version and LooseVersion(pkn.version) > LooseVersion(chk_ver[-1])) or ('>' in version and LooseVersion(pkn.version) <= LooseVersion(chk_ver[-1])) or ('<' in version and LooseVersion(pkn.version) >= LooseVersion(chk_ver[-1])):
                upgrade=True
                install_cmd.append(install_name+version)
            else:
                return True
        else:
            install_cmd.append(install_name)
        if force: install_cmd.append('--force-reinstall')
        if install_account: install_cmd.append(install_account)
        if not force and upgrade: install_cmd.append('--upgrade')
        if pip_main and force or upgrade:
            if err:
                if pip_main(install_cmd) == 0: return True
                return False
            else:
                try:
                    if pip_main(install_cmd) == 0: return True
                    return False
                except:
                    return False
        return True

#    if mode == 'git':
#        git.Repo.clone_from(module,'/tmp/.git.tmp',branch='master')
#        build the source and install
#        return True

    if version:
        install_cmd.append(install_name+version)
    else:
        install_cmd.append(install_name)
    if force: install_cmd.append('--force-reinstall')
    if install_account: install_cmd.append(install_account)

    if err:
        if pip_main(install_cmd) == 0: return True
    else:
        try:
            if pip_main(install_cmd) == 0: return True
        except:
            pass
    return False


def ModLoad(inp,force=False,globalenv=dict(getmembers(stack()[1][0]))["f_globals"],unload=False,re_load=False):
    def Reload(name):
        if isinstance(name,str):
            globalenv[name]=reload(globalenv[name])
        else:
            name=reload(name)
        return True

    def Unload(name):
        if isinstance(name,str):
            del globalenv[name]
        elif isinstance(name,type(inspect)):
            try:
                nname = name.__spec__.name
            except AttributeError:
                nname = name.__name__
            if nname in globalenv: del globalenv[nname]

    if not inp: return 0,''
    inp_a=inp.split()
    wildcard=None
    class_name=None
    if inp_a[0] in ['from','import']:
        del inp_a[0]
    name=inp_a[-1]
    module=inp_a[0]
    if unload:
        if '*' not in inp and name in globalenv: # already loaded
            Unload(name) #Unload
        return 2,module #Not loaded

#    import inspect,sys
#    print(inspect.stack())
#    dep=len(inspect.stack())-1
#    fname=sys._getframe(dep).f_code.co_name
#    if fname == '_bootstrap_inner' or name == '_run_code':
#        fname=sys._getframe(2).f_code.co_name
#    print('>>',fname,':::',name,class_name,module)
    if '*' not in inp and name in globalenv: # already loaded
        if re_load:
            Reload(name) # if force then reload
            return 0,module
        elif force:
            Unload(name) #if force then unload and load again
    if 'import' in inp_a:
        import_idx=inp_a.index('import')
        if len(inp_a) > import_idx+1:
            class_name=inp_a[import_idx+1]
        else:
            print('*** Wrong information')
            return 0,module
    try:
        if class_name:
            if class_name == '*':
                wildcard=import_module(module)
            else:
                try:
                    globalenv[name]=getattr(import_module(module),class_name)
                except:
                    globalenv[name]=import_module('{}.{}'.format(module,class_name))
        else:
            globalenv[name]=import_module(module)
        return wildcard,module # Loaded. So return wildcard information
    except AttributeError: # Try Loading looped Module/Class then ignore  or Wrong define
        return 0,module
    except ImportError: # Import error then try install
        return 1,module

def Import(*inps,**opts):
    '''
    inps has "require <require file>" then install the all require files in <require file>
    '''
    globalenv=opts.get('globalenv',dict(getmembers(stack()[1][0]))["f_globals"]) # Get my parent's globals()
    force=opts.get('force',None) # unload and load again when already loaded (force=True)
    re_load=opts.get('reload',None) #  run reload when already loaded
    unload=opts.get('unload',False) # unload module when True
    err=opts.get('err',False) # show install or loading error when True
    default=opts.get('default',False)
    dbg=opts.get('dbg',False) # show comment when True
    #install_account=opts.get('install_account','--user')
    install_account=opts.get('install_account','') # '--user','user','myaccount','account',myself then install at my local account

    #Append Module Path
    base_lib_path=['/usr/lib/python3.6/site-packages','/usr/lib64/python3.6/site-packages','/usr/local/python3.6/site-packages','/usr/local/lib/python3.6/site-packages','/usr/local/lib64/python3.6/site-packages']
    path=opts.get('path') # if the module file in a special path then define path
    if isinstance(path,str):
        if ',' in path:
            base_lib_path=base_lib_path+path.split(',')
        elif ':' in path:
            base_lib_path=base_lib_path+path.split(':')
    elif isinstance(path,(list,tuple)):
        base_lib_path=base_lib_path+list(path)
    home=str(Path.home())
    if isinstance(home,str):
        base_lib_path.append('{}/.local/lib/python3.6/site-packages'.format(home))
    for ii in base_lib_path:
        if os_path.isdir(ii) and not ii in mod_path:
            mod_path.append(ii)

    if install_account in ['user','--user','personal','myaccount','account','myself']:
        install_account='--user'
    else:
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
        if len(inp_a) ==2 and inp_a[0] in ['require','requirement']:
            if os_path.isfile(inp_a[1]):
                rq=[]
                with open(inp_a[1]) as f:
                    rq=f.read().split('\n')
                for ii in rq:
                    if not ii: continue
                    ii_l=ii.split()
                    version=None
                    if len(ii_l) in [2,3]:
                        if '=' in ii_l[1] or '>' in ii_l[1] or '<' in ii_l[1]:
                            if len(ii_l) == 3:
                                version=ii_l[1]+ii_l[2]
                            else:
                                version=ii_l[1]
                    ii_a=ii_l[0].split(':')
                    if len(ii_a) == 2:
                        ic=Install(ii_a[1],install_account,version=version)
                    else:
                        ic=Install(ii_a[0],install_account,version=version)
                    if ic:
                        loaded,module=ModLoad(ii_a[0],force=force,globalenv=globalenv,re_load=re_load)
            continue
        loaded,module=ModLoad(inp,force=force,globalenv=globalenv,unload=unload,re_load=re_load)
        if loaded == 2: #unloaded
            continue
        if loaded == 1:
            if Install(module,install_account):
                loaded,module=ModLoad(inp,force=force,globalenv=globalenv,re_load=re_load)
            else:
                if dbg:
                    print('*** Import Error or Need install with SUDO or ROOT or --user permission')
                continue
        if loaded not in [None,0,1]: # import wildcard
            for ii in loaded.__dict__.keys():
                if ii not in ['__name__','__doc__','__package__','__loader__','__spec__','__file__','__cached__','__builtins__']:
                    if ii in globalenv:
                        # swap Same Name between module(my module of the wild card) and class(wild card import class name)
                        if ii in loaded.__dict__.keys():
                            if CheckObj(globalenv[ii]) == 'module' and CheckObj(loaded.__dict__[ii]) == 'classobj':
#                                TMP=globalenv[ii] # move to local temporay 
                                globalenv[ii]=loaded.__dict__[ii]
                                continue
                        if not force: continue # Not force then ignore same name
                    globalenv[ii]=loaded.__dict__[ii]
