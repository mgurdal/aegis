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
