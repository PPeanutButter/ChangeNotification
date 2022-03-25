import Registry
from .HTMLMessage import HTMLMessage


@Registry.register_module
class CQMessage(HTMLMessage):
    def __init__(self):
        self.head = "["
        self.content_join = ""","""
        self.tail = "]"
        super(CQMessage, self).__init__()
