from aiohttp import web
from aegis import permissions, JWTAuth
from aegis.matching_algorithms import match_any


class JWTAuthenticator(JWTAuth):
    jwt_secret = "<secret>"

    async def authenticate(self, request: web.Request) -> dict:
        credentials = await request.json()
        username = credentials["username"]

        # Fetch user with its permissions from database
        database = app["db"]
        user = database.get(username)
        return user


def match_any_and_admin(required_permissions, user_permissions) -> bool:
    # ignore the matching algorithm if user is admin
    has_permission = "admin" in user_permissions or match_any(
        required_permissions, user_permissions
    )
    return has_permission


@permissions("user", algorithm=match_any_and_admin)
async def user_page(request):
    return web.json_response({"hello": "user"})


@permissions("admin")
async def admin_page(request):
    return web.json_response({"hello": "admin"})


def create_app():
    app = web.Application()
    database = {"user": {"permissions": ["user"]}, "admin": {"permissions": ["admin"]}}
    app["db"] = database

    app.router.add_get("/user", user_page)
    app.router.add_get("/admin", admin_page)

    JWTAuthenticator.setup(app)

    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app)
