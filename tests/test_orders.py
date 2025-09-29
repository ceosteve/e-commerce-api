
from datetime import datetime

from app import schemas


# create new order in the system
def test_create_order(authorized_client1,test_user, test_products):
    order_data = {
        "items":[{
            "product_id": test_products[0]['id'], "item_quantity":1
        }]

    }
    result= authorized_client1.post("/orders/create", json=order_data)

    order = schemas.OrderOut(**result.json())

    print(result.json())
    print("Response JSON:", result.json())
    print("Order items:", [ (i["product_id"], i["item_quantity"]) for i in result.json()["items"] ])


    assert result.status_code == 201
    assert order.user_id == test_user['id']
    assert order.status == "pending"
    assert float(order.total_price) == float(test_products[0]['price']) 
    assert order.placed_on is not None
    assert order.items[0].product_id== test_products[0]['id']



# test view orders by logged in customer
def test_view_orders(authorized_client1, test_order):
    result = authorized_client1.get("/orders/customer")

    assert result.status_code ==200

    orders = result.json()

    assert len(orders) == 1
    assert orders[0]['id'] == test_order['id']
    assert orders[0]['user_id'] == test_order['user_id']


# test order status update
def test_update_order_status(authorized_client2,test_order):
    order_status= "shipped"
    result = authorized_client2.put(f"/orders/update/{test_order['id']}/status", json={"status":order_status})

    order = result.json()

    assert result.status_code == 200
    assert order['status'] == 'shipped'


# view orders by admin
def test_view_orders_admin(authorized_client2,test_order):
    result=authorized_client2.get("/orders/admin")

    orders = result.json()
    assert result.status_code ==200

    assert len(orders) == 1
    assert orders[0]['id'] == test_order['id']
    assert orders[0]['user_id'] == test_order['user_id']









