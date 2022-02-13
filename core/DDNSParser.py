import base64
import requests
import Registry
from core.BaseParser import BaseParser


@Registry.register_module
class DDNSParser(BaseParser):
    def __init__(self, protocol, web, server, password, domain):
        self.server = server
        self.domain = domain
        self.protocol = protocol
        self.regex = ".*"
        self.authorization = "Basic "+base64.b64encode((":"+password).encode()).decode()
        try:
            ipv6 = self.get(web)
        except BaseException:
            ipv6 = None
        super(DDNSParser, self).__init__([ipv6])

    def get_id(self, selected):
        if selected:
            url = f"https://{self.server}/nic/update?system={self.protocol}&hostname={self.domain}&myip={selected}"
            return requests.request('GET', url=url, headers=dict(authorization=self.authorization)).text
        else:
            return ""

    def get_name(self, selected):
        return self.get_id(selected)
