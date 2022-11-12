import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import aiohttp

from bot import BaseBot

import unittest
from unittest import IsolatedAsyncioTestCase
bot = BaseBot()

class Test(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        pass

    async def test_send_group_message(self):
        async with aiohttp.ClientSession() as session:
            bot.session = session
            await bot.send_group_msg(542423773, 'hello')

    # async def asyncTearDown(self):
    #     await self._async_connection.close()
    #     events.append("asyncTearDown")

if __name__ == '__main__':
    unittest.main()

