import Registry
from bs4 import BeautifulSoup
from .BaseParser import BaseParser


@Registry.register_module
class CSSParser(BaseParser):
    def __init__(self, html_data, selector):
        self.html_data = html_data
        selects = BeautifulSoup(self.html_data, 'html.parser').select(selector)
        super(CSSParser, self).__init__(selects)

    def get_id(self, selected):
        return selected

    def get_name(self, selected):
        return selected
