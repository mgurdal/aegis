# aiohttp_auth

[![codefactor grade](https://www.codefactor.io/repository/github/mgurdal/aiohttp_auth/badge?style=flat-square)](https://www.codefactor.io/repository/github/mgurdal/aiohttp_auth/badge?style=flat-square)

[![Python 3.6](https://img.shields.io/badge/python-3.6-brightgreen.svg?style=flat-square)](https://www.python.org/downloads/release/python-360?style=flat-square)


**aiohttp_auth** adds authentication protection and endpoints to [aiohttp](https://github.com/aio-libs/aiohttp). 

**aiohttp_auth** allows you to **protect endpoints** and also provides **authentication scoping**.

------

### Installation
```bash
pip install aiohttp_auth
```

### Simple Example
```python
# examples/server_simple.py
from aiohttp import web
from aiohttp_auth import auth


DATABASE = {
    5: {'id': 5, 'scopes': ('regular_user', )}
}


async def login(request: web.Request):
    payload = await request.json()

    user_id = payload['user_id']
    # use auth.login to generate a JWT token
    # with some unique user information
    token = await auth.login(request, user_id)

    return web.json_response({'token': token})


@auth.middleware
async def user_middleware(request, jwt_payload: dict):
    # Use the JWT payload to initialize the user
    user_id = jwt_payload['user_id']
    user = DATABASE[user_id]
    request.user = user
    return request


async def public(request):
    return web.json_response({'hello': 'anonymous'})


@auth.scopes('regular_user')
async def protected(request):
    return web.json_response({'hello': 'user'})


def create_app():
    app = web.Application()

    app.router.add_post('/login', login)
    app.router.add_get('/public', public)
    app.router.add_get('/protected', protected)

    auth.setup(app, jwt_secret='secret_key')
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)

```