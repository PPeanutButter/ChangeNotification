import base64
import os
import re

import requests
import Registry
from core.BaseParser import BaseParser


@Registry.register_module
class DDNSParser(BaseParser):
    def __init__(self, protocol, server, password, domain, regex):
        self.server = server
        self.domain = domain
        self.protocol = protocol
        self.regex = regex
        self.authorization = "Basic "+base64.b64encode((":"+password).encode()).decode()
        try:
            self.r = self.get_net_info()
            ipv4 = r"(\d+\.\d+\.\d+\.\d+)"
            for k, v in self.r[regex].items():
                if k.find("IPv4") != -1:
                    r = re.search(ipv4, v)
                    if r:
                        ipv4 = r.group(1)
        except BaseException as e:
            print(e.__str__())
            ipv4 = None
        super(DDNSParser, self).__init__([ipv4])

    def get_id(self, selected):
        if selected:
            url = f"https://{self.server}/nic/update?system={self.protocol}&hostname={self.domain}&myip={selected}"
            r = requests.request('GET', url=url, headers=dict(authorization=self.authorization)).text
            print(r)
            return r
        else:
            return ""

    def get_name(self, selected):
        return self.get_id(selected)

    def get_net_info(self) -> dict:
        import platform
        _r = {}
        if platform.system() == 'Windows':
            import re
            _1 = r"^\S.*适配器 (.*):"
            _2 = r"^ {3}(.*?) +\..*?: (.*)"
            _3 = r"^ {4,}(.*)"
            cache = {}
            cache_name = ""
            last_key = ""
            for line in os.popen("ipconfig /all").readlines():
                r = re.search(_1, line)
                if r:
                    if cache_name:
                        _r[cache_name] = cache
                        cache = {}
                        last_key = ""
                    cache_name = r.group(1)
                    continue
                r = re.search(_2, line)
                if r and cache_name:
                    last_key = r.group(1)
                    cache[r.group(1)] = r.group(2)
                    continue
                r = re.search(_3, line)
                if r and cache_name:
                    c = cache[last_key]
                    if isinstance(c, list):
                        cache[last_key] = c.append(r.group(1))
                    elif isinstance(c, str):
                        cache[last_key] = [c, r.group(1)]
            if cache_name:
                _r[cache_name] = cache
            return _r
        return {}
