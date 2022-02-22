import re


def at(user_id):
    """ https://docs.go-cqhttp.org/cqcode/#%E6%9F%90%E4%BA%BA """
    return f"[CQ:at,qq={user_id}]" 


def image(file):
    """ 构建图片CQ码 """
    return f"[CQ:image,file=file://{file}]"


def get_at_user_id(message) -> int: 
    """ 搜索并返回消息中第一个出现的qq号 """
    match = re.search(r"\[CQ:at,qq=(.*?)]", message)
    if match:
        res = match.group(1)
        try:
            return int(res)
        except ValueError:
            return


if __name__ == '__main__':
    pass