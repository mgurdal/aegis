from aiohttp import web
from aiohttp_auth import auth
from aiohttp_auth.exceptions import UserDefinedException


class UserDoesNotExistsError(UserDefinedException):
    status = 404
    title = "User does not exists."
    detail = "We could not find the user with {name}"


async def authenticate(request):
    raise UserDoesNotExistsError(name="K Lars Lohn")


def create_app():
    app = web.Application()

    auth.setup(app, authenticate, jwt_secret="test")
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)
