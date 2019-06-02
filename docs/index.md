# Welcome to aegis documentation\!

**aegis** provides endpoint protection and authentication scoping for
aiohttp.

[![python](https://img.shields.io/badge/python-3.6-brightgreen.svg)](https://www.python.org/downloads/release/python-360)
[![pypi](https://badge.fury.io/py/aegis.svg)](https://badge.fury.io/py/aegis)
[![travis](https://travis-ci.org/mgurdal/aegis.svg?branch=master)](https://travis-ci.org/mgurdal/aegis)
[![coveralls](https://coveralls.io/repos/github/mgurdal/aegis/badge.svg?branch=master)](https://coveralls.io/github/mgurdal/aegis?branch=master)
[![codefactor](https://www.codefactor.io/repository/github/mgurdal/aegis/badge)](https://www.codefactor.io/repository/github/mgurdal/aegis)
[![code-style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![downloads](https://img.shields.io/pypi/dm/aegis.svg)](https://pypi.python.org/pypi/aegis)

## Installation

``` bash
pip install aegis
```

## Bare Minimum Examples

### Basic Authentication
```python
from aiohttp import web
from aegis import login_required, BasicAuth

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
from aegis import login_required, JWTAuth


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
