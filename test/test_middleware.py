import json
from unittest.mock import patch

import jwt
import pytest
from aiohttp import web

from aiohttp.web import json_response
from aiohttp.test_utils import make_mocked_request
from asynctest import CoroutineMock

from aiohttp_auth import auth


async def test_auth_middleware_checks_aiohttp_auth_initialization():
    @auth.middleware
    async def user_injector(request):
        return {"user": 1}

    # make a mock request
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )

    # make a mock view
    stub_view = CoroutineMock()

    with pytest.raises(AttributeError) as error:
        await user_injector(stub_request, stub_view)

    assert str(error.value) == 'Please initialize aiohttp_auth first.'


async def test_auth_middleware_returns_401_if_token_invalid():
    @auth.middleware
    async def user_injector(request):
        return {"user": 1}

    # make a mock Application
    app = web.Application()
    app['aiohttp_auth'] = auth.JWTAuth(
        jwt_secret='', duration=1, jwt_algorithm=''
    )

    # make a mock request
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'},
        app=app
    )

    # make a mock view
    stub_view = CoroutineMock()
    with patch('aiohttp_auth.auth.jwt.decode') as jwt_decode:
        jwt_decode.side_effect = jwt.DecodeError()
        response = await user_injector(stub_request, stub_view)

        assert response.status == 401
        assert json.loads(response.body) == {
            'message': 'Invalid Token', "errors": []
        }


async def test_auth_middleware_returns_401_on_invalid_header():
    @auth.middleware
    async def user_injector(request):
        return {"user": 1}

    # make a mock Application
    app = web.Application()
    app['aiohttp_auth'] = auth.JWTAuth(
        jwt_secret='', duration=1, jwt_algorithm=''
    )

    # make a mock request
    stub_request = make_mocked_request(
        'GET', '/', headers={},
        app=app
    )

    # make a mock view
    stub_view = CoroutineMock()

    response = await user_injector(stub_request, stub_view)

    assert response.status == 401
    assert json.loads(response.body) == {
        "message": "Please enter your API key.",
        "errors": []
    }


async def test_auth_middleware_returns_401_if_token_expired():
    @auth.middleware
    async def user_injector(request):
        return {"user": 1}

    # make a mock Application
    app = web.Application()
    app['aiohttp_auth'] = auth.JWTAuth(
        jwt_secret='', duration=1, jwt_algorithm=''
    )

    # make a mock request
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'},
        app=app
    )

    # make a mock view
    stub_view = CoroutineMock()
    with patch('aiohttp_auth.auth.jwt.decode') as jwt_decode:
        jwt_decode.side_effect = jwt.ExpiredSignatureError()
        response = await user_injector(stub_request, stub_view)

        assert response.status == 401
        assert json.loads(response.body) == {
            'message': 'Token Has Expired', "errors": []
        }


async def test_auth_middleware_returns_injects_user():
    @auth.middleware
    async def user_injector(request):
        return {"user": 1}

    # make a mock Application
    app = web.Application()
    app['aiohttp_auth'] = auth.JWTAuth(
        jwt_secret='', duration=1, jwt_algorithm=''
    )

    # make a mock request
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'},
        app=app
    )

    # make a mock view
    async def stub_view(request):
        return json_response({})

    with patch('aiohttp_auth.auth.jwt.decode') as jwt_decode:
        jwt_decode.return_value = {
            'user_id': 1,
        }

        await user_injector(stub_request, stub_view)

        assert hasattr(stub_request, 'user')
        assert stub_request.user == {"user": 1}
