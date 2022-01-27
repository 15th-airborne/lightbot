
from logging import critical


# ATTACK_MIN_LIMIT = 
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


