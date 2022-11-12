"""

骂某人
"""
import re
from plugin_manager import GroupMessagePlugin, all_plugins
import random
import pypinyin

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
        if '莫言' in name:
            return '不许骂摸言'

        if name == '鱼哥':
            return '鱼哥是猪'

        replys =['你是狗', '求求你别骂了', '你再说！', 'shut the fxxk up', '骂我不如看色图', '我哭了', '谁骂谁是狗',
        '我免疫了','随便骂','狗是你', '是你狗', '狗你是']
        name_str = set(name)
        for a in 'ÌḼ1г▏ㄧlL∟Ι乚ⅰＬ㇄Ï╘𠄌∣∠┕▎╙ㄥÎÍレ╚｜ḽ﹄Ⅰㄑⅼ┗|Γし┖﹂𠃊└':
            if a in name_str:
                return random.choice(replys)

        pinyin = pypinyin.pinyin(self.message, style=pypinyin.NORMAL)
        pinyin = [p[0] for p in pinyin]
        pinyin = "".join(pinyin)

        if "taoning" in pinyin:
            return '你是狗'
        return name + '是狗'


all_plugins.append(CursePlugin)