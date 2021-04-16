#Kage Park
# Base size 6.4MB
# pip module size : 21MB
from distutils.version import LooseVersion
from inspect import getmembers, stack
from sys import version_info, executable
from os import path
from importlib import import_module
from pkg_resources import working_set
#import pip
from subprocess import check_call
#import git


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

def Install(module,install_account='',mode=None,upgrade=False,version=None,force=False,pkg_map=None):
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

    pkg_name=module.split('.')[0]
    install_name=pkg_map.get(pkg_name,pkg_name)
    # Check installed package
    ipkgs=working_set
    pkn=ipkgs.__dict__.get('by_key',{}).get(install_name)
    # pip module)
    #install_cmd=['install']
    install_cmd=[executable,'-m','pip','install']
    if pkn:
        if pip_main:
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
            if upgrade is True: pip_main(install_cmd)
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

    if pip_main and pip_main(install_cmd) == 0: return True
    return False


def ModLoad(inp,force=False,globalenv=dict(getmembers(stack()[1][0]))["f_globals"]):
    def Reload(name):
        if isinstance(name,str):
            globalenv[name]=reload(globalenv[name])
        else:
            name=reload(name)
        return True

    if not inp: return 0,''
    inp_a=inp.split()
    wildcard=None
    class_name=None
    if inp_a[0] in ['from','import']:
        del inp_a[0]
    name=inp_a[-1]
    module=inp_a[0]
    if '*' not in inp and name in globalenv: # already loaded
        if force: Reload(name) # if force then reload
        return 0,module
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
    globalenv=dict(getmembers(stack()[1][0]))["f_globals"] # Get my parent's globals()
    force=opts.get('force',None)
    err=opts.get('err',False)
    default=opts.get('default',False)
    dbg=opts.get('dbg',False)
    install_account=opts.get('install_account','--user')
    if install_account in ['user','--user']:
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
        if inp_a[0] in ['require','requirement']:
            if path.isfile(inp_a[1]):
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
                        loaded,module=ModLoad(ii_a[0],force=force,globalenv=globalenv)
            continue
        loaded,module=ModLoad(inp,force=force,globalenv=globalenv)
        if loaded == 1:
            if Install(module,install_account):
                loaded,module=ModLoad(inp,force=force,globalenv=globalenv)
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
