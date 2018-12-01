# Soda Project

[![Backers on Open Collective](https://opencollective.com/standard-readme/backers/badge.svg?style=flat-square)](#backers) [![Sponsors on Open Collective](https://opencollective.com/standard-readme/sponsors/badge.svg?style=flat-square)](#sponsors) 


[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

[![codefactor grade](https://www.codefactor.io/repository/github/mgurdal/soda/badge?style=flat-square)](https://www.codefactor.io/repository/github/mgurdal/soda/badge?style=flat-square)

[![Python 3.6](https://img.shields.io/badge/python-3.6-brightgreen.svg?style=flat-square)](https://www.python.org/downloads/release/python-360?style=flat-square)

### Installation
```bash
pip install aiohttp_auth
```

### Standard example
```python
# examples/server_simple.py
from aiohttp import web
from aiohttp_auth import auth


DATABASE = {
    5: {'id': 5, 'scopes': ('regular_user', )}
}


async def login(request: web.Request):
    """
        Define your login route
    """
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


app = web.Application(middlewares=[user_middleware, ])

app.router.add_post('/login', login)
app.router.add_get('/public', public)
app.router.add_get('/protected', protected)

auth.setup(app, jwt_secret='secret_key')
web.run_app(app)

```