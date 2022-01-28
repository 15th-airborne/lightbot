from peewee import *
from logging import critical
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
    kind = CharField(max_length=30)  # 类型

    attr1 = CharField(max_length=30)  # 属性1
    value1 = FloatField()

    attr2 = CharField(max_length=30)  # 属性1
    value2 = FloatField()



def create_equipment(level=5):
    equip_kind = random.choices(EQUIP_TYPES, weights=[0.6, 0.3, 0.1])[0]
    attr1, attr2 = random.choices(ATTRIBUTES, k=2)
    min_val, max_val = EQUIP_LEVEL[level]
    value1 = random.uniform(min_val, max_val)
    value2 = random.uniform(min_val, max_val)

