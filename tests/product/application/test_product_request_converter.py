import pytest
import json
from unittest import TestCase
from application.product.requests import ProductRequestConverter

unittest_assertions = TestCase()


@pytest.fixture
def valid_request():
    data = {
        "name": "This is name",
        "quantity": 12,
        "price": 12.50,
        "currency": "USD",
        "product_type_name": "Sport",
        "product_type_id": "this is and id",
        "images": [
            {"name": "Image", "url": "This is a valid image url"}
        ]
    }
    return json.dumps(data).encode("utf-8")


@pytest.fixture
def converter():
    return ProductRequestConverter()


def test_convert_request_data_bytes_to_product_dto(converter, valid_request):
    correct_data = json.loads(valid_request)
    command = converter.convert_create_request_to_dto(valid_request)
    for key in correct_data:
        assert getattr(command, key) == correct_data.get(key)


def test_convert_request_data_return_empty_product_dto(converter):
    command = converter.convert_create_request_to_dto(b"Thi is no a valid request")
    for key in command.__annotations__:
        unittest_assertions.assertIsNone(getattr(command, key))




