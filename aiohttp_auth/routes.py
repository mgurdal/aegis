from aiohttp import web

from .tokenizers import generate_jwt
from .exceptions import UserDefinedException
from .responses import error_response, access_token, forbidden


def make_auth_route(authenticator):
    async def auth_route(request: web.Request):
        try:
            user = await authenticator(request)
        except UserDefinedException as ude:
            return error_response(request, ude)

        # use auth.login to generate a JWT token
        # with some unique user information
        token = await generate_jwt(request, user)

        return access_token(token)

    return auth_route


def make_me_route():
    async def me_route(request: web.Request):
        user_authenticated = hasattr(request, 'user')
        if user_authenticated:
            user = request.user
            # remove expiration date
            user.pop('exp')
            return web.json_response(request.user)
        else:
            return forbidden(request)

    return me_route
