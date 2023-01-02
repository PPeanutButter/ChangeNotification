import base64
import subprocess

import requests
import Registry
from core.BaseParser import BaseParser


@Registry.register_module
class DDNSParser(BaseParser):
    def __init__(self, protocol, server, password, domain):
        self.server = server
        self.domain = domain
        self.protocol = protocol
        self.authorization = "Basic "+base64.b64encode((":"+password).encode()).decode()
        try:
            ipv4 = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True).decode("utf-8").strip("\n")
        except BaseException as e:
            print(e.__str__())
            ipv4 = None
        super(DDNSParser, self).__init__([ipv4])

    def get_id(self, selected):
        if selected:
            url = f"https://{self.server}/nic/update?system={self.protocol}&hostname={self.domain}&myip={selected}"
            r = requests.request('GET', url=url, headers=dict(authorization=self.authorization)).text
            print(f"https://{self.server}/nic/update?system={self.protocol}&hostname={self.domain}&myip={selected}", r)
        return ""

    def get_name(self, selected):
        return ""
