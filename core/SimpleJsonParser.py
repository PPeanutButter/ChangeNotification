from .JSONParser import JSONParser


class SimpleJsonParser(JSONParser):
    def __init__(self, url, selector, regex='.*'):
        self.regex = regex
        super(SimpleJsonParser, self).__init__(self.get(url), selector)
