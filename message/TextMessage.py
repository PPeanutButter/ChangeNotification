import Registry
from .HTMLMessage import HTMLMessage


@Registry.register_module
class TextMessage(HTMLMessage):
    def __init__(self):
        super(TextMessage, self).__init__()
        self.head = ""
        self.content_join = """\n"""
        self.tail = ""

