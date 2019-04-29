Decorators
==========
Login and permission decorators.

login_required
---------
*``aegis.decorators.login_required``*

If not authenticated user tries to reach to a `login_required` end-point returns
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


scopes
---------
*``aegis.decorators.scopes``*
Opens the end-point for any user who has the permission to access.

**Matching Algorithms**:

- `algorithm='any'` - The default algorithm which opens the end-point for any user who has any of the required permissons.
- `algorithm='all'` - Opens the end-point to users who has all of the required permissons.
In this case end-point is also open for users who has a superset of required permissions.
- `algorithm='exact'` - Opens the end-point for the users who has exactly the same permissions with required permissions.

You can also implement your own matching algorithm and use with scopes.

```python
from aegis import scopes

def lenght_algorithm(required_scopes: Iterable, user_scopes: Iterable) -> bool:
    """
    required_scopes: These permissions defined in the scopes  decorator.
    
    user_scopes: These scopes comes from authenticator.get_scopes method which
    returns the permissions in thee authenticated user's "scopes" key by default.
    """
    has_permission = len(required_scopes) == len(user_scopes)
    return has_permission

@scopes('user', 'admin', algorithm=lenght_algorithm)
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