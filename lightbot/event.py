"""
事件 https://docs.go-cqhttp.org/event/
"""


def unescape(s: str) -> str:
    """对字符串进行 CQ 码去转义。"""
    return s.replace('&#44;', ',') \
        .replace('&#91;', '[') \
        .replace('&#93;', ']') \
        .replace('&amp;', '&')


class Event(dict):
    def __init__(self, event):
        super().__init__()
        self.update(event)

        # 转义字符
        if self.is_message():
            self['message'] = unescape(self['message'])

    def is_message(self):
        return self.get('post_type') == 'message'

    def is_group_message(self):
        return self.get('message_type') == 'group'

    def is_private_message(self):
        return self.get('message_type') == 'private'

    def is_group_ban(self):
        return self.get('notice_type') == 'group_ban'

    # 群和私聊的戳一戳
    def is_group_poke(self):
        return self.get('group_id') and self.get('sub_type') == 'poke'

    def is_private_poke(self):
        return not self.get('group_id') and self.get('sub_type') == 'poke'
