from contextlib import contextmanager

from aiohttp import web

from aegis.routes import make_me_route, make_auth_route


class MockAuthenticator:
    """
    MockAuthenticator has an almost identical API to default
    authenticator classes. You can use this authenticator in your unit tests
    to bypass the authentication logic.
    """
    user = None
    auth_endpoint = None
    me_endpoint = None

    def __init__(self, app):
        authenticator = app.get('authenticator')
        if not authenticator:
            raise AttributeError(
                ("Please initialize the authenticator with "
                 "Authenticator.setup(app) first.")
            )

        # Replace auth middleware with mocked one
        self.auth_middleware = [
            m for m in app.middlewares
            if m.__name__ == "auth_middleware"
        ][0]
        app.middlewares.append(self._mock_auth_middleware)

        # Pass methods to mimic the authentication process
        self.check_permissions = authenticator.check_permissions
        self.get_permissions = authenticator.get_permissions
        self.authenticator = authenticator

    def _inject_user(self, request):
        """Inject the given user into the request."""
        if self.user:
            request.user = self.user

    async def get_user(self, *args, **kwargs):
        """
        Use the test user if available. Otherwise use the authenticator's
        get_user method.
        """
        if self.user:
            return self.user
        return await self.authenticator.get_user(*args, **kwargs)

    async def decode(self, *args, **kwargs):
        """
        Return the test user if available. Otherwise use the authenticator's
        decode method.
        """
        if self.user:
            return self.user
        return await self.authenticator.decode(*args, **kwargs)

    @web.middleware
    async def _mock_auth_middleware(self, request: web.Request, handler):
        """Inject the test user and trigger the middleware."""
        self._inject_user(request)
        response = await self.auth_middleware(request, handler)
        return response

    @classmethod
    def setup(cls, app):
        """Setup the authenticator with mocked features."""
        authenticator = cls(app)
        if app["authenticator"].auth_endpoint:
            auth_route = make_auth_route(authenticator)
            app.router.add_post(app["authenticator"].auth_endpoint, auth_route)

        if app["authenticator"].me_endpoint:
            me_route = make_me_route()
            app.router.add_get(app["authenticator"].auth_endpoint, me_route)

        app["authenticator"] = authenticator

    @contextmanager
    def bypass_auth(self, user: dict):
        """Uses given user to bypass the authentication logic."""
        self.user = user
        yield self
        self.user = None
