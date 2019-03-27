from aiohttp import web

from .exceptions import AuthException, ForbiddenException


def make_auth_route(authenticator):
    async def auth_route(request: web.Request):
        try:
            user = await authenticator.authenticate(request)
        except AuthException as ae:
            return ae.make_response(request)

        # use auth.login to generate a JWT token
        # with some unique user information
        token = await authenticator.encode(user)

        return web.json_response({
            "access_token": token
        }, status=200)

    return auth_route


def make_me_route():
    async def me_route(request: web.Request):
        user_authenticated = hasattr(request, 'user')
        if user_authenticated:
            return web.json_response(request.user)
        else:
            return ForbiddenException.make_response(request)

    return me_route
