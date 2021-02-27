from typing import List
from dataclasses import dataclass

from .exceptions import InvalidOrderException
from .value_objects import Address, Status, Customer, Item, Price


@dataclass
class Order:
    id: str = None
    cart_id: str = None
    customer: Customer = None
    shipping_address: Address = None
    items: List[Item] = None
    status: Status = Status.STARTED
    total: Price = Price(0)
    discount: Price = Price(0)

    def __post_init__(self):
        if not self.id:
            raise InvalidOrderException("Order should have an id")

        if not self.cart_id:
            raise InvalidOrderException("Order should have a cart_id")

        if not self.items:
            raise InvalidOrderException("Order can't be empty")

    def mark_as_ready_to_ship(self):
        if self.shipping_address and self.customer:
            self.status = Status.READY_TO_BE_SHIPPED

    def set_customer_information(self, name: str, surname: str):
        self.customer = Customer(name=name, surname=surname)
        self.mark_as_ready_to_ship()

    def set_shipping_information(self, street: str, city: str, country: str, postal_code: str):
        self.shipping_address = Address(street, city, country, postal_code)
        self.mark_as_ready_to_ship()
