import json

from aiohttp.test_utils import make_mocked_request
from aiohttp_auth.exceptions import UserDefinedException
from aiohttp_auth.routes import make_auth_route, make_me_route
from asynctest import CoroutineMock, patch


async def test_auth_route_awaits_dependencies():

    stub_request = make_mocked_request('GET', '/')

    stub_user = {'user_id': 1}
    authenticator = CoroutineMock(return_value=stub_user)
    auth_route = make_auth_route(authenticator)

    with patch('aiohttp_auth.routes.generate_jwt') as mocked_generate_jwt:
        mocked_generate_jwt.return_value = 'test_token'
        await auth_route(stub_request)

        assert authenticator.awaited_once_with(stub_request)
        assert mocked_generate_jwt.awaited_once_with(
            stub_request, stub_user
        )


async def test_auth_route_returns_access_token():

    stub_request = make_mocked_request('GET', '/')

    stub_user = {'user_id': 1}
    authenticator = CoroutineMock(return_value=stub_user)
    auth_route = make_auth_route(authenticator)

    with patch('aiohttp_auth.routes.generate_jwt') as mocked_generate_jwt:
        with patch('aiohttp_auth.routes.access_token') as access_token:
            access_token.return_value.status = 200
            access_token.return_value.body = b'{"access_token": "x"}'

            token_response = await auth_route(stub_request)
            token_payload = json.loads(token_response.body)

            mocked_generate_jwt.assert_called_with(
                stub_request, stub_user
            )
            assert authenticator.awaited_once_with(stub_request)
            assert token_payload == {
                'access_token': 'x'
            }


async def test_auth_route_handles_user_exceptions():

    stub_request = make_mocked_request('GET', '/')

    class TestException(UserDefinedException):
        status = 400
        title = "test"
        detail = "test"

    authenticator = CoroutineMock(side_effect=TestException())
    auth_route = make_auth_route(authenticator)

    with patch('aiohttp_auth.routes.error_response') as error_response:
        await auth_route(stub_request)

        assert error_response.called


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
    assert 'exp' not in user_payload


async def test_me_route_returns_403_if_user_is_not_authenticated():
    """
    Test me route returns 403, Forbidden if user is not authenticated.
    """
    stub_request = make_mocked_request('GET', '/')
    me_route = make_me_route()
    with patch('aiohttp_auth.routes.forbidden') as forbidden:
        forbidden.return_value.status = 403

        user_response = await me_route(stub_request)

        assert user_response.status == 403
        assert forbidden.called
