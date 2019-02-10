from aiohttp import web
from aiohttp_auth import auth


DATABASE = {
    'david': {'user_id': 5, 'scopes': ('regular_user', )}
}


async def authenticate(request):
    payload = await request.json()
    user = DATABASE.get(payload['username'])

    return user


async def public(request):
    return web.json_response({'hello': 'anonymous'})


@auth.scopes('regular_user')
async def protected(request):
    return web.json_response({'hello': 'user'})


def create_app():
    app = web.Application()

    app.router.add_get('/public', public)
    app.router.add_get('/protected', protected)

    auth.setup(app, authenticate, jwt_secret="test")
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)
