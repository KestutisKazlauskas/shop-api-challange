import pytest
import json
from unittest import TestCase
from application.cart.requests import CartRequestConverter

unittest_assertions = TestCase()


@pytest.fixture
def valid_request():
    data = {
        "items": [
            {"product_id": "id string", "quantity": 1},
            {"product_id": "id string", "quantity": 2}
        ]
    }
    return json.dumps(data).encode("utf-8")


@pytest.fixture
def converter():
    return CartRequestConverter()


def test_convert_create_request_to_dto_works_correctly(converter, valid_request):
    correct_data = json.loads(valid_request)
    cart_dto = converter.convert_create_request_to_dto(valid_request)
    correct_items = correct_data.get("items")
    for key, item in enumerate(correct_items):
        cart_item_dto = cart_dto.items[key]
        for item_key in item:
            assert getattr(cart_item_dto, item_key) == item[item_key]


def test_convert_create_item_request_to_dto_works_correctly(converter):
    valid_request = {"product_id": "id string", "quantity": 1}
    item_dto = converter.convert_create_item_request_to_dto(json.dumps(valid_request).encode("utf-8"))

    assert item_dto.product_id == valid_request.get("product_id")
    assert item_dto.quantity == valid_request.get("quantity")


def test_convert_request_data_return_empty_cart_dto(converter):
    cart_dto = converter.convert_create_request_to_dto(b"Thi is no a valid request")
    unittest_assertions.assertIsNone(cart_dto.items)


def test_convert_create_item_request_to_dto_empty_item(converter):
    item_dto = converter.convert_create_item_request_to_dto(b"Thi is no a valid request")
    assert item_dto.product_id == ""
    assert item_dto.quantity == 0



