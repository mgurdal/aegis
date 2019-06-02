from abc import abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict

import jwt
from aiohttp import web

from ..routes import make_refresh_route
from ..exceptions import InvalidTokenException, TokenExpiredException
from .base import BaseAuthenticator


class JWTAuth(BaseAuthenticator):
    jwt_secret: str
    duration: int = 25_000
    jwt_algorithm: str = "HS256"
    refresh_token = False
    refresh_endpoint = "/auth/refresh"
    auth_schema = "Bearer"

    async def decode(self, jwt_token: str, verify=True) -> dict:
        """Decodes the given token and returns as a dict.
        Raises validation exceptions if verify is set to True."""
        try:
            jwt_token = jwt_token.replace(f"{self.auth_schema} ", "")
            payload = jwt.decode(
                jwt_token,
                self.jwt_secret,
                algorithms=(self.jwt_algorithm,),
                options={"verify_exp": verify},
            )

            return payload

        except jwt.DecodeError:
            raise InvalidTokenException()

        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()

    async def encode(self, payload: dict) -> str:
        """Encodes the given payload and returns as a string."""
        delta_seconds = self.duration
        jwt_data = {
            **payload,
            "exp": datetime.utcnow() + timedelta(seconds=delta_seconds),
        }

        jwt_token = jwt.encode(jwt_data, self.jwt_secret, self.jwt_algorithm)
        token = jwt_token.decode("utf-8")

        return token

    async def get_user(self, credentials) -> dict:
        return credentials

    @abstractmethod
    async def authenticate(self, request: web.Request) -> Dict[str, Any]:
        """Returns JSON serializable user"""

    @classmethod
    def setup(cls, app):
        super().setup(app)
        authenticator = app["authenticator"]

        if authenticator.refresh_token:
            if not hasattr(authenticator, "get_refresh_token"):
                raise NotImplementedError(
                    (
                        "get_refresh_token method needs to be implemented"
                        "in order to use the refresh token feature."
                    )
                )
            app.router.add_post(
                authenticator.refresh_endpoint, make_refresh_route(authenticator)
            )
