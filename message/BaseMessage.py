class BaseMessage:
    def build_message(self, content_list):
        content = [self.head, self.build_content(content_list), self.build_tail()]
        return ''.join(content)

    def build_head(self):
        return ""

    def build_content(self, content_list):
        return ''.join(content_list)

    def build_tail(self):
        return ""
