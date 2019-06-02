from aiohttp import web
from aegis import login_required, JWTAuth


class JWTAuthenticator(JWTAuth):
    jwt_secret = "<secret>"

    async def authenticate(self, request: web.Request) -> dict:
        db = request.app["db"]
        credentials = await request.json()
        id_ = credentials["id"]
        user = db.get(id_)
        return user


@login_required
async def protected(request):
    return web.json_response({"hello": "user"})


def create_app():
    app = web.Application()
    app["db"] = {5: {"name": "test"}}
    app.router.add_get("/protected", protected)

    JWTAuthenticator.setup(app)

    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app)
