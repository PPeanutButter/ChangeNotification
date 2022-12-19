import requests

import Registry
from .CSSParser import CSSParser


@Registry.register_module
class MIUIParser(CSSParser):
    def __init__(self, dh, lx):
        super(MIUIParser, self).__init__(requests.request(method="POST",
                                                          url="https://miui.511i.cn/?index=rom_list",
                                                          files={
                                                              'dh': (None, dh),
                                                              'lx': (None, lx)
                                                          }).text, ".table-responsive tbody tr")

    def get_id(self, selected):
        return selected.contents[3].text

    def get_name(self, selected):
        return selected.contents[3].text + ' ' + selected.contents[1].contents[2].attrs['href']
