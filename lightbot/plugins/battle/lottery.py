import datetime
import random

from peewee import *

from database import create_tables, BaseModel, PublicVariable, database
from plugin_manager import GroupMessagePlugin
from utils import cq
from config import QQ


from .models import get_player
import logging
logger = logging.getLogger(__name__)

logger.info("加载抽签模块")

class LotteryRecord(BaseModel):
    group_id = BigIntegerField()  # 群号
    user_id = BigIntegerField()  # QQ

    bonus = IntegerField()  # 抽奖获得的奖金
    goods = CharField()  # 抽奖获得的物资
    c_time = DateTimeField(default=datetime.datetime.now)  # 抽奖时间


create_tables([LotteryRecord])


class LotteryPlugin(GroupMessagePlugin):
    def get_reply(self):
        if not self.message.startswith('抽奖'):
            return

        logger.info(f"{self.user_id} 抽奖")

        player = get_player(self.user_id, self.group_id)
        bonus_pool = PublicVariable.get_obj(player.group_id, name='奖金池')
        xiaoyue = get_player(QQ, self.group_id)
        now = datetime.datetime.now()
        if now - player.luck_draw_time < datetime.timedelta(hours=8):
            next_draw_time = player.luck_draw_time + datetime.timedelta(hours=8)

            msg = f'你才刚刚抽过奖！\n{next_draw_time.strftime("%Y-%m-%d %X")}后才能再次抽奖！\n'\
                  f'当前奖池:{bonus_pool.value}g'
            return msg

        # if player.is_dead():
        #     return "你挂了, 抽不了奖"

        if player.gold < 100:
            return f"你钱不足，需要100g，当前{player.gold}"

        with database.atomic() as transaction:
            player.gold -= 100
            bonus_pool.value += 80
            xiaoyue.gold += 20

            total_bonus = bonus_pool.value
            get_gold = 0  # 获得的奖金
            get_goods = None  # 获得的物资
            # 抽到了奖品等级
            bonus_level = random.choices([1, 2, 3, 4, 5, 6, 7], weights=[0.01, 0.1, 0.49, 0.1, 0.1, 0.1, 0.1])[0]
            
            if bonus_level == 1:
                msg = "恭喜获得奖金池的所有奖金！！！"
                get_gold = total_bonus
                bonus_pool.value = 0

            elif bonus_level == 2:
                msg = "获得奖金池5%的奖金！"
                get_gold = int(total_bonus * 0.05)
                bonus_pool.value -= get_gold

            elif bonus_level == 3:
                msg = "获得奖金池1%的奖金！"
                get_gold = int(total_bonus * 0.01)
                bonus_pool.value -= get_gold
            
            elif bonus_level == 4:
                msg = "获得2把Q5枪！"
                player.q5_weapon += 5
                get_goods = '2xq5枪'
            
            elif bonus_level == 5:
                msg = "获得5把Q1枪！"
                player.q1_weapon += 5
                get_goods = '5xq1枪'
            
            elif bonus_level == 6:
                msg = "获得2个Q5面包！"
                player.q5_food += 5
                get_goods = '2xq5面包'
            
            elif bonus_level == 7:
                msg = "获得5个Q1面包！"
                player.q1_food += 5
                get_goods = '5xq1面包'

            player.gold += get_gold

            LotteryRecord.create(
                group_id=self.group_id, 
                user_id=self.user_id, 
                bonues=get_gold, 
                godds=get_goods
            )
            
            player.luck_draw_time = now
            bonus_pool.save()
            player.save()
            xiaoyue.save()
            res = f"{cq.at(self.user_id)}\n花费100g抽奖\n{msg}\n"
            res += player.field_status("黄金", player.gold, add=get_gold)
            res += f"当前奖池: {bonus_pool.value}g"
            return  res



class GetMoneyPlugin(GroupMessagePlugin):
    def get_reply(self):
        if not self.message.startswith('取'):
            return
        
        if self.user_id != 435786117:
            return

        words = self.message.split()
        try:
            money = int(words[1])
        except:
            return 

        player = get_player(435786117, self.group_id)
        xiaoyue = get_player(QQ, self.group_id)
        
        if xiaoyue.gold >= money:
            player.gold += money
            xiaoyue.gold -= money
            
            res = ""
            res += player.field_status(f'{cq.at(self.user_id)}黄金', player.gold, add=money)
            res += player.field_status(f'小月黄金', xiaoyue.gold, add=-money)
            player.save()
            xiaoyue.save()
            return res



# class LuckDrawPlugins(GroupMessagePlugin):
#     def get_reply(self):
#         if self.message.startswith('抽奖'):
#             user = get_player(self.user_id, self.group_id)

            
#             user.gold -= 100
#             add_gold = random.choices([1000, 500, 100, 50, 10], weights=[0.01, 0.03, 0.5, 0.41, 0.05], k=1)[0]
#             if add_gold == 100:
#                 add_gold = random.randint(60, 140)

#             user.gold += add_gold
#             user.save()

#             return f"花费100g抽奖\n抽到了{add_gold}g, 当前{user.gold}g"