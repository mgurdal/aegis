import asyncio

import aiohttp

BASE_URL = "http://0.0.0.0:8080"


async def login(session, credentials: dict) -> str:
    """Retrieve token with credentials"""
    resp = await session.post(f"{BASE_URL}/auth", json=credentials)
    assert resp.status == 200, f"Authentication Failed, {resp.reason}"

    token_payload = await resp.json()
    return token_payload["access_token"]


async def get_protected_data(session, access_token: str) -> dict:
    """Fetch data from the protected route"""
    resp = await session.get(
        f"{BASE_URL}/protected", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status == 200, f"Failed to fetch the data, {resp.reason}"

    data = await resp.json()
    return data


async def main():
    async with aiohttp.ClientSession() as session:
        credentials = {"id": 5}
        access_token = await login(session, credentials)
        data = await get_protected_data(session, access_token)
        return data


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(main())
    print(data)
