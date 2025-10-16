
from app import schemas
from app.config import settings
from jose import jwt

""""admin userflows i.e, creating account, adding product and retrieving product"""

def test_admin_flows(client):

    # step 1 is to register
    user_data = {
        "first_name": "Steve",
        "last_name": "Njoroge",
        "email": "steve2@gmail.com",
        "gender":"M",
        "birth_date":"1996-06-10",
        "role":"admin",
        "password": "password233"
    }

    result = client.post("/users/register", json=user_data)
    assert  result.status_code == 201
    new_user = schemas.UserOut(**result.json())
    assert new_user.email == user_data['email']


    # step 2 is to login 
    result = client.post("/login",data={"username":"steve2@gmail.com", "password":"password233"})
    assert result.status_code == 200
    login_output = schemas.TokenOut(**result.json())
    assert login_output.token_type == "bearer"
    assert result.status_code == 200
    token = login_output.access_token
    headers = {"Authorization": f"Bearer {token}"}


    # step 3 create a product (admin)
    product_data = [ {
        "name":"galaxys23",
        "description":"smartphone",
        "brand":"samsung",
        "price":40000,
        "stock":40

    }]

    result = client.post("/products/create", headers=headers, json=product_data)
    assert result.status_code ==201

    created_products= result.json()
    assert created_products[0]['name'] =='galaxys23'


    # retrieve product from db
    result = client.get("/products", headers=headers)
    assert result.status_code == 200
    products = result.json()
    assert any(p["name"] == "galaxys23" for p in products)


