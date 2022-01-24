"""
数据库模型文件

"""
from asyncio import FastChildWatcher
import datetime
from email.policy import default
import random
from this import d

from peewee import *

from database import create_tables, BaseModel
from database.models import GroupMember
from .config import REBORN_REMAIN_TIME, FOODS, WEAPONS
from utils import cq
import logging
logger = logging.getLogger(__name__)



ITEM_NAMES = set()

for item in FOODS:
    ITEM_NAMES.add(item['name']) 

for item in WEAPONS:
    ITEM_NAMES.add(item['name']) 

Q1_FOOD_HEALTH = 10 
Q5_FOOD_HEALTH = 50

WEAPON_DAMAGES = {
    0: 0,
    1: 2,
    5: 10
}

Q1_WEAPON_DAMAGE = 2
Q5_WEAPON_DAMAGE = 10


class Player(BaseModel):
    user_id = BigIntegerField()
    group_id = BigIntegerField()
    health = IntegerField(default=30)
    health_max = IntegerField(default=30)
    attack_min = IntegerField(default=2)
    attack_max = IntegerField(default=12)

    dead_time = TimestampField(default=0)

    # 签到相关
    gold = IntegerField(default=30)
    num_sign = IntegerField(default=0)  # 总签到次数
    last_sign = DateField(default=0)

    # 武器
    q1_weapon = IntegerField(default=5)
    q5_weapon = IntegerField(default=5)
    weapon_limit = IntegerField(default=5)
    weapon_limit_max = IntegerField(default=5)

    # 食物
    q1_food = IntegerField(default=5)
    q5_food = IntegerField(default=5)
    food_limit = IntegerField(default=5)
    food_limit_max = IntegerField(default=5)
    
    limit_refresh_date = DateField(default=0)

    class Meta:
        table_name = "battle_player"

    def __str__(self):
        return f"id={self.id}, user_id={self.user_id}, group_id={self.group_id}"

    def refresh_limit(self):
        # 刷新limit状态
        today = datetime.datetime.now().date()
        if self.limit_refresh_date != today:
            self.food_limit = self.food_limit_max
            self.weapon_limit = self.weapon_limit_max
            self.limit_refresh_date = today
            self.save()
            return True
        return False

    def reborn(self):
        """ 复活 """
        self.health = self.health_max
        self.save()

    def is_dead(self):
        """ 判断玩家是否阵亡 """
        if self.health <= 0:
            if datetime.datetime.now() - self.dead_time < datetime.timedelta(seconds=REBORN_REMAIN_TIME):
                logger.info("阵亡中...")
                return True
            else:
                self.reborn()
                logger.info("复活！")
                return False
        return False

    def hit(self, player, weapon_level=0):
        """
        思路：如果自己或对方是阵亡状态，不执行任何操作，主要看返回值是否是整数，如果是就是造成了伤害。
        """
        # if self.is_dead():
        #     return

        # if player.is_dead():
        #     return

        self.refresh_limit()
        damage = random.randint(self.attack_min, self.attack_max)
        if weapon_level > 0:
            if self.weapon_limit == 0:
                return "武器额度不足！"

            if weapon_level == 1 and self.q1_weapon > 0:
                self.q1_weapon -= 1
                self.weapon_limit -= 1
                damage += Q1_WEAPON_DAMAGE
                self.save()

            elif weapon_level == 5 and self.q5_weapon > 0:
                self.q5_weapon -= 1
                self.weapon_limit -= 1
                damage += Q5_WEAPON_DAMAGE
                self.save()
            else:
                return f"Q{weapon_level}枪不足！"

        player.health = max(0, player.health - damage)
        if player.health <= 0:
            player.dead_time = datetime.datetime.now()

        player.save()
        return damage

    @staticmethod
    def field_status(name, value1, value2=None, add=0):
        add_msg = ""
        if add > 0:
            add_msg += f" (+{add})"
        if value2 is not None:
            return f"{name}: {value1}/{value2}{add_msg}\n"
        return f"{name}: {value1}{add_msg}\n"

    def status(self):
        self.refresh_limit()

        res = f"{cq.at(self.user_id)}当前状态: \n"

        if self.is_dead():
            res += f"阵亡中...({self.reborn_remain_time}秒后复活)\n"

        res += self.field_status('生命值', self.health, self.health_max)
        res += self.field_status('攻击力', self.attack_min, self.attack_max)
        res += self.field_status('黄金', self.gold)
        res += self.field_status('Q1枪', self.q1_weapon)
        res += self.field_status('Q5枪', self.q5_weapon)
        res += self.field_status('Q1面包', self.q1_food)
        res += self.field_status('Q5面包', self.q5_food)
        res += self.field_status('武器额度', self.weapon_limit, self.weapon_limit_max)
        res += self.field_status('食物额度', self.food_limit, self.food_limit_max)

        # res += f"生命值: {self.health}/{self.health_max}\n" \
        #        f"攻击力: {self.attack_min} ~ {self.attack_max}\n" \
        #        f"黄金: {self.gold}\n" \
        #        f"Q1枪: {self.q1_weapon}\n" \
        #        f"Q5枪: {self.q5_weapon}\n" \
        #        f"Q1面包: {self.q1_food}\n" \
        #        f"Q5面包: {self.q5_food}\n" \
        #        f"武器额度: ({self.weapon_limit}/{self.weapon_limit_max})\n" \
        #        f"食物额度: ({self.food_limit}/{self.food_limit_max})\n" \

        return res

    # 双击
    def sign(self, gold_add):
        if not self.is_sign_today:
            self.attack_min += 1
            self.attack_max += 1
            self.health_max += 2
            self.health += 2

            self.gold += gold_add
            self.last_sign = datetime.datetime.now().date()
            self.num_sign += 1
            self.save()
            return True
        return False

    # 吃食物
    def eat_food(self, level=1):
        self.refresh_limit()
        if level == 1 and self.q1_food > 0 and self.food_limit > 0:
            self.q1_food -= 1
            heal = Q1_FOOD_HEALTH
        elif level == 5 and self.q5_food > 0 and self.food_limit > 0:
            self.q5_food -= 1
            heal = Q5_FOOD_HEALTH
        else:
            return False

        self.food_limit -= 1
        self.health = min(self.health_max, self.health + heal)
        self.save()
        return True
    

    @property
    def is_sign_today(self):
        return datetime.datetime.now().date() == self.last_sign

    @property
    def reborn_remain_time(self):
        res = REBORN_REMAIN_TIME - (datetime.datetime.now() - self.dead_time).seconds
        return res


def get_player(user_id, group_id):
    """ 只有存在群员表里的成员会被夯 """
    logger.info(user_id, group_id)
    try:
        player = Player.get(user_id=user_id, group_id=group_id)
    except Player.DoesNotExist:
        member = GroupMember.get_obj(user_id=user_id, group_id=group_id)
        if member is not None:
            player = Player.create(user_id=user_id, group_id=group_id)
        else:
            return
    return player


def attack_someone_reply(attacker_user_id, defender_user_id, group_id, weapon_level=0):
    if not defender_user_id:
        return "404 Not Found"

    attacker = get_player(attacker_user_id, group_id)
    defender = get_player(defender_user_id, group_id)
    if attacker is None or defender is None:
        return "无法夯不在群里的人!"
        
    if attacker.is_dead():
        return f"{cq.at(attacker_user_id)}你都挂了还想揍人？{attacker.reborn_remain_time}秒后复活。"
    if defender.is_dead():
        return f"{cq.at(defender_user_id)}已经挂了。{defender.reborn_remain_time}秒后复活。"

    damage = attacker.hit(defender, weapon_level)
    if type(damage) is not int:
        return damage

    weapon_msg = ""
    if weapon_level > 0:
        weapon_msg = f"使用Q{weapon_level}枪(伤害+{WEAPON_DAMAGES[weapon_level]})"

    res = f"{cq.at(attacker_user_id)}{weapon_msg}夯了{cq.at(defender_user_id)}\n" \
          f"造成了{damage}点伤害\n"

    if defender.is_dead():
        gold = random.randint(5, 15)
        attacker.gold += gold
        attacker.save()
        res += f"{cq.at(defender_user_id)} 挂了，需要{REBORN_REMAIN_TIME}秒复活 \n"
        res += attacker.field_status('黄金', attacker.gold, add=gold)
    else:
        res += f"{cq.at(defender_user_id)} 当前生命值: ({defender.health}/{defender.health_max})"
    return res


def show_market():
    res = ""
    res += "食物:\n-------\n"
    for food in FOODS:
        res += f"Q{food['level']}面包: 回血+{food['recover']} ({food['price']}g)\n"

    res += "武器:\n-------\n"
    for weapon in WEAPONS:
        if weapon['level'] == 0:
            continue
        res += f"Q{weapon['level']}枪: 伤害+{weapon['damage']} ({weapon['price']}g)\n"

    res += "其他:\n-------\n"

    res += "活: 立即复活 (20g)\n"
    res += "输入: 买Q1枪 <数量>\n即可购买，不写数量默认买1个\n"
    return res


def sign_reply(user_id, group_id):
    user = get_player(user_id, group_id)
    if user:
        gold_add = random.randint(5, 20)
        is_sign = user.sign(gold_add)
        if not is_sign:
            return "今天已经签到过了!"
        
        res = "签到成功！\n"
        res += user.field_status('生命值', user.health, user.health_max, add=2)
        res += user.field_status('攻击力', user.attack_min, user.attack_max, add=1)
        res += user.field_status('黄金', user.gold, add=gold_add)
        user.refresh_limit()
        return res
    else:
        return "404 Not Found"


def get_item(item_name):
    for item in FOODS:
        if item['name'] == item_name:
            return item

    for item in WEAPONS:
        if item['name'] == item_name:
            return item


def buy_reply(user_id, group_id, item_name, item_num):
    item_name = item_name.lower()
    user = get_player(user_id, group_id)
    

    if item_name == "活":
        if not user.is_dead():
            return "你又没挂"

        if user.gold < 20:
            return "你钱不足"

        user.gold -= 20
        user.reborn()
        user.save()
        return "你活了"

    if user.is_dead():
        return "你挂了，买不了东西！"
        
    item = get_item(item_name)
    if not item:
        return ""
    
    spend_money = item['price'] * item_num
    if user.gold < spend_money:
        return "你钱不足"
    
    user.gold -= spend_money

    if item_name == 'q1枪':
        user.q1_weapon += item_num
    elif item_name == 'q5枪':
        user.q5_weapon += item_num
    elif item_name == 'q1面包':
        user.q1_food += item_num
    elif item_name == 'q5面包':
        user.q5_food += item_num

    user.save()
    return f"成功购买{item_name} x{item_num}"
    
    


create_tables([Player])
