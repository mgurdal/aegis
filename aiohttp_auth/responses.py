from aiohttp import web
from aiohttp_auth.exceptions import UserDefinedException


def access_token(token: str):
    return web.json_response({
        "access_token": token
    }, status=200)


def auth_required(request):
    detail = ("You did not specify the required token information "
              "in headers or you provided it incorrectly.")
    url = request.url
    return web.json_response({
        "type": "https://mgurdal.github.io/aiohttp_auth/docs.html",
        "title": "Authentication Required",
        "detail": detail,
        "instance": F"{url}",
        "code": 401
    }, status=401)


def invalid_token(request):
    detail = "You provided an invalid JWT signature."
    url = request.url
    return web.json_response({
        "type": "https://mgurdal.github.io/aiohttp_auth/docs.html",
        "title": "Invalid Token",
        "detail": detail,
        "instance": F"{url}",
        "code": 400
    }, status=400)


def token_expired(request):
    detail = "The access token provided has expired."
    url = request.url
    return web.json_response({
        "type": "https://mgurdal.github.io/aiohttp_auth/docs.html",
        "title": "Invalid Token",
        "detail": detail,
        "instance": F"{url}",
        "code": 401
    }, status=401)


def forbidden(request):
    url = request.url
    detail = F"User scope does not meet access requests for {url}"
    return web.json_response({
        "type": "https://mgurdal.github.io/aiohttp_auth/docs.html",
        "title": "You do not have access to this url.",
        "detail": detail,
        "instance": F"{url}",
        "code": 403
    }, status=403)


def error_response(request, exception: UserDefinedException):
    url = request.url
    return web.json_response({
        "type": "https://mgurdal.github.io/aiohttp_auth/docs.html",
        "title": exception.title,
        "detail": exception.detail,
        "instance": F"{url}",
        "code": exception.status
    }, status=exception.status)
