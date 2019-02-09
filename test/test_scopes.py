from aiohttp import web
from aiohttp_auth import auth


async def test_setup_injects_jwt_auth():
    app = web.Application()
    initialized_app = auth.setup(app, jwt_secret='test')

    assert 'aiohttp_auth' in initialized_app
