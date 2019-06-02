from unittest.mock import MagicMock

import pytest
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop, make_mocked_request
from aiohttp import web
from asynctest import CoroutineMock

from aegis import BasicAuth, JWTAuth
from aegis.test_utils import MockAuthenticator


class MockAuthenticatorBasicTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()

        class BasicAuthenticator(BasicAuth):
            async def authenticate(self, request: web.Request) -> dict:
                pass

        BasicAuthenticator.setup(app)
        MockAuthenticator.setup(app)
        return app

    @unittest_run_loop
    async def test_mock_authenticator_setup_checks_initialization(self):
        """
        MockAuthenticator.setup raises AttributeError if authenticator
        is not set up.
        """
        stub_app = {}
        with pytest.raises(AttributeError) as error:
            # noinspection PyTypeChecker
            await MockAuthenticator.setup(stub_app)

        assert str(error.value) == (
            "Please initialize the authenticator with "
            "Authenticator.setup(app) first."
        )

    @unittest_run_loop
    async def test__mock_auth_middleware_injects_user(self):
        mocked_authenticator = self.app["authenticator"]
        mocked_authenticator._inject_user = MagicMock()
        expected_response = "Response"
        mocked_view = CoroutineMock(return_value=expected_response)
        req = make_mocked_request("GET", "/login_required")
        resp = await mocked_authenticator._mock_auth_middleware(req, mocked_view)

        mocked_authenticator._inject_user.assert_called_once_with(req)
        assert resp == expected_response

    @unittest_run_loop
    async def test__inject_user_adds_user_into_request(self):
        mocked_authenticator = self.app["authenticator"]

        stub_user = {"permissions": ("user",)}
        mocked_authenticator.user = stub_user

        req = make_mocked_request("GET", "/login_required")
        mocked_authenticator._inject_user(req)

        assert hasattr(req, "user")
        assert req.user == stub_user

    @unittest_run_loop
    async def test_get_user_returns_injected_user(self):
        mocked_authenticator = self.app["authenticator"]
        mocked_authenticator.authenticator.get_user = CoroutineMock()

        stub_user = {"permissions": ("user",)}
        mocked_authenticator.user = stub_user

        req = make_mocked_request("GET", "/login_required")
        user = await mocked_authenticator.get_user(req)

        assert user == stub_user
        assert mocked_authenticator.authenticator.get_user.not_awaited

    @unittest_run_loop
    async def test_get_user_returns_default_user_if_not_injected(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {"permissions": ("user",)}
        mocked_authenticator.authenticator.get_user = CoroutineMock(
            return_value=stub_user
        )

        req = make_mocked_request("GET", "/")
        us = await mocked_authenticator.get_user(req)
        assert us == stub_user
        assert mocked_authenticator.authenticator.get_user.awaited_once_with(req)

    @unittest_run_loop
    async def test_decode_returns_injected_user(self):
        mocked_authenticator = self.app["authenticator"]
        mocked_authenticator.authenticator.decode = CoroutineMock()

        stub_user = {"permissions": ("user",)}
        mocked_authenticator.user = stub_user

        req = make_mocked_request("GET", "/")
        user = await mocked_authenticator.decode(req)

        assert user == stub_user
        assert mocked_authenticator.authenticator.decode.not_awaited

    @unittest_run_loop
    async def test_decode_uses_default_decode_if_not_injected(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {"permissions": ("user",)}
        mocked_authenticator.authenticator.decode = CoroutineMock(
            return_value=stub_user
        )

        req = make_mocked_request("GET", "/")
        user = await mocked_authenticator.decode(req)
        assert user == stub_user
        assert mocked_authenticator.authenticator.decode.awaited_once_with(req)

    @unittest_run_loop
    async def test_bypass_auth_sets_and_removes_user(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {"test": "user"}

        assert not mocked_authenticator.user
        with mocked_authenticator.bypass_auth(user=stub_user):
            assert mocked_authenticator.user == stub_user

        assert not mocked_authenticator.user


class MockAuthenticatorJWTTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()

        class JWTAuthenticator(JWTAuth):
            async def authenticate(self, request: web.Request) -> dict:
                pass

        JWTAuthenticator.setup(app)
        MockAuthenticator.setup(app)
        return app

    @unittest_run_loop
    async def test_mock_authenticator_setup_checks_initialization(self):
        """
        MockAuthenticator.setup raises AttributeError if authenticator
        is not set up.
        """
        stub_app = {}
        with pytest.raises(AttributeError) as error:
            # noinspection PyTypeChecker
            await MockAuthenticator.setup(stub_app)

        assert str(error.value) == (
            "Please initialize the authenticator with "
            "Authenticator.setup(app) first."
        )

    @unittest_run_loop
    async def test__mock_auth_middleware_injects_user(self):
        mocked_authenticator = self.app["authenticator"]
        mocked_authenticator._inject_user = MagicMock()
        expected_response = "Response"
        mocked_view = CoroutineMock(return_value=expected_response)
        req = make_mocked_request("GET", "/login_required")
        resp = await mocked_authenticator._mock_auth_middleware(req, mocked_view)

        mocked_authenticator._inject_user.assert_called_once_with(req)
        assert resp == expected_response

    @unittest_run_loop
    async def test__inject_user_adds_user_into_request(self):
        mocked_authenticator = self.app["authenticator"]

        stub_user = {"permissions": ("user",)}
        mocked_authenticator.user = stub_user

        req = make_mocked_request("GET", "/login_required")
        mocked_authenticator._inject_user(req)

        assert hasattr(req, "user")
        assert req.user == stub_user

    @unittest_run_loop
    async def test_get_user_returns_injected_user(self):
        mocked_authenticator = self.app["authenticator"]
        mocked_authenticator.authenticator.get_user = CoroutineMock()

        stub_user = {"permissions": ("user",)}
        mocked_authenticator.user = stub_user

        req = make_mocked_request("GET", "/login_required")
        user = await mocked_authenticator.get_user(req)

        assert user == stub_user
        assert mocked_authenticator.authenticator.get_user.not_awaited

    @unittest_run_loop
    async def test_get_user_returns_default_user_if_not_injected(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {"permissions": ("user",)}
        mocked_authenticator.authenticator.get_user = CoroutineMock(
            return_value=stub_user
        )

        req = make_mocked_request("GET", "/")
        us = await mocked_authenticator.get_user(req)
        assert us == stub_user
        assert mocked_authenticator.authenticator.get_user.awaited_once_with(req)

    @unittest_run_loop
    async def test_decode_returns_injected_user(self):
        mocked_authenticator = self.app["authenticator"]
        mocked_authenticator.authenticator.decode = CoroutineMock()

        stub_user = {"permissions": ("user",)}
        mocked_authenticator.user = stub_user

        req = make_mocked_request("GET", "/")
        user = await mocked_authenticator.decode(req)

        assert user == stub_user
        assert mocked_authenticator.authenticator.decode.not_awaited

    @unittest_run_loop
    async def test_decode_uses_default_decode_if_not_injected(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {"permissions": ("user",)}
        mocked_authenticator.authenticator.decode = CoroutineMock(
            return_value=stub_user
        )

        req = make_mocked_request("GET", "/")
        user = await mocked_authenticator.decode(req)
        assert user == stub_user
        assert mocked_authenticator.authenticator.decode.awaited_once_with(req)

    @unittest_run_loop
    async def test_setup_initializes_app_with_mock(self):
        async def auth_middleware():
            pass

        authenticator = MagicMock()
        authenticator.auth_endpoint = None
        authenticator.me_endpoint = None

        app = web.Application(middlewares=[auth_middleware])
        app["authenticator"] = authenticator

        MockAuthenticator.setup(app)
        assert "authenticator" in app
        assert isinstance(app["authenticator"], MockAuthenticator)

    @unittest_run_loop
    async def test_bypass_auth_sets_and_removes_user(self):
        mocked_authenticator = self.app["authenticator"]
        stub_user = {"test": "user"}

        assert not mocked_authenticator.user
        with mocked_authenticator.bypass_auth(user=stub_user):
            assert mocked_authenticator.user == stub_user

        assert not mocked_authenticator.user
