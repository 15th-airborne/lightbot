"""
插件管理，实现编写类并放到指定文件目录下就能加载插件的功能

"""
from api import Api
all_plugins = []


class GroupMessagePlugin:
    def __init__(self, event):
        self.message = event['message']
        self.group_id = event['group_id']
        self.user_id = event['sender']['user_id']

    def is_activated(self):
        """ 是否激活该插件 """
        raise NotImplemented


    def get_reply(self):
        pass

    def api(self):
        reply = self.get_reply()
        if reply is not None:
            return Api(
                action="send_group_msg",
                group_id=self.group_id, 
                message=reply
            )