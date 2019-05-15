Decorators
==========
Login and permission decorators.

login_required
---------
*``aegis.decorators.login_required``*

If unauthorized user tries to reach to a `login_required` end-point returns
`UNAUTHORIZED` response.

```python
# server
from aegis import login_required

@login_required
async def protected(request):
    return web.json_response({'hello': 'user'})

app.router.add_get('/protected', protected)

# client
response = await session.get("http://0.0.0.0:8080/protected")
assert response.status == 401

error = await response.json()
assert error == {
    "type": "https://mgurdal.github.io/aegis/api.html#AuthRequiredException",
    "title": "Authentication Required",
    "detail": "You did not specify the required token in headers or you provided it incorrectly.",
    "instance": "http://0.0.0.0:8080/protected",
    "status": "401"
}
```


permissions
---------
*``aegis.decorators.permissions``*
Opens the end-point for any user who has the permission to access.

**Matching Algorithms**:

- `algorithm='any'` - The default algorithm which opens the end-point for any user who has any of the required permissons.
- `algorithm='all'` - Opens the end-point to users who has all of the required permissons.
In this case end-point is also open for users who has a superset of required permissions.
- `algorithm='exact'` - Opens the end-point for the users who has exactly the same permissions with required permissions.

You can also implement your own matching algorithm and use with permissions.

```python
from aegis import permissions
from aegis.matching_algorithms import match_any

def match_any_and_admin(required_permissions, user_permissions) -> bool:
    # ignore the matching algorithm if user is admin
    has_permission = (
        "admin" in user_permissions
        or match_any(required_permissions, user_permissions)
    )
    return has_permission

@permissions("user", algorithm=match_any_and_admin)
async def protected(request):
    return web.json_response({'hello': 'user'})
```

- If user has no permission to access to scoped end-point, returns `FORBIDDEN` response.

```python
response = await session.get("http://0.0.0.0:8080/protected")
assert response.status == 401

error = await response.json()
assert error == {
    "type": "https://mgurdal.github.io/aegis/api.html#ForbiddenException",
    "title": "Forbidden Access",
    "detail": "User permissions does not meet access requests for http://0.0.0.0:8080/protected",
    "instance": "http://0.0.0.0:8080/protected",
    "status": "403"
}
```