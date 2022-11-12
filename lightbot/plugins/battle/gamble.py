import re
from plugin_manager import GroupMessagePlugin, all_plugins
from peewee import *
import datetime
from database import database, create_tables, BaseModel
import random
from .models import get_player

class Gambel(BaseModel):
    user_id = BigIntegerField()
    group_id = BigIntegerField()
    game_name = CharField()
    choices = CharField()
    gold = BigIntegerField()

create_tables([Gambel])

games = {
    '1': {
        'title': '佩洛西是否会窜访台湾',
        'choices': {
            '1': '会',
            '2': '不会'
        }
    }
}

class GamblePlugin(GroupMessagePlugin):
    def get_reply(self):
        # 例如
        # 下注 1 1 100
        player = get_player(self.user_id, self.group_id)
        if not self.message.startswith("下注"):
            return 
        if datetime.datetime.now() >= datetime.datetime(2022, 8, 1, 23, 0, 0):
            return '游戏结束'
        args = self.message.split()[:]
        if len(args) != 3:
            games = Gambel.select()\
                .where(
                    Gambel.group_id == self.group_id,
                    Gambel.game_name == '佩洛西是否会窜访台湾',
                )
            yes = no = 0
            for game in games:
                if game.choices == '会':
                    yes += game.gold
                elif game.choices == '不会':
                    no += game.gold

            会 = no / yes if yes != 0 else 1
            不会 = yes / no if no != 0 else 1
            return (
                '当前盘口：佩洛西是否会窜访台湾\n'
                f'赔率: 会({会}) 不会({不会})\n'
                '截止日期: 2022年8月1日 23点\n'
                '下注举例：下注 会 1000\n'
                '表示认为佩洛西会窜访台湾并下注1000g\n'
            ) 
        try:
            gold = int(args[2])
            if player.gold < gold:
                return '你钱不足'
            
            if gold <= 0:
                return '只能输入正数！'
        except:
            replys = [
                '金额必须是数字！',
                '金额必须是数字！！',
                '金额必须是数字！！！',
                '你是狗，别测试了，金额必须为数字！！！！'
            ]
            return random.choices(replys)[0]

        with database.atomic() as transaction:
            if args[1] not in ['会', '不会']:
                return '选择“会”或“不会”'
            player.gold -= gold
            Gambel.create(
                user_id=self.user_id, 
                group_id=self.group_id,
                game_name='佩洛西是否会窜访台湾',
                gold=gold,
                choices=args[1]
            )
            player.save()
            return '下注成功！'


all_plugins.append(GamblePlugin)