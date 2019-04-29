Routes
==========
Pre-defined authentication and user routes.

Authentication Route
---------
*``aegis.routes.make_auth_route``*

User authentication route that returns the access token. Uses **`authenticator.authenticate()`**
to authenticate the user. 

```python
credentials = {"username": "test", "password": "test"}
token_response = await session.post(
    "http://0.0.0.0:8080/auth",
    json=credentials
)
assert token_response.status == 200

token_payload = await token_response.json()
assert token_payload == {
    "access_token": "Bearer token",
}
```

- If user enables refresh token, returns the refresh token with the access token.  

```python
credentials = {"username": "test", "password": "test"}
token_response = await session.post(
    "http://0.0.0.0:8080/auth",
    json=credentials
)
assert token_response.status == 200

token_payload = await token_response.json()
assert token_payload == {
    "access_token": "Bearer token",
    "refresh_token": "refresh_token"
}
```

- If authenticate returns `None` or raises `AuthException` returns an authorization failing response based on the condition.

```python
credentials = {"username": "test", "password": "test"}
token_response = await session.post(
    "http://0.0.0.0:8080/auth",
    json=credentials
)
assert token_response.status == 401

error = await token_response.json()
assert error == {
    "type": "https://mgurdal.github.io/aegis/api.html#AuthenticationFailedException",
    "title": "Authentication Failed",
    "detail": "The credentials you supplied were not correct.",
    "instance": "http://0.0.0.0:8080/auth",
    "status": "401"
}
```

---------
Me Route
---------
*``aegis.routes.make_me_route``*

Shown authenticated user's information.

- Returns the user if user is authenticated.

```python
user_response = await session.get("http://0.0.0.0:8080/me")
assert user_response.status == 200

user = await user_response.json()
assert user == {
    "id": 1,
    "scopes": ["user"],
    "exp": 1212.121
 }
```

- Returns `UNAUTHORIZED` response if user is not authenticated.

```python
error_response = await session.get("http://0.0.0.0:8080/me")
assert error_response.status == 401

error = await error_response.json() 
assert error == {
    "type": "https://mgurdal.github.io/aegis/api.html#AuthRequiredException",
    "title": "Authentication Required",
    "detail": "You did not specify the required token information in headers or you provided it incorrectly.",
    "instance": "http://0.0.0.0:8080/me",
    "status": "401"
}
```


---------
Refresh Route
---------
*``aegis.routes.make_me_route``*

Retrieve a new access token with the refresh token.

- Returns the user if user is authenticated.

```python
refresh_payload = {"refresh_token": "ec597c581c09466badd8376b56102052"}
access_token_response = await session.post(
    "http://0.0.0.0:8080/auth/refresh",
    json=refresh_payload
)
assert access_token_response.status == 200

user = await access_token_response.json()
assert user == {
    "access_token": "Bearer token.."
}
```

- Returns `UNAUTHORIZED` response if refresh token is invalid.

```python
refresh_payload = {"refresh_token": "Invalid refresh token"}
error_response = await session.post(
    "http://0.0.0.0:8080/auth/refresh",
    json=refresh_payload
)
assert error_response.status == 401

error = await error_response.json()
assert error == {
    "type": "https://mgurdal.github.io/aegis/api.html#InvalidRefreshTokenException",
    "title": "Invalid Token",
    "detail": "You have provided an invalid refresh token.",
    "instance": "http://0.0.0.0:8080/auth/refresh",
    "status": "401"
 }

```
