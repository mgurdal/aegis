from aiohttp import web
from aegis import decorators, JWTAuth


class JWTAuthenticator(JWTAuth):
    jwt_secret = "<secret>"

    async def authenticate(self, request: web.Request) -> dict:
        # You can get the request payload of the /auth route
        payload = await request.json()

        # Assuming the name parameter send in the request payload
        searched_name = payload["name"]

        # fetch the user from your storage
        db = request.app["db"]
        user = db.get(searched_name, None)

        # return the JSON serializable user
        return user


@decorators.login_required
async def protected(request):
    return web.json_response({'hello': 'user'})


if __name__ == "__main__":
    app = web.Application()

    database = {
        'david': {'id': 5}
    }
    app["db"] = database

    app.router.add_get('/', protected)

    JWTAuthenticator.setup(app)

    web.run_app(app)
