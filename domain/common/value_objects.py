from dataclasses import dataclass
from enum import Enum

from domain.common.exceptions import InValidDomainException, InvalidPriceComparisonException


class CurrencyEnum(Enum):
    @staticmethod
    def value_list():
        raise NotImplementedError


class Currency(CurrencyEnum):
    USD = "USD"

    @staticmethod
    def value_list():
        return [currency.value for currency in Currency]


@dataclass(frozen=True)
class Price:
    value: float = None
    currency: str = Currency.USD.value
    currency_enum: CurrencyEnum = Currency

    def __add__(self, other):
        self.__can_make_operation(other)
        return Price(value=self.value + other.value, currency=self.currency)

    def __sub__(self, other):
        self.__can_make_operation(other)
        return Price(value=self.value - other.value, currency=self.currency)

    def __gt__(self, other):
        self.__can_make_operation(other)
        return self.value > other.value

    def __ge__(self, other):
        self.__can_make_operation(other)
        return self.value >= other.value

    def __mul__(self, value: int):
        return Price(value=self.value*value, currency=self.currency)

    def __post_init__(self):
        if self.value is None:
            raise InValidDomainException("price is required.")

        if self.value < 0:
            raise InValidDomainException("Price could not be negative.")

        if self.currency not in self.currency_enum.value_list():
            raise InValidDomainException(f"currency not matches {str(self.currency_enum.value_list())}")

    def __can_make_operation(self, other):
        if self.currency != other.currency:
            raise InvalidPriceComparisonException("Currency is not the same")
