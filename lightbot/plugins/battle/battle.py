from plugin_manager import add_command_temp
from plugins.battle.models import Player, get_player, attack_someone_reply
from utils import cq


def get_user_id(event):
    user_id = cq.get_at_user_id(event['message'])
    if user_id is None:
        user_id = event['sender']['user_id']
    return user_id


@add_command_temp(keywords=["查看状态"])
async def check_player_status(bot, event):
    """ 查看玩家状态 """
    user_id = get_user_id(event)
    group_id = event['group_id']
    print(user_id, group_id)
    player = get_player(user_id, group_id)
    status = player.status()
    print(status)

    await bot.send_group_msg(group_id, status)


@add_command_temp(keywords=["揍"])
async def attack_someone(bot, event):
    """ 攻击某人 """
    attacker_user_id = event['sender']['user_id']
    defender_user_id = get_defender_user_id(event['message'])

    group_id = event['group_id']
    print(attacker_user_id, defender_user_id, group_id)
    msg = attack_someone_reply(attacker_user_id, defender_user_id, group_id)
    await bot.send_group_msg(group_id, msg)


def get_defender_user_id(message):
    return cq.get_at_user_id(message)

# 查看玩家状态
