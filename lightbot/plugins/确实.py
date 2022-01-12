"""
当群友说确实时，响应群友的确实以免冷场
"""
import pypinyin
from plugin_manager import all_plugins, GroupMessagePlugin


class IndeedPlugin(GroupMessagePlugin):

    def get_reply(self):
            # message = event['message']
        pinyin = pypinyin.pinyin(self.message, style=pypinyin.NORMAL)
        pinyin = [p[0] for p in pinyin]
        pinyin = "".join(pinyin)

        if "queshi" in pinyin:
            return "确实"

        for text in ['确实', 'indeed', 'たぃかに', '確かに', '確か']:
            if text in self.message:
                return text

all_plugins.append(IndeedPlugin)