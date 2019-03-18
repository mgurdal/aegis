from aiohttp_auth.matching_algorithms import match_all, match_any, match_exact


async def test_match_any_matches_subset():

    required_permissions = ('regular_user', )

    provided_permissions = ('super_user', 'regular_user')

    has_permission = match_any(
        required=required_permissions,
        provided=provided_permissions
    )
    assert has_permission


async def test_match_any_matches_superset():

    required_permissions = ('regular_user', 'super_user', )

    provided_permissions = ('regular_user',)

    has_permission = match_any(
        required=required_permissions,
        provided=provided_permissions
    )
    assert has_permission


async def test_match_any_not_matches_empty():

    required_permissions = ('regular_user', 'super_user', )

    provided_permissions = []

    has_permission = match_any(
        required=required_permissions,
        provided=provided_permissions
    )
    assert not has_permission


async def test_match_any_not_matches_different_permissions():

    required_permissions = ('regular_user', 'super_user', )

    provided_permissions = ('admin', 'test')

    has_permission = match_any(
        required=required_permissions,
        provided=provided_permissions
    )
    assert not has_permission


async def test_match_exact_not_matches_different_permissions():

    required_permissions = ('regular_user', 'super_user', )

    provided_permissions = ('admin', 'test')

    has_permission = match_exact(
        required=required_permissions,
        provided=provided_permissions
    )
    assert not has_permission


async def test_match_exact_not_matches_empty():

    required_permissions = ('regular_user', 'super_user', )

    provided_permissions = set()

    has_permission = match_exact(
        required=required_permissions,
        provided=provided_permissions
    )
    assert not has_permission


async def test_match_exact_not_matches_superset():

    required_permissions = ('regular_user', )

    provided_permissions = ('regular_user', 'super_user', )

    has_permission = match_exact(
        required=required_permissions,
        provided=provided_permissions
    )
    assert not has_permission


async def test_match_exact_not_matches_subset():

    required_permissions = ('regular_user', 'super_user', )

    provided_permissions = ('regular_user', )

    has_permission = match_exact(
        required=required_permissions,
        provided=provided_permissions
    )
    assert not has_permission


async def test_match_exact_matches_exact_subset():

    required_permissions = ('regular_user', 'super_user', )

    provided_permissions = ('regular_user', 'super_user', )

    has_permission = match_exact(
        required=required_permissions,
        provided=provided_permissions
    )
    assert has_permission


async def test_match_all_matches_exact_set():

    required_permissions = ('regular_user', 'super_user', )

    provided_permissions = ('regular_user', 'super_user', )

    has_permission = match_all(
        required=required_permissions,
        provided=provided_permissions
    )
    assert has_permission


async def test_match_all_not_matches_provided_subset():

    required_permissions = ('regular_user', 'super_user', )

    provided_permissions = ('regular_user', )

    has_permission = match_all(
        required=required_permissions,
        provided=provided_permissions
    )
    assert not has_permission


async def test_match_all_matches_provided_superset():

    required_permissions = ('regular_user',)

    provided_permissions = ('regular_user', 'super_user', )

    has_permission = match_all(
        required=required_permissions,
        provided=provided_permissions
    )
    assert has_permission


async def test_match_all_not_matches_empty_set():

    required_permissions = ('regular_user',)

    provided_permissions = set()

    has_permission = match_all(
        required=required_permissions,
        provided=provided_permissions
    )
    assert not has_permission


async def test_match_all_not_matches_different_sets():

    required_permissions = ('regular_user',)

    provided_permissions = ('super_user',)

    has_permission = match_all(
        required=required_permissions,
        provided=provided_permissions
    )
    assert not has_permission
