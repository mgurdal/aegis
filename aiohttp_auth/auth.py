import functools
from datetime import datetime, timedelta
from typing import Callable, Union

import jwt

from aiohttp import web
from aiohttp.web import json_response
from aiohttp_auth.exceptions import UserDefinedException

from .responses import (access_token, auth_required, error_response, forbidden,
                        invalid_token, token_expired)


async def generate_jwt(request: web.Request, payload: dict) -> str:
    delta_seconds = request.app['aiohttp_auth'].duration
    jwt_data = {
        **payload,
        'exp': datetime.utcnow() + timedelta(seconds=delta_seconds)
    }

    jwt_token = jwt.encode(
        jwt_data,
        request.app['aiohttp_auth'].jwt_secret,
        request.app['aiohttp_auth'].jwt_algorithm
    )
    token = jwt_token.decode('utf-8')

    return token


def login_required(func):

    def wrapper(request):
        if not isinstance(request, web.Request):
            raise TypeError(F"Invalid Type '{type(request)}'")

        if not hasattr(request, 'user'):
            return auth_required(request)
        return func(request)

    return wrapper


def check_permissions(request: web.Request, scopes: Union[set, tuple]) -> bool:
    # if a user injected into request by the auth_middleware
    user = getattr(request, 'user', None)
    has_permission = False
    if user:
        # if a non-anonymous user tries to reach to
        # a scoped endpoint
        user_is_anonymous = user['scopes'] == ('anonymous_user',)
        if not user_is_anonymous:
            user_scopes = set(request.user['scopes'])
            required_scopes = set(scopes)
            if user_scopes.intersection(required_scopes):
                has_permission = True

    return has_permission


def scopes(*required_scopes: Union[set, tuple]) -> web.json_response:
    assert required_scopes, 'Cannot be used without any scope!'

    def request_handler(view: Callable) -> Callable:
        @functools.wraps(view)
        async def wrapper(request: web.Request):
            if not isinstance(request, web.Request):
                raise TypeError(F"Invalid Type '{type(request)}'")

            has_permission = check_permissions(request, required_scopes)

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
            user = jwt.decode(
                jwt_token,
                request.app['aiohttp_auth'].jwt_secret,
                algorithms=[request.app['aiohttp_auth'].jwt_algorithm]
            )
            request.user = user
            return await handler(request)

        except jwt.DecodeError:
            return invalid_token(request)

        except jwt.ExpiredSignatureError:
            return token_expired(request)

        except UserDefinedException as ude:
            return error_response(request, ude)

    # if view uses the scope decorator and
    # does not have he _scoped postfix
    elif handler.__name__.endswith('_scoped'):
        return forbidden(request)
    else:
        return await handler(request)


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
            return json_response(request.user)
        else:
            return forbidden(request)

    return me_route


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
