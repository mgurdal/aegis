from aiohttp import web
from aegis import JWTAuth, permissions


class JWTAuthenticator(JWTAuth):
    jwt_secret = "<secret>"

    async def authenticate(self, request: web.Request) -> dict:
        credentials = await request.json()
        username = credentials["username"]

        # Fetch user with its permissions from database
        database = app["db"]
        user = database.get(username)
        return user


@permissions('user', 'admin')
async def user_page(request):
    return web.json_response({'hello': 'user'})


@permissions('admin')
async def admin_page(request):
    return web.json_response({'hello': 'admin'})


def create_app():
    app = web.Application()
    database = {
        "user": {
            "permissions": ["user"]
        },
        "admin": {
            "permissions": ["user", "admin"]
        }
    }
    app["db"] = database

    app.router.add_get('/user', user_page)
    app.router.add_get('/admin', admin_page)

    JWTAuthenticator.setup(app)

    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app)
