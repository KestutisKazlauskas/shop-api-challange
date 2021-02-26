import pytest
from domain.common.exceptions import InvalidPriceComparisonException
from domain.common.value_objects import Price, CurrencyEnum


class MockCurrency(CurrencyEnum):
    USD = "USD"
    EUR = "EUR"

    @staticmethod
    def value_list():
        return [currency.value for currency in MockCurrency]


def test_price_addition():
    addition = Price(10.0, "USD") + Price(2.50, "USD")
    assert addition.value == 12.50


def test_price_subtraction():
    subtraction = Price(10.0, "USD") - Price(2.0, "USD")
    assert subtraction.value == 8.0


def test_price_multiplication():
    multiplication = Price(10.0, "USD") * 2
    assert multiplication.value == 20.0


def test_price_grater_then():
    bigger = Price(10.0, "USD") > Price(2, "USD")
    smaller = Price(10.0, "USD") > Price(20, "USD")
    assert bigger == True
    assert smaller == False


def test_price_grater_then_equal():
    bigger = Price(10.0, "USD") >= Price(2, "USD")
    smaller = Price(10.0, "USD") >= Price(20, "USD")
    equal = Price(10.0, "USD") >= Price(10.0, "USD")
    assert bigger == True
    assert smaller == False
    assert equal == True


def test_price_invalid_comparasion_exception():
    with pytest.raises(InvalidPriceComparisonException):
        compare = Price(10.0, "USD") > Price(2, "EUR", currency_enum=MockCurrency)
