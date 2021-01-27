import base64
import json
import jose.jwt
import time

# seconds until the token expires
TOKEN_EXPIRES = 2

def get_auth_token(app):
    """
    Generated an auth token for testing.
    :param app: a chalice app.
    :return:
    """
    expires_at = time.time()
    headers = dict(alg="RS256", kid="BB810D292A4EE6FCD0334B755967DFAC")
    payload = dict(
        name="Fake User", sub="test_user_id", email="fake_user@email.com", email_verified=True, exp=expires_at
    )

    jwt = jose.jwt.encode(claims=payload, key="mysecret", algorithm="HS256", headers=headers)
    r = {
        "access_token": f"access-{time.time()}",
        "id_token": jwt,
        "refresh_token": f"random-{time.time()}",
        "scope": "openid profile email offline",
        "expires_in": TOKEN_EXPIRES,
        "token_type": "Bearer",
        "expires_at": expires_at,
    }
    cookie = base64.b64encode(json.dumps(r).encode()).decode()
    return f"cxguser={cookie}; Domain=localhost"
