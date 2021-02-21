from dataclasses import dataclass
from enum import Enum
from domain.product.exceptions import InvalidProductException


class Currency(Enum):
    USD = "USD"
    GBP = "GBP"
    EUR = "EUR"

    @staticmethod
    def value_list():
        return [currency.value for currency in Currency]


@dataclass(frozen=True)
class Image:
    name: str = None
    url: str = None

    def __post_init__(self):
        if not self.name:
            raise InvalidProductException("Product image name is required.")

        if not self.url:
            raise InvalidProductException("Product image url is required.")


@dataclass(frozen=True)
class Price:
    value: float = None
    currency: str = None
    currency_enum: Currency = Currency

    def __post_init__(self):
        if self.value is None:
            raise InvalidProductException("Product price is required.")

        if self.value < 0:
            raise InvalidProductException("Price could not be negative.")

        if self.currency not in self.currency_enum.value_list():
            raise InvalidProductException(f"currency not matches {str(self.currency_enum.value_list())}")
