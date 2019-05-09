from datetime import datetime
from unittest.mock import patch

import jwt
import pytest
from aegis.authenticators.jwt import JWTAuth
from aegis.exceptions import (InvalidTokenException,
                              TokenExpiredException)


async def test_decode_raises_invalid_token_exception_on_decode_error():
    with patch('aegis.authenticators.jwt.jwt.decode') as decode:
        decode.side_effect = jwt.DecodeError()

        class TestJWTAuth(JWTAuth):
            jwt_secret = ""

            async def authenticate(self, request):
                pass

        auth = TestJWTAuth()
        invalid_token = "test"

        with pytest.raises(InvalidTokenException) as ex:
            await auth.decode(invalid_token)

        assert ex is not None
        assert decode.called


async def test_decode_raises_token_expired_exception_expired_signature():
    with patch('aegis.authenticators.jwt.jwt.decode') as decode:
        decode.side_effect = jwt.ExpiredSignatureError()

        class TestJWTAuth(JWTAuth):
            jwt_secret = ""

            async def authenticate(self, request):
                pass

        auth = TestJWTAuth()
        token = "test"

        with pytest.raises(TokenExpiredException) as ex:
            await auth.decode(token)

        assert ex is not None
        assert decode.called


async def test_decode_removes_token_type_and_decodes_token():
    with patch('aegis.authenticators.jwt.jwt.decode') as decode:
        class TestJWTAuth(JWTAuth):
            jwt_secret = ""

            async def authenticate(self, request):
                pass

        auth = TestJWTAuth()
        token = "Bearer test"

        await auth.decode(token)

        decode.assert_called_once_with(
            "test", auth.jwt_secret,
            algorithms=(auth.jwt_algorithm,),
            options={'verify_exp': True}
        )


async def test_encode_encodes_payload_with_expiration_date():
    with patch('aegis.authenticators.jwt.jwt.encode') as encode:
        with patch('aegis.authenticators.jwt.datetime') as mockdate:
            mockdate.utcnow.return_value = datetime(2017, 1, 1)
            mockdate.side_effect = lambda *args, **kw: mockdate(*args, **kw)

            class TestJWTAuth(JWTAuth):
                jwt_secret = ""
                duration = 0

                async def authenticate(self, request):
                    pass

            auth = TestJWTAuth()

            payload = {"test": 12}

            await auth.encode(payload)

            encode.assert_called_once_with(
                {
                    "test": 12,
                    "exp": datetime(2017, 1, 1)
                },
                auth.jwt_secret,
                auth.jwt_algorithm
            )

            encode.return_value.decode.assert_called_with('utf-8')


async def test_get_user_returns_credentials_by_default():
    class TestJWTAuth(JWTAuth):
        jwt_secret = ""

        async def authenticate(self, request):
            pass

    auth = TestJWTAuth()
    credentials = {
        "id": 1,
        "exp": 5
    }

    user = await auth.get_user(credentials)

    assert user == credentials
