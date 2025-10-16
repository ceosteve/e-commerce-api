import pytest 
from app import utils

def test_hash_password():

    password = "steven01"

    hashed = utils.hash_password(password)

    print(hashed)

    assert isinstance(hashed, str)
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

    assert utils.verify_password(password,hashed)
