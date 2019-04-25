from aiohttp import web
from aegis import auth
from aegis.authenticators.jwt import JWTAuth

DATABASE = {
    'david': {'user_id': 5, 'scopes': ('user', 'admin')}
}


class MyAuth(JWTAuth):
    jwt_secret = "test"

    async def authenticate(self, request: web.Request) -> dict:
        payload = await request.json()
        user = DATABASE.get(payload['username'])
        return user


def scope_algorithm(required_scopes, user_scopes) -> bool:
    has_permission = len(user_scopes) == len(required_scopes)
    return has_permission


async def public(request):
    return web.json_response({'hello': 'anonymous'})


@auth.scopes('user', 'test', algorithm=scope_algorithm)
async def protected(request):
    return web.json_response({'hello': 'user'})


def create_app():
    app = web.Application()

    app.router.add_get('/public', public)
    app.router.add_get('/protected', protected)

    MyAuth.setup(app)
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)
