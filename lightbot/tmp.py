import os

# os.chdir(os.path.dirname(os.path.dirname(__file__)))
# print("----------------", os.getcwd(), "----------------")
import asyncio
import aiohttp

from bot import BaseBot


if __name__ == '__main__':
    bot = BaseBot()
    asyncio.run(bot.main())
