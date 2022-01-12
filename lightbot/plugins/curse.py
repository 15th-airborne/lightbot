"""

骂某人
"""
import re
from plugin_manager import GroupMessagePlugin, all_plugins


class CursePlugin(GroupMessagePlugin):
    def get_reply(self):
        if not self.message.startswith("骂"):
            return 
            
        is_include_image = True if re.search(r'\[CQ:image.*?]', self.message) else False
        is_include_face = True if re.search(r'\[CQ:face.*?]', self.message) else False

        message = self.message.replace(' ', '').lower()

        name = message[1:]
        if len(name) >= 30:
            return '你是狗，哪有这么长的名字'

        if is_include_image:
            return '你是狗，别发图片了'

        if is_include_face:
            return '骂人别带表情了，求求'

        if '我' in name or ('小月' in name):
            return '你是狗'

        if '群主' in name:
            return '我不敢骂群主'

        return name + '是狗'


all_plugins.append(CursePlugin)