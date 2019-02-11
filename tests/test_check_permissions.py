from aiohttp.test_utils import make_mocked_request
from aiohttp_auth import auth


async def test_returns_false_if_user_not_in_request():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )

    has_permissions = auth.check_permissions(
        stub_request, ('test_scope',)
    )

    assert not has_permissions


async def test_returns_false_if_user_is_anonymous():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )

    has_permissions = auth.check_permissions(
        stub_request, ('anonymous_user',)
    )

    assert not has_permissions


async def test_returns_false_if_scopes_not_matches():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )

    stub_request.user = {
        'scopes': ('regular_user',)
    }

    required_permissions = ('super_user',)
    has_permissions = auth.check_permissions(
        stub_request, required_permissions
    )

    assert not has_permissions


async def test_returns_true_if_scopes_matches():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )

    stub_request.user = {
        'scopes': ('super_user',)
    }

    required_permissions = ('super_user',)
    has_permissions = auth.check_permissions(
        stub_request, required_permissions
    )

    assert has_permissions


async def test_returns_true_if_scopes_intersects():
    stub_request = make_mocked_request(
        'GET', '/', headers={'authorization': 'x'}
    )

    stub_request.user = {
        'scopes': ('regular_user',)
    }

    required_permissions = ('super_user', 'regular_user')
    has_permissions = auth.check_permissions(
        stub_request, required_permissions
    )

    assert has_permissions
