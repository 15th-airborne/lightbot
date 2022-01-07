import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("ws://127.0.0.1:6700") as ws_connection:
            print('连接成功！')
            while True:
                event = await ws_connection.receive_json()
                print(event)


async def send_p_msg(message):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("ws://127.0.0.1:6700/api") as ws:
            print("success connect!")
            json_data = {
                "action": "send_group_msg",
                "params": {
                    "group_id": 542423773,
                    "message": message,
                }
            }
            await ws.send_json(json_data)
            resp = await ws.receive_json()
            print(resp)


if __name__ == '__main__':
    # asyncio.run(main())
    img = "[CQ:image,file=52a5384382d152c61f0cbf4e5307961b.image,url=https://gchat.qpic.cn/gchatpic_new/1420125167/565657000-2931184282-52A5384382D152C61F0CBF4E5307961B/0?term=3,subType=0]"
    import re
    m = re.sub("^(\[CQ:image,file)(=.*?)(=.*?\])$", r"\1\3", img)
    #  = "[CQ:image,file=https://gchat.qpic.cn/gchatpic_new/1420125167/565657000-2931184282-52A5384382D152C61F0CBF4E5307961B/0?term=3,subType=0]"
    asyncio.run(send_p_msg(m))
    # asyncio.run(send_p_msg(m))
