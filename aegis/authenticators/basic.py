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
    auth_schema = "Basic"

    @abstractmethod
    async def authenticate(self, request: web.Request) -> Dict[str, Any]:
        """Returns JSON serializable user"""

    async def get_user(self, credentials) -> dict:
        """Retrieve user with credentials."""

    async def decode(self, token: str, verify=True) -> dict:
        """
        Decodes basic token and returns user's id and password as a dict.
        """
        try:
            basic_token = token.replace(f"{self.auth_schema} ", "").encode()

            decoded_credentials = base64.b64decode(
                basic_token, validate=verify
            ).decode()
            user_id, password = decoded_credentials.split(":")
            # create payload with pre-defined keys
            payload = {self.user_id: user_id, self.password: password}
            return payload
        except binascii.Error:
            raise InvalidTokenException()
