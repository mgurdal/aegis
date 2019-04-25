import functools
from typing import Callable, Union

from aiohttp import web

from .exceptions import AuthRequiredException, ForbiddenException


def login_required(func):

    def wrapper(request):
        if not isinstance(request, web.Request):
            raise TypeError(F"Invalid Type '{type(request)}'")

        if not hasattr(request, 'user'):
            return AuthRequiredException.make_response(request)
        return func(request)

    return wrapper


def scopes(
        *required_scopes: Union[set, tuple],
        algorithm='any') -> web.json_response:
    assert required_scopes, 'Cannot be used without any scope!'

    def request_handler(view: Callable) -> Callable:
        @functools.wraps(view)
        async def wrapper(request: web.Request):
            if not isinstance(request, web.Request):
                raise TypeError(F"Invalid Type '{type(request)}'")

            authenticator = request.app['authenticator']

            provided_scopes = await authenticator.get_scopes(request)
            has_permission = await authenticator.check_permissions(
                provided_scopes, required_scopes, algorithm=algorithm
            )

            if not has_permission:
                return ForbiddenException.make_response(request)
            else:
                return await view(request)

        return wrapper

    return request_handler
