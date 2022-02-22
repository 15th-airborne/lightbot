import datetime

from peewee import *
from .params import EQUIP_TYPES, ATTRIBUTES, EQUIP_LEVEL
import random

# ATTACK_MIN_LIMIT = 

damage = 1 # x
class Equipment:
    def __init__(self):
        self._attack_min = 0  # 小伤
        self._attack_max = 0  # 大伤
        self._critical = 0  # 暴击率
        self._evade = 0  # 闪避率
        self._hit_rate = 0  # 命中率
        self._hp = 0  # 生命值
        self._gold = 0  # 黄金

    @property
    def critical(self):
        return self._critical

    @critical.setter
    def critical(self, val):
        self._critical = max(40, val)

    @property
    def evade(self):
        return self._evade

    @evade.setter
    def evade(self, val):
        self._evade = max(40, val)


class Equipment:
    user_id = BigIntegerField()  # 所属人(Q号)
    group_id = BigIntegerField()  # 所属群
    kind = CharField(max_length=30)  # 类型
    rarity = IntegerField()  # 稀有度
    level = IntegerField(default=1)  # 强化等级

    base_attr1 = CharField(max_length=30)  # 基础属性1
    base_value1 = FloatField()

    base_attr2 = CharField(max_length=30)  # 基础属性2
    base_value2 = FloatField()

    attr1 = CharField(max_length=30)  # 额外属性1
    value1 = FloatField() 

    attr2 = CharField(max_length=30)  # 额外属性2
    value2 = FloatField()

    c_time = DateTimeField(default=datetime.datetime.now)  # 创建时间



def create_equipment(level=5):
    equip_kind = random.choices(EQUIP_TYPES, weights=[0.6, 0.3, 0.1])[0]
    attr1, attr2 = random.choices(ATTRIBUTES, k=2)
    min_val, max_val = EQUIP_LEVEL[level]
    value1 = random.uniform(min_val, max_val)
    value2 = random.uniform(min_val, max_val)

