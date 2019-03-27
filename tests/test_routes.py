import json

from aiohttp import web
from aiohttp.test_utils import make_mocked_request
from aiohttp_auth.exceptions import AuthException
from aiohttp_auth.routes import make_auth_route, make_me_route
from asynctest import CoroutineMock, patch


async def test_auth_route_returns_access_token():

    stub_request = make_mocked_request('GET', '/')

    stub_user = {'user_id': 1}
    authenticator = CoroutineMock()
    authenticator.authenticate = CoroutineMock(return_value=stub_user)
    encoder = authenticator.encode = CoroutineMock(return_value="token")

    auth_route = make_auth_route(authenticator)
    token_payload = await auth_route(stub_request)

    assert encoder.encode.awaited_once_with(stub_user)
    assert authenticator.authenticate.awaited_once_with(stub_request)
    assert json.loads(token_payload.body) == {
        'access_token': 'token'
    }


async def test_auth_route_handles_auth_exception():

    stub_request = make_mocked_request('GET', '/')
    AuthException.make_response = CoroutineMock(
        return_value=web.json_response({})
    )

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
    stub_request = make_mocked_request('GET', '/')
    stub_user = {
        'user_id': 1,
        'exp': 1
    }

    # force auth
    stub_request.user = stub_user

    me_route = make_me_route()

    user_response = await me_route(stub_request)
    user_payload = json.loads(user_response.body)

    assert user_response.status == 200
    assert user_payload == stub_user


async def test_me_route_uses_forbidden_exception_if_not_authenticated():
    """
    Test me route returns 403, Forbidden if user is not authenticated.
    """
    stub_request = make_mocked_request('GET', '/')
    me_route = make_me_route()
    with patch('aiohttp_auth.routes.ForbiddenException.make_response') as fe:
        fe.return_value.status = 403

        await me_route(stub_request)

        assert fe.awaited_once_with(stub_request)
