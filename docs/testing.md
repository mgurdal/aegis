Testing
=======

Testing can be really tricky if a library adds bunch of middle-wares and 
decorators in your application.
However, aegis includes some testing utilities to help you
to have better control in your application state.

Lets dive into some code!

First, we will create a really simple app with an authentication logic in it.
In this example, user will never be able to reach to the `"/"` endpoint.

```python
# examples/testing/app.py

from aiohttp import web
from aegis import login_required, BasicAuth

class BasicAuthenticator(BasicAuth):

    async def authenticate(self, request: web.Request) -> dict:
        pass


@login_required
async def protected(request):
    return web.json_response({'hello': 'user'})

def create_app():
    app = web.Application()
    app.router.add_get('/', protected)
    
    BasicAuthenticator.setup(app)
    return app

if __name__ == "__main__":
    app = create_app()
    web.run_app(app)

```

Now, lets write some test to get the authentication error response.

We will define our test case by inheriting from aiohttp's `AioHTTPTestCase`
and overriding the `get_application` method.

```python
# examples/testing/test_app.py

from aiohttp.test_utils import AioHTTPTestCase

# import the app factory
from app import create_app


class AppTestCase(AioHTTPTestCase):

    async def get_application(self):
        app = create_app()
        return app
```

Next, we will create a test method that sends a get request
to the protected `/` route and validates the response's status code.

```python
    @unittest_run_loop
    async def test_protected_route_without_credentials(self):
        # AioHTTPTestCase provides us a client to send requests. 
        resp = await self.client.request("GET", "/")

        assert resp.status == 200
```

If we run this with pytest, it will fail with this message.
```
=================================== FAILURES ===================================
_______________ AppTestCase.test_protected_route_without_credentials _______________

self = <test_app.AppTestCase testMethod=test_protected_route_without_credentials>

    @unittest_run_loop
    async def test_protected_route_without_credentials(self):
        resp = await self.client.request("GET", "/")
>       assert resp.status == 200
E       AssertionError: assert 401 == 200
E        +  where 401 = <ClientResponse(http://127.0.0.1:59273/) [401 Unauthorized]>\n<CIMultiDictProxy('Content-Type': 'application/json; charset=utf-8', 'Content-Length': '276', 'Date': 'Mon, 06 May 2019 22:50:50 GMT', 'Server': 'Python/3.7 aiohttp/3.5.4')>\n.status
```
Since this application does not use any real authentication logic.
We have to bypass the authentication system completely. To do this,
We need to mock our authenticator with `aegis.test_utils.MockAuthenticator`.
We can do it by simply calling the `MockAuthenticator.setup` method with our `àpp`
instance.

```python
class AppTestCase(AioHTTPTestCase):

    async def get_application(self):
        app = create_app()
        MockAuthenticator.setup(app)
        return app
```
By calling the setup method, MockAuthenticator will mock the `BasicAuthenticator`
that we have been using in our app. MockAuthenticator is almost the
same with our previous authenticator, in addition to that, it also has some 
extra features to help us to `bypass` the authentication system.

bypass_auth(user)
------------------

We only need the `bypass_auth` method to control the authentication logic. It is a `contextmanager`. So you can disable
the permission control multiple times in your test suite.
To use the `bypass_auth`, we first need to reach to our mocked authenticator.
And then, we can control the authentication by calling the `mocked_authenticator.bypass_auth` method with a test user.

```python
    @unittest_run_loop
    async def test_protected_route_without_credentials(self):
        mocked_authenticator = self.app["authenticator"]
        mock_user = {"permissions": ("user",)}

        with mocked_authenticator.bypass_auth(user=mock_user):
            resp = await self.client.request("GET", "/")
            assert resp.status == 200
        
        resp = await self.client.request("GET", "/")
        assert resp.status == 401

```

Have fun!