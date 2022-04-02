import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("ws://127.0.0.1:6700") as ws_connection:
            print('连接成功！')
            while True:
                event = await ws_connection.receive_json()
                if event.get('message_type') == 'group':
                    print(event['sender']['nickname'], event['message'])

if __name__ == '__main__':
    asyncio.run(main())
