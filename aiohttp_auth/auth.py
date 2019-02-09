import jwt
from datetime import datetime, timedelta

from typing import Callable, Union
from aiohttp import web
from aiohttp.web import json_response


async def login(request: web.Request, payload: dict) -> str:
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


def scopes(*scopes: Union[set, tuple]) -> web.json_response:
    assert scopes, 'Cannot be used without any scope!'

    def request_handler(func: Callable) -> Callable:
        async def wrapper(request_or_view: Union[web.Request, web.View]):
            if isinstance(request_or_view, web.View):
                request = request_or_view.request
            elif isinstance(request_or_view, web.Request):
                request = request_or_view
            else:
                raise TypeError(F"Invalid Type '{type(request_or_view)}'")

            has_permission = False
            if scopes:
                # if a user injected into request by the auth_middleware
                user = getattr(request, 'user', None)
                if user:
                    # if a non-anonymous user tries to reach to
                    # a scoped endpoint
                    user_is_anonymous = user['scopes'] == ('anonymous_user',)
                    if not user_is_anonymous:
                        user_scopes = set(request.user['scopes'])
                        required_scopes = set(scopes)
                        if user_scopes.intersection(required_scopes):
                            has_permission = True

            if not has_permission:
                return json_response(
                    {'status': 403, 'message': 'Forbidden'},
                    status=403
                )
            else:
                return await func(request_or_view)

        return wrapper
    return request_handler


def middleware(user_injector: Callable) -> web.middleware:
    @web.middleware
    async def wrapper(request: web.Request, handler: Callable):
        if 'aiohttp_auth' not in request.app:
            raise AttributeError('Please initialize aiohttp_auth first.')

        jwt_token = request.headers.get('authorization')
        if jwt_token:
            try:
                jwt_token = jwt_token.replace('Bearer ', '')
                payload = jwt.decode(
                    jwt_token,
                    request.app['aiohttp_auth'].jwt_secret,
                    algorithms=[request.app['aiohttp_auth'].jwt_algorithm]
                )
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return json_response(
                    {"status": 401, 'message': 'Invalid Token'},
                    status=401
                )
            request = await user_injector(request, payload)
        else:
            anonymous_user = {
                'scopes': ('anonymous_user', )
            }
            request.user = anonymous_user
        return await handler(request)
    return wrapper


class JWTAuth:
    def __init__(self, jwt_secret: str, duration: int, jwt_algorithm: str):
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm
        self.duration = duration


def setup(app, jwt_secret, duration=259200, jwt_algorithm='HS256'):
    app['aiohttp_auth'] = JWTAuth(jwt_secret, duration, jwt_algorithm)
    return app
