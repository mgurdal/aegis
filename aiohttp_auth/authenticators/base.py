import inspect
from abc import ABCMeta, abstractmethod
from typing import Callable, Hashable, Iterable, Union

from aiohttp import web

from ..matching_algorithms import match_all, match_any, match_exact
from ..middlewares import auth_middleware
from ..routes import make_auth_route, make_me_route


class BaseAuthenticator(metaclass=ABCMeta):
    type: str

    @staticmethod
    async def check_permissions(
            user_scopes: Iterable[Hashable],
            required_scopes: Iterable[Hashable],
            algorithm: Union[str, Callable] = 'any'
    ) -> bool:
        # user tries to reach to a scoped end-point
        if algorithm == 'any':
            has_permission = match_any(
                required=required_scopes,
                provided=user_scopes
            )
        elif algorithm == 'all':
            has_permission = match_all(
                required=required_scopes,
                provided=user_scopes
            )
        elif algorithm == 'exact':
            has_permission = match_exact(
                required=required_scopes,
                provided=user_scopes
            )
        elif inspect.isfunction(algorithm):
            has_permission = algorithm(
                required=required_scopes,
                provided=user_scopes
            )
        else:
            raise TypeError(
                "Invalid algorithm type. "
                "Options 'all', 'any', 'exact', callable"
            )
        return has_permission

    @abstractmethod
    async def decode(self, token: str) -> dict:
        """Rreturns the user information as dict"""

    @abstractmethod
    async def authenticate(self, request: web.Request):
        """Returns JSON serializable user"""

    @abstractmethod
    async def get_scopes(self, request: web.Request):
        """Returns user's permissions"""

    @classmethod
    def setup(cls, app, name='aiohttp_auth'):
        app.middlewares.append(auth_middleware)
        authenticator = cls()
        auth_route = make_auth_route(authenticator)
        me_route = make_me_route()
        app.router.add_post('/auth', auth_route)
        app.router.add_get('/me', me_route)
        app[name] = authenticator
