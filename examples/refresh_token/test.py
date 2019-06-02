from unittest.mock import patch

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

        resp = await self.client.request(
            "GET", "/protected", headers={"Authorization": "Bearer x"}
        )
        assert resp.status == 401

    @unittest_run_loop
    async def test_validate_refresh_token_with_invalid_token(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {
            "name": "test",
            "refresh_token": "expected_token",
            "permissions": ("user",),
        }

        refresh_token_payload = {"refresh_token": "invalid_token"}
        with patch("app.find_user_with_name") as find_user:
            find_user.return_value = stub_user

            with mocked_authenticator.bypass_auth(user=stub_user):
                resp = await self.client.request(
                    "POST", "/auth/refresh", json=refresh_token_payload
                )
                assert resp.status == 400

    @unittest_run_loop
    async def test_validate_refresh_token_with_valid_token(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {
            "name": "test",
            "refresh_token": "expected_token",
            "permissions": ("user",),
        }

        refresh_token_payload = {"refresh_token": "expected_token"}
        with patch("app.find_user_with_name") as find_user:
            find_user.return_value = stub_user

            with mocked_authenticator.bypass_auth(user=stub_user):
                resp = await self.client.request(
                    "POST", "/auth/refresh", json=refresh_token_payload
                )
                assert resp.status == 200

                token_payload = await resp.json()
                assert "access_token" in token_payload

    @unittest_run_loop
    async def test_auth_returns_refresh_token(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {
            "id": 7,
            "name": "test",
            "refresh_token": "expected_token",
            "permissions": ("user",),
        }

        stub_db = {7: stub_user}
        self.app["db"] = stub_db

        with patch("app.find_user_with_name") as find_user:
            find_user.return_value = stub_user

            with mocked_authenticator.bypass_auth(user=stub_user):
                resp = await self.client.request(
                    "POST", "/auth", json={"name": stub_user["name"]}
                )

        assert resp.status == 200

        token_payload = await resp.json()
        assert "refresh_token" in token_payload

    @unittest_run_loop
    async def test_auth_registers_refresh_token(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {
            "id": 7,
            "name": "test",
            "refresh_token": "expected_token",
            "permissions": ("user",),
        }

        stub_db = {7: stub_user}
        self.app["db"] = stub_db

        with patch("app.find_user_with_name") as find_user:
            find_user.return_value = stub_user

            with mocked_authenticator.bypass_auth(user=stub_user):
                resp = await self.client.request(
                    "POST", "/auth", json={"name": stub_user["name"]}
                )

        token_payload = await resp.json()
        assert token_payload["refresh_token"] == stub_user["refresh_token"]
