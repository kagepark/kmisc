#Kage Park

import pprint
import pickle
import sys
import os

def peeling(v,ignore=[],collect=[],jump=None):
  if isinstance(v,dict):
    v=v.copy()
    if jump is not None:
      if jump in v:
         v=v[jump]
    if isinstance(v,dict):
      rc={}
      for k in v:
        if k not in ignore or k in collect:
          if isinstance(v[k],dict) and jump is not None and jump in v[k]:
            vv=v[k][jump]
          else:
            vv=v[k]
          if isinstance(vv,dict):
            rr=peeling(vv,ignore=ignore,jump=jump)
            rc[k]=rr
          else:
            rc[k]=vv
      return rc

  if isinstance(v,dict) and jump and jump in v:
      if isinstance(v[jump],dict):
          rr=peeling(v[jump],ignore=ignore,jump=jump)
          return rr
      return v[jump]
  else:
      return v

class DICT(dict):
    MARKER = {}
    _p_='._p'
    _d_='._d'
    _n_=False # True: Notice to Standard error output
    _dfile_=None

    def __init__(self, value=None):
        if value is None:
            pass
        elif isinstance(value, dict):
            for key in value:
                self.__setitem__(key, value[key])
        else:
            raise TypeError('expected dict')

    # moving step by step with dot('.') keys
    def __getitem__(self, key):
#        try:
#            found = dict.__getitem__(self,key)
#            # not dict value change to Dict value for ignore error
#            if not isinstance(found,dict): 
#                found=Dict({self._d_:found}) # Fake for ignore error only 
#                # Updated Dictionary with Dict
#    #            new_found=Dict({self._d_:found})
#    #            super(Dict, self).__setitem__(key, new_found)
#    #            found = dict.__getitem__(self,key)
#            print('__getitem__ found:',found)
#        except:
#            found=Dict.MARKER
#            print('__getitem__ except found:',found)
        found=self.get(key,DICT.MARKER) # same as above code
        if not isinstance(found,dict):
            found=DICT({self._d_:found})
        if found is DICT.MARKER:
            found = DICT() # make a fake data for ignore error at Get(),Put(),.... 
            # Really Generate A.B.C. .... new items
#            print('__getitem__ generate new:',found)
#            super(DICT, self).__setitem__(key, found)

# Property setting issue
        # If the data is not Dict type data then convert the data to Dict type
        # for example: root.abc.test=[1,2,3] => root.abc.Put('test',[1,2,3])

        #    new_found=Dict({self._d_:found}) # Remove property. because, can known that is fake data or not in the call function.
#            new_found=Dict({self._d_:found, self._p_:{}})
#            super(Dict, self).__setitem__(key,new_found) # If you want change original data then enable
        #    return new_found # it just reutn fake data for ignore error for Get() when the data is not Dict type data.
        return found

    # Generate new dict key with data(value)
    def __setitem__(self, key, value):
        found=self.get(key,None)
        if self._is_ro(found,key=key):
            return False
        if isinstance(found,dict) and self._p_ in found:
            if isinstance(value, dict) and self._d_ in value:
                found[self._d_]=value[self._d_]
            else:
                found[self._d_]=value
            super(DICT, self).__setitem__(key, found)
        else:
            if isinstance(value, dict) and not isinstance(value, DICT):
                value = DICT(value)
            super(DICT, self).__setitem__(key, value)

    # del dictionary[key]
    def __delitem__(self, key, default=False):
        if self._is_ro(self.get(key,None),key=key):
            return default
        if key in self:
            super(DICT, self).__delitem__(key) # delete data
            return True
        else:
            return default

    # readonly property check
    def _is_ro(self,found,key=None):
        if isinstance(found, dict):
            if key and key in found:
                found=found[key]
            if self._p_ in found and 'readonly' in found[self._p_] and found[self._p_]['readonly']:
                if 'force' in found[self._p_]:
                    found[self._p_].__delitem__('force')
                    return False
                if self._n_:
                    if key:
                        sys.stderr.write('item({}) is readonly\n'.format(key))
                    else:
                        sys.stderr.write('item is readonly\n')
                    sys.stderr.flush()
                return True
        return False

        
    def Proper(self, key=None, value=None):
        if value is not None and key is not None:
            if self._p_ in self:
                self[self._p_][key]=value
                nvalue=self[self._p_]
                super(DICT, self).__setitem__(self._p_,nvalue)
            else:
                #nvalue={key:value}
                if self._n_:
                    sys.stderr.write('the item have no property. if you need property then change the data to Dict type\n')
                    sys.stderr.flush()
                return False
            super(DICT, self).__setitem__(self._p_,nvalue)
            return True
        elif key is not None:
            if self._p_ in self:
                if key in self[self._p_]:
                    return self[self._p_][key]
            return None
        else:
            if self._p_ in self:
                return self[self._p_]
            else:
                return None


    def Get(self,key=None,default=None,raw=False,path=None,symbol='.'):
        try:
            if path:
                self=self.Cd(path,symbol=symbol,default=default)
            if not self or self == default:
                return default
            if key is None:
                if raw:
                    return peeling(self)
                return peeling(self,ignore=[self._p_],jump=self._d_)
            else:
                # Add read method for dictionary or self._d_ value
                if self._d_ in self and key in self[self._d_]:
                    found=dict.__getitem__(self[self._d_],key)
                elif key in self:
                    found=self[key]
                else:
                    #original code
                    found=dict.__getitem__(self,key)
                if not found:
                    return default
                if isinstance(found,dict):
                    if raw:
                        return peeling(found)
                    return peeling(found,ignore=[self._p_],jump=self._d_)
                return found
        except:
            return default

    def Check(self,value,idx=0):
        try:
            found=peeling(self,ignore=[self._p_],jump=self._d_)
            type_found=type(found)
            if type_found in [list,tuple]:
                if idx in [None,False,'all','any','*']:
                    if value in found:
                        return True
                else:
                    if value == found[idx]:
                        return True
            elif type_found in [dict]:
                if value in found:
                    return True
            else:
                if value == found:
                    return True
        except:
            pass
        return False

    # Good
    def Put(self,key,value,proper={},force=False,new=False,path=None,symbol='.',default=False):
#        if value is None:
#            return
        if path:
            self=self.Cd(path,force=True,symbol=symbol,default=default)
        if key is None or self == default:
            return default
        if new:
            if self.__getitem__(key):
                return default
        if force:
            self.__getitem__(key).Proper('force',True)
        if proper == {}:
            self.__setitem__(key, value)
        else:
            self.__setitem__(key, {self._d_:value,self._p_:proper})
        return True

    # Good proper issue
    def Update(self,data,force=False,path=None,symbol='.',default=False):
        if path:
            self=self.Cd(path,force=True,symbol=symbol)
        if not isinstance(data,dict) or self == default:
            return default
        if force is False and isinstance(data,dict):
            for ii in data:
                if self._is_ro(self,ii):
                    return default
        if isinstance(self,dict) and self._d_ in self:
            self[self._d_].update(data)
        else:
            super(DICT, self).update(data)
        return True

    # Good dictionary.pop(key)
    def Pop(self,key,force=False,default=False):
        if force:
            self.__getitem__(key).Proper('force',True)
        found = self.Get(key, default=None)
        rc=self.__delitem__(key,default=default) # delete data with __delitem() in this class
        if rc:
            return found
        return rc

    # Good
    def Del(self,key,force=False,default=False):
        #if self._is_ro(self.__getitem__(key),key=key):
        #    return False
        #super(DICT, self).__delitem__(key) # delete data without __delitem() in this class
        if force:
            self.__getitem__(key).Proper('force',True)
        return self.__delitem__(key,default=default) # delete data with __delitem() in this class

    # moving key step by step with path by seperated symbol 
    def Cd(self,path,force=False,symbol='/',default_path='_',default=False): #force=True, generate new key
        if isinstance(path,str):
            path=path.split(symbol)
        if isinstance(path,list):
            for p in path:
                if self._d_ in self:
                    self=self[self._d_]
                if p in self:
                    self=self[p]
                elif force:
                    super(DICT, self).__setitem__(p, DICT())
                    self=self[p]
                else:
                    if default_path=='_':
                        return DICT()
                    return default_path
            return self
        return default

    # generate new key
    def Mk(self,path,symbol='.'):
        return self.Cd(path,force=True,symbol=symbol)

    def Find(self,find,proper=None,mode='value'):
        path=[]
        if proper:
            dep=self._p_
        else:
            dep=self._d_
        if isinstance(self,dict):
            for key in self:
                if mode in ['key','*','all']: # find in key only
                    if find == key:
                        path.append(key)
                found=self.get(key,None)
                if isinstance(found,dict):
                    if dep in found:
                         if mode in ['value','*','all'] and (find == found[dep] or (type(found[dep]) in [DICT,dict,list,tuple] and find in found[dep]) or (type(find) is str and type(found[dep]) is str and find in found[dep])): # find in 'find' only
                              # Proper find
                              if proper:
                                  if found[dep][find] == proper:
                                      path.append(key)
                              else:
                              # Value find
                                  path.append(key)
                         elif isinstance(found[dep], dict): # recursing
                              found[dep].Find(find,proper=proper,mode=mode)
                    else:
                         if mode in ['value','*','all'] and find == found or (type(found) in [list,tuple] and find in found) or (type(find) is str and type(found) is str and find in found):
                             path.append(key)
                         else:
                             for kk in self[key].Find(find,proper=proper,mode=mode): # recursing
                                 path.append(key+'/'+kk)
                else:
                    if mode in ['value','*','all'] and find == found or (type(found) in [list,tuple] and find in found) or (type(find) is str and type(found) is str and find in found):
                        path.append(key)
        return path

    def Diff(self,oo,proper=False):
        if proper:
            diff1=self.copy()
            diff2=oo.copy()
        else:
            diff1=peeling(self.copy(),ignore=[self._p_],jump=self._d_)
            diff2=peeling(oo.copy(),ignore=[self._p_],jump=self._d_)
        if diff1 == diff2:
            return True
        else:
            return False

    def Keys(self):
        if isinstance(self,dict) and self._p_ in self:
            mm=self.keys()
            mm.remove(self._p_)
            return mm
        return self.keys()

    def List(self,keys=[]):
        rc=[]
        for ii in keys:
            if ii in self:
                rc.append(peeling(self[ii],ignore=[self._p_],jump=self._d_))
        return rc

    def Len(self,default=False):
        if isinstance(self,dict):
            if self._p_ in self:
                return len(self)-1
            return len(self)
        return default

    def Print(self,whole=False):
        if whole:
            pprint.pprint(self)
        else:
            pprint.pprint(self.Get())

    def Save(self,default=False):
        if self._dfile_ :
            with open(self._dfile_,'wb') as dd:
                pickle.dump(peeling(self),dd,protocol=2)
                return True
        return default

    def Load(self,default=False):
        if self._dfile_ and os.path.isfile(self._dfile_):
            with open(self._dfile_,'rb') as dd:
                try:
                    mm=pickle.load(dd)
                except:
                    return
                self.__init__(mm)
                return True
        return default

    def Sort(self,base='key',reverse=False,func=None,order=None):
        lst=[]
        if base == 'key':
            lst=list(self.keys())
            if order in [int,'int','digit','number']:
                def _cint_(e):
                    try:
                        return int(e)
                    except:
                        return e
                return lst.sort(reverse=reverse,key=_cint_)
            elif order in [str,'str']:
                def _cint_(e):
                    return '''{}'''.format(e)
                return lst.sort(reverse=reverse,key=_cint_)
            else:
                return lst.sort(reverse=reverse,func=func)
        elif base == 'value':
            lst=self.items()
            if order in [int,'int','digit','number']:
                def _cint_(e):
                    try:
                        return int(e[1])
                    except:
                        return e[1]
                lst.sort(reverse=reverse,key=_cint_)
            elif order in [str,'str']:
                def _cint_(e):
                    return '''{}'''.format(e[1])
                lst.sort(reverse=reverse,key=_cint_)
            else:
                lst.sort(reverse=reverse,func=func)
            return [i[0] for i in lst]

    def FirstKey(self):
        return next(iter(self))

    __setattr__, __getattr__ = __setitem__, __getitem__

#OLD Command Support
class kDict(dict):
    def __init__(self,value=None):
        self.kDict=DICT(value)

    def PROPER(self, key=None, value=None):
        return self.kDict.Proper(key=key,value=value)

    def GET(self,key=None,default=None,raw=False,path=None,symbol='.'):
        return self.kDict.Get(key=key,default=default,raw=raw,path=path,symbol=symbol)

    def CHECK(self,value,idx=0):
        return self.kDict.Check(value,idx=idx)

    def PUT(self,key,value,proper={},force=False,new=False,path=None,symbol='.',default=False):
        return self.kDict.Put(key,value,proper=proper,force=force,new=new,path=path,symbol=symbol,default=default)

    def UPDATE(self,data,force=False,path=None,symbol='.',default=False):
        return self.kDict.Update(data,force=force,path=path,symbol=symbol,default=default)

    def POP(self,key,force=False,default=False):
        return self.kDict.Pop(key,force=force,default=default)

    def DEL(self,key,force=False,default=False):
        return self.kDict.Del(key,force=force,default=default)

    def CD(self,path,force=False,symbol='/',default_path='_',default=False):
        return self.kDict.Cd(path,force=force,symbol=symbol,default_path=default_path,default=default)

    def MK(self,path,symbol='.'):
        return self.kDict.Mk(path,symbol=symbol)

    def FIND(self,value,proper=None,mode='value'):
        return self.kDict.Find(value,proper=proper,mode=mode)

    def DIFF(self,oo,proper=False):
        return self.kDict.Diff(oo,proper=proper)

    def KEYS(self):
        return self.kDict.Keys()

    def LIST(self,keys=[]):
        return self.kDict.List(keys=keys)

    def LEN(self,default=False):
        return self.kDict.Len(default=default)

    def PRINT(self,whole=False):
        return self.kDict.Print(whole=whole)

    def SAVE(self,default=False):
        return self.kDict.Save(default=default)

    def LOAD(self,default=False):
        return self.kDict.Load(default=default)

