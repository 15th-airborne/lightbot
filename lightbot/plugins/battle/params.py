REBORN_REMAIN_TIME = 60 * 60 * 2  # 复活所需时间
REBORN_SPEND = 50  # 买活价格
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


ARMOR = {
    "q6":{
        "暴击": 0.07,  # 百分比 浮动0.01
        "小伤": 0.07,
        "大伤": 0.07,  
        "生命": 10,
        "":2,
    }
}