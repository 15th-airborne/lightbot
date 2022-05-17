import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# os.chdir()
# print("----------------", os.getcwd(), "----------------")
import asyncio
import aiohttp

from api import SendGroupMessage

class Bot:
    async def run(self):
        async with aiohttp.ClientSession() as session:
            self.session = session
            # self.ws = await session.ws_connect("ws://127.0.0.1:6700")
            async with session.ws_connect("ws://127.0.0.1:6700") as ws:
                self.ws = ws
                print('连接成功！')
                while True:
                    event = await self.ws.receive_json()
                    if event.get('message_type') == 'group':
                        print(event['sender']['nickname'], event['message'])
                        # 当有满足条件的事件发生时，创建一个task交给主循环即可
                        asyncio.create_task(self.repeat(event['message']))

    async def test(self):
        for i in range(100):
            await asyncio.sleep(3)
            api = SendGroupMessage(542423773, f'test{i}')
            await self.ws.send_json(api.json())

    async def repeat(self, msg):
        # 从连接池中获取一个连接
        async with self.session.ws_connect("ws://127.0.0.1:6700") as ws:
            api = SendGroupMessage(542423773, msg)
            await ws.send_json(api.json())
        
        # 使用run函数里面的ws连接
        # api = SendGroupMessage(542423773, msg)
        # await self.ws.send_json(api.json())

    async def main(self):
        task = asyncio.create_task(self.run())
        asyncio.create_task(self.test())
        await task

if __name__ == '__main__':
    bot = Bot()
    asyncio.run(bot.main())
