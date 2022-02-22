import asyncio
import aiohttp

import log
from event import Event
import plugins
from plugin_manager import all_plugins
from api import Api

import logging
logger = logging.getLogger(__name__)
from database.models import Group, GroupMember, get_object
DEBUG = False


class Bot:
    def __init__(self):
        pass
    
    async def update_group_info(self):
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
                logger.info("群 %s 已存在" % group['group_name'])
                continue
                
            Group.create(**group)
            logger.info("创建 %s" % group['group_name'])

    async def update_group_member_info(self, group_id):
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
                logger.info("用户 %s 已存在" % member['card'])
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
                        # await bot.check_group_poke_command(event)

                        # texts = ['戳我干嘛！', '疼！', '别戳了别戳了']
                        # ans = random.choice(texts)
                        # resp = await self.send_group_msg(event['group_id'], ans)
                    # except Exception as e:
                    #     api = Api(
                    #         action="send_group_msg",
                    #         group_id=event.get('group_id'), 
                    #         message="我炸了\n %s" % e
                    #     )
                    #     logger.error(str(e))
                        # await self.do(api)
                        
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
