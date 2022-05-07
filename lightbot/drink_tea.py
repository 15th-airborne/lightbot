msg = "三点几了,做卵啊做,饮茶先啦"
group_ids = [
    # 321997010,
    # 565657000,
    542423773,
]
import asyncio
import aiohttp
from api import Api

async def drink_tea(group_id):
    api = Api(
        action="send_group_msg",
        group_id=group_id,
        message=msg
    )
    json_data = api.json()
    async with aiohttp.ClientSession() as session:   
        async with session.ws_connect('ws://127.0.0.1:6700/api') as ws:
            await ws.send_json(json_data)
            resp = await ws.receive_json()
            return resp

async def main():
    await drink_tea(565657000)
    await drink_tea(321997010)

asyncio.run(main())
