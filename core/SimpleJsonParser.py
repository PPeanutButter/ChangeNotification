import Registry
from .JSONParser import JSONParser


@Registry.register_module
class SimpleJsonParser(JSONParser):
    def __init__(self, url, selector, regex='.*'):
        self.regex = regex
        super(SimpleJsonParser, self).__init__(self.get(url), selector)
