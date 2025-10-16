
from app import schemas
from jose import jwt
from app.config import settings


"""customer userflows i.e creating account, loging in, adding items to cart and checking out"""

def test_customer_flows(client, test_products, authorized_client1, test_cart):

    # step 1 - register an account 
    user_data = {
        "first_name": "Steve",
        "last_name": "Njoroge",
        "email": "steve23@gmail.com",
        "gender":"M",
        "birth_date":"1996-06-10",
        "role":"customer",
        "password": "password234"
    }
    result = client.post("/users/register", json=user_data)
    assert result.status_code == 201

    data = schemas.UserOut(**result.json())
    assert data.email == user_data['email']


    # step 2 - login 
    result= client.post("/login", data={"username":"steve23@gmail.com", "password":"password234"})
    assert result.status_code == 200

    login_info = schemas.TokenOut(**result.json())
    payload = jwt.decode(login_info.access_token, settings.secret_key, settings.algorithm)
    user_id = payload.get("user_id")
    assert user_id == data.id
    assert login_info.token_type == "bearer"



    # step 3 - get all products from database
    result = client.get("/products")
    assert result.status_code == 200
    product_data = result.json()

    # assert len(product_data) == len(test_products)
    assert product_data[0]['name'] == test_products[0]['name']


    # step 4 - add items to cart
    items_to_add = {
        "items":[{"product_id":test_products[0]['id'], "item_quantity":2}]
    }

    result = authorized_client1.post("/cart/add", json=items_to_add)
    assert result.status_code == 201

    cart_data = schemas.CartOut(**result.json())
    assert cart_data.status == "active"


    # step 5 - checkout
    result = authorized_client1.post("/cart/checkout")
    assert result.status_code == 200

    checked_out_cart = result.json()
    assert checked_out_cart['status'] == 'pending'

    # Step 6- Verify cart persisted as checked_out in DB
    cart_id = test_cart['id']
    cart_response = authorized_client1.get(f"/cart/{cart_id}")
    assert cart_response.status_code == 200
    cart = cart_response.json()
    assert cart['status'] == 'checked_out'





