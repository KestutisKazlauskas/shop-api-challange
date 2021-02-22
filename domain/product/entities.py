from typing import List
from dataclasses import dataclass
from domain.product.exceptions import InvalidProductException

from .value_objects import Image, Price


@dataclass
class ProductType:
    id: str = None
    name: str = None

    def __post_init__(self):
        if not self.name:
            raise InvalidProductException("Product type name is required.")

        if len(self.name) > 255:
            raise InvalidProductException("Product type name is to long.")


@dataclass
class Product:
    id: str = None
    name: str = None
    quantity: int = None
    type: ProductType = None
    images: List[Image] = None
    price: Price = Price(value=0.0, currency=Price.currency_enum.USD.value)
    # TODO do we really need this field??
    is_archived: bool = False

    def __post_init__(self):
        if not self.name:
            raise InvalidProductException("Product name  is required.")

        if len(self.name) > 255:
            raise InvalidProductException("Product name is to long.")

        if not self.type:
            raise InvalidProductException("Product type is required.")

        if not self.quantity or self.quantity < 0:
            raise InvalidProductException("Quantity can not be less than 0")

    def add_image(self, name: str, url: str):
        image = Image(name, url)
        if not self.images:
            self.images = [image]

            return

        self.images.append(image)

    def set_product_price(self, price: float, currency: str):
        self.price = Price(price, currency)

    def archive_product(self):
        self.is_archived = True

