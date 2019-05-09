import asyncio

import aiohttp

BASE_URL = "http://0.0.0.0:8080"


async def login(session, credentials: dict) -> dict:
    """Retrieve token with credentials"""
    resp = await session.post(F"{BASE_URL}/auth", json=credentials)
    assert resp.status == 200, F"Authentication Failed, {resp.reason}"

    token_payload = await resp.json()
    return token_payload


async def refresh(session, access_token: str, refresh_token: str) -> str:
    """Retrieve new access token with refresh token."""
    resp = await session.post(
        F"{BASE_URL}/auth/refresh",
        json={"refresh_token": refresh_token},
        headers={"Authorization": F"Bearer {access_token}"}
    )
    assert resp.status == 200, F"Failed to refresh, {resp.reason}"

    token_payload = await resp.json()
    return token_payload["access_token"]


async def get_protected_data(session, access_token: str) -> dict:
    """Fetch data from the protected route"""
    resp = await session.get(
        F"{BASE_URL}/protected",
        headers={"Authorization": F"Bearer {access_token}"}
    )

    data = await resp.json()
    return data


async def main():
    async with aiohttp.ClientSession() as session:
        credentials = {"name": "david"}
        print("Logging in.")
        token_payload = await login(session, credentials)
        access_token = token_payload["access_token"]

        print("Fetching data with access token.")
        data = await get_protected_data(session, access_token)
        print(data)

        print("Waiting access token to expire.")
        await asyncio.sleep(3.2)

        print("Trying to fetch the data with expired token.")
        response = await get_protected_data(session, access_token)
        print(response)

        print("Refreshing the access token.")
        refresh_token = token_payload["refresh_token"]
        access_token = await refresh(session, access_token, refresh_token)

        print("Fetching data with new access token.")
        data = await get_protected_data(session, access_token)
        print(data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(main())
