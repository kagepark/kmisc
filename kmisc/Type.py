#Kage Park
"""
Based on Python2.7 and Python3.x's types module
Inhance for make sure
"""
import sys,os
from klib.MODULE import *
MODULE().Import('magic')

def ObjName(obj,default=None):
    if isinstance(obj,str):
        if os.path.isfile(obj):
            aa=magic.from_buffer(open(obj,'rb').read(2048))
            if aa: return aa.split()[0].lower()
            try:
                with open(obj,'rb') as f: # Pickle Type
                    pickle.load(f)
                    return 'pickle'
            except:
                pass
        return 'str'
    else:
        obj_dir=dir(obj)
        obj_name=type(obj).__name__
        if obj_name in ['function']: return obj_name
        if '__dict__' in obj_dir:
            if obj_name == 'type': return 'classobj'
            return 'instance'
#        elif obj_name == 'type':
#            return obj.__name__
        return obj_name.lower() # Object Name
    return default

#def TypeFixer(name,default=None):
def TypeFixer(obj,default='unknown'):
    if obj == default: return default
    if isinstance(obj,str): 
        name=obj.lower()
    else: 
        name=ObjName(obj).lower()
    # Fix short word to correct name
    if name in ['none']: return 'nonetype'
    if name in ['byte']: return 'bytes'
    if name in ['obj']: return 'object'
    if name in ['func','unboundmethod']: return 'function'
    if name in ['class']: return 'classobj'
    if name in ['yield']: return 'generator'
    if name in ['builtinfunction','builtinmethod','builtin_function_or_method']: return 'builtin_function_or_method'
    # function: function and instance's function in Python3
    # method:  class's function in Python3
    # instancemethod: instance's and class's function in Python2
    if name in ['method','classfunction','instancemethod','unboundmethod']: return 'method' # function in the class
    # it changed name between python versions, so return both name for this name
    if name in ['dictproxy','mappingproxy']: return ['dictproxy','mappingproxy'] # function in the class
    # Fix python version for long
    if name in ['long']:
        if sys.version_info[0] < 3: return name
        return 'int'
    # return original name
    return name

def Type(*inp,**opts):
    '''
       instance: <class name>()
       classobj : <class name>
       function : <func name>
       return value: <func name>()
       method   : <class name>().<func name>
    '''
    inpn=len(inp)
    default=opts.get('default','unknown')
    if inpn == 0: return default
    obj=inp[0]
    if inpn == 1: return TypeFixer(obj,default=default)
    chk_type=[]
    for name in inp[1:]:
        if not isinstance(name,(tuple,list)): name=[name]
        for ii in name:
            a=TypeFixer(TypeFixer(ii,default=default),default=default)
            if a == default: continue
            if isinstance(a,list): 
                chk_type=chk_type+a
            elif a not in chk_type:
                chk_type.append(a)
    if chk_type: 
        obj_type=ObjName(obj)
#        print('    ::',obj_type,'  in  ',chk_type)
        if obj_type == default: return default
        if obj_type == 'instance':
            if 'int' in chk_type: 
                if isinstance(obj,int): return True
            elif 'dict' in chk_type:
                if isinstance(obj,dict): return True
            elif 'list' in chk_type:
                if isinstance(obj,list): return True
            elif 'tuple' in chk_type:
                if isinstance(obj,tuple): return True
            elif 'float' in chk_type:
                if isinstance(obj,float): return True
        if obj_type in chk_type: return True
    return False

if __name__ == "__main__":
    print('* None:',TypeFixer(None),type(None))
    print(" TypeFixer('none'):", TypeFixer('none'))
    print(" Type(None,'none'):", Type(None,'none'))
    print('* type:',TypeFixer(type),type(type))
    print(" TypeFixer('type'):", TypeFixer('type'))
    print(" Type(type,'type'):", Type(type,'type'))
    print(" Type(type,'class'):", Type(type,'class'))
    print(" Type(int,'type'):", Type(int,'type'))
    print(" Type(list,'type'):", Type(list,'type'))
    print(" Type(tuple,'type'):", Type(tuple,'type'))
    print(" Type(dict,'type'):", Type(dict,'type'))
    print(" Type(str,'type'):", Type(str,'type'))
    print(" Type(object,'type'):", Type(object,'type'))
    print('* object:',TypeFixer(object),type(object))
    print('* int:',TypeFixer(int),type(int))
    print(" Type(1,'int'):", Type(1,'int'))
    print(" Type(1.1,'int'):", Type(1.1,'int'))
    print(" Type('1','int'):", Type('1','int'))
    if sys.version_info[0] < 3:
        print('* long:',TypeFixer(long),type(long))
        print(" Type(100000000000000,'long'):", Type(100000000000000,'long'))
        print(" Type(10,'long'):", Type(10,'long'))
        print(" Type(10.1,'long'):", Type(10.1,'long'))
    print('* float:',TypeFixer(float),type(float))
    print(" Type(1.1,'float'):", Type(1.1,'float'))
    print(" Type(1,'float'):", Type(1,'float'))
    print('* bool:',TypeFixer(bool),type(bool))
    print(" Type(True,'bool'):", Type(True,'bool'))
    print(" Type(False,'bool'):", Type(False,'bool'))
    print(" Type(0,'bool'):", Type(0,'bool'))
    print(" Type(1,'bool'):", Type(1,'bool'))
    print(" Type(3,'bool'):", Type(3,'bool'))
    print('* str:',TypeFixer(str),type(str))
    print(" Type('1','str'):", Type('1','str'))
    print(" Type('a','str'):", Type('a','str'))
    print(" Type(1,'str'):", Type(1,'str'))
    if sys.version_info[0] < 3:
        print('* unicode:',TypeFixer(unicode),type(unicode))
        print(" Type(unicode('3'),'unicode'):", Type(unicode('3'),'unicode'))
        print(" Type(bytes('3','utf-8'),'unicode'):", Type(bytes('3'),'unicode'))
    print('* bytes:',TypeFixer(bytes),type(bytes))
    if sys.version_info[0] < 3:
        print(" Type(bytes('3'),'bytes'):", Type(bytes('3'),'bytes'))
        print(" Type('3','bytes'):", Type('3','bytes'))
        print(" Type(3,'bytes'):", Type(3,'bytes'))
    else:
        print(" Type(bytes('3','utf-8'),'bytes'):", Type(bytes('3','utf-8'),'bytes'))
        print(" Type('3','bytes'):", Type('3','bytes'))
        print(" Type(3,'bytes'):", Type(3,'bytes'))
    print('* tuple:',TypeFixer(tuple),type(tuple))
    print(" Type((1,2,3),'tuple'):", Type((1,2,3),'tuple'))
    print(" Type([1,2,3],'tuple'):", Type([1,2,3],'tuple'))
    print('* list:',TypeFixer(list),type(list))
    print(" Type([1,2,3],'list'):", Type([1,2,3],'list'))
    print(" Type((1,2,3),'list'):", Type((1,2,3),'list'))
    print('* dict:',TypeFixer(dict),type(dict))
    print(" Type({1:2},'dict'):", Type({1:2},'dict'))
    print(" Type({1},'dict'):", Type({1},'dict'))
    print('* set:',TypeFixer(set),type(set))
    print(" Type({1},'set'):", Type({1},'set'))
    print(" Type({1:2},'set'):", Type({1:2},'set'))
    def _F(): pass
    print('* function:',TypeFixer(_F),type(_F))
    print(" Type(_F,'function'):", Type(_F,'function'))
    print('* lambda:',TypeFixer(lambda: None))
    print(" Type(lambda:None,'function'):", Type(lambda:None,'function'))

    if sys.version_info[0] < 3:
        print('* code v2:',TypeFixer(_F.func_code),type(_F.func_code)) #v2
    else:
        print('* code v3:',TypeFixer(_F.__code__),type(_F.__code__)) #v3
    def _Y(): 
        yield 1
    print('* generator for yield:',TypeFixer(_Y()),type(_Y()))
    print(" _Y() return yield 1: Type(_Y(),'yield'):", Type(_Y(),'yield'))
    class _C:   # basic class
        def _M(self): pass
    print('-----------------------')
    print(' class _C:')
    print('    def _M(self): pass')
    print('-----------------------')
    print('* class: ',TypeFixer(_C),type(_C))
    print(" Type(_C,'class'):", Type(_C,'class'))
    print(" Type(_C,'dict'):", Type(_C,'dict'))
    print('* instance: ',TypeFixer(_C()),type(_C()))
    print(" Type(_C(),'instance'):", Type(_C(),'instance'))
    print(" Type(_C(),'dict'):", Type(_C(),'dict'))
    print('* unboundMethod:',TypeFixer(_C._M),type(_C._M))
    print(" Type(_C._M,'unboundmethod'):", Type(_C._M,'unboundmethod'))
    print('* method:',TypeFixer(_C()._M),type(_C()._M))
    print(" Type(_C()._M,'method'):", Type(_C()._M,'method'))
    class _D(dict): # inheritance class
        def _H(self): pass
    print('-----------------------')
    print(' class _D(dict):')
    print('    def _H(self): pass')
    print('-----------------------')
    print('* class-dict:',TypeFixer(_D),type(_D))
    print(" Type(_D,'class'):", Type(_D,'class'))
    print(" Type(_D,'dict'):", Type(_D,'dict'))
    print('* instance: ',TypeFixer(_D()),type(_D()))
    print(" Type(_D(),'instance'):", Type(_D(),'instance'))
    print(" Type(_D(),'dict'):", Type(_D(),'dict'))
    print('* unboundMethod:',TypeFixer(_D._H),type(_D._H))
    print(" Type(_D._H,'function'):", Type(_D._H,'function'))
    print(" Type(_D._H,'unboundmethod'):", Type(_D._H,'unboundmethod'))
    print('* method:',TypeFixer(_D()._H),type(_D()._H))
    print(" Type(_D()._H,'method'):", Type(_D()._H,'method'))

    print('* builtinfunction:',TypeFixer(len),type(len))
    print(" Type(len,'builtinfunction'):", Type(len,'builtinfunction'))

    print('* builtinmethod:',TypeFixer([].append),type([].append))
    print(" Type([].append,'builtinmethod'):", Type([].append,'builtinmethod'))

    print('* module:',TypeFixer(os),type(os))
    print('* slice:',TypeFixer(slice),type(slice))
    print('* ellipsis:',TypeFixer(Ellipsis),type(Ellipsis))
    print('* dictproxy:',TypeFixer(type.__dict__),type(type.__dict__))
    print('* notimplemented:',TypeFixer(NotImplemented),type(NotImplemented))

    if sys.version_info[0] < 3:
        print('* getsetdescriptor v2:',TypeFixer(_F.func_code),type(_F.func_code))
        print('* memberdescriptor v2:',TypeFixer(_F.func_globals),type(_F.func_globals))
    else:
        print('* getsetdescriptor v3:',TypeFixer(_F.__code__),type(_F.__code__))
        print('* memberdescriptor v3:',TypeFixer(_F.__globals__),type(_F.__globals__))

