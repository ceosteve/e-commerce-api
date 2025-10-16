
from app import models, schemas


def test_create_product(authorized_client2):
    product_info = [{"name":"calculator",
        "description":"casio fx",
        "brand":"casio",
        "price":1500,
        "stock":10}]
    
    result = authorized_client2.post("/products/create", json=product_info)

    data = result.json()[0]
    product = schemas.ProductOut(**data)

    assert result.status_code == 201
    assert product.brand== 'casio'
    assert product.description == "casio fx"



def test_get_all_products(client,test_products):
    result = client.get("/products")
    assert result.status_code == 200
    data = result.json()

    # assert len(data) ==len(test_products)
    assert data[0]['name'] == test_products[0]['name']
    assert data[0]['description'] == test_products[1]['description']



def test_create_product_unauthorised_user(authorized_client1):
    product_info = [{"name":"calculator",
    "description":"casio fx",
    "brand":"casio",
    "price":1500,
    "stock":10}]
    result = authorized_client1.post("/products/create", json=product_info)
    assert result.status_code == 401



def test_update_products(authorized_client2, test_products):

    result= authorized_client2.put(f"/products/update/{test_products[0]['id']}", json={"name":"Iphone11", "price":25000})

    assert result.status_code == 200

    data = result.json()
    assert data['name'] == 'Iphone11'
    assert data ['price'] == 25000



def test_delete_products(authorized_client2, test_products):
    result= authorized_client2.delete(f"/products/delete/{test_products[1]['id']}")
    assert result.status_code == 204



def test_delete_non_existent_product(authorized_client2, test_products):
    result = authorized_client2.delete(f"products/delete/3")
    assert result.status_code == 404









    

    



