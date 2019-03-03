aiohttp\_auth
=============

|Python 3.6| |travis-badge| |coveralls| |codefactor grade|

.. |Python 3.6| image:: https://img.shields.io/badge/python-3.6-brightgreen.svg
   :target: https://www.python.org/downloads/release/python-360
.. |codefactor grade| image:: https://www.codefactor.io/repository/github/mgurdal/aiohttp_auth/badge
   :target: https://www.codefactor.io/repository/github/mgurdal/aiohttp_auth/badge
.. |travis-badge| image:: https://travis-ci.org/mgurdal/aiohttp_auth.svg?branch=master
   :target: https://travis-ci.org/mgurdal/aiohttp_auth
.. |coveralls| image:: https://coveralls.io/repos/github/mgurdal/aiohttp_auth/badge.svg?branch=master
   :target: https://coveralls.io/github/mgurdal/aiohttp_auth?branch=master
   
**aiohttp\_auth** allows to **protect endpoints** and also provides
**authentication scoping**.

--------------

Simple Example
~~~~~~~~~~~~~~

.. code:: python

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
        auth.setup(app, authenticate, jwt_secret="secret_token")
        return app


    if __name__ == '__main__':
        app = create_app()
        web.run_app(app)

--------------

TODO
~~~~

- [X] unit tests
- [ ] documentation
- [X] CD/CI
- [X] Web Page