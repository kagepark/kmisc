Open Kage's useful tools and class to public.
(Long time used and upgraded)
But, this is develope version.
So, suddenly it will be big change when I got some more good idea.
I re-groupped to library.
and change name to klib

# Install
```javascript
pip3 install kmisc
```
# Custom Dictionary Class

Convert Dictionary to Object style Dictionary
## Contents
1. Create tree type items 
1. Added New commands
   1. Put()    : Put value at a item
   1. Get()    : Get value of item
   1. Del()    : Delete item
   1. Update() : Update value at item
   1. Print()  : Print dictionary 
   1. Diff()   : Compare two dictionary
   1. Check()  : Check put the value is same as the item(key)'s value
   1. List()   : Return list of keys value 
   1. Proper() : Show/Set/Update property at the item.
   1. Find()   : Find data in the dictionary
   1. Load()   : Load saved data from file
   1. Save()   : dictionary save to file
   1. Sort()   : Sort dictionary
   1. FirstKey(): Get first Key 
1. Added property at each key

- Initialize dictionary 


```javascript
from DICT import DICT
root=DICT()
```
or
```javascript
import DICT
root=DICT.DICT()
```


```javascript
from DICT import DICT
>>> test={
      'a':123,
      'b':{
         'c':{'ddd'},
         'e':{}
      }
    }
root=DICT(test)
```

or 

```javascript
from DICT import DICT
>>> root=DICT()
```

- Add new data

```javascript
>>> root.tree.apple.color='red'
```
or

```javascript
>>> root.tree.apple.Put('color','red')
```
or
```javascript
>>> root.tree.apple['color']='red'
```
- Get data
```javascript
>>> root.tree.apple.color.Get()
```
or
```javascript
>>> root.tree.apple.Get('color')
```
- Print dictionary
```javascript
>>> root.Print()
>>> root.tree.Print()
```
- Set property at Apple's color

  - Set readonly
```javascript
>>> root.tree.apple.color.Proper('readonly',True)
```
  - Try change data
```javascript
>>> root.tree.apple.Put('color','white')
item is readonly

>>> root.tree.Print()
{'color': {'._d': 'red', '._p': {'readonly': True}}}
```
  - Unset readonly
```javascript
>>> root.tree.apple.color.Proper('readonly',False)
```
  - Try change data
```javascript
>>> root.tree.apple.Put('color','white')
>>> root.tree.Print()
{'color': {'._d': 'red', '._p': {'readonly': True}}}
```
Sample Dictionary:
```javascript
{'a': 123,
 'b': {'c': set(['ddd']), 'e': {}, 'z': 123},
 'tree': {'apple': {'color': {'._d': 'white', '._p': {'readonly': False}}},
          'banana': {'banana2': {'._d': 'white', '._p': {}},
                     'banana3': {'._d': 'yellow', '._p': {}},
                     'color': {'._d': 'yellow', '._p': {'readonly': True}}},
          'yellow': {'monkey': {'._d': 'white', '._p': {}}}}}
```
  - Find readonly property item path
```javascript
>>> root.Find('readonly',property=True)
['tree/banana/color']
```
  - Find apple key path
```javascript
>>> root.Find('apple',mode='key')
['tree/apple']
```
  - Find white color data path
```javascript
>>> root.Find('white')
['tree/apple/color', 'tree/yellow/monkey', 'tree/banana/banana2']
```
  - Find 123 data path
```javascript
>>> root.Find('white')
['a', 'b/z']
```
  - Find white color data path in key and value
```javascript
>>> root.Find('yellow',mode='all')
['tree/yellow', 'tree/banana/color', 'tree/banana/banana3']
```
  - Save Data (always use root if not then save partial data)
```javascript
>>> from DICT import DICT
>>> DICT._dfile_='<dict file name>'
>>> root.Save()
```
or
```javascript
>>> import DICT
>>> DICT.DICT._dfile_='<dict file name>'
>>> root.Save()
```
  - Load Data (always use root if not then load at key)
```javascript
>>> from DICT import DICT
>>> DICT._dfile_='<dict file name>'
>>> root.Load()
```
or
```javascript
>>> import DICT
>>> DICT.DICT._dfile_='<dict file name>'
>>> root.Load()
```

# MISC functions
Useful commands
