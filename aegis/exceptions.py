from aiohttp import web


class AuthException(Exception):
    status: int

    @classmethod
    def make_response(cls, request: web.Request):
        """
        Creates a response based on exception schema.
        """
        schema = cls.get_schema()
        payload = cls._format_schema(schema, url=request.url,
                                     status=cls.status)
        return web.json_response(payload, status=cls.status)

    @staticmethod
    def get_schema() -> dict:
        """
        Returns response payload schema
        """

    @staticmethod
    def _format_schema(schema: dict, **kwargs) -> dict:
        """
        Formats response schema placeholders with given key-word arguments.
        """
        result = {}
        for name, value in schema.items():
            try:
                result[name] = value.format(**kwargs)
            except (KeyError, AttributeError):
                result[name] = value

        return result


class AuthRequiredException(AuthException):
    status = 401

    @staticmethod
    def get_schema() -> dict:
        detail = ("You did not specify the required token information "
                  "in headers or you provided it incorrectly.")
        doctype = ("https://mgurdal.github.io/aegis/exceptions/"
                   "#AuthRequiredException")
        return {
            "type": doctype,
            "title": "Authentication Required",
            "detail": detail,
            "instance": "{url}",
            "status": "{status}"
        }


class InvalidTokenException(AuthException):
    """Raise exception if user uses an invalid token."""
    status = 401

    @staticmethod
    def get_schema() -> dict:
        detail = "You have provided an invalid token signature."
        doctype = ("https://mgurdal.github.io/aegis/exceptions/"
                   "#InvalidTokenException")
        return {
            "type": doctype,
            "title": "Invalid Token",
            "detail": detail,
            "instance": "{url}",
            "status": "{status}"
        }


class TokenExpiredException(AuthException):
    """Raise exception if user uses an expired token."""
    status = 401

    @staticmethod
    def get_schema() -> dict:
        detail = "The access token provided has expired."
        doctype = ("https://mgurdal.github.io/aegis/exceptions/"
                   "#TokenExpiredException")

        return {
            "type": doctype,
            "title": "Invalid Token",
            "detail": detail,
            "instance": "{url}",
            "status": "{status}"
        }


class ForbiddenException(AuthException):
    status = 403

    @staticmethod
    def get_schema() -> dict:
        detail = "User scope does not meet access requests for {url}"
        doctype = ("https://mgurdal.github.io/aegis/exceptions/"
                   "#ForbiddenException")

        return {
            "type": doctype,
            "title": "Forbidden Access",
            "detail": detail,
            "instance": "{url}",
            "status": "{status}"
        }


class InvalidRefreshTokenException(AuthException):
    status = 400

    @staticmethod
    def get_schema() -> dict:
        detail = "You have provided an invalid refresh token."
        doctype = ("https://mgurdal.github.io/aegis/exceptions/"
                   "#InvalidRefreshTokenException")
        return {
            "type": doctype,
            "title": "Invalid Token",
            "detail": detail,
            "instance": "{url}",
            "status": "{status}"
        }


class AuthenticationFailedException(AuthException):
    status = 401

    @staticmethod
    def get_schema() -> dict:
        detail = "The credentials you supplied were not correct."
        doctype = ("https://mgurdal.github.io/aegis/exceptions/"
                   "#AuthenticationFailedException")
        return {
            "type": doctype,
            "title": "Authentication failed.",
            "detail": detail,
            "instance": "{url}",
            "status": "{status}"
        }
