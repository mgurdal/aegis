import functools
from typing import Callable, Union

from aiohttp import web

from .exceptions import AuthRequiredException, ForbiddenException, AuthException


def login_required(func):
    """
    If not authenticated user tries to reach to a `login_required` end-point
    returns UNAUTHORIZED response.
    """

    def wrapper(request):
        if not isinstance(request, web.Request):
            raise TypeError(f"Invalid Type '{type(request)}'")

        if not getattr(request, "user", None):
            return AuthRequiredException.make_response(request)
        return func(request)

    return wrapper


def permissions(
    *required_scopes: Union[set, tuple], algorithm="any"
) -> web.json_response:

    """
    Open the end-point for any user who has the permission to access.
    """
    assert required_scopes, "Cannot be used without any permission!"

    def request_handler(view: Callable) -> Callable:
        @functools.wraps(view)
        async def wrapper(request: web.Request):
            if not isinstance(request, web.Request):
                raise TypeError(f"Invalid Type '{type(request)}'")

            authenticator = request.app["authenticator"]
            try:
                provided_scopes = await authenticator.get_permissions(request)
                has_permission = await authenticator.check_permissions(
                    provided_scopes, required_scopes, algorithm=algorithm
                )

                if not has_permission:
                    raise ForbiddenException()

                return await view(request)

            except AuthException as e:
                return e.make_response(request)

        return wrapper

    return request_handler
