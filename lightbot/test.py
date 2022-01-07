import unittest
from message import get_cq_code
from bot import Bot


class TestEvent(unittest.TestCase):
    def test_get_cq_code(self):
        """ 测试是否能获得正确的CQ码 """
        data = {"url": "https://www.baidu.com", "title": "百度"}
        text = get_cq_code(type_="share", url="https://www.baidu.com", title="百度")

        self.assertEqual(text, "[CQ:share,url=https://www.baidu.com,title=百度]")

    def test_at(self):
        """ 测试是否能正确at某人 """
        bot = Bot()
        text = bot.at(user_id=123456)
        self.assertEqual(text, "[CQ:at,qq=123456]")




if __name__ == '__main__':
    unittest.main()