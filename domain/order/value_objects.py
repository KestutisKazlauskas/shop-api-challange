from dataclasses import dataclass
from enum import Enum

from domain.common.value_objects import Price


class Status(Enum):
    STARTED = "started"
    SHIPPED = "shipped"
    RECEIVED = "received"


@dataclass(frozen=True)
class Address:
    street: str
    city: str
    country: str
    postal_code: str


@dataclass(frozen=True)
class Customer:
    customer_id: str
    name: str
    surname: str


@dataclass(frozen=True)
class Item:
    name: str
    quantity: int
    price: Price
