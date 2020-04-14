from unittest.mock import patch

import pytest
from aiohttp import web
from aiohttp.test_utils import make_mocked_request
from aegis import decorators
from asynctest import CoroutineMock


async def test_login_required_raises_TypeError_on_invalid_request():
    with pytest.raises(TypeError) as error:

        @decorators.login_required
        async def test_view(request):
            return web.json_response({})

        invalid_request = object()
        await test_view(invalid_request)

    assert str(error.value) == f"Invalid Type '{type(invalid_request)}'"


async def test_login_required_handles_no_user():
    with patch("aegis.decorators.AuthRequiredException.make_response") as auth_required:

        @decorators.login_required
        async def test_view(request):
            return web.json_response({})

        stub_request = make_mocked_request("GET", "/", headers={"authorization": "x"})
        auth_required.return_value.status = 401
        response = test_view(stub_request)

        assert response.status == 401
        auth_required.assert_called_once_with(stub_request)

async def test_login_required_returns_401_if_request_user_is_invalid():
    with patch("aegis.decorators.AuthRequiredException.make_response") as auth_required:

        @decorators.login_required
        async def test_view(request):
            return web.json_response({})

        stub_request = make_mocked_request("GET", "/", headers={"authorization": "x"})
        stub_request.user = None
        auth_required.return_value.status = 401
        response = test_view(stub_request)

        assert response.status == 401
        auth_required.assert_called_once_with(stub_request)

async def test_login_required_returns_200_if_request_has_user():
    @decorators.login_required
    async def test_view(request):
        return web.json_response({})

    stub_request = make_mocked_request("GET", "/", headers={"authorization": "x"})
    stub_request.user = {"id": 7}
    response = await test_view(stub_request)

    assert response.status == 200


async def test_get_permissions_cannot_be_initialized_without_parameters():
    with pytest.raises(AssertionError) as error:
        decorators.permissions()
    assert str(error.value) == "Cannot be used without any permission!"


async def test_permissions_raises_TypeError_on_invalid_request():
    with pytest.raises(TypeError) as error:

        @decorators.permissions("test_permission")
        async def test_view(request):
            return web.json_response({})

        invalid_request = object()
        await test_view(invalid_request)

    assert str(error.value) == f"Invalid Type '{type(invalid_request)}'"


async def test_permissions_returns_403_if_not_has_permisions():
    with patch("aegis.decorators.ForbiddenException.make_response") as forbidden:
        required_permissions = ("test_permission",)
        provided_permissions = ()

        @decorators.permissions(*required_permissions, algorithm="any")
        async def test_view(request):
            return web.json_response({})

        stub_request = make_mocked_request("GET", "/", headers={"authorization": "x"})
        authenticator = CoroutineMock()
        stub_request.app["authenticator"] = authenticator
        authenticator.get_permissions = CoroutineMock(return_value=provided_permissions)
        authenticator.check_permissions = CoroutineMock(return_value=False)

        await test_view(stub_request)

        assert forbidden.awaited_once_with(stub_request)
        assert authenticator.get_permissions.awaited_once_with(stub_request)
        assert authenticator.get_permissions.awaited_once_with(
            provided_permissions, required_permissions, "any"
        )


async def test_permissions_awaits_view_on_happy_path():
    with patch("aegis.decorators.ForbiddenException.make_response") as forbidden:
        required_permissions = ("test_permission",)
        provided_permissions = ()

        @decorators.permissions(*required_permissions)
        async def test_view(request):
            return web.json_response({})

        stub_request = make_mocked_request("GET", "/", headers={"authorization": "x"})
        authenticator = CoroutineMock()
        stub_request.app["authenticator"] = authenticator
        authenticator.get_permissions = CoroutineMock(return_value=provided_permissions)
        authenticator.check_permissions = CoroutineMock(return_value=True)

        await test_view(stub_request)

        assert authenticator.get_permissions.awaited_once_with(stub_request)
        assert authenticator.get_permissions.awaited_once_with(
            provided_permissions, required_permissions, "any"
        )
        assert forbidden.not_awaited
