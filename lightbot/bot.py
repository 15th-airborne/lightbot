import asyncio
import re

import aiohttp
import random
from event import Event
from commands import say_yes, command_functions, command_keywords
import plugins
from plugins.teacher import answer_question


class Bot:
    def __init__(self):
        # self.session = session
        # self.group = await
        #
        # self.ws = ws
        pass

    async def send_json(self, action, **kwargs):
        json_data = {
            "action": action,
            "params": kwargs
        }

        print(json_data)
        async with self.session.ws_connect('ws://127.0.0.1:6700/api') as ws:
            await ws.send_json(json_data)
            resp = await ws.receive_json()
            return resp

    async def get_group_member_list(self, group_id):
        resp = await self.send_json(action="get_group_member_list", group_id=group_id)
        return resp

    async def send_group_msg(self, group_id, message):
        resp = await self.send_json(action="send_group_msg", group_id=group_id, message=message)
        return resp

    async def get_image(self, file):
        resp = await self.send_json(action="get_image", file=file)
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
                        res = await self.check_group_message_command(event)
                        if res:
                            continue

                        answer = answer_question(event['message'])
                        if answer is not None:
                            resp = await self.send_group_msg(event['group_id'], answer)
                            print(resp)
                            continue

                    elif event.is_group_poke():
                        pass
                        # await bot.check_group_poke_command(event)

                        # texts = ['戳我干嘛！', '疼！', '别戳了别戳了']
                        # ans = random.choice(texts)
                        # resp = await self.send_group_msg(event['group_id'], ans)

    async def check_group_message_command(self, event):
        for func in command_functions:
            res = await func(self, event)
            if res:
                return True

        message = event['message']
        for kw, func in command_keywords.items():
            if message.startswith(kw):
                await func(self, event)
                return True
        return False
        #
        # print(event['message'])
        # if "有无" in event['message']:
        #     texts = ['有', '1', '来来来']
        #     ans = random.choice(texts)
        #     resp = await self.send_group_msg(event['group_id'], ans)
        #
        # if "夯" in event['message']:
        #     resp = await self.send_group_msg(event['group_id'], '别夯了，esim都亡了')
        #     print(resp)


if __name__ == '__main__':
    bot = Bot()
    asyncio.run(bot.run())
