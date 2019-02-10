# aiohttp_auth

[![Python 3.6](https://img.shields.io/badge/python-3.6-brightgreen.svg?style=flat-square)](https://www.python.org/downloads/release/python-360?style=flat-square)
[![codefactor grade](https://www.codefactor.io/repository/github/mgurdal/aiohttp_auth/badge?style=flat-square)](https://www.codefactor.io/repository/github/mgurdal/aiohttp_auth/badge?style=flat-square)


**aiohttp_auth** adds authentication protection and endpoints to [aiohttp](https://github.com/aio-libs/aiohttp). 

**aiohttp_auth** allows you to **protect endpoints** and also provides **authentication scoping**.

------

### Installation
```bash
pip install https://github.com/mgurdal/aiohttp_auth
```

### Simple Example
```python
# examples/server_simple.py
from aiohttp import web
from aiohttp_auth import auth


DATABASE = {
    'david': {'user_id': 5, 'scopes': ('regular_user', )}
}


async def authenticate(request):
    payload = await request.json()
    user = DATABASE.get(payload['username'])

    return user


async def public(request):
    return web.json_response({'hello': 'anonymous'})


@auth.scopes('regular_user')
async def protected(request):
    return web.json_response({'hello': 'user'})


def create_app():
    app = web.Application()

    app.router.add_get('/public', public)
    app.router.add_get('/protected', protected)

    auth.setup(app, authenticate, jwt_secret="test")
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)

```
----
### TODO

- [X] unit tests
- [ ] documentation
- [ ] CD/CI
- [ ] Web Page


