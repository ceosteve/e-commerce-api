from urllib import response
from venv import create

import requests

baseurl = 'http://127.0.0.1:8002/'
endpoint = 'products'

def get_products(baseurl, endpoint):

    print("🔄 Sending request...")

    try:
        response = requests.get(baseurl + endpoint, timeout=5)
        r = response.json()

    except requests.exceptions.RequestException as e:
        print(" Request failed:", e)

    prod_counts = []
    for product in r:
        name = product['name']
        
        if name not in prod_counts:
            prod_name ={
                'name':name, 
                'count':0
                }
        prod_name['count'] +=1


        prod_counts.append(prod_name)

    return r

# print(get_products(baseurl,endpoint))



# send a post request to the api

products_url = 'http://127.0.0.1:8002/products/create'
payload = [{
    "name":'mouse',
    "description":"wireless mouse",
    "brand":"Dell",
    "price":1000,
    "stock":25
}]

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzcwMjU4OTJ9.xMQabnVmcpLhT_ZNLjZElkVOVTSAHj3jklltuF9Sp44"

headers = {
    "Authorization": f"Bearer {token}"
}
def create_products(url, json):

    response = requests.post(products_url,json=payload, headers=headers)
    
    status_code = response.status_code
    data = response.json()

    return data, status_code

# data, status_code = create_products(products_url, json=payload)

# print(data)
# print(status_code)



# put request for a product (full update)
prod_id = 3

update_url  = f"http://127.0.0.1:8002/products/update/{prod_id}"


update_payload = {
        "name": "flash disk",
        "description": "32GB flashdisk",
        "brand": "Hp",
        "price": 1200,
        "stock": 100,
        "id": 3
    }

def update_product(url, json):
    response = requests.put(update_url,json=update_payload, headers=headers)
    status_code = response.status_code
    data = response.json()

    return data, status_code


data, status_code = update_product(update_url,json=update_payload)

print(data)