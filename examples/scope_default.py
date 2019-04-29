from aiohttp import web
from aegis import decorators
from aegis.authenticators.jwt import JWTAuth


class MyAuth(JWTAuth):
    jwt_secret = "test"

    async def authenticate(self, request: web.Request) -> dict:
        payload = await request.json()
        user = request.app["db"].get(payload['username'])
        return user


async def public(request):
    return web.json_response({'hello': 'anonymous'})


@decorators.scopes('regular_user')
async def protected(request):
    return web.json_response({'hello': 'user'})


def create_app():
    app = web.Application()

    database = {
        'david': {'user_id': 5, 'scopes': ('user',)}
    }
    app["db"] = database

    app.router.add_get('/public', public)
    app.router.add_get('/protected', protected)

    MyAuth.setup(app)
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)
