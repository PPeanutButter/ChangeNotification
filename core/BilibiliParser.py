import json

import Registry
from .JSONParser import JSONParser
from hcy.HCY import HCYRequest


@Registry.register_module
class BilibiliParser(JSONParser):
    def __init__(self, url, selector, cookie, regex='.*'):
        self.regex = regex
        self.hcy = HCYRequest(url=url, method='GET', base_headers='hcy/bilibili.hcy', cookie=cookie)
        super(BilibiliParser, self).__init__(self.hcy.request().text, selector)

    def get_id(self, selected):
        selected = json.loads(selected)
        owner_name = selected['owner']['name'] if 'owner' in selected else selected['apiSeasonInfo']['title']
        title = selected['title'] if 'title' in selected else selected['new_desc']
        return owner_name+title

    def get_name(self, selected):
        selected = json.loads(selected)
        owner_name = selected['owner']['name'] if 'owner' in selected else selected['apiSeasonInfo']['title']
        title = selected['title'] if 'title' in selected else selected['new_desc']
        cover = selected['pic'] if 'pic' in selected else selected['cover']
        return f'<h3>{owner_name}</h3>'+title+f'\n<img src="{cover}"/>\n' if cover else ""
