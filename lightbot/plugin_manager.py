"""
插件管理，实现编写类并放到指定文件目录下就能加载插件的功能
https://docs.go-cqhttp.org/event/#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF
"""
from api import Api
all_plugins = []


class PluginManager:
    def __init__(self):
        self.plugins = []
    
    def add_plugins(self, plugins):
        for plugin in plugins:
            self.plugins.append(plugin)


class GroupMessagePlugin:
    def __init__(self, event):
        self.message = event['message']
        self.group_id = event['group_id']
        self.user_id = event['sender']['user_id']
        self.username = event['sender']['nickname']

    def is_activated(self):
        """ 是否激活该插件 """
        raise NotImplemented

    def get_reply(self):
        pass

    def api(self):
        reply = self.get_reply()
        if reply is not None and reply != "":
            return Api(
                action="send_group_msg",
                group_id=self.group_id, 
                message=reply
            )


def parse_params(message, prefix=None):
    if prefix:
        message = message[len(prefix):]  # 移除前缀关键词

    words = message.split()
    return words
    
plugin_manager = PluginManager()
add_plugins = plugin_manager.add_plugins