# Shop api

## About the project 
Small products, cart and order api written in python with DDD approch in mind

## Used technologies
- Python3.9 and Flask framework for Restfull api.
- Postgresql for storing Products, Carts and Orders data
- SqlAlchemy as ORM for migrations of the database schema.
- Docker and docker compose for running api

## How to run the api
1. Clone the repository or download the zip file of the repository:
```
git clone git@github.com:KestutisKazlauskas/shop-api-challange.git 
```
2. In the cloned repo directory build the docker container with docker-compose
```
docker-compose build
```
3. Run the built containers in the background
```
docker-compose up -d
```
3. Migrate the database schema
```
docker-compose exec shop-api  bash -c "cd infrastructure && flask db upgrade"
```
4. Run flask app
```
docker-compose exec shop-api python infrastructure/run.py
```

## How to run the tests
1. Run the test from docker-compose
```
docker-compose exec shop-api pytest
```

## How to use the api
1. Creating the products
```
POST http://0.0.0.0:8080/api/products/
Request body: 
{
    "name": "First product",
    "product_type_name": "New type",
    "product_type_id": "",
    "quantity": 30,
    "price": 23.00,
    "currency": "USD",
    "images": [
        {"name": "This is a name", "url": "https://via.placeholder.com/300/09f/fff.png"}
    ]
}
```
IMPORTANT
Creating the product for the same product_type the product_type id should be sent - "product_type_id": "created_product_type_id",
```
{
    "name": "Second product",
    "product_type_id": "cd9d39a0-073a-4b38-b233-cc19612e7567",
    "quantity": 30,
    "price": 23.00,
    "currency": "USD",
    "images": [
        {"name": "This is a name", "url": "https://via.placeholder.com/300/09f/fff.png"}
    ]
}
```

2. Getting the products
```
GET http://0.0.0.0:8080/api/products/
```

3. Getting specific product
```
GET http://0.0.0.0:8080/api/products/{product_id}/
example: http://0.0.0.0:8080/api/products/3bd08ab6-82cb-4d47-9f3a-62f1cef5274a/
```

4. Deleting specific product
```
DELETE http://0.0.0.0:8080/api/products/{product_id}/
```

5. Creating the cart
```
POST http://0.0.0.0:8080/api/carts/
Request body: 
{
    "items": [
        {"product_id": "{product_id}", "quantity": 1},
        {"product_id": "{product_id}", "quantity": 2}
    ]
}
```

6. Getting the cart
```
GET http://0.0.0.0:8080/api/carts/{cart_id}/
example: http://0.0.0.0:8080/api/carts/e7760259-08d3-4e38-9073-d6070853dcf2/
```

7. Deleting the cart
```
DELETE http://0.0.0.0:8080/api/carts/{cart_id}/
```

8. Adding product to the cart
```
POST http://0.0.0.0:8080/api/carts/{cart_id}/items/
Request body: 
{"product_id": "{product_id}", "quantity": 1}
```
IMPORTANT: 
After adding the product to the cart. 
Need to get the need data from the cart api, 
because other data of the cart could be changed on adding the item to the cart

9. Removing the product from the cart
```
DELETE http://0.0.0.0:8080/api/carts/{cart_id}/items/{item_id}/
```
IMPORTANT: 
After adding the product to the cart. 
Need to get the need data from the cart api, 
because other data of the cart could be changed on removing the item form the cart


10. Placing the order
```
POST http://0.0.0.0:8080/api/orders/
Request body:
{
    "cart_id": "{cart_id}",
    "name": "Kestutis",
    "surname": "Kazlauskas",
    "street": "Zirmunu g.",
    "city": "Vilnius",
    "country": "lithuania",
    "postal_code": "LT-32323"
}
```
IMPORTANT:
name, surname, street, city, country, postal_code is not required

11. Retrieving order information with order status
```
GET http://0.0.0.0:8080/api/orders/{order_id}/
```

## Left TODO
1. Write integrations tests for flask views, models and Product,Cart,Order repositories