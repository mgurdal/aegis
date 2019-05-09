import asyncio

import aiohttp

BASE_URL = "http://0.0.0.0:8080"
CAN_ACCESS = True
CANNOT_ACCESS = False


async def login(session, credentials: dict) -> str:
    """Retrieve token with credentials"""
    resp = await session.post(F"{BASE_URL}/auth", json=credentials)
    assert resp.status == 200, F"Authentication Failed, {resp.reason}"

    token_payload = await resp.json()
    return token_payload["access_token"]


async def fetch_page(session, page: str, access_token: str) -> int:
    """Fetch data from the protected route"""
    resp = await session.get(
        F"{BASE_URL}/{page}",
        headers={"Authorization": F"Bearer {access_token}"}
    )
    return resp.status == 200


async def main():
    """Test endpoints with both admin and user access tokens."""
    user_credentials = {"username": "user"}
    admin_credentials = {"username": "admin"}
    async with aiohttp.ClientSession() as session:
        # Retrieve tokens
        user_token = await login(session, user_credentials)
        admin_token = await login(session, admin_credentials)

        test_results = [
            # Try to fetch user page with user token
            CAN_ACCESS == await fetch_page(session, "user", user_token),

            # Try to fetch admin page with admin token
            CAN_ACCESS == await fetch_page(session, "admin", admin_token),

            # Try to fetch user page with admin token
            CAN_ACCESS == await fetch_page(session, "user", admin_token),

            # Try to fetch admin page with user token
            CANNOT_ACCESS == await fetch_page(session, "admin", user_token)
        ]

        assert all(test_results), "Test suite failed."
        print("All tests passed.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
