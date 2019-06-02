import binascii
from unittest.mock import patch

import pytest

from aegis.authenticators.basic import BasicAuth
from aegis.exceptions import InvalidTokenException


async def test_decode_raises_invalid_token_exception_on_decode_error():
    with patch("aegis.authenticators.basic.base64.b64decode") as decode:
        decode.side_effect = binascii.Error()

        class TestBasicAuth(BasicAuth):
            async def authenticate(self, request):
                pass

        auth = TestBasicAuth()
        invalid_token = "test"

        with pytest.raises(InvalidTokenException) as ex:
            await auth.decode(invalid_token)

        assert ex is not None
        assert decode.called
        assert auth


async def test_decode_returns_credentials_with_default_keys():
    with patch("aegis.authenticators.basic.base64.b64decode") as decode:
        credentials = b"test:test"
        decode.return_value = credentials

        class TestBasicAuth(BasicAuth):
            async def authenticate(self, request):
                pass

        auth = TestBasicAuth()
        token = "test=="

        decoded_credentials = await auth.decode(token)
        expected_credentials = {"user_id": "test", "password": "test"}
        assert decoded_credentials == expected_credentials


async def test_decode_returns_credentials_with_altered_keys():
    with patch("aegis.authenticators.basic.base64.b64decode") as decode:
        credentials = b"test:test"
        decode.return_value = credentials

        class TestBasicAuth(BasicAuth):
            user_id = "email"
            password = "password"

            async def authenticate(self, request):
                pass

        auth = TestBasicAuth()
        token = "test=="

        decoded_credentials = await auth.decode(token)
        expected_credentials = {"email": "test", "password": "test"}
        assert decoded_credentials == expected_credentials


async def test_decode_passes_verify_parameter_into_decoder():
    with patch("aegis.authenticators.basic.base64.b64decode") as decode:
        credentials = b"test:test"
        decode.return_value = credentials

        class TestBasicAuth(BasicAuth):
            async def authenticate(self, request):
                pass

        auth = TestBasicAuth()
        token = "test=="

        await auth.decode(token, verify=False)

        decode.assert_called_once_with(token.encode(), validate=False)

        await auth.decode(token, verify=True)
        decode.assert_called_with(token.encode(), validate=True)
