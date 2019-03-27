from abc import abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict

import jwt
from aiohttp import web

from ..exceptions import InvalidTokenException, TokenExpiredException
from .base import BaseAuthenticator


class JWTAuth(BaseAuthenticator):
    jwt_secret: str
    duration: int = 25_000
    jwt_algorithm: str = 'HS256'

    async def decode(self, jwt_token: str) -> dict:

        try:
            jwt_token = jwt_token.replace('Bearer ', '')
            payload = jwt.decode(
                jwt_token,
                self.jwt_secret,
                algorithms=(self.jwt_algorithm,)
            )
            return payload

        except jwt.DecodeError:
            raise InvalidTokenException()

        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()

    async def encode(self, payload: dict) -> str:
        delta_seconds = self.duration
        jwt_data = {
            **payload,
            'exp': datetime.utcnow() + timedelta(seconds=delta_seconds)
        }

        jwt_token = jwt.encode(
            jwt_data,
            self.jwt_secret,
            self.jwt_algorithm
        )
        token = jwt_token.decode('utf-8')

        return token

    async def get_scopes(self, request: web.Request):
        # TODO: handle exceptions
        return request.user['scopes']

    @abstractmethod
    async def authenticate(self, request: web.Request) -> Dict[str, Any]:
        """Returns JSON serializable user"""
