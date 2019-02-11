from aiohttp import web
from aiohttp_auth import auth


async def test_setup_injects_jwt_auth():
    app = web.Application()

    initialized_app = auth.setup(app, authenticator=None, jwt_secret='tests')

    assert 'aiohttp_auth' in initialized_app
