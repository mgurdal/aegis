import pytest
from aiohttp.test_utils import make_mocked_request
from aiohttp.web import json_response
from aegis import middlewares
from aegis.exceptions import AuthException
from asynctest import CoroutineMock


async def test_auth_middleware_checks_aiohttp_auth_initialization():
    # make a mock request
    stub_request = CoroutineMock()
    stub_request.app = {}

    # make a mock view
    stub_view = CoroutineMock()

    with pytest.raises(AttributeError) as error:
        # noinspection PyTypeChecker
        await middlewares.auth_middleware(stub_request, stub_view)

    assert str(error.value) == ("Please initialize the authenticator with "
                                "Authenticator.setup(app) first.")


async def test_auth_middleware_uses_auth_exception_if_token_invalid():
    # make a mock Application

    auth_exception = AuthException()
    auth_exception.make_response = CoroutineMock()

    authenticator = CoroutineMock()
    authenticator.decode = CoroutineMock(side_effect=auth_exception)

    app = {'authenticator': authenticator}
    token = 'x'
    # make a mock request
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': token},
        app=app
    )
    # make a mock view
    stub_view = CoroutineMock()

    await middlewares.auth_middleware(stub_request,
                                      stub_view)

    authenticator.decode.awaited_once_with(token)
    assert auth_exception.make_response.awaited_once_with(stub_request)


async def test_auth_middleware_handles_non_scope_views():
    # make a mock Application

    auth_exception = AuthException()
    auth_exception.make_response = CoroutineMock()

    stub_user = {}
    authenticator = CoroutineMock()
    authenticator.decode = CoroutineMock()
    authenticator.get_user = CoroutineMock(return_value=stub_user)

    app = {'authenticator': authenticator}
    token = 'x'
    # make a mock request
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': token},
        app=app
    )

    # make a mock view
    stub_view = CoroutineMock()

    await middlewares.auth_middleware(stub_request, stub_view)

    assert stub_view.awaited_once_with(stub_request)


async def test_auth_middleware_awaits_scoped_views():
    # make a mock Application

    auth_exception = AuthException()
    auth_exception.make_response = CoroutineMock()

    stub_user = {}
    authenticator = CoroutineMock()
    authenticator.decode = CoroutineMock()
    authenticator.get_user = CoroutineMock(return_value=stub_user)

    app = {'authenticator': authenticator}
    token = 'x'
    # make a mock request
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': token},
        app=app
    )

    # make a mock view
    stub_view = CoroutineMock()

    await middlewares.auth_middleware(stub_request, stub_view)

    assert stub_view.awaited_once_with(stub_request)


async def test_auth_middleware_gets_user_from_authenticator():
    # make a mock Application
    user = {'user_id': 1}
    auth_exception = AuthException()
    auth_exception.make_response = CoroutineMock()

    authenticator = CoroutineMock()
    authenticator.decode = CoroutineMock()
    authenticator.get_user = CoroutineMock(return_value=user)

    app = {'authenticator': authenticator}
    token = 'x'
    # make a mock request
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': token},
        app=app
    )

    # make a mock view
    async def stub_view(request):
        return json_response({})

    await middlewares.auth_middleware(stub_request, stub_view)

    assert hasattr(stub_request, 'user')
    assert stub_request.user == {"user_id": 1}


async def test_auth_middleware_awaits_non_scope_views():

    auth_exception = AuthException()
    auth_exception.make_response = CoroutineMock()

    authenticator = CoroutineMock()
    authenticator.decode = CoroutineMock(side_effect=auth_exception)

    app = {'authenticator': authenticator}
    # make a mock request
    stub_request = make_mocked_request(
        'GET', '/', app=app
    )

    handler = CoroutineMock(return_value='test')
    response = await middlewares.auth_middleware(
        stub_request, handler
    )
    assert handler.awaited_once_with(stub_request)
    assert response


async def test_auth_middleware_decodes_expired_refresh_token():
    stub_user = {}
    authenticator = CoroutineMock()
    authenticator.refresh_token = True
    authenticator.decode = CoroutineMock()
    authenticator.get_user = CoroutineMock(return_value=stub_user)

    app = {'authenticator': authenticator}
    # make a mock request for auth/refresh route
    stub_request = make_mocked_request(
        'POST', '/auth/refresh', app=app, headers={
            "Authorization": "Bearer token"
        }
    )

    handler = CoroutineMock(return_value='test')
    response = await middlewares.auth_middleware(
        stub_request, handler
    )
    assert handler.awaited_once_with(stub_request)
    assert response
    authenticator.decode.assert_called_with("Bearer token", verify=False)
