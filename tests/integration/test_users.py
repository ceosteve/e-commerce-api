
from typing import assert_type
from jose import jwt
from app import schemas
from app.config import settings
import pytest


def test_register_user(client):
    result= client.post("users/register", json={
                "first_name": "Steve",
                "last_name": "Njoroge",
                "email": "steve@gmail.com",
                "gender":"M",
                "birth_date":"1996-06-10",
                "role":"customer",
                "password": "password233"})
    
    assert result.status_code ==201
    new_user = schemas.UserOut(**result.json())
    assert new_user.email == "steve@gmail.com"


def test_login(client, test_user):
    result = client.post("/login", data={
        "username":"steve@gmail.com",
        "password":"password233"
    })
    login_data = schemas.TokenOut(**result.json())
    payload = jwt.decode(login_data.access_token, settings.secret_key, settings.algorithm)
    user_id = payload.get("user_id")
    assert user_id == test_user['id']
    assert login_data.token_type == "bearer"
    assert result.status_code == 200


@pytest.mark.parametrize("email,password,status_code", [
    ("steve@gmail.com","password233",200),
    ("steven@gmail.com","password233",404),
    ("steve@gmail.com", "wrongpassword", 429)
])
def test_incorrect_login(client,test_user,email,password,status_code):
    result = client.post("/login", data={"username":email, "password":password})
    
    assert result.status_code == status_code
    if status_code == 404:
        assert result.json().get('detail')== 'username not found'
    elif status_code ==429:
        assert result.json().get('detail') == "5 per 1 minute"

    
# delete another user's id
def test_delete_user(authorized_client1,test_user2):
    result = authorized_client1.delete(f"/users/delete/{test_user2['id']}")
    assert result.status_code==403


# delete your own user id
def test_own_user_id(authorized_client1, test_user):
    result = authorized_client1.delete(f"users/delete/{test_user['id']}")

    assert result.status_code == 204

# test duplicate email registration
def test_register_duplicate_email(client, test_user):
    result = client.post("/users/register", json=test_user)

    assert result.status_code == 422



