import time
import asyncio
import aiohttp
import datetime
from matplotlib.pyplot import get

json_data = {
    "action": "set_group_ban",
    "params": {
        "group_id": 347043955,
        "user_id": 1434469194,
        "duration": 60 * 60 * 24 * 7,
    }
}

async def ban():
    while True:
        time.sleep(60)
        msg = await get_group_member_info()
        if msg['shut_up_timestamp'] < datetime.datetime.now().timestamp():
            async with aiohttp.ClientSession() as session:   
                async with session.ws_connect('ws://127.0.0.1:6701/api') as ws:
                    await ws.send_json(json_data)
                    resp = await ws.receive_json()
                    return resp

async def get_group_member_info():
    json_data = {
        "action": "get_group_member_info",
        "params": {
            "group_id": 347043955,
            "user_id": 1434469194,
        }
    }
    async with aiohttp.ClientSession() as session:   
        async with session.ws_connect('ws://127.0.0.1:6701/api') as ws:
            await ws.send_json(json_data)
            resp = await ws.receive_json()
    print(resp)
    return resp

    # shut_up_timestamp

    
def ban_bot():
    pass

async def main():
    # await ban()
    await get_group_member_info()

asyncio.run(main())