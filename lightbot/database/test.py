# import os
# print(os.getcwd())
#
# import asyncio
# import aiohttp
# from database.old_models import engine, Group, Session
# from sqlalchemy.dialects.mysql import insert
#
#
# d = {
#     "group_create_time": 0,
#     "group_id": 321997010,
#     "group_level": 0,
#     "group_memo": "",
#     "group_name": "🐴娘交流群",
#     "max_member_count": 500,
#     "member_count": 17
# }

#
# with Session() as session:
#     g = Group(**d)
#     session.add(g)
#     session.commit()
#
from models import get_image_answer, answer_question
import asyncio
import aiohttp

# question = "[CQ:image,file=c1aeff39fcasdf338e6ba9e0f3d226f68496.image,url=https://gchat.qpic.cn/gchatpic_new/1420125167/565657000-2887674161-C1AEFF39FC338E6BA9E0F3D226F68496/0?term=3,subType=1]"
# qa = get_image_answer(question)
# print(answer_question(question))

async def demo():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('ws://127.0.0.1:6700/api') as ws:
            json_data = {
                "action": "get_image",
                "params": {
                    "file": "cc2b0635cb9e9708299a49e65c518ca9.image"
                }
            }
            await ws.send_json(json_data)
            resp = await ws.receive_json()
            return resp


async def send_img(img_file_path):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('ws://127.0.0.1:6700/api') as ws:
            json_data = {
                "action": "send_private_msg",
                "params": {
                    "attacker_user_id": "435786117",
                    "message": f"[CQ:image,file=file://{img_file_path}]",
                }
            }
            await ws.send_json(json_data)
            resp = await ws.receive_json()
            return resp

# resp = asyncio.run(demo())
# resp = asyncio.run(send_img('/home/qq_bot/cqhttp/data/cache/cc2b0635cb9e9708299a49e65c518ca9.image.png'))
resp = asyncio.run(send_img('data/cache/cc2b0635cb9e9708299a49e65c518ca9.image.png'))
print(resp)
