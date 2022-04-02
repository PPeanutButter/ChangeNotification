import os
import urllib.parse

import Registry
from .CSSParser import CSSParser


@Registry.register_module
class BTBTTParser(CSSParser):
    def __init__(self, url, selector, regex='.*'):
        self.url = url
        self.selector = self.build_selector(selector)
        self.regex = regex
        super(BTBTTParser, self).__init__(self.get(self.url), self.selector)

    def get_id(self, selected):
        return selected.text

    def get_name(self, selected):
        ori_url = urllib.parse.urlparse(self.url)
        if selected.name == 'a' and str(selected.text).endswith('.torrent'):
            download_url = f"{ori_url.scheme}://{ori_url.hostname}/{selected.attrs['href']}"\
                .replace("-dialog-", "-download-")
            return '📺'+self.get_id(selected) + '\n🧲'+os.popen(f'bt2magnet "{download_url}"').read().strip('\n')
        else:
            return self.get_id(selected)

    @staticmethod
    def build_selector(selector):
        if isinstance(selector, int):
            return f"div#body table:nth-child({selector}) div.attachlist a"
        else:
            return selector
