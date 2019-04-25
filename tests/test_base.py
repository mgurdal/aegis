from unittest.mock import MagicMock, patch

import pytest
from aegis.authenticators.base import BaseAuthenticator


async def test_check_permissions_returns_uses_any_match_as_default():
    user_permissions = ('super_user',)

    required_permissions = ('super_user',)
    with patch('aegis.authenticators.base.match_any') as match_any:
        has_permissions = await BaseAuthenticator.check_permissions(
            user_permissions, required_permissions
        )

        assert has_permissions
        match_any.assert_called_once_with(
            required=required_permissions,
            provided=user_permissions
        )


async def test_check_permissions_returns_with_calls_any_match_algorithm():
    user_permissions = ('regular_user',)

    required_permissions = ('super_user', 'regular_user')
    with patch('aegis.authenticators.base.match_any') as match_any:
        has_permissions = await BaseAuthenticator.check_permissions(
            user_permissions, required_permissions, algorithm='any'
        )

        assert has_permissions
        match_any.assert_called_once_with(
            required=required_permissions,
            provided=user_permissions
        )


async def test_check_permissions_returns_calls_all_match_algorithm():
    user_permissions = ('regular_user',)

    required_permissions = ('super_user', 'regular_user')

    with patch('aegis.authenticators.base.match_all') as match_all:
        match_all.return_value = True
        has_permissions = await BaseAuthenticator.check_permissions(
            user_permissions, required_permissions, algorithm='all'
        )

        assert has_permissions
        match_all.assert_called_once_with(
            required=required_permissions,
            provided=user_permissions
        )


async def test_check_permissions_returns_calls_exact_match_algorithm():
    user_permissions = ('regular_user',)

    required_permissions = ('super_user', 'regular_user')

    with patch('aegis.authenticators.base.match_exact') as match_exact:
        match_exact.return_value = True
        has_permissions = await BaseAuthenticator.check_permissions(
            user_permissions, required_permissions, algorithm='exact'
        )

        assert has_permissions
        match_exact.assert_called_once_with(
            required=required_permissions,
            provided=user_permissions
        )


async def test_check_permissions_returns_calls_custom_algorithm():
    user_permissions = ('regular_user',)

    required_permissions = ('super_user', 'regular_user')

    custom_mock = MagicMock(return_value=True)

    def custom_algorithm(*args, **kwargs):
        return custom_mock(*args, **kwargs)

    has_permissions = await BaseAuthenticator.check_permissions(
        user_permissions, required_permissions, algorithm=custom_algorithm
    )

    assert has_permissions
    custom_mock.assert_called_once_with(
        required_permissions,
        user_permissions
    )


async def test_check_permissions_handles_invalid_algorithm():

    user_permissions = ('regular_user',)

    required_permissions = ('super_user', 'regular_user')

    invalid_algorithm = object()

    with pytest.raises(TypeError) as te:
        # noinspection PyTypeChecker
        await BaseAuthenticator.check_permissions(
            user_permissions, required_permissions, algorithm=invalid_algorithm
        )

    assert str(te.value) == (
        "Invalid algorithm type. Options 'all', 'any', 'exact', callable"
    )
