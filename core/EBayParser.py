import Registry
from .SimpleJsonParser import SimpleJsonParser


@Registry.register_module
class EBayParser(SimpleJsonParser):
    def __init__(self, url, selector="$.data.Catalog.searchStore.elements[?(@.promotions.promotionalOffers)]", regex='.*'):
        super(EBayParser, self).__init__(url, selector, regex)

    def get_id(self, selected):
        return selected['title']

    def get_name(self, selected):
        return f"《{selected['title']}》免费送啦~</br><img src=\"{selected['keyImages'][-1]['url']}\"/>"
