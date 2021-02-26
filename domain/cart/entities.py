from dataclasses import dataclass
from typing import List

from domain.cart.value_objects import Discount
from domain.cart.exceptions import InvalidCartException
from domain.common.value_objects import Price


@dataclass
class Item:
    id: str = None
    product_id: str = None
    product_type_id: str = None
    product_name: str = ""
    quantity: int = 0
    unit_price: Price = None
    free_unit_price: Price = None

    def __post_init__(self):
        required_fields = [
            "id",
            "product_id",
            "product_type_id",
            "unit_price"
        ]
        for required in required_fields:
            if not getattr(self, required):
                raise InvalidCartException(f"Item {required} is required")

        if self.quantity <= 0:
            raise InvalidCartException("Item quantity should be more then 0")

    def is_same_type(self, other_item) -> bool:
        return self.product_type_id == other_item.product_type_id

    def make_free(self):
        self.free_unit_price = self.unit_price
        self.unit_price = Price(0)

    def rollback_free_item_price(self):
        if self.free_unit_price:
            self.unit_price = self.free_unit_price

        self.free_unit_price = None


class Cart:

    def __init__(
            self,
            id: str = None,
            items: List[Item] = None,
    ):
        if not id:
            raise InvalidCartException("id is required")

        if not items:
            raise InvalidCartException("Cart could not be empty")

        self.max_total_amount = Price(100)
        self.total_amount_for_discount = Price(20)
        self.total_amount_discount = Discount(name="Cart amount discount", value=1.0, currency="USD")

        self.id = id
        self.total = Price(0)
        self.items = []
        self.discounts = []

        for item in items:
            self.add_item(item)

    def _find_item_by_id(self, item_id: str) -> Item:
        for cart_item in self.items:
            if cart_item.id == item_id:
                return cart_item

    def _find_free_item_by_type(self, product_type: str):
        for cart_item in self.items:
            is_item_type = cart_item.product_type_id == product_type
            is_item_free = cart_item.unit_price.value == 0
            if is_item_type and is_item_free:
                return cart_item

    def is_item_free(self, item: Item) -> bool:
        same_items = len([item_in_cart for item_in_cart in self.items if item.is_same_type(item_in_cart)])

        return (same_items + 1) % 5 == 0

    def can_add_item(self, item: Item) -> bool:
        if item.id in [item.id for item in self.items]:
            return False

        if self.is_item_free(item):
            return True

        if (self.total + item.unit_price * item.quantity) > self.max_total_amount:
            return False
        return True

    def calculate_total(self):
        total = Price(0)
        for item in self.items:
            total += item.unit_price * item.quantity

        for discount in self.discounts:
            total -= discount

        self.total = total

        if self.total >= self.total_amount_for_discount:
            self.apply_discount(self.total_amount_discount)
        else:
            self.unapply_discount(self.total_amount_discount)

    def apply_discount(self, discount: Discount):
        if discount in self.discounts:
            return

        total = self.total - discount
        if total.value < 0:
            raise InvalidCartException("total can't be less then 0")

        self.discounts.append(discount)
        self.total = total

    def unapply_discount(self, discount: Discount):
        if discount in self.discounts:
            self.discounts.remove(discount)
            self.total += discount

    def unapply_free_item_of_item_type(self, item):
        # Check if removed not free item of the same product_type
        if not item.free_unit_price and self.is_item_free(item):
            free_item = self._find_free_item_by_type(item.product_type_id)
            if free_item:
                free_item.rollback_free_item_price()

    def add_item(self, item: Item):
        if not self.can_add_item(item):
            raise InvalidCartException("Cant add item")

        if self.is_item_free(item):
            item.make_free()

        self.items.append(item)
        self.calculate_total()

    def remove_item(self, item_id: str):
        if len(self.items) == 1:
            raise InvalidCartException("Can not remove last item from cart.")

        item = self._find_item_by_id(item_id)
        if item in self.items:
            self.items.remove(item)
            self.unapply_free_item_of_item_type(item)
            self.calculate_total()
