from unittest.mock import MagicMock

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aegis.test_utils import MockAuthenticator

from app import create_app


class AppTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = create_app()
        MockAuthenticator.setup(app)
        return app

    @unittest_run_loop
    async def test_protected_route_with_headers(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {"permissions": ("user",)}
        with mocked_authenticator.bypass_auth(user=stub_user):
            resp = await self.client.request(
                "GET", "/protected", headers={"Authorization": "Bearer x"}
            )
            assert resp.status == 200
            text = await resp.json()
            assert text == {"hello": "user"}

        resp = await self.client.request(
            "GET", "/protected", headers={"Authorization": "Bearer x"}
        )
        assert resp.status == 401

    @unittest_run_loop
    async def test_auth_route_calls_db_with_credentials(self):
        stub_user = {"permissions": ("user",)}
        credentials = {"id": 4}

        # mock database
        self.app["db"] = MagicMock()
        self.app["db"].get.return_value = stub_user

        resp = await self.client.request("POST", "/auth", json=credentials)
        assert resp.status == 200

        self.app["db"].get.assert_called_once_with(credentials["id"])
