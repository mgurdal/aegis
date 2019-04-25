import base64
import binascii
from abc import abstractmethod
from typing import Dict, Any

from aiohttp import web

from aegis.exceptions import InvalidTokenException
from .base import BaseAuthenticator


class BasicAuth(BaseAuthenticator):
    user_id = "user_id"
    password = "password"
    auth_endpoint = None
    me_endpoint = None

    async def get_scopes(self, request: web.Request):
        """:returns user's permissions"""

    @abstractmethod
    async def authenticate(self, request: web.Request) -> Dict[str, Any]:
        """Returns JSON serializable user"""

    async def decode(self, token: str, verify=True) -> dict:
        """
        Decodes basic token and returns user's id and password as a dict.
        """
        try:
            basic_token = token.replace("Basic ", "").encode()

            decoded_credentials = base64.b64decode(
                basic_token, validate=verify
            ).decode()
            user_id, password = decoded_credentials.split(":")
            # create payload with pre-defined keys
            payload = {
                self.user_id: user_id,
                self.password: password
            }
            return payload
        except binascii.Error:
            raise InvalidTokenException()
