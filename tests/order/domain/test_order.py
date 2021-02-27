import pytest
import datetime
from tests.common.mock_order import create_order_item, create_order
from domain.order.exceptions import InvalidOrderException
from domain.order.entities import Order, Item, Price


@pytest.fixture
def order_item():
    return create_order_item()


@pytest.fixture
def order(order_item):
    return create_order([order_item])


@pytest.fixture
def customer_data():
    return {"name": "Mark", "surname": "MarkToo"}


@pytest.fixture
def address_data():
    return {"street": "test", "city": "test", "country": "test", "postal_code": "test"}


def test_order_without_id_exception():
    with pytest.raises(InvalidOrderException) as error:
        Order()

    assert error.value.message == "Order should have an id"


def test_order_without_cart_id_exception():
    with pytest.raises(InvalidOrderException) as error:
        Order(id="1234")

    assert error.value.message == "Order should have a cart_id"


def test_order_without_items_exception():
    with pytest.raises(InvalidOrderException) as error:
        Order(id="1234", cart_id="1234")

    assert error.value.message == "Order can't be empty"


@pytest.mark.parametrize("field, value", [("name", ""), ("surname", "")])
def test_set_customer_information_is_required(order, customer_data, field, value):
    with pytest.raises(InvalidOrderException) as error:
        customer_data[field] = value
        order.set_customer_information(**customer_data)

    assert error.value.message == f"Customer {field} is required"


@pytest.mark.parametrize("field, value", [("street", ""), ("city", ""), ("country", ""), ("postal_code", "")])
def test_set_address_information_is_required(order, address_data,  field, value):
    with pytest.raises(InvalidOrderException) as error:
        address_data[field] = value
        order.set_shipping_information(**address_data)

    assert error.value.message == f"Address {field} is required"


def test_set_customer_information_is_correct(order, customer_data):
    order.set_customer_information(**customer_data)
    for key in customer_data:
        assert getattr(order.customer, key) == customer_data[key]


def test_set_shipping_information_is_correct(order, address_data):
    order.set_shipping_information(**address_data)
    for key in address_data:
        assert getattr(order.shipping_address, key) == address_data[key]
