aegis
=============

|Python 3.6| |pypi| |travis-badge| |coveralls| |codefactor grade|

.. |Python 3.6| image:: https://img.shields.io/badge/python-3.6-brightgreen.svg
   :target: https://www.python.org/downloads/release/python-360
.. |codefactor grade| image:: https://www.codefactor.io/repository/github/mgurdal/aegis/badge
   :target: https://www.codefactor.io/repository/github/mgurdal/aegis/badge
.. |travis-badge| image:: https://travis-ci.org/mgurdal/aegis.svg?branch=master
   :target: https://travis-ci.org/mgurdal/aegis
.. |coveralls| image:: https://coveralls.io/repos/github/mgurdal/aegis/badge.svg?branch=master
   :target: https://coveralls.io/github/mgurdal/aegis?branch=master
.. |pypi| image:: https://badge.fury.io/py/aegis.svg
    :target: https://badge.fury.io/py/aegis
 
**aegis** allows to **protect endpoints** and also provides
**authentication scoping**.

--------------

Installation
~~~~~~~~~~~~
.. code:: bash

     pip install aegis


Simple Example
~~~~~~~~~~~~~~

.. code:: python

   # examples/login_required.py
   from aiohttp import web
   from aegis import decorators
   from aegis.authenticators.jwt import JWTAuth


   class JWTAuthenticator(JWTAuth):
       jwt_secret = "test"

       async def authenticate(self, request: web.Request) -> dict:
           # You can get the request payload of the /auth route
           payload = await request.json()

           # Assuming the name parameter send in the request payload
           searched_name = payload["name"]

           # fetch the user from your storage
           db = request.app["db"]
           user = db.get(searched_name, None)

           # return the JSON serializable user
           return user


   @decorators.login_required
   async def protected(request):
       return web.json_response({'hello': 'user'})


   if __name__ == "__main__":
       app = web.Application()

       database = {
           'david': {'id': 5}
       }
       app["db"] = database

       app.router.add_get('/', protected)

       JWTAuthenticator.setup(app)

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
