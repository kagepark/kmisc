#Kage Park
import os

def Path(*inp,**opts):
    sym=opts.get('sym','/')
    out=opts.get('out','str')
    if inp:
        full_path=[]
        if isinstance(inp[0],str):
            root_a=inp[0].split(sym)
            if len(root_a):
                if root_a[0] == '~': 
                    full_path=os.environ['HOME'].split(sym)
                else:
                    full_path=[root_a[0]]
            for zz in range(1,len(root_a)):
                if full_path and not root_a[zz]: continue
                full_path.append(root_a[zz])
        for ii in inp[1:]:
            if isinstance(ii,str):
                for zz in ii.split(sym):
                    if full_path and not zz: continue
                    if zz == '.': continue
                    if full_path and full_path[-1] != '..' and zz == '..':
                        del full_path[-1]
                        continue
                    full_path.append(zz)
        if full_path:
            if out in [str,'str']:return sym.join(full_path)
            return full_path
    return os.path.dirname(os.path.abspath(__file__)) # Not input then get current path
