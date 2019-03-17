from unittest.mock import patch

import pytest
from aiohttp import web
from aiohttp.test_utils import make_mocked_request
from aiohttp_auth import auth


async def test_login_required_raises_TypeError_on_invalid_request():
    with pytest.raises(TypeError) as error:
        @auth.login_required
        async def test_view(request):
            return web.json_response({})

        invalid_request = object()
        await test_view(invalid_request)

    assert str(error.value) == F"Invalid Type '{type(invalid_request)}'"


async def test_login_required_handles_no_user():

    @auth.login_required
    async def test_view(request):
        return web.json_response({})

    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )
    with patch('aiohttp_auth.auth.auth_required') as auth_required:
        auth_required.return_value.status = 401
        response = test_view(stub_request)

        assert response.status == 401
        auth_required.assert_called_once_with(stub_request)


async def test_login_required_returns_200_if_request_has_user():

    @auth.login_required
    async def test_view(request):
        return web.json_response({})

    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )
    stub_request.user = {
        "id": 7
    }
    response = await test_view(stub_request)

    assert response.status == 200
