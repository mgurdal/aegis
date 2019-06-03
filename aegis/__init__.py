"""
aegis allows to protect endpoints
and also provides authentication scoping.
"""

__version__ = "1.1.0"

__all__ = [
    "BaseAuthenticator",
    "JWTAuth",
    "BasicAuth",
    "login_required",
    "permissions",
    "AuthException",
    "AuthRequiredException",
    "AuthenticationFailedException",
    "TokenExpiredException",
    "InvalidRefreshTokenException",
    "ForbiddenException",
    "InvalidTokenException",
]
from .authenticators.base import BaseAuthenticator
from .authenticators.jwt import JWTAuth
from .authenticators.basic import BasicAuth

from .decorators import login_required, permissions

from .exceptions import (
    AuthException,
    AuthRequiredException,
    AuthenticationFailedException,
    TokenExpiredException,
    InvalidRefreshTokenException,
    ForbiddenException,
    InvalidTokenException,
)
