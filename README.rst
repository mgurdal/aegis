aiohttp\_auth
=============

|Python 3.6| |build| |codefactor grade|

**aiohttp\_auth** adds authentication protection and endpoints to
`aiohttp <https://github.com/aio-libs/aiohttp>`__.

**aiohttp\_auth** allows to **protect endpoints** and also provides
**authentication scoping**.

--------------

Installation
~~~~~~~~~~~~

.. code:: bash

    pip install https://github.com/mgurdal/aiohttp_auth

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

        auth.setup(app, authenticate, jwt_secret=tests)
        return app


    if __name__ == '__main__':
        app = create_app()
        web.run_app(app)

--------------

TODO
~~~~

-  [X] unit tests
-  [ ] documentation
-  [X] CD/CI
-  [ ] Web Page

.. |Python 3.6| image:: https://img.shields.io/badge/python-3.6-brightgreen.svg?style=flat-square
   :target: https://www.python.org/downloads/release/python-360?style=flat-square
.. |codefactor grade| image:: https://www.codefactor.io/repository/github/mgurdal/aiohttp_auth/badge?style=flat-square
   :target: https://www.codefactor.io/repository/github/mgurdal/aiohttp_auth/badge?style=flat-square
.. build:: https://travis-ci.org/mgurdal/aiohttp_auth.svg?branch=master
    :target: https://travis-ci.org/mgurdal/aiohttp_auth