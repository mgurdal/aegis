from aiohttp import web

from .auth import login_required
from .exceptions import (AuthException, ForbiddenException,
                         InvalidRefreshTokenException)


def make_auth_route(authenticator):
    async def auth_route(request: web.Request):
        try:
            user = await authenticator.authenticate(request)
            request.user = user
        except AuthException as ae:
            return ae.make_response(request)

        # use auth.login to generate a JWT token
        # with some unique user information
        token = await authenticator.encode(user)
        token_payload = {
            "access_token": token
        }
        if authenticator.refresh_token:
            token_payload[
                "refresh_token"] = await authenticator.get_refresh_token(
                request)

        return web.json_response(token_payload, status=200)

    return auth_route


def make_me_route():
    async def me_route(request: web.Request):
        user_authenticated = hasattr(request, 'user')
        if user_authenticated:
            return web.json_response(request.user)
        else:
            return ForbiddenException.make_response(request)

    return me_route


def make_refresh_route(authenticator):
    @login_required
    async def refresh_route(request: web.Request):
        refresh_valid = await authenticator.validate_refresh_token(request)
        if not refresh_valid:
            return InvalidRefreshTokenException.make_response(request)

        access_token = await authenticator.encode(request.user)
        return web.json_response({
            "access_token": access_token
        })

    return refresh_route
