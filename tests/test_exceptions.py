from unittest.mock import MagicMock, patch

from aiohttp.test_utils import make_mocked_request
from aegis.exceptions import (
    AuthException,
    InvalidRefreshTokenException,
    AuthenticationFailedException,
)


async def test_make_response_uses_get_schema():
    with patch("aegis.exceptions.AuthException.get_schema") as get_schema:
        with patch("aegis.exceptions.AuthException._format_schema") as _format_schema:
            with patch("aegis.exceptions.web"):

                get_schema.return_value = {"test": True}

                request = make_mocked_request("GET", "/")

                class CustomException(AuthException):
                    status = 501

                CustomException.make_response(request)
                assert get_schema.called
                _format_schema.assert_called_with(
                    {"test": True}, url=request.url, status=501
                )


async def test_make_response_formats_with_kwargs():
    with patch("aegis.exceptions.web"):
        with patch("aegis.exceptions.AuthException._format_schema") as _format_schema:

            request = make_mocked_request("GET", "/")

            class CustomException(AuthException):
                status = 501

                @staticmethod
                def get_schema():
                    return {}

            kwargs = {"test": "test_info"}
            CustomException.make_response(request, **kwargs)

            _format_schema.assert_called_with(
                {"test": "test_info"}, url=request.url, status=501
            )


async def test_format_schema_handles_keyerror():
    # make a mock request

    invalid_attr = MagicMock()
    invalid_attr.format.side_effect = KeyError()
    schema = {"test_key": invalid_attr}

    result = AuthException._format_schema(schema)

    assert result == schema


async def test_format_schema_handles_attributeerror():
    # make a mock request

    invalid_attr = MagicMock()
    invalid_attr.format.side_effect = AttributeError()
    schema = {"test_key": invalid_attr}

    result = AuthException._format_schema(schema)

    assert result == schema


async def test_format_schema_formats_values():
    # make a mock request

    schema = {"test_key": "{test}"}

    result = AuthException._format_schema(schema, test="test_value")

    assert "test_key" in result
    assert result["test_key"] == "test_value"


async def test_invalid_refresh_token_schema_returns_expected_fields():
    expected_fields = {"type", "title", "detail", "instance", "status"}
    schema = InvalidRefreshTokenException.get_schema()
    assert set(schema) == expected_fields


async def test_auth_failed_schema_returns_expected_fields():
    expected_fields = {"type", "title", "detail", "instance", "status"}
    schema = AuthenticationFailedException.get_schema()
    assert set(schema) == expected_fields
