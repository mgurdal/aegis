from unittest.mock import MagicMock, patch

from aiohttp.test_utils import make_mocked_request
from aiohttp_auth.exceptions import AuthException


@patch('aiohttp_auth.exceptions.AuthException.get_schema')
@patch('aiohttp_auth.exceptions.AuthException._format_schema')
async def test_make_response_uses_get_schema(get_schema, _format_schema):
    get_schema.return_value = {"test": True}
    # make a mock request

    request = make_mocked_request('GET', '/')

    class CustomException(AuthException):
        status = 501

    CustomException.make_response(request)
    assert get_schema.called
    _format_schema.assert_called_with(
        {"test": True},
        url='/',
        status=501
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

    result = AuthException._format_schema(schema, test='test_value')

    assert 'test_key' in result
    assert result['test_key'] == 'test_value'