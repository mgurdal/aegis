import asyncio

import aiohttp

BASE_URL = "http://0.0.0.0:8080"


async def login(session, credentials: dict) -> str:
    """Retrieve token with credentials"""
    resp = await session.post(F"{BASE_URL}/auth", json=credentials)
    return await resp.json()


async def main():
    async with aiohttp.ClientSession() as session:
        credentials = {"id": 5}
        response = await login(session, credentials)
        print(response)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(main())
