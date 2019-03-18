import jwt

from aiohttp import web
from aiohttp.test_utils import make_mocked_request
from aiohttp_auth import auth
from aiohttp_auth.tokenizers import generate_jwt


async def test_generate_jwt_adds_expiration_date():

    app = web.Application()
    app['aiohttp_auth'] = auth.JWTAuth(
        jwt_secret='test_secret',
        duration=259200,
        jwt_algorithm='HS256'
    )

    stub_request = make_mocked_request(
        'GET', '/', app=app
    )

    payload = {'user_id': 4}
    token = await generate_jwt(
        stub_request, payload
    )

    jwt_payload = jwt.decode(
        token,
        'test_secret',
        algorithms=['HS256']
    )

    assert 'exp' in jwt_payload
