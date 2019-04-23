from typing import Callable

from aiohttp import web

from .exceptions import AuthException


@web.middleware
async def auth_middleware(request: web.Request, handler: Callable):
    authenticator = request.app.get('aiohttp_auth')
    if not authenticator:
        raise AttributeError('Please initialize aiohttp_auth first.')

    token = request.headers.get('authorization')

    if token:
        try:
            user_trying_to_refresh = (
                    str(request.rel_url) == "/auth/refresh"
                    and authenticator.refresh_token
            )
            if user_trying_to_refresh:
                user = await authenticator.decode(token, verify=False)
            else:
                user = await authenticator.decode(token)

            request.user = user
            return await handler(request)

        except AuthException as ae:
            return ae.make_response(request)

    else:
        response = await handler(request)
        return response
