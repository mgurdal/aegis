# Welcome to aegis's documentation\!

**aegis** provides endpoint protection and authentication scoping for
aiohttp.

Current version is 0.3.1.

## Installation

``` bash
$ pip3 install aegis
```

## Bare Minimum Examples

### Basic Authentication
```python
from aiohttp import web
from aegis.decorators import login_required
from aegis.authenticators.basic import BasicAuth

class BasicAuthenticator(BasicAuth):

    async def authenticate(self, request: web.Request) -> dict:
        return {}


@login_required
async def protected(request):
    return web.json_response({'hello': 'user'})

app = web.Application()
app.router.add_get('/', protected)

BasicAuthenticator.setup(app)

web.run_app(app)

```

### JWT Authentication

```python
from aiohttp import web
from aegis.decorators import login_required
from aegis.authenticators.jwt import JWTAuth


class JWTAuthenticator(JWTAuth):
    jwt_secret = "<secret>"

    async def authenticate(self, request: web.Request) -> dict:
        return {}


@login_required
async def protected(request):
    return web.json_response({'hello': 'user'})


app = web.Application()

app.router.add_get('/', protected)

JWTAuthenticator.setup(app)

web.run_app(app)
```

## Source code

The project is hosted on GitHub: <https://github.com/mgurdal/aegis>

Please feel free to file an issue on the bug tracker if you have found a
bug or have some suggestion in order to improve the library.

## Author and License

The `aegis` package is written by Mehmet Gürdal.

It's *Apache 2* licensed and freely available.
