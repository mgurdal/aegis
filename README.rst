aegis
=============

|Python 3.6| |travis-badge| |coveralls| |codefactor grade|

.. |Python 3.6| image:: https://img.shields.io/badge/python-3.6-brightgreen.svg
   :target: https://www.python.org/downloads/release/python-360
.. |codefactor grade| image:: https://www.codefactor.io/repository/github/mgurdal/aegis/badge
   :target: https://www.codefactor.io/repository/github/mgurdal/aegis/badge
.. |travis-badge| image:: https://travis-ci.org/mgurdal/aegis.svg?branch=master
   :target: https://travis-ci.org/mgurdal/aegis
.. |coveralls| image:: https://coveralls.io/repos/github/mgurdal/aegis/badge.svg?branch=master
   :target: https://coveralls.io/github/mgurdal/aegis?branch=master
   
**aegis** allows to **protect endpoints** and also provides
**authentication scoping**.

--------------

Installation
~~~~~~~~~~~~
.. code:: bash

     pip install -e git://github.com/mgurdal/aegis.git@v0.3.0#egg=aegis


Simple Example
~~~~~~~~~~~~~~

.. code:: python

   # examples/login_required.py
   from aiohttp import web
   from aegis import auth
   from aegis.authenticators.jwt import JWTAuth


   DATABASE = {
       'david': {'id': 5, 'scopes': ('user',)}
   }


   class MyAuth(JWTAuth):
       jwt_secret = "test"

       async def authenticate(self, request: web.Request) -> dict:
           payload = await request.json()
           user = DATABASE.get(payload['username'])
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


   {"access_token": "<access_token>"}

Get user

.. code:: bash

   curl http://0.0.0.0:8080/me -H 'Authorization: Bearer <access_token>'


   {"id": 5, "scopes": ["user"], "exp": 1553753859}



Test
~~~~~~~~~~~~~~

.. code:: bash

    git clone https://github.com/mgurdal/aegis.git
    cd aegis
    make cov

Requirements
~~~~~~~~~~~~

- Python >= 3.6
- aiohttp
- PyJWT

License
~~~~~~~~

``aegis`` is offered under the Apache 2 license.
