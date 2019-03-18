from datetime import datetime, timedelta

import jwt
from aiohttp import web


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


def decode_jwt(request, jwt_token):
    payload = jwt.decode(
        jwt_token,
        request.app['aiohttp_auth'].jwt_secret,
        algorithms=[request.app['aiohttp_auth'].jwt_algorithm]
    )
    return payload
