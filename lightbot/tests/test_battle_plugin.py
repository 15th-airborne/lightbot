import unittest
from database import database, GroupMember
# from plugins.battle.models import get_player

event = {
    'message': 'setu',
    'group_id': 542423773,
    'sender': {
        'user_id': 435786117
    }
}


class TestEvent(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_group_member(self):
        """ 测试demo """
        user = GroupMember.get_or_none(user_id=435786117, group_id=542423773)
        self.assertEqual(user.nickname, "梦见月球的猫")

    # @unittest.expectedFailure
    # def test_fail(self):
    #     """测试预计失败的"""
    #     self.assertEqual(1, 1, "broken")
