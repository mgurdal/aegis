import json
from unittest.mock import MagicMock

from aiohttp import web
from aiohttp.test_utils import make_mocked_request
from aegis.exceptions import AuthException
from aegis.routes import make_auth_route, make_me_route, make_refresh_route
from asynctest import CoroutineMock, patch


async def test_auth_route_returns_auth_failed_if_not_user():
    with patch("aegis.routes.AuthException.make_response") as auth_required:
        stub_request = make_mocked_request("GET", "/")

        stub_user = {}
        authenticator = CoroutineMock()
        authenticator.refresh_token = False
        authenticator.authenticate = CoroutineMock(return_value=stub_user)
        encoder = authenticator.encode = CoroutineMock(return_value="token")

        auth_route = make_auth_route(authenticator)
        await auth_route(stub_request)

        assert encoder.encode.awaited_once_with(stub_user)
        assert authenticator.authenticate.awaited_once_with(stub_request)
        assert auth_required.called_once_with(stub_request)


async def test_auth_route_only_returns_access_token_if_not_refresh():
    stub_request = make_mocked_request("GET", "/")

    stub_user = {"user_id": 1}
    authenticator = CoroutineMock()
    authenticator.refresh_token = False
    authenticator.authenticate = CoroutineMock(return_value=stub_user)
    encoder = authenticator.encode = CoroutineMock(return_value="token")

    auth_route = make_auth_route(authenticator)
    token_payload = await auth_route(stub_request)

    assert encoder.encode.awaited_once_with(stub_user)
    assert authenticator.authenticate.awaited_once_with(stub_request)
    assert json.loads(token_payload.body) == {"access_token": "token"}


async def test_auth_route_returns_access_and_refresh_token():
    stub_request = make_mocked_request("GET", "/")

    stub_user = {"user_id": 1}
    refresh_token = "test_refresh"
    access_token = "test_access"
    authenticator = CoroutineMock()
    authenticator.refresh_token = True
    authenticator.authenticate = CoroutineMock(return_value=stub_user)
    authenticator.get_refresh_token = CoroutineMock(return_value=refresh_token)
    encoder = authenticator.encode = CoroutineMock(return_value=access_token)

    auth_route = make_auth_route(authenticator)
    token_payload = await auth_route(stub_request)

    assert encoder.encode.awaited_once_with(stub_user)
    assert authenticator.authenticate.awaited_once_with(stub_request)
    assert json.loads(token_payload.body) == {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


async def test_auth_route_handles_auth_exception():
    stub_request = make_mocked_request("GET", "/")
    AuthException.make_response = CoroutineMock(return_value=web.json_response({}))

    class TestException(AuthException):
        status = 400

        @staticmethod
        def get_schema():
            return {}

    authenticator = CoroutineMock()
    authenticator.authenticate = CoroutineMock(side_effect=TestException())

    auth_route = make_auth_route(authenticator)

    await auth_route(stub_request)

    assert AuthException.make_response.called_once_with(stub_request)


async def test_me_route_returns_user_information():
    """
    Test me route returns user information except the expiration date
    if user is authenticated.
    """
    stub_request = make_mocked_request("GET", "/")
    stub_user = {"user_id": 1, "exp": 1}

    # force auth
    stub_request.user = stub_user

    me_route = make_me_route()

    user_response = await me_route(stub_request)
    user_payload = json.loads(user_response.body)

    assert user_response.status == 200
    assert user_payload == stub_user


async def test_auth_route_adds_refresh_token_if_activated():
    stub_request = make_mocked_request("GET", "/")

    stub_user = {"user_id": 1}
    authenticator = CoroutineMock()
    authenticator.authenticate = CoroutineMock(return_value=stub_user)
    authenticator.refresh_token = True
    authenticator.encode = CoroutineMock(return_value="token")
    authenticator.get_refresh_token = CoroutineMock(return_value="refresh_token")

    auth_route = make_auth_route(authenticator)
    token_payload = await auth_route(stub_request)

    response_data = json.loads(token_payload.body)

    authenticator.get_refresh_token.assert_called_once()
    assert "refresh_token" in response_data


async def test_refresh_route_renews_access_token():
    """
    Validates refresh token with authenticator.validate_refresh_token
    Calls authenticator.renew_access_token to retrieve a new access token
    """
    refresh_payload = {"refresh_token": "test"}
    access_token = "access_token"

    stub_request = CoroutineMock()
    stub_request.json = CoroutineMock(return_value=refresh_payload)

    authenticator = CoroutineMock()
    authenticator.encode = CoroutineMock(return_value=access_token)
    authenticator.validate_refresh_token = CoroutineMock(return_value=True)

    # bypass login
    with patch("aegis.routes.login_required", lambda x: x):
        refresh_route = make_refresh_route(authenticator)
        token_payload = await refresh_route(stub_request)

        response_data = json.loads(token_payload.body)

        assert authenticator.encode.called
        assert authenticator.validate_refresh_token.called
        assert "access_token" in response_data


async def test_refresh_returns_bad_request_if_refresh_token_invalid():
    """
    Validates refresh token with authenticator.validate_refresh_token
    returns InvalidRefreshTokenException.make_response if invalid
    """
    refresh_payload = {"refresh_token": "test"}
    access_token = "access_token"

    stub_request = CoroutineMock()
    stub_request.json = CoroutineMock(return_value=refresh_payload)

    authenticator = CoroutineMock()
    authenticator.renew_access_token = CoroutineMock(return_value=access_token)
    authenticator.validate_refresh_token = CoroutineMock(return_value=False)

    with patch("aegis.routes.InvalidRefreshTokenException") as irte:
        # bypass login
        with patch("aegis.routes.login_required", lambda x: x):
            irte.make_response = MagicMock()
            refresh_route = make_refresh_route(authenticator)
            await refresh_route(stub_request)

            assert authenticator.validate_refresh_token.called
            assert not authenticator.encode.called
            irte.make_response.assert_called_once_with(stub_request)
