import os

# os.chdir(os.path.dirname(os.path.dirname(__file__)))
# print("----------------", os.getcwd(), "----------------")
import asyncio
import aiohttp

from api import SendGroupMessage

class Demo:
    async def run(self):
        async with aiohttp.ClientSession() as session:
            # self.ws = await session.ws_connect("ws://127.0.0.1:6700")
            async with session.ws_connect("ws://127.0.0.1:6700") as ws:
                self.ws = ws
                print('连接成功！')
                while True:
                    event = await self.ws.receive_json()
                    if event.get('message_type') == 'group':
                        print(event['sender']['nickname'], event['message'])
                        asyncio.create_task(self.repeat(event['message']))

    async def test(self):
        for i in range(100):
            await asyncio.sleep(3)
            api = SendGroupMessage(542423773, f'test{i}')
            await self.ws.send_json(api.json())

    async def repeat(self, msg):
        api = SendGroupMessage(542423773, msg)
        await self.ws.send_json(api.json())

    async def main(self):
        task = asyncio.create_task(self.run())
        asyncio.create_task(self.test())
        await task

if __name__ == '__main__':
    demo = Demo()
    asyncio.run(demo.main())
