from aiohttp import web
from aiohttp_auth import auth


DATABASE = {
    5: {'id': 5, 'scopes': ('regular_user', )}
}


async def login(request: web.Request):
    payload = await request.json()

    user_id = payload['user_id']
    # use auth.login to generate a JWT token
    # with some unique user information
    token = await auth.login(request, user_id)

    return web.json_response({'token': token})


@auth.middleware
async def user_middleware(request, jwt_payload: dict):
    # Use the JWT payload to initialize the user
    user_id = jwt_payload['user_id']
    user = DATABASE[user_id]
    request.user = user
    return request


async def public(request):
    return web.json_response({'hello': 'anonymous'})


@auth.scopes('regular_user')
async def protected(request):
    return web.json_response({'hello': 'user'})

if __name__ == '__main__':
    app = web.Application(middlewares=[user_middleware, ])

    app.router.add_post('/login', login)
    app.router.add_get('/public', public)
    app.router.add_get('/protected', protected)

    auth.setup(app, jwt_secret='secret_key')
    web.run_app(app)
