import random
import datetime

import asyncio
from re import L
import aiohttp
from api import Api

import requests
app_id='ouqzjomlvnk2vmdp'
app_secret='Y2RwT25VSGp3N25JL3BneTAxazlDUT09'
url = f'https://www.mxnzp.com/api/history/today?type=1&app_id={app_id}&app_secret={app_secret}'
resp = requests.get(url)

data = resp.json()['data']
history_today_data = []
for d in data:
    text = f"{d['year']}年{d['month']}月{d['day']}日，{d['title']}"
    history_today_data.append(text)
sub_data = random.sample(history_today_data, k=3)
history_today_text = '历史上的今天\n' + '\n'.join(sub_data)

msgs = [
    '周一周一，nmgb',
    '周二周二，辗转反侧', # 辗转反侧 天气炎热
    '周三周三，不动如山', # 周三周三，坐立不安 不动如山  左顾右盼 身经百战

    # '周三周三，如坐针毡',
    # '疯狂周四，V我50',
    '周四周四，不如周日',  # 
    '周五周五，行将入土',  # 行将入土 朝秦暮楚
    # '周五周五，千辛万苦',
    '周六周六，逆来顺受',  # 昼伏夜游
    '周日周日，敷衍了事'  # 
    # '这个b班今天就上完了',
    # '不会吧不会吧，这个点大家不会都睡了吧？',
    # '现在不睡，周一遭罪'

    # 虽然今天是星期四，但我们不吃肯德基了，我们回家
]

msg = "三点几了,做卵啊做,饮茶先啦"
msg = msgs[datetime.datetime.now().weekday()]

group_ids = [
    # 321997010,
    # 565657000,
    542423773,
]

expired_date = datetime.date(2022, 11, 24)
td = expired_date - datetime.date.today()


# 0 3 * * * /opt/miniconda3/envs/lightbot/bin/python /projects/lightbot/lightbot/drink_tea.py
async def drink_tea(group_id):
    api = Api(
        action="send_group_msg",
        group_id=group_id,
        message=msg + f'\n距离小月宕机还有{td.days}天'
    )

    api2 = Api(
        action="send_group_msg",
        group_id=group_id,
        message=history_today_text
    )
    json_data = api.json()
    json_data2 = api2.json()
    async with aiohttp.ClientSession() as session:   
        async with session.ws_connect('ws://127.0.0.1:6700/api') as ws:
            await ws.send_json(json_data)
            await ws.send_json(json_data2)
            resp = await ws.receive_json()
            return resp

async def main():
    await drink_tea(565657000)
    await drink_tea(321997010)
    # await drink_tea(542423773)


async def test():
    async def history_today(group_id):
        api2 = Api(
            action="send_group_msg",
            group_id=group_id,
            message=history_today_text
        )
        json_data2 = api2.json()
        async with aiohttp.ClientSession() as session:   
            async with session.ws_connect('ws://127.0.0.1:6700/api') as ws:
                await ws.send_json(json_data2)
                resp = await ws.receive_json()
                return resp
    await history_today(542423773)

#
# asyncio.run(test())  
asyncio.run(main())
# print(history_today_data)


