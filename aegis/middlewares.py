from typing import Callable

from aiohttp import web

from .exceptions import AuthException


@web.middleware
async def auth_middleware(request: web.Request, handler: Callable):
    """Handles token decoding, failed authorization responses,  """
    authenticator = request.app.get("authenticator")
    if not authenticator:
        raise AttributeError(
            (
                "Please initialize the authenticator with "
                "Authenticator.setup(app) first."
            )
        )

    token = request.headers.get("authorization")

    if token:
        try:
            user_trying_to_refresh = (
                str(request.rel_url) == "/auth/refresh" and authenticator.refresh_token
            )
            if user_trying_to_refresh:
                credentials = await authenticator.decode(token, verify=False)
            else:
                credentials = await authenticator.decode(token)

            request.user = await authenticator.get_user(credentials)
            return await handler(request)

        except AuthException as ae:
            return ae.make_response(request)

    else:
        response = await handler(request)
        return response
