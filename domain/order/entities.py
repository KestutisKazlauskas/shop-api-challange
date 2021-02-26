from typing import List
from dataclasses import dataclass

from .value_objects import Address, Status, Customer, Item, Price


@dataclass
class Order:
    id: int
    # Reference to the cart
    cart_id: str
    customer: Customer
    shipping_address: Address
    billing_address: Address
    status: Status
    items: List[Item]
    # TODO here maybe ad a discount entity?
    discounts: List[Price]
    total: Price
