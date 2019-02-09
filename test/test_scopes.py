import json
from unittest.mock import patch

import pytest
from aiohttp import web
from aiohttp.test_utils import make_mocked_request

from aiohttp_auth import auth


async def test_scopes_cannot_be_initialized_withot_parameters():
    with pytest.raises(AssertionError) as error:
        auth.scopes()
    assert str(error.value) == 'Cannot be used without any scope!'


async def test_scopes_raises_TypeError_on_invalid_request():
    with pytest.raises(TypeError) as error:
        @auth.scopes('test_scope')
        async def test_view(request):
            return web.json_response({})

        invalid_request = object()
        await test_view(invalid_request)

    assert str(error.value) == F"Invalid Type '{type(invalid_request)}'"


async def test_scopes_returns_403_if_not_has_permisions():
    with patch('aiohttp_auth.auth.check_permissions') as check_permissions:
        check_permissions.return_value = False

        @auth.scopes('test_scope')
        async def test_view(request):
            return web.json_response({})

        stub_request = make_mocked_request(
            'GET', '/', headers={'authorization': 'x'}
        )
        response = await test_view(stub_request)

        assert response.status == 403
        assert json.loads(response.body) == {
            'message': 'Forbidden', "errors": []
        }
