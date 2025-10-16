import hashlib
from types import SimpleNamespace
from fastapi import Request
import pytest 
from app import utils
from app.authentication.oauth2 import create_access_token


def test_hash_password():

    password = "steven01"

    hashed = utils.hash_password(password)

    assert isinstance(hashed, str)
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

    assert utils.verify_password(password,hashed)


def test_hash_access_token():

    token = create_access_token({"user_id":1, "user_role":"customer"})

    hashed_token = utils.hash_token(token)

    assert isinstance(hashed_token, str)
    assert hashed_token.startswith("$2b$") or hashed_token.startswith("$2a$")

    assert utils.verify_token(token, hashed_token)


class FakeRquest:
    def __init__(self, path:str, query_params:dict):
        self.url = SimpleNamespace(path=path)
        self.query_params = query_params

def test_make_cache_key_from_request():

    request = FakeRquest("/products", {"skip":1, "limit":2, "search":"book"})

    cache_key = utils.make_cache_key_from_request(request)
    assert cache_key.startswith("cache:/products:")

    # test that same input gives same output
    cache_key_2 = utils.make_cache_key_from_request(request)
    assert cache_key == cache_key_2

    # test hashing of the query params
    param_string = "&".join(f"{k}={v}" for k, v in sorted({"skip":1, "limit":2, "search":"book"}.items()))

    hashed_key = hashlib.md5(param_string.encode()).hexdigest()
    assert hashed_key in cache_key_2