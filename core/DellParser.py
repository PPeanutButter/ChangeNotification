import Registry
from .JSONParser import JSONParser
import requests


@Registry.register_module
class DellParser(JSONParser):
    def __init__(self, url, selector, regex='.*'):
        self.regex = regex
        super(DellParser, self).__init__(requests.post(url, data=dict(
            v="2jU1XC1N+dJSMBZIgk7PzuDmHNcN2T7yQulvTETprwibEG27SukdTDlLqeElDFAU",
            src="oc"
        )).json(), selector)
