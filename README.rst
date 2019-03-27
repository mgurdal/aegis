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

Installation
~~~~~~~~~~~~
.. code:: bash

     pip install -e git://github.com/mgurdal/aiohttp_auth.git@v0.1.0#egg=aiohttp_auth


Simple Example
~~~~~~~~~~~~~~

.. code:: python

   # examples/login_required.py
   from aiohttp_auth import auth
   from aiohttp_auth.authenticators.jwt import JWTAuth


   class MyAuth(JWTAuth):
       jwt_secret = "test"

       async def authenticate(self, request):
           user = {
               "user_id": "5",
               "name": "K Lars Lohn",
           }
           return user


   async def public(request):
       return web.json_response({'hello': 'anonymous'})


   @auth.login_required
   async def protected(request):
       return web.json_response({'hello': 'user'})


   def create_app():
       app = web.Application()

       app.router.add_get('/public', public)
       app.router.add_get('/protected', protected)

       MyAuth.setup(app)
       return app


   if __name__ == '__main__':
       app = create_app()
       web.run_app(app)


Get access token

.. code:: bash

   curl -X POST http://0.0.0.0:8080/auth -d '{"username": "david"}'

Get user

.. code:: bash

   curl http://0.0.0.0:8080/me -H 'Authorization: Bearer <access_token>'



Test
~~~~~~~~~~~~~~

.. code:: bash

    git clone https://github.com/mgurdal/aiohttp_auth.git
    cd aiohttp_auth
    make cov

Requirements
~~~~~~~~~~~~

- Python >= 3.6
- aiohttp
- PyJWT

License
~~~~~~~~

``aiohttp_auth`` is offered under the Apache 2 license.
