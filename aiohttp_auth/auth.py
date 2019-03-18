import functools
import inspect
from typing import Callable, Union

import jwt

from aiohttp import web

from .exceptions import UserDefinedException
from .matching_algorithms import match_all, match_any, match_exact
from .responses import (auth_required, error_response, forbidden,
                        invalid_token, token_expired)
from .routes import make_auth_route, make_me_route
from .tokenizers import decode_jwt


def login_required(func):

    def wrapper(request):
        if not isinstance(request, web.Request):
            raise TypeError(F"Invalid Type '{type(request)}'")

        if not hasattr(request, 'user'):
            return auth_required(request)
        return func(request)

    return wrapper


async def check_permissions(
        request: web.Request,
        scopes: Union[set, tuple],
        algorithm: Union[str, Callable] = 'any') -> bool:
    # user injected into request by the auth_middleware
    user = getattr(request, 'user', None)
    has_permission = False
    if user:
        # non-anonymous user tries to reach to a scoped end-point
        user_is_anonymous = user['scopes'] == ('anonymous_user',)
        if not user_is_anonymous:
            if algorithm == 'any':
                has_permission = match_any(
                    required=scopes,
                    provided=request.user['scopes']
                )
            elif algorithm == 'all':
                has_permission = match_all(
                    required=scopes,
                    provided=request.user['scopes']
                )
            elif algorithm == 'exact':
                has_permission = match_exact(
                    required=scopes,
                    provided=request.user['scopes']
                )
            elif inspect.isfunction(algorithm):
                has_permission = algorithm(
                    required=scopes,
                    provided=request.user['scopes']
                )
            else:
                raise TypeError(
                    "Invalid algorithm type. "
                    "Options 'all', 'any', 'exact', callable"
                )
    return has_permission


def scopes(
        *required_scopes: Union[set, tuple],
        algorithm='any') -> web.json_response:
    assert required_scopes, 'Cannot be used without any scope!'

    def request_handler(view: Callable) -> Callable:
        @functools.wraps(view)
        async def wrapper(request: web.Request):
            if not isinstance(request, web.Request):
                raise TypeError(F"Invalid Type '{type(request)}'")

            has_permission = await check_permissions(
                request, required_scopes, algorithm=algorithm
            )

            if not has_permission:
                return forbidden(request)
            else:
                return await view(request)

        wrapper.__name__ = F"{wrapper.__name__}_scoped"
        return wrapper

    return request_handler


@web.middleware
async def auth_middleware(request: web.Request, handler: Callable):
    if 'aiohttp_auth' not in request.app:
        raise AttributeError('Please initialize aiohttp_auth first.')
    jwt_token = request.headers.get('authorization')
    if jwt_token:
        try:
            jwt_token = jwt_token.replace('Bearer ', '')
            user = decode_jwt(request, jwt_token)
            request.user = user
            return await handler(request)

        except jwt.DecodeError:
            return invalid_token(request)

        except jwt.ExpiredSignatureError:
            return token_expired(request)

        except UserDefinedException as ude:
            return error_response(request, ude)

    # view uses the scope decorator and
    # does not have he _scoped postfix
    elif handler.__name__.endswith('_scoped'):
        return forbidden(request)
    else:
        return await handler(request)


class JWTAuth:
    def __init__(self, jwt_secret: str, duration=25e3, jwt_algorithm='HS256'):
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm
        self.duration = duration


def setup(app, authenticator, jwt_secret: str):
    app['aiohttp_auth'] = JWTAuth(jwt_secret)
    app.middlewares.append(auth_middleware)
    auth_route = make_auth_route(authenticator)
    me_route = make_me_route()
    app.router.add_post('/auth', auth_route)
    app.router.add_get('/me', me_route)
    return app
