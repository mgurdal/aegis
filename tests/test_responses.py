import json

from aiohttp.test_utils import make_mocked_request
from aiohttp_auth.exceptions import UserDefinedException
from aiohttp_auth.responses import (access_token, auth_required,
                                    error_response, forbidden, invalid_token,
                                    token_expired)


async def test_access_token():
    resp = access_token('test_token')
    token_payload = json.loads(resp.text)

    assert resp.status == 200
    assert 'access_token' in token_payload
    assert token_payload['access_token'] == 'test_token'


async def test_auth_required():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'},
    )
    resp = auth_required(stub_request)

    assert resp.status == 401


async def test_invalid_token():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'},
    )
    resp = invalid_token(stub_request)

    assert resp.status == 400


async def test_token_expired():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'},
    )
    resp = token_expired(stub_request)

    assert resp.status == 401


async def test_forbidden():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'},
    )
    resp = forbidden(stub_request)

    assert resp.status == 403


async def test_error_response():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'},
    )

    class TestException(UserDefinedException):
        status = 500
        title = "test"
        detail = "test"

    exception = TestException()
    resp = error_response(stub_request, exception)

    assert resp.status == 500
