import datetime
from domain.cart.entities import Item, Cart, Price


def create_cart_item(price_value: float = 10.0, price_currency: str = "USD"):
    return Item(
        id=str(datetime.datetime.now()),
        product_id="product_id",
        product_type_id="product_type_id",
        quantity=1,
        unit_price=Price(price_value, price_currency)
    )


def create_cart(items):
    return Cart(id="id", items=items)
