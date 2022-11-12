# import asyncio
# import aiohttp

# from ..event import Event

# async def main():
#     async with aiohttp.ClientSession() as session:
#         async with session.ws_connect("ws://127.0.0.1:6700") as ws:
#             print('连接成功！')
#             while True:
#                 event = Event(await ws.receive_json())
#                 if event.is_private_message():
