"""
事件 https://docs.go-cqhttp.org/event/
"""


def unescape(s: str) -> str:
    """对字符串进行 CQ 码去转义。"""
    return s.replace('&#44;', ',') \
        .replace('&#91;', '[') \
        .replace('&#93;', ']') \
        .replace('&amp;', '&')


def fake_group_msg_event(msg, user_id=435786117, group_id=542423773, nickname='LightL'):
    event={
        'user_id': user_id,
        'group_id': group_id,
        'message': msg,
        'sender': {
            'user_id': user_id,
            'nickname': nickname
        }
    }
    return event


class Event(dict):
    def __init__(self, event):
        super().__init__()
        self.update(event)

        # 转义字符
        if self.is_message():
            self['message'] = unescape(self['message'])
        
        self.user_id = self.get('user_id')
        self.group_id = self.get('group_id')
        self.message = self.get('message')
        self.sender = Sender(self.get('sender', {}))

    def __getattr__(self, key):
        return self[key]
    
    def __setattr__(self, key, value):
        self[key] = value

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
        return self.group_id and self.get('sub_type') == 'poke'

    def is_private_poke(self):
        return not self.group_id and self.get('sub_type') == 'poke'


class Sender(dict):
    def __init__(self, sender):
        super().__init__()
        self.update(sender)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value
