import re


def at(user_id):
    """ https://docs.go-cqhttp.org/cqcode/#%E6%9F%90%E4%BA%BA """
    return "[CQ:at,qq=%s]" % user_id


def image(file):
    return "[CQ:image,file=file://%s]" % file


def get_at_user_id(message):
    match = re.search(r"\[CQ:at,qq=(.*?)]", message)
    if match:
        res = match.group(1)
        try:
            return int(res)
        except ValueError:
            return


if __name__ == '__main__':
    msg = "夯[CQ:at,qq='or 1=1 --]"
    print(get_at_user_id(msg))