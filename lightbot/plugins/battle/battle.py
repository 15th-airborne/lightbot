from plugin_manager import GroupMessagePlugin
from .models import get_player, attack_someone_reply
from utils import cq


# def get_user_id(event):
#     user_id = cq.get_at_user_id(event['message'])
#     if user_id is None:
#         user_id = event['sender']['user_id']
#     return user_id


# @add_command_temp(keywords=["查看状态"])
# async def check_player_status(bot, event):
#     """ 查看玩家状态 """
#     user_id = get_user_id(event)
#     group_id = event['group_id']
#     print(user_id, group_id)
#     player = get_player(user_id, group_id)
#     status = player.status()
#     print(status)

#     await bot.send_group_msg(group_id, status)


class CheckStatusPlugin(GroupMessagePlugin):
    def __init__(self, event):
        super().__init__(event)
        self.user_id = self.get_user_id(event)
    

    def get_reply(self):
        if not self.message.startswith('查看状态'):
            return
        
        player = get_player(self.user_id, self.group_id)
        if player is not None:
            return player.status()

    def get_user_id(self, event):
        user_id = cq.get_at_user_id(event['message'])
        if user_id is None:
            user_id = event['sender']['user_id']
        return user_id


# @add_command_temp(keywords=["揍"])
# async def attack_someone(bot, event):
#     """ 攻击某人 """
#     attacker_user_id = event['sender']['user_id']
#     defender_user_id = get_defender_user_id(event['message'])

#     group_id = event['group_id']
#     print(attacker_user_id, defender_user_id, group_id)
#     msg = attack_someone_reply(attacker_user_id, defender_user_id, group_id)
#     await bot.send_group_msg(group_id, msg)


# def get_defender_user_id(message):
#     return cq.get_at_user_id(message)

# 查看玩家状态


class AttackSomeonePlugin(GroupMessagePlugin):
    def __init__(self, event):
        super().__init__(event)
        self.sender = event.get('sender', {})
        self.attacker_user_id = self.sender.get('user_id', None)
        self.defender_user_id = self.get_defender_user_id()
    
    # def is_activated(self):
    #     res = super().is_activated()
    #     if not res:
    #         return False
        
    #     for v in [self.sender, self.attacker_user_id, self.defender_user_id]:
    #         if v is None:
    #             return False
                
    #     return True

    def get_reply(self):
        if self.message.startswith('揍'):
            """ 攻击某人 """
            # attacker_user_id = event['sender']['user_id']
            # defender_user_id = get_defender_user_id(event['message'])

            # group_id = event['group_id']
            # print(attacker_user_id, defender_user_id, group_id)

            reply = attack_someone_reply(self.attacker_user_id, self.defender_user_id, self.group_id)
            return reply

    def get_defender_user_id(self):
        return cq.get_at_user_id(self.message)
