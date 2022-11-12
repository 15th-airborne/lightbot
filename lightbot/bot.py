import asyncio
import aiohttp

import log
from event import Event
from database.models import Group, GroupMember, get_object
import plugins
from plugin_manager import all_plugins, commands, all_private_plugins
from api import Api

import logging
logger = logging.getLogger(__name__)
DEBUG = False


class BaseBot:
    async def run(self):
        async with aiohttp.ClientSession() as session:
            self.session = session
            # self.ws = await session.ws_connect("ws://127.0.0.1:6700")
            async with session.ws_connect("ws://127.0.0.1:6700") as ws:
                print('连接成功！')
                while True:
                    event = Event(await ws.receive_json())
                    if event.is_group_message() and event.message:
                        asyncio.create_task(self.process_group_event(event))
                        # print(event['sender']['nickname'], event['message'])
                        # asyncio.create_task(self.repeat(event['message']))

    async def main(self):
        task = asyncio.create_task(self.run())
        await task

    async def send_group_msg(self, group_id, message):
        json_data = self.get_api_json(
            'send_group_msg', 
            group_id=group_id, 
            message=message
        )
        await self.send_json(json_data)

    async def send_private_msg(self, user_id, message):
        json_data = self.get_api_json(
            'send_private_msg', 
            user_id=user_id,
            message=message
        )
        await self.send_json(json_data)

    @staticmethod
    def get_api_json(action, **params):
        return {
            "action": action,
            "params": params
        }

    async def send_json(self, json_data):
        async with self.session.ws_connect('ws://127.0.0.1:6700/api') as ws:
            await ws.send_json(json_data)
            # resp = await ws.receive_json()
            # return resp

    async def process_group_event(self, event: Event):
        print(event.group_id, event.sender.nickname, event.message)
        # 判断发言人触发事件的间隔。
        
        # 判断是否触发关键词
        prefix = event.message.split()[0]
        command = commands.get(prefix)
        if command:
            await command(self, event)
            print('asdfasdf')
        pass


class Bot:
    def __init__(self):
        pass
    
    async def update_group_info(self):
        """ 启动时更新群信息 """
        get_group_list_api = Api(action='get_group_list')
        resp = await self.do(get_group_list_api)

        logger.info("\n-----------------updating group info---------------------\n")
        logger.info(resp)

        if resp.get('status') == 'ok':
            group_list = resp.get('data')
        else:
            return

        for group in group_list:
            await self.update_group_member_info(group['group_id'])

            if get_object(Group, group_id=group['group_id']) is not None:
                # logger.info("群 %s 已存在" % group['group_name'])
                continue
                
            Group.create(**group)
            logger.info("创建 %s" % group['group_name'])

    async def update_group_member_info(self, group_id):
        from plugins.battle.models import Player
        api = Api(action='get_group_member_list', group_id=group_id)
        resp = await self.do(api)

        logger.info("\n-----------------updating group member info---------------------\n")
        logger.info(resp)

        if resp.get('status') == 'ok':
            member_list = resp.get('data')
        else:
            return

        for member in member_list:
            if get_object(GroupMember, group_id=group_id, user_id=member['user_id']):
                name = member['card'] if member['card'] else member['nickname']
                res = (
                    Player
                    .update({Player.name:name})
                    .where(
                        (Player.user_id == member['user_id']) & 
                        (Player.group_id == group_id)
                    )
                    .execute()
                )

                # logger.info("用户 %s 已存在" % member['card'])
                continue

            GroupMember.create(**member)


            logger.info("创建用户 %s" % member['card'])

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
                await self.update_group_info()  # 更新群信息

                while True:
                   #  try:
                    event = Event(await ws.receive_json())
                    print(event)

                    if event.is_group_message():
                        if DEBUG and event.group_id != 542423773:
                            continue
                        
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
                    elif event.is_private_message():
                        # print('private_message!')
                        res = await self.check_private_message_plugin(event)
                        # api = Api('send_private_msg', user_id=event.user_id, message='hello!')
                        # await self.do(api)
                        
    async def check_group_message_plugin(self, event):
        for plugin in all_plugins:
            api = plugin(event).api()
            if api is not None:
                await self.do(api)
                return True
        return False
    
    async def check_private_message_plugin(self, event):
        for plugin in all_private_plugins:
            api = plugin(event).api()
            if api is not None:
                await self.do(api)
                return True
        return False


if __name__ == '__main__':
    bot = Bot()
    asyncio.run(bot.run())
