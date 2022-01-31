import datetime
import random

from peewee import *

from database import create_tables, BaseModel, PublicVariable, database
from plugin_manager import GroupMessagePlugin
from utils import cq

from .models import get_player
import logging
logger = logging.getLogger(__name__)

logger.info("加载抽签模块")

class LotteryRecord(BaseModel):
    group_id = BigIntegerField()  # 群号
    user_id = BigIntegerField()  # QQ

    bonus = IntegerField()  # 抽奖获得的奖金
    c_time = DateTimeField(default=datetime.datetime.now)  # 抽奖时间


class LotteryPlugin(GroupMessagePlugin):
    def get_reply(self):
        logger.info(f"{self.user_id} 抽奖")

        if not self.message.startswith('抽奖'):
            return

        logger.info(f"{self.user_id} 抽奖")

        player = get_player(self.user_id, self.group_id)
        bonus_pool = PublicVariable.get_obj(player.group_id, name='奖金池')

        # if player.is_dead():
        #     return "你挂了, 抽不了奖"

        if player.gold < 100:
            return f"你钱不足，需要100g，当前{player.gold}"

        with database.atomic() as transaction:
            player.gold -= 100
            bonus_pool.value += 100
            total_bonus = bonus_pool.value
            get_gold = 0  # 获得的奖金
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
                msg = "获得5把Q5枪！"
                player.q5_weapon += 5
            
            elif bonus_level == 5:
                msg = "获得5把Q1枪！"
                player.q1_weapon += 5
            
            elif bonus_level == 6:
                msg = "获得5个Q5面包！"
                player.q5_food += 5
            
            elif bonus_level == 7:
                msg = "获得5个Q1面包！"
                player.q1_food += 5
            
            player.gold += get_gold

            bonus_pool.save()
            player.save()
            res = f"{cq.at(self.user_id)}\n花费100g抽奖\n{msg}\n"
            res += player.field_status("黄金", player.gold, add=get_gold)
            res += f"当前奖池: {bonus_pool.value}g"
            return  res
            
            

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