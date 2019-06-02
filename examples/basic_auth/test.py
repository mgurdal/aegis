from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aegis.test_utils import MockAuthenticator

from app import create_app


class AppTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = create_app()
        MockAuthenticator.setup(app)
        return app

    @unittest_run_loop
    async def test_protected_route_with_bypass(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {"permissions": ("user",)}
        with mocked_authenticator.bypass_auth(user=stub_user):
            resp = await self.client.request("GET", "/protected")
            assert resp.status == 200
            text = await resp.json()
            assert text == {"hello": "user"}

    @unittest_run_loop
    async def test_protected_route_without_bypass(self):
        resp = await self.client.request("GET", "/protected")
        assert resp.status == 401
