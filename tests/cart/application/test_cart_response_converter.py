from unittest import TestCase

import pytest

from application.cart.responses import CartResponseConverter
from tests.common.mock_cart import create_cart_item, create_cart

unittest_assertions = TestCase()


@pytest.fixture
def response_converter():
    return CartResponseConverter()


def test_convert_cart_to_response_correctly(response_converter):
    cart_item = create_cart_item()
    cart = create_cart([cart_item])

    data = response_converter.convert_cart_to_response(cart)
    assert len(data.get("items")) == 1

    correct_item = {
        "id": cart_item.id,
        "product_id": cart_item.product_id,
        "name": cart_item.product_name,
        "quantity": cart_item.quantity,
        "price": cart_item.unit_price.value
    }
    correct_cart_data = {
        "id": cart.id,
        "currency": cart.total.currency,
        "total": cart.total.value,
        "discount": sum([dis.value for dis in cart.discounts]),
        "items": [correct_item]
    }
    unittest_assertions.assertDictEqual(data, correct_cart_data)
