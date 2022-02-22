REBORN_REMAIN_TIME = 60 * 60 * 2  # 复活所需时间
REBORN_SPEND = 200  # 买活价格
WASH_POINTS_SPEND = 200 # 洗点价格
ATTACK_COLD_TIME = 3  # 攻击冷却时间
DONATE_COOLDOWN = 60  # 捐钱冷却时间
FOODS = [
    {
        'name': 'q1面包',
        'level': 1,
        'recover': 1,
        'price': 5,

    },
    {
        'name': 'q5面包',
        'level': 5,
        'recover': 5,
        'price': 50
    }
]

WEAPONS = [
    {
        'name': '空手',
        'level': 0,
        'damage': 0,
        
    },
    {
        'name': 'q1枪',
        'level': 1,
        'damage': 0.1,
        'price': 5,
    },
    {
        'name': 'q5枪',
        'level': 5,
        'damage': 0.5,
        'price': 50,
    },
]

    # _base_health_max = 20  # 基础生命值
    # _base_damage = 4
    # _base_attack_min = 1  # 基础小伤加成倍率
    # _base_attack_max = 2  # 基础大伤加成倍率-> 伤害相当于 4 ~ 4*2
    # _base_hit_rate = 0.05  # 基础命中率
    # _base_evade = 0.15  # 基础闪避率
    # _base_critical = 0.15  # 基础暴击率
    # _base_counter_attack = 0.15  # 基础反击率

ATTRIBUTE_POINTS = {
    'health_max': 5,
    'damage': 1,
    # 'attack_min': 0.01,
    # 'attack_max': 0.02,
    'hit_rate': 0.015   ,
    'evade': 0.01,
    'critical': 0.01,
    'counter_attack': 0.01,
}

# 物资名称
GOODS_NAMES = {'g', '面包', '枪'}  # g表示黄金

# 装备类型
EQUIP_TYPES = ['weapon', 'armor', 'jewelry']

# 获取某类型装备的权重
EQUIP_TYPE_WEIGHTS = [0.4, 0.4, 0.2]

# 属性
ATTRIBUTES = [
    'attack_min',  # 小伤
    'attack_max',  # 大伤
    'critical',  # 暴击率
    'evade',  # 闪避率
    'hit_rate',  # 命中率
    'health',  # 生命值
]

# 等级对应的属性
EQUIP_LEVEL = {
    5: [0.04, 0.06],
    6: [0.06, 0.08],
}

