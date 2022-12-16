import os
import urllib.parse

import requests

import Registry
from hcy.HCY import build_request_from_hcy
from .CSSParser import CSSParser


@Registry.register_module
class MIUIParser(CSSParser):
    def __init__(self):
        self.hcy = build_request_from_hcy("hcy/miui.hcy")
        self.hcy.set_data(None)
        super(MIUIParser, self).__init__(requests.request(method="POST",
                         url="https://miui.511i.cn/?index=rom_list",
                         files={
                             'dh': (None, 'UNICORN'),
                             'lx': (None, '1b')
                         }).text, ".table-responsive tbody tr")

    def get_id(self, selected):
        return selected.contents[3].text

    def get_name(self, selected):
        return selected.contents[3].text + ' ' + selected.contents[1].contents[2].attrs['href']
