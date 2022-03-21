import Registry
from .HTMLMessage import HTMLMessage


@Registry.register_module
class TextMessage(HTMLMessage):
    def __init__(self):
        self.head = ""
        self.content_join = """\n"""
        self.tail = ""
        super(TextMessage, self).__init__()
