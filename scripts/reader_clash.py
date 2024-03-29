from io import BufferedIOBase
from typing import Dict, List
from data import ISubscribeReader, Proxy, ProxyGroup, Rule

try:
    from yaml import CLoader as Loader
except ImportError as e:
    print('[warning] unable to load libyaml; use python module instead', e)
    from yaml import Loader


class ClashSubscribeReader(ISubscribeReader):
    
    inner: Dict

    def __init__(self):
        super().__init__()

    def get_cache_name(self, filename: str) -> str:
        return filename + '.yml'

    def read(self, ifile: BufferedIOBase, is_cache: bool, ofile_cache: BufferedIOBase | None = None) -> None:
        loader = Loader(ifile)
        try:
            self.inner = loader.get_single_data()
        finally:
            loader.dispose()
        if not is_cache and ofile_cache is not None:
            ifile.seek(0)
            while True:
                data = ifile.read(1024)
                if not data:
                    break
                ofile_cache.write(data)


    def get_proxies(self) -> List[Proxy]:
        proxies = self.inner.get('proxies')
        if proxies is None:
            return None
        return [Proxy(p) for p in proxies]
    
    def get_all_proxies(self, name: str) -> ProxyGroup:
        proxies = self.inner.get('proxies')
        if proxies is None:
            return None
        inner = {
            'name': name,
            'type': 'select',
            'proxies': [p['name'] for p in proxies]
        }
        return ProxyGroup(inner)

    def get_proxy_groups(self) -> List[ProxyGroup]:
        groups = self.inner.get('proxy-groups')
        if groups is None:
            return None
        return [ProxyGroup(g) for g in groups]

    def get_rules(self, name: str) -> List[Rule]:
        rules = None
        if not name:
            rules = self.inner.get('rules')
        else:
            sub_rules = self.inner.get('sub-rules')
            if sub_rules is None:
                return None
            rules = sub_rules.get(name)
        if rules is None:
            return None
        return [Rule(r) for r in rules]

# __main__
#
# args[0]:      template file name
# args[1..n]:   variables "<GeneralGroup>=<value>"
#                   enable_tun:bool=true
#                   port:int=10000
#                   qb:null=
#
# example:
#   python reader_clash.py config.template.yaml "enable_tun:bool=true" "port:int=10086"
#

if __name__ == '__main__':
    from sys import argv
    from data import Info, GeneralGroup

    args = argv[1:]
    if len(args) < 1:
        exit()
    ifile_name = args[0]
    variables = dict()
    args = args[1:]
    for arg in args:
        sp = arg.find('=')
        if sp < 0:
            continue
        _name = arg[:sp]
        _value = arg[sp+1:]
        variables[GeneralGroup.__dict__[_name]] = _value

    with open(ifile_name, 'r', encoding='utf-8') as ifile:
        reader = ClashSubscribeReader()
        reader.read(ifile)
        item = Info(reader, 'test', 1, True, variables)
        item.modify_by_name('test')
        print('====proxy====')
        for p in item.proxies.values():
            print(p)
        print('====group====')
        for g in item.proxy_groups_general.values():
            print(g)
        print('====group====')
        for g in item.proxy_groups_other.values():
            print(g)
        print('====rules====')
        for r in item.rules['']:
            print(r)
    pass