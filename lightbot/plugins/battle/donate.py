import datetime
import random

from peewee import *

from database import create_tables, BaseModel, PublicVariable, database
from plugin_manager import GroupMessagePlugin
from utils import cq
from config import QQ
from .helper import check_num, get_item_level_and_name
from .params import DONATE_COOLDOWN
from .models import get_player
import logging
logger = logging.getLogger(__name__)

logger.info("加载捐赠模块")

class DonateRecord(BaseModel):
    group_id = BigIntegerField()  # 群号
    sender_id = BigIntegerField()  # 发送人QQ
    receiver_id = BigIntegerField()  # 接收人QQ

    num = IntegerField()  # 转的钱
    item = CharField(default=None)  # 转的东西
    c_time = DateTimeField(default=datetime.datetime.now)  # 转账时间


create_tables([DonateRecord])


class DonatePlugin(GroupMessagePlugin):

    def get_num_and_item(self):
        """ 不输入物品默认是转g 第二个参数是数量 第三个参数是物品"""
        words = self.message.split()
        if len(words) < 2:
            num = 0
            item = None
        elif len(words) == 2:
            item = 'g'
        else:
            level, name = get_item_level_and_name(words[2])
            item = f'q{level}{name}'
        # 物品数量
        num = check_num(words[1], default=0)

        return num, item

    def get_reply(self):
        

        if not self.message.lower().startswith('d'):
            return
            
        logger.info(f"{self.user_id} 转账")
        player = get_player(self.user_id, self.group_id)
        receiver_id = cq.get_at_user_id(self.message)
        receiver = get_player(receiver_id, self.group_id)

        if not receiver:
            return

        if int(receiver_id) == int(self.user_id):
            return "不能d给自己！"

        # 上一条捐赠记录
        last_donate_record = DonateRecord \
            .select() \
            .where(DonateRecord.group_id==self.group_id, DonateRecord.sender_id==self.user_id) \
            .order_by(DonateRecord.c_time.desc()) \
            .get_or_none()
        
        # 冷却判定
        if last_donate_record is not None:
            now = datetime.datetime.now()
            d = (now - last_donate_record.c_time).total_seconds()
            if d <= DONATE_COOLDOWN:
                return "捐赠还有%.3f秒冷却" % (DONATE_COOLDOWN - d)

        # 获取捐赠数量和物品名称
        num, item = self.get_num_and_item()

        if num == 0:
            return

        if item is None:
            return
        
        # 回复语句
        res = f"{cq.at(player.user_id)}转给{cq.at(receiver.user_id)}\n"

        if item == 'g':
            if player.gold >= num:
                with database.atomic() as t:
                    player.gold -= num
                    receiver.gold += num
                    DonateRecord.create(
                        group_id=self.group_id, 
                        sender_id=player.user_id, 
                        receiver_id=receiver.user_id,
                        num=num, 
                        item=item
                    )
                    
                    player.save()
                    receiver.save()

                res += player.field_status('转账人黄金', player.gold, add=-num)
                res += player.field_status('接收人黄金', receiver.gold, add=num)
                return res
            else:
                return f"穷狗！你钱不足\n当前{player.gold}g，要转{num}g"

        else:
            return '当前版本暂时只能转g'




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