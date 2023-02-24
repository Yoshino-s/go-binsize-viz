import sys
from typing import BinaryIO
from re_set import *

def process(file: BinaryIO):
    vtables_sz = 0
    typeinfo_sz = 0
    init_sz = 0
    rest_sz = 0
    gotyp_sz = 0

    values = {}

    def store_rec(values, path, sz):
        if len(path) == 0:
            v = values.get("value", 0)
            v += sz
            values["value"] = v
        else:
            n = path[0]
            d1 = values.get("children", {})
            d = d1.get(n, {})
            d1[n] = d
            values["children"] = d1
            store_rec(d, path[1:], sz)

    def store(path, sz):
        nonlocal values
        store_rec(values, path, sz)

    with open(sys.argv[1]) as f:
        for line in f:
            if undefined_re.match(line) is not None:
                
                continue
            if line.endswith('\n'):
                line = line[:-1]

            m = entries_re.match(line)
            if m is None:
                continue

            typ = m.group(3).strip()
            if typ == 'U':
                
                continue

            sz = m.group(2).strip()
            try:
                sz = int(sz)
            except:
                continue
            if sz == 0:
                
                continue

            sym = m.group(4).strip()
            if sym == '':
                continue
            if sym.startswith('construction vtable ') or sym.startswith('vtable for '):
                
                vtables_sz += sz
                continue
            if sym.startswith('__static_initialization_and_destruction'):
                
                init_sz += sz
                continue
            if sym.startswith('typeinfo '):
                
                typeinfo_sz += sz
                continue
            if sym.startswith('type:'):
                
                gotyp_sz += sz
                continue

            parts = cpp_sym_re.match(sym)
            parts_re = None
            if parts is not None:
                prefix = ['c/c++ · ']
                parts_re = cpp_path_re

            if parts is None:
                parts = go_sym_re.match(sym)
                if parts is not None:
                    prefix = ['go · ']
                    parts_re = go_path_parts_re

            if parts is None:
                rest_sz += sz
                continue

            if not parts_re:
                continue

            path = parts.group(2)
            path = parts_re.findall(path)
            name = parts.group(1) + parts.group(3)

            

            fullpath = prefix+path+[name] # type: ignore            


            store(fullpath, sz)

    store(['c/c++ · ','VTABLES'], vtables_sz)
    store(['c/c++ · ','TYPEDATA'], typeinfo_sz)
    store(['c/c++ · ','INITIALIZERS'], init_sz)
    store(['go · ','TYPEDATA'], gotyp_sz)
    store(['UNKNOWN'], rest_sz)


    values['name'] = '>'
    def flatten(d):
        vals = []
        for k, v in d.items():
            if isinstance(v, dict):
                v['name'] = k
                vals.append(v)
        return vals

    def transform(d):
        # transform [A, B., X] into  [A, B/, _self_, X]  if [A, B/] also exists already.
        maybecopy = None
        for k in d:
            if k.endswith('.'):
                dirkey = k[:-1] + '/'
                if dirkey in d:
                    if maybecopy is None:
                        maybecopy = d.copy()
                    maybecopy[dirkey]['children']['· self'] = d[k]
                    del(maybecopy[k])
        if maybecopy is not None:
            d = maybecopy

        for k, v in list(d.items()):
            if type(v) == type({}):
                ename, v = transform(v)
                del d[k]
                d[k+ename] = v
        ename = ""
        if "children" in d:
            c = flatten(d['children'])
            if len(c) == 1 and "children" in c[0]:
                c0 = c[0]
                ename = c0["name"]
                c = c0["children"]
            d['children'] = c
        return ename, d

    _, values = transform(values)

    return values

