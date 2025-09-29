
from datetime import datetime
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.authentication.oauth2 import create_access_token
from app.main import app
from app.database import get_db, Base
from app import models


DATABASE_URL = "postgresql+psycopg2://postgres:postgres254@localhost:5432/ecommerce_test"

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# create a new session for each test
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db= TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# create test client to send HTTP requests without running the application server

@pytest.fixture()
def client(session):

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] =override_get_db
    yield TestClient(app)




# test_user fixture
@pytest.fixture()
def test_user(client):
    user_info = {
    "first_name": "Steve",
    "last_name": "Njoroge",
    "email": "steve@gmail.com",
    "gender":"M",
    "birth_date":"1996-06-10",
    "role":"customer",
    "password": "password233"}

    result = client.post("/users/register", json=user_info)
    assert result.status_code == 201

    new_user = result.json()
    new_user['password'] = user_info['password']

    return new_user


# access token fixture for customer
@pytest.fixture()
def customer_token(test_user):
    return create_access_token(data={"user_id":test_user['id']})


@pytest.fixture
def authorized_client1(client, customer_token):
    new_client = client.__class__(app=client.app, base_url=client.base_url)
    new_client.headers={
        **client.headers, 
        "Authorization":f"Bearer {customer_token}"
    }

    return new_client



#  test_user 2, with admin role 

@pytest.fixture()
def test_user2(client):
    user_info = {
    "first_name": "ceo",
    "last_name": "steve",
    "email": "ceo@gmail.com",
    "gender":"M",
    "birth_date":"1998-06-11",
    "role":"admin",
    "password": "password234"}

    result = client.post("/users/register", json=user_info)
    assert result.status_code == 201

    new_user = result.json()
    new_user['password'] = user_info['password']
    new_user ['role'] = user_info ['password']
    return new_user


# access token fixture for admin user
@pytest.fixture
def admin_token(test_user2):
    return create_access_token(data={'user_id':test_user2['id'], "role":test_user2['role']})


@pytest.fixture
def authorized_client2(client, admin_token):
    new_client = client.__class__(app=client.app, base_url=client.base_url)
    new_client.headers={
        **client.headers, 
        "Authorization":f"Bearer {admin_token}"
    }

    return new_client


# create test products in database and enforce admin access
@pytest.fixture
def test_products(authorized_client2, session):
    product_data = [ {
        "name":"galaxys23",
        "description":"smartphone",
        "brand":"samsung",
        "price":40000,
        "stock":40

    },
    {
        "name":"infinix hot 8",
        "description":"smartphone",
        "brand":"infinix",
        "price":30000,
        "stock":50  
    }
    ]


    result = authorized_client2.post("/products/create", json=product_data)

    assert result.status_code == 201
 

    return result.json()


# create new test order and new order item in the database
@pytest.fixture
def test_order(authorized_client1, test_products, session):
    new_order = {
        "items":[
            {"product_id": test_products[0]['id'], "item_quantity":1},
            {"product_id": test_products[1]['id'], "item_quantity":1}]

    }

    result = authorized_client1.post("/orders/create", json=new_order)

    assert result.status_code == 201

    data = result.json()
    


    for item in new_order['items']:
        new_order_item = models.OrderItem(
             order_id=data['id'],
             product_id=item['product_id'],
             item_quantity = item['item_quantity'],
             unit_price= item.get('unit_price', 100))
        
        session.add(new_order_item)

    session.commit()
    return data







