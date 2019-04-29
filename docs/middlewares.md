Middlewares
==========

---------
auth_middleware
---------
*``aegis.middlewares.auth_middleware``*

```auth_middleware(request: web.Request, handler: Callable) -> web.Response```


Decodes the access token and injects the user into the request object. 
It also handles authentication exceptions. 

*This middleware is designed for use 
in the interior parts of the library and has nothing to do in the user space.*

