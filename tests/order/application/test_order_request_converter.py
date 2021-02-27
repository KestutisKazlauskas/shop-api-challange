import pytest
import json
from application.order.requests import OrderRequestConverter


@pytest.fixture
def valid_request():
    data = {
        "cart_id": "cart_id",
        "name": "Mark",
        "surname": "Mark",
        "street": "Street st. 23",
        "city": "Vilnius",
        "country": "Lithuania",
        "postal_code": "LT-09315"
    }
    return json.dumps(data).encode("utf-8")


@pytest.fixture
def converter():
    return OrderRequestConverter()


def test_convert_create_request_to_dto_works_correctly(converter, valid_request):
    correct_data = json.loads(valid_request)
    order_dto = converter.convert_create_request_to_dto(valid_request)
    for key in correct_data:
        assert getattr(order_dto, key) == correct_data[key]


def test_convert_create_request_to_dto_empty_dto(converter):
    order_dto = converter.convert_create_request_to_dto(b"Thi is no a valid request")
    for key in order_dto.__annotations__:
        assert getattr(order_dto, key) is None
