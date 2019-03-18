from unittest.mock import MagicMock, patch

import pytest
from aiohttp.test_utils import make_mocked_request
from aiohttp_auth import auth


async def test_returns_false_if_user_not_in_request():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )

    has_permissions = await  auth.check_permissions(
        stub_request, ('test_scope',)
    )

    assert not has_permissions


async def test_returns_false_if_user_is_anonymous():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )
    has_permissions = await auth.check_permissions(
        stub_request, ('anonymous_user',)
    )

    assert not has_permissions


async def test_returns_uses_any_match_as_default():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )

    stub_request.user = {
        'scopes': ('super_user',)
    }
    required_permissions = ('super_user',)
    with patch('aiohttp_auth.auth.match_any') as match_any:

        has_permissions = await auth.check_permissions(
            stub_request, required_permissions
        )

        assert has_permissions
        match_any.assert_called_once_with(
            required=required_permissions,
            provided=stub_request.user['scopes']
        )


async def test_returns_with_calls_any_match_algorithm():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )

    stub_request.user = {
        'scopes': ('super_user',)
    }
    required_permissions = ('super_user',)
    with patch('aiohttp_auth.auth.match_any') as match_any:

        has_permissions = await auth.check_permissions(
            stub_request, required_permissions, algorithm='any'
        )

        assert has_permissions
        match_any.assert_called_once_with(
            required=required_permissions,
            provided=stub_request.user['scopes']
        )


async def test_returns_calls_all_match_algorithm():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )

    stub_request.user = {
        'scopes': ('regular_user',)
    }
    required_permissions = ('super_user', 'regular_user')

    with patch('aiohttp_auth.auth.match_all') as match_all:
        match_all.return_value = True
        has_permissions = await auth.check_permissions(
            stub_request, required_permissions, algorithm='all'
        )

        assert has_permissions
        match_all.assert_called_once_with(
            required=required_permissions,
            provided=stub_request.user['scopes']
        )


async def test_returns_calls_exact_match_algorithm():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )

    stub_request.user = {
        'scopes': ('regular_user',)
    }
    required_permissions = ('super_user', 'regular_user')

    with patch('aiohttp_auth.auth.match_exact') as match_exact:
        match_exact.return_value = True
        has_permissions = await auth.check_permissions(
            stub_request, required_permissions, algorithm='exact'
        )

        assert has_permissions
        match_exact.assert_called_once_with(
            required=required_permissions,
            provided=stub_request.user['scopes']
        )


async def test_returns_calls_custom_algorithm():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )

    stub_request.user = {
        'scopes': ('regular_user',)
    }
    required_permissions = ('super_user', 'regular_user')

    custom_mock = MagicMock(return_value=True)

    def custom_algorithm(*args, **kwargs):
        return custom_mock(*args, **kwargs)

    has_permissions = await auth.check_permissions(
        stub_request, required_permissions, algorithm=custom_algorithm
    )

    assert has_permissions
    custom_mock.assert_called_once_with(
        required=required_permissions,
        provided=stub_request.user['scopes']
    )


async def test_handles_invalid_algorithm():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )

    stub_request.user = {
        'scopes': ('regular_user',)
    }
    required_permissions = ('super_user', 'regular_user')

    invalid_algorithm = object()

    with pytest.raises(TypeError) as te:
        # noinspection PyTypeChecker
        await auth.check_permissions(
            stub_request, required_permissions, algorithm=invalid_algorithm
        )

    assert str(te.value) == (
        "Invalid algorithm type. Options 'all', 'any', 'exact', callable"
    )
