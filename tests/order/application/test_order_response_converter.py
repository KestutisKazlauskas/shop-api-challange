from unittest import TestCase

import pytest

from application.order.responses import OrderResponseConverter
from tests.common.mock_order import create_order, create_order_item

unittest_assertions = TestCase()


@pytest.fixture
def response_converter():
    return OrderResponseConverter()


def test_convert_order_to_response_correctly(response_converter):
    order = create_order([create_order_item()])
    order.set_customer_information(name="Mark", surname="Mark")
    order.set_shipping_information("test", "test", "test", "LT-12323")
    correct_response = {
        "id": order.id,
        "cart_id": order.cart_id,
        "name": order.customer.name,
        "surname": order.customer.surname,
        "street": order.shipping_address.street,
        "city": order.shipping_address.city,
        "country": order.shipping_address.country,
        "postal_code": order.shipping_address.postal_code,
        "items": [{"name": item.name, "quantity": item.quantity, "price": item.price.value} for item in order.items],
        "status": order.status.value,
        "total": order.total.value,
        "discount": order.discount.value,
        "currency": order.total.currency
    }

    resposne_data = response_converter.convert_order_to_response(order)
    unittest_assertions.assertDictEqual(resposne_data, correct_response)
