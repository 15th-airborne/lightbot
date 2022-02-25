"""
数据库模型文件

"""
import datetime
import random

from peewee import *

from database import create_tables, BaseModel, PublicVariable
from database.models import GroupMember
from .params import (
    REBORN_REMAIN_TIME, FOODS, WEAPONS, REBORN_SPEND, WASH_POINTS_SPEND,
    ATTACK_COLD_TIME, ATTRIBUTE_POINTS, BASE_ATTR_POINTS, LEVEL_ATTR_POINTS
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

Q1_WEAPON_DAMAGE = 0.1
Q5_WEAPON_DAMAGE = 0.5


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

    exp = IntegerField(default=0, column_name='exp')  # 总经验值
    level = IntegerField(default=1)  # 等级
    level_up_exp = IntegerField(default=100)  # 升级所需经验值

    # 属性值 加点
    health = IntegerField(default=30, column_name='health')  # 生命值

    _health_max = IntegerField(default=0, column_name='health_max')  # 生命上限
    _damage = IntegerField(default=0, column_name='damage')  # 伤害

    _attack_min = FloatField(default=0, column_name='attack_min')  # 最小攻击力伤害加成
    _attack_max = FloatField(default=0, column_name='attack_max')  # 最大攻击力伤害加成

    # 命中 (实际命中 = 100 + 攻击者命中 - 防御者闪避)
    _hit_rate = IntegerField(default=0, column_name='hit_rate')
    # 闪避 
    _evade = IntegerField(default=0, column_name='evade')
    # 暴击
    _critical = IntegerField(default=0, column_name='critical')
    # 反击
    _counter_attack = IntegerField(default=0, column_name='counter_attack')

    # 体力
    energy =  IntegerField(default=20, column_name='energy')  # 体力值
    energy_limit =  IntegerField(default=20, column_name='energy_limit')  # 体力值上限
    
    # 最后一次攻击的时间
    last_hit_time = DateTimeField(default=datetime.datetime.now)

    # 补偿g
    supply_gold = IntegerField(default=0)
    
    _base_health_max = 200  # 基础生命值
    _base_damage = 40
    _base_attack_min = 1  # 基础小伤加成倍率
    _base_attack_max = 2  # 基础大伤加成倍率-> 伤害相当于 4 ~ 4*2
    _base_hit_rate = 0.05  # 基础命中率
    _base_evade = 0.1  # 基础闪避率
    _base_critical = 0.1  # 基础暴击率
    _base_counter_attack = 0.05  # 基础反击率

    class Meta:
        table_name = "battle_player"

    @property
    def health_max(self):
        return self._base_health_max + self._health_max * ATTRIBUTE_POINTS['health_max']

    @property
    def damage(self):
        return self._base_damage + self._damage * ATTRIBUTE_POINTS['damage']

    @property
    def hit_rate(self):
        return self._base_hit_rate + self._hit_rate * ATTRIBUTE_POINTS['hit_rate']
    
    @property
    def evade(self):
        return self._base_evade + self._evade * ATTRIBUTE_POINTS['evade']
    
    @property
    def critical(self):
        return self._base_critical + self._critical * ATTRIBUTE_POINTS['critical']

    @property
    def counter_attack(self):
        return self._base_counter_attack + self._counter_attack * ATTRIBUTE_POINTS['counter_attack']

    @property
    def attack_min(self):
        return int(self.damage * (self._base_attack_min + self._attack_min))

    @property
    def attack_max(self):
        return int(self.damage * (self._base_attack_max + self._attack_max))

    # 等级
    # @property
    # def level(self):
    #     self.num_sign
    #     return self.level * 2

    # 总属性点
    @property
    def total_attr_points(self):
        return self.level * LEVEL_ATTR_POINTS + BASE_ATTR_POINTS

    # 可用属性点
    @property
    def curr_attr_points(self):
        return self.total_attr_points - self._health_max - self._damage \
            - self._hit_rate - self._evade\
            - self._critical - self._counter_attack

    def wash_points(self):
        self._health_max = 0
        self.health = min(self.health_max, self.health)

        self._damage = 0
        self._hit_rate = 0
        self._evade = 0
        self._critical = 0
        self._counter_attack = 0
        self.save()

    # # 升级
    # def level_up(self):

    #     pass

    # @property
    # def exp(self):
    #     return self._exp

    
    # 获取升级所需经验值
    @staticmethod
    def get_level_up_exp(level):
        """
        等级 天数 总共 每级经验
        20   20   20    100
        30   20   40    200
        40   40   80    400
        50   80   160   800
        60   160  320   1600
        """
        if level <= 20:
            return 100
        elif level <= 30:
            return 200
        elif level <= 40:
            return 400
        elif level <= 50:
            return 800
        else:
            return 1600

    # 获得经验
    def get_exp(self, new_exp):
        assert new_exp >= 0
        self.exp += new_exp

        while new_exp > 0:
            if new_exp >= self.level_up_exp:
                self.level += 1
                new_exp -= self.level_up_exp
                self.level_up_exp = self.get_level_up_exp(self.level)
            else:
                self.level_up_exp -= new_exp
                break

    
    # 装备
    # helmet = ForeignKeyField(Equipment, default=None)  # 头盔
    # armor = ForeignKeyField(Equipment, default=None)  # 盔甲
    # shoes = ForeignKeyField(Equipment, default=None)  # 鞋子

    # armor = IntegerField()  # 盔甲
    # shoes = IntegerField()  # 鞋子
    # equipments = IntegerField()  # 未装备的装备



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
    def attr_change(name, a):
        pass


    @staticmethod
    def field_status(name, *values, add=0, unit='', end='\n'):
        add_msg = ""
        if add != 0:
            flag = "+" if add >= 0 else ""
            add_msg += f" ({flag}{add}{unit})"
        values = [str(round(v, 1)) + unit for v in values]
        values = "/".join(values)

        return f"{name}: {values}{add_msg}{end}"

    # def kda_status(self):
    #     return f"击杀/死亡: {self.kill}/{self.dead}"

    def status(self):
        self.refresh_status()

        res = f"{cq.at(self.user_id)}({self.level}级)当前状态: \n"

        if self.is_dead():
            res += f"阵亡中...({self.reborn_remain_time}复活)\n"
        res += self.field_status('升级所需经验', self.level_up_exp)
        res += self.field_status('生命', self.health, self.health_max, end=" ")
        res += self.field_status('体力', self.energy, self.energy_limit)
        res += self.field_status('攻击', self.attack_min, self.attack_max)
        res += self.field_status("击杀\阵亡", self.kill, self.dead)
        res += self.field_status('黄金', self.gold)
        
        # res += self.field_status("闪避\反击", self.evade * 100, self.counter_attack * 100, unit="%")
        # res += self.field_status("命中\暴击", self.hit_rate * 100, self.critical * 100, unit="%")
        # res += self.field_status('可用属性点', self.curr_attr_points)

        return res

    def goods_status(self):
        res = ""
        res += self.field_status('黄金', self.gold)
        res += self.field_status('Q1/Q5 面包', self.q1_food, self.q5_food)
        # res += self.field_status('Q5枪/面包', self.q5_weapon, self.q5_food)
        res += self.field_status('食物额度', self.food_limit, self.food_limit_max)
        return res

    # 双击
    def sign(self, gold_add):
        if not self.is_sign_today:
            self.get_exp(100)
            # self.attack_min += 1
            # self.attack_max += 1
            # self.health_max += 2
            # self.health += 2

            self.gold += gold_add
            self.last_sign = datetime.datetime.now().date()
            self.num_sign += 1
            self.save()
            return True
        return False

    # 吃食物
    @property
    def is_sign_today(self):
        return datetime.datetime.now().date() == self.last_sign

    @property
    def reborn_remain_time(self):
        # res = REBORN_REMAIN_TIME - (datetime.datetime.now() - self.dead_time).seconds
        #
        dt = self.dead_time + datetime.timedelta(seconds=7200)
        return dt.strftime("%X")


# def foo(user_id, group_id):
#     for row in Player.select(Player, Equipment).join(Equipment).where(user_id=user_id, group_id=group_id).dicts():
#         pass

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

    # # 命中判定
    # hit_rate = 1 + attacker.hit_rate - defender.evade
    # if random.random() > hit_rate:
    #     return f"{cq.at(attacker_user_id)}的攻击Miss了！"

    # # 伤害判定
    # damage = random.randint(attacker.attack_min, attacker.attack_max)


    # # 武器判定
    # weapon_msg = ""
    # if weapon_level > 0:
    #     if weapon_level == 1 and attacker.q1_weapon > 0:
    #         attacker.q1_weapon -= 1
    #         add_damage = int(damage * Q1_WEAPON_DAMAGE)
    #     elif weapon_level == 5 and attacker.q5_weapon > 0:
    #         attacker.q5_weapon -= 1
    #         add_damage = int(damage * Q5_WEAPON_DAMAGE)
            
    #     else:
    #         return f"Q{weapon_level}枪不足！"

    #     damage += add_damage
    #     weapon_msg = f"使用Q{weapon_level}枪(伤害+{add_damage})"


    # # 暴击判定
    # critical_msg = ""
    # if random.random() < attacker.critical:
    #     critical_msg = "(暴击!)"
    #     damage *= 2
    
    # #  伤害判定
    # defender.health = max(0, defender.health - damage)

    # # 阵亡判定
    # if defender.health <= 0:
    #     defender.dead_time = datetime.datetime.now()

    # res += f"{cq.at(attacker_user_id)}{weapon_msg}夯了{cq.at(defender_user_id)}\n" \
    #       f"造成了{damage}点伤害{critical_msg}\n"

    # if defender.is_dead():
    #     gold = random.randint(15, 30)
    #     gold += defender.num_sign * 3

    #     attacker.gold += gold
    #     attacker.kill += 1
    #     defender.dead += 1
        
    #     res += f"{cq.at(defender_user_id)} 挂了，{defender.reborn_remain_time}复活 \n"
    #     res += attacker.field_status('黄金', attacker.gold, add=gold)
    #     res += f"击杀数+1(当前:{attacker.kill})\n"
    # else:
    #     res += f"{cq.at(defender_user_id)} 当前生命值: ({defender.health}/{defender.health_max})"

    res = attack_help(attacker, defender, weapon_level=weapon_level)

    # 反击判定
    if not defender.is_dead() and random.random() < defender.counter_attack:
        res += "触发反击!\n"
        res += attack_help(defender, attacker, weapon_level=0)

    #
    #     counter_attack_msg = ""
    #     if random.random() < defender.counter_attack:
    #         res += "触发反击!\n"
    #         damage *= random.randint(defender.attack_min, defender.attack_max)

    #         # 暴击判定

    #         # 命中判定
    #         hit_rate = 1 + defender.hit_rate - attacker.evade
    #         if random.random() > hit_rate:
    #             return f"{cq.at(attacker_user_id)}的反击Miss了！"

    # 数据更新
    attacker.last_hit_time = now
    attacker.attack_num += 1
    defender.defend_num += 1
    attacker.energy -= 1
    defender.save()
    attacker.save()
    return res

# 攻击判定辅助
def attack_help(attacker, defender, weapon_level=0):
    res = ""
    # 命中判定
    hit_rate = 1 + attacker.hit_rate - defender.evade
    if random.random() > hit_rate:
        return f"{cq.at(attacker.user_id)}的攻击Miss了！"

    # 伤害判定
    damage = random.randint(attacker.attack_min, attacker.attack_max)

    # 武器判定
    weapon_msg = ""
    if weapon_level > 0:
        if weapon_level == 1 and attacker.q1_weapon > 0:
            attacker.q1_weapon -= 1
            add_damage = int(damage * Q1_WEAPON_DAMAGE)
        elif weapon_level == 5 and attacker.q5_weapon > 0:
            attacker.q5_weapon -= 1
            add_damage = int(damage * Q5_WEAPON_DAMAGE)
            
        else:
            return f"Q{weapon_level}枪不足！"

        damage += add_damage
        weapon_msg = f"使用Q{weapon_level}枪(伤害+{add_damage})"


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

    res += f"{cq.at(attacker.user_id)}{weapon_msg}夯了{cq.at(defender.user_id)}\n" \
          f"造成了{damage}点伤害{critical_msg}\n"

    if defender.is_dead():
        gold = random.randint(15, 30)
        gold += defender.num_sign * 3

        attacker.gold += gold
        attacker.kill += 1
        defender.dead += 1
        
        res += f"{cq.at(defender.user_id)} 挂了，{defender.reborn_remain_time}复活 \n"
        res += attacker.field_status('黄金', attacker.gold, add=gold)
        res += f"击杀数+1(当前:{attacker.kill})\n"
    else:
        res += f"{cq.at(defender.user_id)} 当前生命值: ({defender.health}/{defender.health_max})\n"

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
        res += f"Q{weapon['level']}枪: 伤害+{weapon['damage'] * 100}% ({weapon['price']}g)\n"

    res += "其他:\n-------\n"

    res += "活: 立即复活 (%sg)\n" % REBORN_SPEND
    res += "洗点: 属性归零 (%sg)\n" % WASH_POINTS_SPEND

    res += "输入: 买Q1枪 <数量>\n即可购买，不写数量默认买1个\n"
    return res


def sign_reply(user_id, group_id):
    player = get_player(user_id, group_id)
    if player:
        gold_add = random.randint(50, 150)
        old_level = player.level
        is_sign = player.sign(gold_add)
        
        if not is_sign:
            return "今天已经签到过了!"
        player.refresh_status()
        res = f"{cq.at(player.user_id)}签到成功！\n经验+100\n"

        if player.level > old_level:
            res += f"升级了！获得{LEVEL_ATTR_POINTS}属性点！\n"

        res += f"当前等级: {player.level}\n"

        bonus_pool = PublicVariable.get_obj(player.group_id, name='奖金池')
        bonus_pool.value += 10
        bonus_pool.save()
        
        res += player.field_status('黄金', player.gold, add=gold_add)
        res += player.field_status('奖池', bonus_pool.value, add=10)
            
        # res += user.field_status('生命值', user.health, user.health_max, add=2)
        # res += user.field_status('攻击力', user.attack_min, user.attack_max, add=1)
        
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

    if item_name == '洗点':
        if user.gold < WASH_POINTS_SPEND:
            return f"你钱不足,需要{WASH_POINTS_SPEND}g"
        user.wash_points()
        user.gold -= WASH_POINTS_SPEND
        res = user.field_status('黄金', user.gold, add=-WASH_POINTS_SPEND)
        res += f"洗点成功，可用属性:{user.curr_attr_points}"
        user.save()
        return res

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
