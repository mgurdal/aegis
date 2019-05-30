aegis
=============

|Python 3.6| |pypi| |travis-badge| |pyup| |coveralls| |codefactor grade| |downloads|

.. |Python 3.6| image:: https://img.shields.io/badge/python-3.6-brightgreen.svg
   :target: https://www.python.org/downloads/release/python-360
.. |codefactor grade| image:: https://www.codefactor.io/repository/github/mgurdal/aegis/badge
   :target: https://www.codefactor.io/repository/github/mgurdal/aegis/badge
.. |travis-badge| image:: https://travis-ci.org/mgurdal/aegis.svg?branch=master
   :target: https://travis-ci.org/mgurdal/aegis
.. |coveralls| image:: https://coveralls.io/repos/github/mgurdal/aegis/badge.svg
   :target: https://coveralls.io/github/mgurdal/aegis
.. |pypi| image:: https://badge.fury.io/py/aegis.svg
    :target: https://badge.fury.io/py/aegis
.. |downloads| image:: https://img.shields.io/pypi/dm/aegis.svg
    :target: https://pypi.python.org/pypi/aegis
.. |pyup| image:: https://pyup.io/repos/github/mgurdal/aegis/shield.svg
     :target: https://pyup.io/repos/github/mgurdal/aegis/
     :alt: Updates

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

   from aiohttp import web
   from aegis import login_required, JWTAuth


   class JWTAuthenticator(JWTAuth):
       jwt_secret = "<secret>"

       async def authenticate(self, request: web.Request) -> dict:
           db = request.app["db"]
           credentials = await request.json()
           id_ = credentials["id"]
           user = db.get(id_)
           return user


   @login_required
   async def protected(request):
       return web.json_response({'hello': 'user'})


   def create_app():
       app = web.Application()
       app["db"] = {
           5: {
               "name": "test"
           }
       }
       app.router.add_get('/protected', protected)

       JWTAuthenticator.setup(app)

       return app


   if __name__ == "__main__":
       app = create_app()
       web.run_app(app)


Get access token

.. code:: bash

   curl -X POST http://0.0.0.0:8080/auth -d '{"id": 5}'


   {"access_token": "<access_token>"}

Get user

.. code:: bash

   curl http://0.0.0.0:8080/protected -H 'Authorization: Bearer <access_token>'


   {'hello': 'user'}



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
