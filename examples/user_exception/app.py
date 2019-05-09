from aiohttp import web
from aegis import AuthException, JWTAuth


class UserDoesNotExistsError(AuthException):
    status = 401

    @staticmethod
    def get_schema() -> dict:
        return {"message":  "User does not exists."}


class JWTAuthenticator(JWTAuth):
    jwt_secret = "<secret>"

    async def authenticate(self, request):
        raise UserDoesNotExistsError()


def create_app():
    app = web.Application()

    JWTAuthenticator.setup(app)
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)
