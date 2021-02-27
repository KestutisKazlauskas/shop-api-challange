from dataclasses import dataclass
from enum import Enum

from domain.common.value_objects import Price
from .exceptions import InvalidOrderException


class Status(Enum):
    STARTED = "started"
    READY_TO_BE_SHIPPED = "ready_to_be_shipped"
    RECEIVED = "received"


class AllFieldsRequiredMixin:

    def validate_required(self, message: str):
        for key in self.__annotations__:
            if not getattr(self, key):
                raise InvalidOrderException(f"{message} {key} is required")


@dataclass(frozen=True)
class Address(AllFieldsRequiredMixin):
    street: str = ""
    city: str = ""
    country: str = ""
    postal_code: str = ""

    def __post_init__(self):
        self.validate_required("Address")


@dataclass(frozen=True)
class Customer(AllFieldsRequiredMixin):
    name: str = ""
    surname: str = ""

    def __post_init__(self):
        self.validate_required("Customer")


@dataclass(frozen=True)
class Item:
    name: str
    quantity: int
    price: Price
