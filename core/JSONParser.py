import json
import Registry
from jsonpath import jsonpath
from .BaseParser import BaseParser


@Registry.register_module
class JSONParser(BaseParser):
    def __init__(self, json_data, selector):
        self.json_data = json_data
        selects = jsonpath(json_data if isinstance(json_data, dict) else json.loads(json_data), selector)
        super(JSONParser, self).__init__(selects if selects else [])

    def get_id(self, selected):
        return selected

    def get_name(self, selected):
        return self.get_id(selected)
