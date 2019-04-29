Authenticators
==========

Default authenticators.

---------
BasicAuth
---------

``aegis.authenticators.basic.BasicAuth``

Base authenticator for Basic authentication.

Authenticator is set-up by `setup()`.

The class implements `aegis.authenticators.base.BaseAuth`.

User should never instantiate the class but create a new class that
inherits and overrides required variables and methods.
`user_id`, `password` and `authenticate`
is forced to override.

**Arguments**:

* `me_endpoint` - User information endpoint URI. Default route is ``/me``.
      
* `auth_endpoint` - End-point URI for authenticating the user. If user sends a ``POST``
      request to this end-point it triggers the :meth:`authenticate` method. Default route is ``/auth``.

* `user_id: str` - The key name to retain the user ID when the token is decoded. Default value is ``user_id``.

* `password: str`- The key name to retain the password when the token is decoded. Default value is ``password``.


**Methods**:

* **`decode(jwt_token: str, verify=True) -> dict`**
    
    Decode basic token and return user's id and password as a dict.
    
    **Exceptions**:
    
    * `InvalidTokenException` will be raised if `base64.b64decode` fails to decode the token.

* **`get_scopes(request: web.Request)`**

    Get the user from the request and return user's permissions.

* **`authenticate(self, request: web.Request) -> Dict[str, Any]`**
    
    Return JSON serializable user. This is an abstract method and should be overridden.
        
* *classmethod* **`setup(app, name='authenticator')`**
    
    Set-up the authenticator.

---------
JWTAuth
---------

``aegis.authenticators.jwt.JWTAuth``

Base authenticator for JSON Web Token authentication.

Authenticator is set-up by :meth:`setup`.

The class implements :class:`aegis.authenticators.base.BaseAuth`.

User should never instantiate the class but create a new class that
inherits and overrides required variables and methods.
:attr:`jwt_secret` and :meth:`authenticator` is forced to override.

**Arguments**:

* **`jwt_secret: str`** - The secret key for encoding and decoding unique tokens.

* **`duration: int`** - Access token expiration limit. Default limit is ``25_000``.

* **`jwt_algorithm: str`** - The algorithm that will be used to generate the tokens. Default algorithm is ``HS256``.

* **`refresh_token: bool`** - The flag that activates the refresh token feature. Default value is ``Fals``.

* **`refresh_endpoint: str`** - Token refreshing endpoint URI. Default route is ``/auth/refresh``.

**Methods**:

* **`decode(jwt_token: str, verify=True) -> dict`**

    Decode the given token and return as a ``dict``. Raise validation exceptions if verify is set to ``True``.
    
    **Exceptions**:

     * `InvalidTokenException` will be raised if PyJWT fails to decode the access token.
    
     * `TokenExpiredException` will be raised if access token has expired.
    
* **`encode(payload: dict) -> str`**

    Encode given payload and return as a string.

* **`get_scopes(request: web.Request)`**

    Get the user from the request and return user's permissions.

* **`authenticate(self, request: web.Request) -> Dict[str, Any]`**
    
    Return JSON serializable user. This is an abstract method and should be overridden.
        
* *classmethod* **`setup(app, name='authenticator')`**
    
    Set-up the authenticator.
    

---------
BaseAuth
---------

``aegis.authenticators.base.BaseAuth``

Abstract base authenticator. User can implement new authenticators based on their needs.

**Arguments**:

* `me_endpoint` - User information endpoint URI. Default route is ``/me``.
      
* `auth_endpoint` - End-point URI for authenticating the user. If user sends a ``POST``
      request to this end-point it triggers the :meth:`authenticate` method. Default route is ``/auth``.

**Methods**:

* **`check_permissions(user_scopes, required_scopes, algorithm='any') -> bool`**

    Check whether user's permissions matches with required permissions to
    reach to the end-point.
    
    By default check_permissions uses the ``any`` algorithm opens the end-point
    for any user who has any of the required permissions.
    
    We can use other pre-defined algorithms. ``algorithm='all'`` opens the
    end-point to users who has all of the required permissions. End-point will
    also be open for users with more permissions than its required with ``all``
    algorithm.
    
    If you want to open the end-point for the users who have exactly the same
    permissions with the end-point` you can use the ``algorithm='exact'``.

* *abstractmethod* **`decode(jwt_token: str, verify=True) -> dict`**

    Decode token and return user credentials as a dict.
    
    This is an abstract method and should be overridden.
      
* *abstractmethod* **`get_scopes(request: web.Request)`**

    Decode token and return user credentials as a dict.
    
    This is an abstract method and should be overridden.

* *abstractmethod* **`authenticate(self, request: web.Request) -> Dict[str, Any]`**
    
    Return JSON serializable user.
    
    This is an abstract method and should be overridden.

* *classmethod* **`setup(app, name='authenticator')`**

    Set-up the authenticator.
