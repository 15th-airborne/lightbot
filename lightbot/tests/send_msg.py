import asyncio
import aiohttp

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import Api
async def do(session, action: Api):
    async with session.ws_connect('ws://127.0.0.1:6700/api') as ws:
        await ws.send_json(action.json())
        resp = await ws.receive_json()
        return resp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("ws://127.0.0.1:6700") as ws_connection:
            get_group_list_api = Api(action='get_group_list')
            res = await do(session, get_group_list_api)
            print("\n--------------------------------------\n")
            print(res)

            if res.get('status') == 'ok':
                group_list = res.get('data')
            else:
                return
                


if __name__ == '__main__':
    asyncio.run(main())
