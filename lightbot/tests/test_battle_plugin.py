import unittest
from database import database, GroupMember
from plugins.battle.models import get_player

# from peewee import SqliteDatabase
def fake_group_msg_event(msg, user_id=435786117, group_id=542423773, nickname='LightL'):
    event={
        'user_id': user_id,
        'group_id': group_id,
        'message': msg,
        'sender': {
            'user_id': user_id,
            'nickname': nickname
        }
    }
    return event
# 323566263


class TestEvent(unittest.TestCase):
    # def setUpClass(cls):
    #     pass
    
    def test_check_status_plugin(self):
        from plugins.battle import CheckStatusPlugin

        event = fake_group_msg_event('状态')
        plugin = CheckStatusPlugin(event)
        reply = plugin.get_reply()

        self.assertIn('升级所需经验', reply)
        self.assertIn('生命', reply)
    
    def test_goods_status_plugin(self):
        from plugins.battle import GoodsStatusPlugin

        event = fake_group_msg_event('物资')
        plugin = GoodsStatusPlugin(event)
        reply = plugin.get_reply()

        self.assertIn('面包', reply)
        self.assertIn('枪', reply)

    def test_attack_someone_plugin(self):
        from plugins.battle import AttackSomeonePlugin
        event = fake_group_msg_event('揍[CQ:at,qq=435786117]')
        
    def test_get_group_member(self):
        """ 测试demo """
        user = GroupMember.get_or_none(user_id=435786117, group_id=542423773)
        self.assertEqual(user.nickname, "梦见月球的猫")

    # @unittest.expectedFailure
    # def test_fail(self):
    #     """测试预计失败的"""
    #     self.assertEqual(1, 1, "broken")
