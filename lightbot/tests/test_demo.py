import unittest
from message import get_cq_code

class TestEvent(unittest.TestCase):
    def setUp(self):
        pass

    def test_demo(self):
        """ 测试demo """
        self.assertEqual(2+3, 5)

    @unittest.expectedFailure
    def test_fail(self):
        """测试预计失败的"""
        self.assertEqual(1, 1, "broken")
