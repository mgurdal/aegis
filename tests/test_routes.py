import json

from aiohttp.test_utils import make_mocked_request
from aiohttp_auth import auth
from asynctest import CoroutineMock, patch


async def test_auth_route_awaits_dependencies():

    stub_request = make_mocked_request('GET', '/')

    stub_user = {'user_id': 1}
    authenticator = CoroutineMock(return_value=stub_user)
    auth_route = auth.make_auth_route(authenticator)

    with patch('aiohttp_auth.auth.generate_jwt') as mocked_generate_jwt:
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
    auth_route = auth.make_auth_route(authenticator)

    with patch('aiohttp_auth.auth.generate_jwt') as mocked_generate_jwt:
        mocked_generate_jwt.return_value = 'test_token'
        token_response = await auth_route(stub_request)
        token_payload = json.loads(token_response.body)

        assert token_payload == {
            'access_token': 'test_token'
        }


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

    me_route = auth.make_me_route()

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

    me_route = auth.make_me_route()

    user_response = await me_route(stub_request)
    error_payload = json.loads(user_response.body)

    assert user_response.status == 403
    assert error_payload == {
        "message": "Please login."
    }
