from aiohttp import web
from aegis import auth
from aegis.authenticators.basic import BasicAuth
from aegis.exceptions import AuthRequiredException

DATABASE = {
    'david': {
        'user_id': 5,
        'scopes': ('regular_user',),
        'password': 'test'
    }
}


class AuthenticationFailedException(AuthRequiredException):
    status = 401

    @staticmethod
    def get_schema() -> dict:
        # get default schema
        schema = AuthRequiredException.get_schema()
        # alter response title and detail
        schema["title"] = "Invalid Credentials."
        schema["detail"] = (
            "You have provided invalid authorization"
            "token or user_id/password pair."
        )
        return schema


class MyAuth(BasicAuth):
    user_id = "username"  # default is user_id
    password = "password"

    async def authenticate(self, request: web.Request) -> dict:
        token = request.headers.get("Authorization")
        credentials = await self.decode(token)

        username = credentials.get("username")
        password = credentials.get("password")

        user = DATABASE.get(username)
        if not user or user["password"] != password:
            raise AuthenticationFailedException()

        # Returned user will also be stored in the request object
        # for further permission checks in middlewares and views.
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

    MyAuth.setup(app)
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)
