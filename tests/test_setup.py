import pytest
from aiohttp import web
from aegis.authenticators.jwt import JWTAuth


async def test_setup_requires_authenticate_method():
    app = web.Application()

    class TestAuth(JWTAuth):
        pass

    with pytest.raises(TypeError) as err:
        TestAuth.setup(app)

    assert err


async def test_setup_injects_jwt_auth():
    app = web.Application()

    class TestAuth(JWTAuth):
        async def authenticate(self, request: web.Request):
            pass

    TestAuth.setup(app)

    assert "authenticator" in app


async def test_setup_raises_error_if_refresh_token_true_and_no_method():
    """JWT Authenticator setup raises if the refresh_token flag is set to True
    and authenticator class does not have the get_refresh_token implemented.
    """
    app = web.Application()

    class TestAuth(JWTAuth):
        refresh_token = True

        async def authenticate(self, request: web.Request):
            pass

    with pytest.raises(NotImplementedError):
        TestAuth.setup(app)


async def test_setup_adds_refresh_route_if_refresh_token_is_set():
    """JWT Authenticator setup completes with success
    if the refresh_token flag is set to True and get_refresh_token implemented.
    """
    app = web.Application()

    class TestAuth(JWTAuth):
        refresh_token = True

        async def authenticate(self, request: web.Request):
            pass

        async def get_refresh_token(self, request):
            pass

    TestAuth.setup(app)

    resource_paths = [resource._path for resource in app.router.resources()]
    assert "/auth/refresh" in resource_paths


async def test_not_setup_refresh_token_if_false():
    app = web.Application()

    class TestAuth(JWTAuth):
        refresh_token = False

        async def authenticate(self, request: web.Request):
            pass

    TestAuth.setup(app)

    resource_paths = [resource._path for resource in app.router.resources()]
    assert "/auth/refresh" not in resource_paths
