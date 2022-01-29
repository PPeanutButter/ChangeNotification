import Registry
from .BaseMessage import BaseMessage


@Registry.register_module
class HTMLMessage(BaseMessage):
    def __init__(self):
        self.head = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body><ul><li>"""
        self.content_join = """</li><li>"""
        self.tail = """</li></ul></body></html>"""
        super(HTMLMessage, self).__init__()

    def build_head(self):
        return self.head

    def build_content(self, content_list):
        return self.content_join.join(content_list)

    def build_tail(self):
        return self.tail
