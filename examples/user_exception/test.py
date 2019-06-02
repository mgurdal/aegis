from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aegis.test_utils import MockAuthenticator

from app import create_app


class AppTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = create_app()
        MockAuthenticator.setup(app)
        return app

    @unittest_run_loop
    async def test_auth_route_returns_user_exception(self):
        credentials = {"id": 4}

        resp = await self.client.request("POST", "/auth", json=credentials)
        assert resp.status == 401

        error_message = await resp.json()
        assert error_message == {"message": "User does not exists."}
