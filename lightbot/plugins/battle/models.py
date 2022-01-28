"""
数据库模型文件

"""
import datetime
from email.policy import default
import random
from this import d
from xmlrpc.client import MININT

from peewee import *

from database import create_tables, BaseModel
from database.models import GroupMember
from .params import (
    REBORN_REMAIN_TIME, FOODS, WEAPONS, REBORN_SPEND,
    ATTACK_COLD_TIME
)
from utils import cq
import logging
logger = logging.getLogger(__name__)

from config import QQ


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


# class Equipment(BaseModel):
#     player = ForeignKeyField('Player', backref='equipments')  # 用户
#     level = IntegerField()  # 装备等级  Q5 Q6

#     attack_min = FloatField()
#     attack_max = FloatField()
#     health_max = IntegerField()

#     attack_max = FloatField()
#     attack_max = FloatField()





class Player(BaseModel):
    user_id = BigIntegerField()  # Q号
    group_id = BigIntegerField()  # 群号
    health = IntegerField(default=30)  # 生命值
    health_max = IntegerField(default=30)  # 生命上限
    attack_min = IntegerField(default=2)  # 最小攻击力
    attack_max = IntegerField(default=12)  # 最大攻击力

    dead_time = TimestampField(default=0)  # 死亡时间

    # 签到相关
    gold = IntegerField(default=30)  # 黄金
    num_sign = IntegerField(default=0)  # 总签到次数
    last_sign = DateField(default=0)  # 最近签到时间

    # 武器
    q1_weapon = IntegerField(default=5)  # Q1武器数量
    q5_weapon = IntegerField(default=5)  # Q5武器数量
    weapon_limit = IntegerField(default=5)  # 武器使用上限
    weapon_limit_max = IntegerField(default=5)  # 武器使用最大上限

    # 食物
    q1_food = IntegerField(default=5)  # 
    q5_food = IntegerField(default=5)
    food_limit = IntegerField(default=5)
    food_limit_max = IntegerField(default=5)
    
    limit_refresh_date = DateField(default=0)

    # 统计
    kill = IntegerField(default=0)  # 击杀数
    dead = IntegerField(default=0)  # 死亡数
    attack_num = IntegerField(default=0)  # 攻击次数
    defend_num = IntegerField(default=0)  # 防御次数

    # 属性值
    # 命中 (实际命中 = 100 + 攻击者命中 - 防御者闪避)
    hit_rate = FloatField(default=0.05)

    # 闪避 
    evade = FloatField(default=0.15)
    # 暴击
    critical = FloatField(default=0.15)

    # 体力
    energy =  IntegerField(default=20)  # 体力值
    energy_limit =  IntegerField(default=20)  # 体力值上限
    
    # 最后一次攻击的时间
    last_hit_time = DateTimeField(default=datetime.datetime.now)


    # 装备
    # helmet = ForeignKeyField(Equipment, default=None)  # 头盔
    # armor = ForeignKeyField(Equipment, default=None)  # 盔甲
    # shoes = ForeignKeyField(Equipment, default=None)  # 鞋子

    # armor = IntegerField()  # 盔甲
    # shoes = IntegerField()  # 鞋子
    # equipments = IntegerField()  # 未装备的装备



    class Meta:
        table_name = "battle_player"

    def __str__(self):
        return f"id={self.id}, user_id={self.user_id}, group_id={self.group_id}"

    def refresh_status(self):
        # 刷新limit状态
        today = datetime.datetime.now().date()
        if self.limit_refresh_date != today:
            self.food_limit = self.food_limit_max
            self.weapon_limit = self.weapon_limit_max
            self.energy = self.energy_limit

            self.health = self.health_max
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

    # def hit(self, defender, damage, weapon_level=0):
    #     """        """
    #     # if self.is_dead():
    #     #     return

    #     # if player.is_dead():
    #     #     return
    #     damage = random.randint(self.attack_min, self.attack_max)



    #     if weapon_level > 0:
    #         if self.weapon_limit == 0:
    #             return "武器额度不足！"

    #         if weapon_level == 1 and self.q1_weapon > 0:
    #             self.q1_weapon -= 1
    #             self.weapon_limit -= 1
    #             damage += Q1_WEAPON_DAMAGE

    #         elif weapon_level == 5 and self.q5_weapon > 0:
    #             self.q5_weapon -= 1
    #             self.weapon_limit -= 1
    #             damage += Q5_WEAPON_DAMAGE
                
    #         else:
    #             return f"Q{weapon_level}枪不足！"

    #     defender.health = max(0, defender.health - damage)
    #     if defender.health <= 0:
    #         defender.dead_time = datetime.datetime.now()

    #     defender.save()
    #     self.save()
    #     return damage

    @staticmethod
    def field_status(name, value1, value2=None, add=0, unit=''):
        add_msg = ""
        if add != 0:
            flag = "+" if add >= 0 else "-"
            add_msg += f" ({flag}{add})"
        if value2 is not None:
            return f"{name}: {value1}/{value2}{add_msg}\n"

        return f"{name}: {value1}{unit}{add_msg}\n"

    def status(self):
        self.refresh_status()

        res = f"{cq.at(self.user_id)}当前状态: \n"

        if self.is_dead():
            res += f"阵亡中...({self.reborn_remain_time}复活)\n"

        res += self.field_status('生命值', self.health, self.health_max)
        res += self.field_status('攻击力', self.attack_min, self.attack_max)
        res += self.field_status('命中率', self.hit_rate * 100, unit="%")
        res += self.field_status('闪避率', self.evade * 100, unit="%")
        res += self.field_status('暴击率', self.critical * 100, unit="%")
        res += self.field_status('击杀数', self.kill)
        res += self.field_status('阵亡数', self.dead)
        res += self.field_status('体力值', self.energy, self.energy_limit)

        res += self.field_status('黄金', self.gold)
        res += self.field_status('Q1枪', self.q1_weapon)
        res += self.field_status('Q5枪', self.q5_weapon)
        res += self.field_status('Q1面包', self.q1_food)
        res += self.field_status('Q5面包', self.q5_food)
        res += self.field_status('食物额度', self.food_limit, self.food_limit_max)

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
        self.refresh_status()
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
        # res = REBORN_REMAIN_TIME - (datetime.datetime.now() - self.dead_time).seconds
        #
        dt = self.dead_time + datetime.timedelta(seconds=7200)
        return dt.strftime("%X")


def foo(user_id, group_id):
    for row in Player.select(Player, Equipment).join(Equipment).where(user_id=user_id, group_id=group_id).dicts():
        pass

def get_player(user_id, group_id):
    """ 只有存在群员表里的成员会被夯 """
    # logger.info(user_id, group_id)
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
    res = ""


    if not defender_user_id:
        return "找不到你要夯的人(长按头像)"


    attacker = get_player(attacker_user_id, group_id)
    defender = get_player(defender_user_id, group_id)

    # 管理员判定
    if int(defender_user_id) == QQ:
        attacker_user_id, defender_user_id = defender_user_id, attacker_user_id
        attacker, defender = defender, attacker
        # res += "居然敢夯我?!\n(夯小月不成反被夯)\n"
    
    # 冷却判定
    now = datetime.datetime.now()
    d = (now - attacker.last_hit_time).total_seconds()
    if d <= ATTACK_COLD_TIME:
        return "攻击还有%.3f秒冷却" % (ATTACK_COLD_TIME - d)

    attacker.refresh_status()
    defender.refresh_status()

    if defender is None or attacker is None:
        return "无法夯不在群里的人!"

    
    # 判断是否阵亡
    if attacker.is_dead():
        return f"{cq.at(attacker_user_id)}你都挂了还想揍人？\n{attacker.reborn_remain_time}复活。"
    if defender.is_dead():
        return f"{cq.at(defender_user_id)}已经挂了。\n{defender.reborn_remain_time}复活。"

    # 体力判定
    if attacker.energy == 0:
        return f"{cq.at(attacker_user_id)}体力值为0，无法攻击！"

    # 命中判定
    hit_rate = 1 + attacker.hit_rate - defender.evade
    if random.random() > hit_rate:
        return f"{cq.at(attacker_user_id)}的攻击Miss了！"

    # 伤害判定
    damage = random.randint(attacker.attack_min, attacker.attack_max)


    # 武器判定
    weapon_msg = ""
    if weapon_level > 0:
        if weapon_level == 1 and attacker.q1_weapon > 0:
            attacker.q1_weapon -= 1
            damage += Q1_WEAPON_DAMAGE
        elif weapon_level == 5 and attacker.q5_weapon > 0:
            attacker.q5_weapon -= 1
            damage += Q5_WEAPON_DAMAGE
        else:
            return f"Q{weapon_level}枪不足！"

        weapon_msg = f"使用Q{weapon_level}枪(伤害+{WEAPON_DAMAGES[weapon_level]})"


    # 暴击判定
    critical_msg = ""
    if random.random() < attacker.critical:
        critical_msg = "(暴击!)"
        damage *= 2
    
    #  伤害判定
    defender.health = max(0, defender.health - damage)

    # 阵亡判定
    if defender.health <= 0:
        defender.dead_time = datetime.datetime.now()

    res += f"{cq.at(attacker_user_id)}{weapon_msg}夯了{cq.at(defender_user_id)}\n" \
          f"造成了{damage}点伤害{critical_msg}\n"

    if defender.is_dead():
        gold = random.randint(5, 15)
        attacker.gold += gold
        attacker.kill += 1
        defender.dead += 1
        
        res += f"{cq.at(defender_user_id)} 挂了，{defender.reborn_remain_time}复活 \n"
        res += attacker.field_status('黄金', attacker.gold, add=gold)
        res += f"击杀数+1(当前:{attacker.kill})\n"
    else:
        res += f"{cq.at(defender_user_id)} 当前生命值: ({defender.health}/{defender.health_max})"

    # 数据更新
    attacker.last_hit_time = now
    attacker.attack_num += 1
    defender.defend_num += 1
    attacker.energy -= 1
    defender.save()
    attacker.save()
    return res


def show_market():
    res = ""
    res += "食物:\n-------\n"
    for food in FOODS:
        res += f"Q{food['level']}面包: 体力+{food['recover']} ({food['price']}g)\n"

    res += "武器:\n-------\n"
    for weapon in WEAPONS:
        if weapon['level'] == 0:
            continue
        res += f"Q{weapon['level']}枪: 伤害+{weapon['damage']} ({weapon['price']}g)\n"

    res += "其他:\n-------\n"

    res += "活: 立即复活 (%sg)\n" % REBORN_SPEND
    res += "输入: 买Q1枪 <数量>\n即可购买，不写数量默认买1个\n"
    return res


def sign_reply(user_id, group_id):
    user = get_player(user_id, group_id)
    if user:
        gold_add = random.randint(5, 20)
        is_sign = user.sign(gold_add)
        if not is_sign:
            return "今天已经签到过了!"
        user.refresh_status()
        res = "签到成功！\n"
        res += user.field_status('生命值', user.health, user.health_max, add=2)
        res += user.field_status('攻击力', user.attack_min, user.attack_max, add=1)
        res += user.field_status('黄金', user.gold, add=gold_add)
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

        if user.gold < REBORN_SPEND:
            return "你钱不足"

        user.gold -= REBORN_SPEND
        user.reborn()
        user.save()
        return "你活了" + user.field_status('黄金', user.gold, add=-REBORN_SPEND)

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
