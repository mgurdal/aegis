from aiohttp.test_utils import make_mocked_request
from aegis.exceptions import (
    AuthException,
    AuthRequiredException,
    ForbiddenException,
    InvalidTokenException,
    TokenExpiredException,
)


async def test_auth_required():
    stub_request = make_mocked_request("GET", "/", headers={"authorization": "x"})
    resp = AuthRequiredException.make_response(stub_request)

    assert resp.status == 401


async def test_invalid_token():
    stub_request = make_mocked_request("GET", "/", headers={"authorization": "x"})
    resp = InvalidTokenException.make_response(stub_request)

    assert resp.status == 401


async def test_token_expired():
    stub_request = make_mocked_request("GET", "/", headers={"authorization": "x"})
    resp = TokenExpiredException.make_response(stub_request)

    assert resp.status == 401


async def test_forbidden():
    stub_request = make_mocked_request("GET", "/", headers={"authorization": "x"})
    resp = ForbiddenException.make_response(stub_request)

    assert resp.status == 403


async def test_custom_error_response():
    stub_request = make_mocked_request("GET", "/", headers={"authorization": "x"})

    class TestException(AuthException):
        status = 500

        @staticmethod
        def get_schema():
            return {}

    resp = TestException.make_response(stub_request)

    assert resp.status == 500
