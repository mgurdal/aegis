from unittest.mock import patch

import jwt

import pytest
from aiohttp import web
from aiohttp.test_utils import make_mocked_request
from aiohttp.web import json_response
from aiohttp_auth import auth
from aiohttp_auth.exceptions import UserDefinedException
from asynctest import CoroutineMock


async def test_auth_middleware_checks_aiohttp_auth_initialization():

    # make a mock request
    stub_request = CoroutineMock()
    stub_request.app = {}

    # make a mock view
    stub_view = CoroutineMock()

    with pytest.raises(AttributeError) as error:
        await auth.auth_middleware(stub_request, stub_view)

    assert str(error.value) == 'Please initialize aiohttp_auth first.'


async def test_auth_middleware_returns_400_if_token_invalid():

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
        with patch('aiohttp_auth.auth.invalid_token') as invalid_token:
            invalid_token.return_value.status = 400
            jwt_decode.side_effect = jwt.DecodeError()
            response = await auth.auth_middleware(stub_request, stub_view)

            assert response.status == 400
            assert invalid_token.called


async def test_auth_middleware_handles_non_scope_views():

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
    stub_view.__name__ = 'test_view'

    await auth.auth_middleware(stub_request, stub_view)

    assert stub_view.awaited_once_with(stub_request)


async def test_auth_middleware_awaits_scoped_views():

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
    stub_view.__name__ = 'test_view_scoped'

    await auth.auth_middleware(stub_request, stub_view)

    assert stub_view.awaited_once_with(stub_request)


async def test_auth_middleware_returns_401_if_token_expired():

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
    stub_view.__name__ = 'test_view'

    with patch('aiohttp_auth.auth.jwt.decode') as jwt_decode:
        with patch('aiohttp_auth.auth.token_expired') as token_expired:
            token_expired.return_value.status = 401
        jwt_decode.side_effect = jwt.ExpiredSignatureError()
        response = await auth.auth_middleware(stub_request, stub_view)

        assert response.status == 401


async def test_auth_middleware_injects_user():

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

        await auth.auth_middleware(stub_request, stub_view)

        assert hasattr(stub_request, 'user')
        assert stub_request.user == {"user_id": 1}


async def test_auth_middleware_handles_user_exceptions():

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

    class TestException(UserDefinedException):
        status = 401
        title = "test"
        detail = "test"

    # make a mock view
    stub_view = CoroutineMock(side_effect=TestException())
    stub_view.__name__ = 'test_view'

    with patch('aiohttp_auth.auth.jwt.decode') as decode:
        with patch('aiohttp_auth.auth.error_response') as error_response:
            error_response.return_value.status = 401
            response = await auth.auth_middleware(stub_request, stub_view)

            assert response.status == 401
            assert error_response.called
            assert decode.called
