import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.lolicon.app/setu/v2") as resp:
            data = await resp.json()
            return data
aiohttp.ClientSession()
data = asyncio.run(main())