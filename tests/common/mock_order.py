import datetime

from domain.order.entities import Order, Item, Price


def create_order_item():
    return Item(name="Product", quantity=1, price=Price(0))


def create_order(items):
    return Order(id=str(datetime.datetime.now()), cart_id="cart_id", items=items)