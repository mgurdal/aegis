Exceptions
==========

Pre-defined authentication and authorization exceptions.

---------
AuthRequiredException
---------

``aegis.exceptions.AuthRequiredException``

Raise exception if user tries to reach to a protected route without
credentials.

**Attributes**:

* `status: 401` - Exception will create an `UNAUTHORIZED` response.
      
**Methods**:

* *staticmethod* **`get_schema() -> dict`**

```python
from aegis.exceptions import AuthRequiredException

schema = AuthRequiredException.get_schema()

assert schema == {
    "type": "https://mgurdal.github.io/aegis/api.html#AuthRequiredException",
    "title": "Authentication Required",
    "detail": "You did not specify the required token information in headers or you provided it incorrectly.",
    "instance": "{url}",
    "status": "401"
}
```


---------
InvalidTokenException
---------

``aegis.exceptions.InvalidTokenException``

Raise exception if user uses an invalid access token.

**Attributes**:

* `status: 401` - Exception will create an `UNAUTHORIZED` response.
      
**Methods**:

* *staticmethod* **`get_schema() -> dict`**

```python
from aegis.exceptions import InvalidTokenException

schema = InvalidTokenException.get_schema()

assert schema == {
    "type": "https://mgurdal.github.io/aegis/api.html#InvalidTokenException",
    "title": "Invalid Token",
    "detail": "You have provided an invalid token signature.",
    "instance": "{url}",
    "status": "401"
 }
```


---------
TokenExpiredException
---------

``aegis.exceptions.TokenExpiredException``

Raise exception if user uses an expired access token.

**Attributes**:

* `status: 401` - Exception will create an `UNAUTHORIZED` response.
      
**Methods**:

* *staticmethod* **`get_schema() -> dict`**

```python
from aegis.exceptions import TokenExpiredException

schema = TokenExpiredException.get_schema()

assert schema == {
    "type": "https://mgurdal.github.io/aegis/api.html#TokenExpiredException",
    "title": "Invalid Token",
    "detail": "The access token provided has expired.",
    "instance": "{url}",
    "status": "401"
 }
```


---------
InvalidRefreshTokenException
---------

``aegis.exceptions.InvalidRefreshTokenException``

Raise exception if user uses an invalid refresh token.

**Attributes**:

* `status: 401` - Exception will create an `UNAUTHORIZED` response.
      
**Methods**:

* *staticmethod* **`get_schema() -> dict`**

```python
from aegis.exceptions import InvalidRefreshTokenException

schema = InvalidRefreshTokenException.get_schema()

assert schema == {
    "type": "https://mgurdal.github.io/aegis/api.html#InvalidRefreshTokenException",
    "title": "Invalid Token",
    "detail": "You have provided an invalid refresh token.",
    "instance": "{url}",
    "status": "401"
 }
```


---------
AuthenticationFailedException
---------

``aegis.exceptions.AuthenticationFailedException``

Raise exception if user tries to authenticate with invalid credentials.

**Attributes**:

* `status: 401` - Exception will create an `UNAUTHORIZED` response.
      
**Methods**:

* *staticmethod* **`get_schema() -> dict`**

```python
from aegis.exceptions import AuthenticationFailedException

schema = AuthenticationFailedException.get_schema()

assert schema == {
    "type": "https://mgurdal.github.io/aegis/api.html#AuthenticationFailedException",
    "title": "Authentication Failed",
    "detail": "The credentials you supplied were not correct.",
    "instance": "{url}",
    "status": "401"
 }
```


---------
ForbiddenException
---------

``aegis.exceptions.ForbiddenException``

Raise exception if user tries to reach to an end-point without permissions.


**Attributes**:

* `status: 403` - Exception will create an `FORBIDDEN` response.
      
**Methods**:

* *staticmethod* **`get_schema() -> dict`**

```python
from aegis.exceptions import ForbiddenException

schema = ForbiddenException.get_schema()

assert schema == {
    "type": "https://mgurdal.github.io/aegis/api.html#ForbiddenException",
    "title": "Forbidden Access",
    "detail": "User permissions does not meet access requests for {url}",
    "instance": "{url}",
    "status": "403"
}
```


---------
AuthException
---------

``aegis.exceptions.AuthException``

Base authentication exception.

It is not recommended create instances directly from ``AuthException``. 
Instead, inherit from ``AuthException`` and override `status` code 
and `get_schema` method for understandable responses.

User should never instantiate the class but create a new class that
inherits and overrides required variables and methods.
`user_id`, `password` and `authenticate`
is forced to override.

**Attributes**:

* `status: int` - The HTTP status code that will be used when the error response is sent.
      
**Methods**:

* *classmethod* **`make_response(cls, request: web.Request)`**
    
    Create a response based on exception schema.

* *staticmethod* **`get_schema() -> dict`**
    
    Return response payload schema.

* *staticmethod* **`_format_schema(schema: dict, **kwargs) -> dict`**
    
    Format response schema placeholders with given key-word arguments.
