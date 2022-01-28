import json

from jsonpath import jsonpath
from .BaseParser import BaseParser


class JSONParser(BaseParser):
    def __init__(self, json_data, selector):
        self.json_data = json_data
        selects = jsonpath(json_data if isinstance(json_data, dict) else json.loads(json_data), selector)
        super(JSONParser, self).__init__(selects)

    def get_id(self, selected):
        return selected.text

    def get_name(self, selected):
        return self.get_id(selected)
