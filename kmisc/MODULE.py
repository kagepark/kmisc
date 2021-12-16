#Kage Park
import inspect
from sys import modules
from sys import path as mod_path
from sys import version_info
import importlib
import pip

Py2=False
Py3=False
if version_info[0] < 3: # Python 2 has built in reload
    Py2=True
elif version_info[0] == 3 and version_info[1] <= 4:
    Py3=True
    from imp import reload # Python 3.0 - 3.4 
else:
    Py3=True
    from importlib import reload # Python 3.5+

class MODULE:
    def __init__(self,path=None):
        self.src=dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"] # Get my parent's globals()
        if isinstance(path,str):
            for ii in path.split(','):
                mod_path.append(ii)

    def AppendPath(self,*inp):
        for pp in inp:
            if isinstance(pp,str):
                for ii in pp.split(','):
                    mod_path.append(ii)

    def Loaded(self,name):
        if type(name).__name__ == 'module':
            name=name.__name__
        if isinstance(name,str):
            if name in self.src:
                return True
        return False

    def Reload(self,name):
        if self.Loaded(name):
            if isinstance(name,str):
                modules[name]=reload(modules[name])
            else:
                name=reload(name)
            return True
        return False

    def Unload(self,name):
        if self.Loaded(name):
            if isinstance(name,str):
                del self.src[name]
                if name in modules:
                    del modules[name]
            elif isinstance(name,type(inspect)):
                try:
                    nname = name.__spec__.name
                except AttributeError:
                    nname = name.__name__
                del self.src[nname]
                if nname in modules:
                    del modules[nname]

    #try:
    #    name = module.__spec__.name
    #except AttributeError:
    #    name = module.__name__
    def Import(self,*inps,**opts):
        force=opts.get('force',None)
        err=opts.get('err',False)
        default=opts.get('default',False)
        dbg=opts.get('dbg',False)
        install_account=opts.get('install_account','--user')
        if install_account in ['root','all','*','global','system','os']:
            install_account=''
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
            if '*' not in inp and name in self.src: # already loaded
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
                        self.src[name]=getattr(importlib.import_module(module),class_name)
                    else:
                        self.src[name]=importlib.import_module(module)
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
                else:
                    install_name='{}'.format(module.split('.')[0])
                if pip_main and pip_main(['install',install_name,install_account]) == 0:
                #if pip_main and pip_main(['install',install_name]) == 0:
                    if class_name == '*':
                        wildcard=importlib.import_module(module)
                    else:
                        if classm:
                            self.src[name]=getattr(importlib.import_module(module),name)
                        else:
                            self.src[name]=importlib.import_module(module)
                else:
                    if dbg:
                        print('*** Import Error or Need install with SUDO or ROOT or --user permission')
                    continue
            if wildcard: # import wildcard
                for ii in wildcard.__dict__.keys():
                    if ii not in ['__name__','__doc__','__package__','__loader__','__spec__','__file__','__cached__','__builtins__']:
                        if ii in self.src:
                            # swap Same Name between module(my module of the wild card) and class(wild card import class name)
                            if ii in wildcard.__dict__.keys():
                                if type(self.src[ii]).__name__ == 'module' and type(wildcard.__dict__[ii]).__name__ == 'classobj':
#                                    TMP=self.src[ii] # move to local temporay 
                                    self.src[ii]=wildcard.__dict__[ii]
                                    continue
                            if not force: continue # Not force then ignore same name
                        self.src[ii]=wildcard.__dict__[ii]

    def Load(self,*inps,**opts):
        self.Import(*inps,**opts)

    def List(self):
        return list(self.src.keys())

    def Dict(self):
        return self.src
