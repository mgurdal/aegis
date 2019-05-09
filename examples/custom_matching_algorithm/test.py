from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aegis.test_utils import MockAuthenticator

from app import create_app


class AppTestCase(AioHTTPTestCase):

    async def get_application(self):
        app = create_app()
        MockAuthenticator.setup(app)
        return app

    @unittest_run_loop
    async def test_user_can_access_to_user_page(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {
            "permissions": ("user",)
        }
        with mocked_authenticator.bypass_auth(user=stub_user):
            resp = await self.client.request("GET", "/user")
        assert resp.status == 200

    @unittest_run_loop
    async def test_user_cannot_access_to_admin_page(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {
            "permissions": ("user",)
        }
        with mocked_authenticator.bypass_auth(user=stub_user):
            resp = await self.client.request("GET", "/admin")
        assert resp.status == 403

    @unittest_run_loop
    async def test_admin_can_access_to_admin_page(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {
            "permissions": ("admin",)
        }
        with mocked_authenticator.bypass_auth(user=stub_user):
            resp = await self.client.request("GET", "/admin")
        assert resp.status == 200

    @unittest_run_loop
    async def test_admin_can_access_to_user_page(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {
            "permissions": ("admin",)
        }
        # Admin can access to user page even its not defined in
        # permissions
        with mocked_authenticator.bypass_auth(user=stub_user):
            resp = await self.client.request("GET", "/admin")
        assert resp.status == 200

    @unittest_run_loop
    async def test_anonymous_user_cannot_access_to_user_page(self):
        resp = await self.client.request("GET", "/user")
        assert resp.status == 403

    @unittest_run_loop
    async def test_anonymous_user_cannot_access_to_admin_page(self):
        resp = await self.client.request("GET", "/admin")
        assert resp.status == 403
