import re
from .params import GOODS_NAMES

def check_num(num, default=0, limit=None):
    try:
        num = int(num)
        num = max(0, num)
        if limit:
            num = min(limit, num)
        return num
    except ValueError:
        return default


def get_item_level_and_name(item, default_level=0, default_name=None):
    """
    例：
    - input: Q5面包 return: (5, 面包)
    - input: q123啦啦啦 return: (123, 啦啦啦)
    - input q枪 return: (0, 枪)
    
    """
    item = item.lower()
    if not item.startswith('q'):
        return default_level, default_name

    # 匹配等级和物品名称
    level = re.search(r'q(\d+)', item)
    name = re.search(r'q\d(.+)', item)

    level = level.group(1) if level else default_level
    name = name.group(1) if name else default_name

    # 检查整型
    level = check_num(level, default=default_level, limit=5)
    
    # 确保物品名存在
    if name not in GOODS_NAMES:
        name = default_name

    return level, name