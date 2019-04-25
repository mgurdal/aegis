from aiohttp import web
from aegis.exceptions import AuthException
from aegis.authenticators.jwt import JWTAuth


class UserDoesNotExistsError(AuthException):
    status = 404

    @staticmethod
    def get_schema() -> dict:
        return {"message":  "User does not exists."}


class MyAuth(JWTAuth):
    jwt_secret = "secret"

    async def authenticate(self, request):
        raise UserDoesNotExistsError()


def create_app():
    app = web.Application()

    MyAuth.setup(app)
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)
