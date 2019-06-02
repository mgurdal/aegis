import asyncio

import aiohttp
from aiohttp import BasicAuth

BASE_URL = "http://0.0.0.0:8080"


async def get_protected_data(session, credentials: dict) -> dict:
    """Fetch data from the protected route with credentials"""
    resp = await session.get(f"{BASE_URL}/protected", auth=credentials)
    assert resp.status == 200, f"Failed to fetch the data, {resp.reason}"

    data = await resp.json()
    return data


async def main():
    async with aiohttp.ClientSession() as session:

        credentials = BasicAuth(login="david", password="test")
        data = await get_protected_data(session, credentials)
        return data


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(main())
    print(data)
