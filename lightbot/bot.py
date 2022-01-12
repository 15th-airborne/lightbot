import asyncio
import aiohttp

from event import Event
import plugins
from plugin_manager import all_plugins
from api import Api


class Bot:
    def __init__(self):
        pass

    async def do(self, action: Api):
        async with self.session.ws_connect('ws://127.0.0.1:6700/api') as ws:
            await ws.send_json(action.json())
            resp = await ws.receive_json()
            return resp


    async def run(self):
        async with aiohttp.ClientSession() as session:
            self.session = session
            async with self.session.ws_connect("ws://127.0.0.1:6700") as ws:
                print('连接成功！')
                while True:
                    event = Event(await ws.receive_json())
                    print(event)

                    if event.is_group_message():
                        res = await self.check_group_message_plugin(event)
                        # if res:
                        #     continue

                        # answer = answer_question(event['message'])
                        # if answer is not None:
                        #     resp = await self.send_group_msg(event['group_id'], answer)
                        #     print(resp)
                        #     continue

                    elif event.is_group_poke():
                        pass
                        # await bot.check_group_poke_command(event)

                        # texts = ['戳我干嘛！', '疼！', '别戳了别戳了']
                        # ans = random.choice(texts)
                        # resp = await self.send_group_msg(event['group_id'], ans)

    async def check_group_message_plugin(self, event):
        for plugin in all_plugins:
            api = plugin(event).api()
            if api is not None:
                await self.do(api)
                return True
        return False


if __name__ == '__main__':
    bot = Bot()
    asyncio.run(bot.run())
