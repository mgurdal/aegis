import pytest
from aiohttp import web
from aiohttp_auth.authenticators.jwt import JWTAuth


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

    assert 'aiohttp_auth' in app
