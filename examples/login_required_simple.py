from aiohttp import web
from aiohttp_auth import auth


async def authenticate(request):
    user = {
        "user_id": "5",
        "name": "K Lars Lohn",
    }
    return user


async def public(request):
    return web.json_response({'hello': 'anonymous'})


@auth.login_required
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
