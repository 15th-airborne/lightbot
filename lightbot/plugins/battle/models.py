"""
数据库模型文件

"""
import datetime
import random

from peewee import *

from database import create_tables, BaseModel
from utils import cq
REBORN_REMAIN_TIME = 120  # 复活所需时间



class Player(BaseModel):
    user_id = IntegerField()
    group_id = IntegerField()
    health = IntegerField(default=30)
    health_max = IntegerField(default=30)
    attack_min = IntegerField(default=2)
    attack_max = IntegerField(default=12)

    dead_time = TimestampField(default=0)

    class Meta:
        table_name = "battle_player"

    def __str__(self):
        return f"id={self.id}, user_id={self.user_id}, group_id={self.group_id}"

    def reborn(self):
        """ 复活 """
        self.health = self.health_max
        self.save()

    def is_dead(self):
        """ 判断玩家是否阵亡 """
        if self.health <= 0:
            if datetime.datetime.now() - self.dead_time < datetime.timedelta(seconds=60):
                print("阵亡中...")
                return True
            else:
                self.reborn()
                print("复活！")
                return False
        return False

    def hit(self, player):
        """
        思路：如果自己或对方是阵亡状态，不执行任何操作，主要看返回值是否是整数，如果是就是造成了伤害。
        """
        if self.is_dead():
            return

        if player.is_dead():
            return

        damage = random.randint(self.attack_min, self.attack_max)
        player.health = max(0, player.health - damage)

        if player.health <= 0:
            player.dead_time = datetime.datetime.now()

        player.save()
        return damage

    def status(self):
        res = f"{cq.at(self.user_id)}当前状态: \n"

        if self.is_dead():
            res += f"阵亡中...({self.reborn_remain_time}秒后复活)\n"

        res += f"生命值: {self.health}/{self.health_max}\n" \
               f"攻击力: {self.attack_min} ~ {self.attack_max}\n"

        return res

    @property
    def reborn_remain_time(self):
        res = REBORN_REMAIN_TIME - (datetime.datetime.now() - self.dead_time).seconds
        return res


def get_player(user_id, group_id):
    print(user_id, group_id)
    try:
        player = Player.get(user_id=user_id, group_id=group_id)
    except Player.DoesNotExist:
        player = Player.create(user_id=user_id, group_id=group_id)
    return player


def attack_someone_reply(attacker_user_id, defender_user_id, group_id):
    if defender_user_id is None:
        return "找不到你要揍的人(长按要揍的人的头像艾特他)"

    attacker = get_player(attacker_user_id, group_id)
    defender = get_player(defender_user_id, group_id)

    if attacker.is_dead():
        return f"{cq.at(attacker_user_id)}你都挂了还想揍人？{attacker.reborn_remain_time}秒后复活。"
    if defender.is_dead():
        return f"{cq.at(defender_user_id)}已经挂了。{defender.reborn_remain_time}秒后复活。"

    damage = attacker.hit(defender)
    res = f"{cq.at(attacker_user_id)}夯了{cq.at(defender_user_id)}\n" \
          f"造成了{damage}点伤害\n"

    if defender.is_dead():
        res += f"{cq.at(defender_user_id)} 挂了，需要{REBORN_REMAIN_TIME}秒复活"
    else:
        res += f"{cq.at(defender_user_id)} 当前生命值: ({defender.health}/{defender.health_max})"
    return res


create_tables([Player])
