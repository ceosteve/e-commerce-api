
from app import schemas



def test_add_to_cart(authorized_client1,test_products, test_user):
    items_to_add = {
         "items": [
    {"product_id": test_products[0]['id'], "item_quantity": 5},
    {"product_id": test_products[1]['id'], "item_quantity": 1}
  ]
    }
    result=authorized_client1.post("/cart/add", json=items_to_add)
    assert result.status_code ==201

    cart_items = schemas.CartOut(**result.json())
    assert cart_items.user_id == test_user['id']


def test_logged_out_user_add_to_cart(client,test_products,test_user):
    items_to_add = {
         "items": [
    {"product_id": test_products[0]['id'], "item_quantity": 5},
    {"product_id": test_products[1]['id'], "item_quantity": 1}
  ]
    }
    result=client.post("/cart/add", json=items_to_add)
    assert result.status_code == 401



def test_update_cart_item(authorized_client1, test_products,test_cart):
    update_data = {
        "items":[
            {"product_id": test_products[0]['id'], "item_quantity":3},
            {"product_id": test_products[1]['id'], "item_quantity":10}
            ]
    }
    result=authorized_client1.put(f"/cart/update/{test_cart['id']}/items", json=update_data)
    assert result.status_code == 200

    cart_items = result.json()
    assert cart_items['items'][0]['item_quantity'] == update_data['items'][0]['item_quantity']



def test_checkout(authorized_client1,test_cart):
    result=authorized_client1.post("cart/checkout")
    assert result.status_code == 200

    checked_out_cart = result.json()
    assert checked_out_cart['status'] == 'pending'

    cart_id = test_cart['id']
    cart_response = authorized_client1.get(f"cart/{cart_id}")
    cart = cart_response.json()
    assert cart['status'] == 'checked_out'



def test_delete_cart_item(authorized_client1,test_cart, test_products):
    result=authorized_client1.delete(f"cart/delete/cart/{test_cart['id']}/product/{test_products[0]['id']}")
    assert result.status_code == 204


def test_delete_cart(authorized_client1,test_cart):
    result=authorized_client1.delete(f"/cart/delete/{test_cart['id']}")
    assert result.status_code == 204




     
    