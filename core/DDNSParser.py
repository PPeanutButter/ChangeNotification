import base64
import os

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
            self.r = {}
            card = ""
            ipv4 = ""
            for line in os.popen("ipconfig").readlines():
                if line.startswith("以太网适配器"):
                    card = str(' '.join(line.split(" ")[1:])[:-2])
                    self.r[card] = dict(name=card)
                elif line.find(":") != -1:
                    self.r[card][line.split(':')[0].strip()] = ':'.join([i.strip() for i in line.split(':')[1:]])
            for k, v in self.r[regex].items():
                if k.find("IPv4") != -1:
                    ipv4 = v
        except BaseException:
            ipv4 = None
        super(DDNSParser, self).__init__([ipv4])

    def get_id(self, selected):
        if selected:
            url = f"https://{self.server}/nic/update?system={self.protocol}&hostname={self.domain}&myip={selected}"
            return requests.request('GET', url=url, headers=dict(authorization=self.authorization)).text
        else:
            return ""

    def get_name(self, selected):
        return self.get_id(selected)
