REBORN_REMAIN_TIME = 60 * 60 * 2  # 复活所需时间
REBORN_SPEND = 50  # 买活价格
ATTACK_COLD_TIME = 3  # 攻击冷却时间
DONATE_COOLDOWN = 60  # 捐钱冷却时间
FOODS = [
    {
        'name': 'q1面包',
        'level': 1,
        'recover': 2,
        'price': 5,

    },
    {
        'name': 'q5面包',
        'level': 5,
        'recover': 10,
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
        'damage': 2,
        'price': 1,
    },
    {
        'name': 'q5枪',
        'level': 5,
        'damage': 10,
        'price': 10,
    },
]

# 物资名称
GOODS_NAMES = {'g', '面包', '枪'}  # g表示黄金

# 装备类型
EQUIP_TYPES = ['helmet', 'armor', 'shoes']

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

