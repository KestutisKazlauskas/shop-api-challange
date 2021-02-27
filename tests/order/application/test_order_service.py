import pytest

from tests.common.mock_repositories import CartMockRepository, OrderMockRepository
from domain.order.exceptions import InvalidOrderException
from application.order.services import OrderService
from application.order.dtos import OrderCreateDTO


@pytest.fixture()
def cart_repository():
    return CartMockRepository()


@pytest.fixture()
def order_repository():
    return OrderMockRepository()


@pytest.fixture
def service(order_repository, cart_repository):
    return OrderService(order_repository, cart_repository)


def test_create_order_service_working_correctly(service, cart_repository):
    dto = OrderCreateDTO(
        cart_id="exists",
        name="mark",
        surname="mark",
        street="street",
        city="city",
        country="country",
        postal_code="postal code"
    )
    order = service.create_order(dto)
    cart = cart_repository.find_by("exists")
    assert len(order.items) == len(cart.items)
    assert order.cart_id == cart.id
    assert order.customer.name == dto.name
    assert order.customer.surname == dto.surname
    assert order.shipping_address.street == dto.street
    assert order.shipping_address.city == dto.city
    assert order.shipping_address.country == dto.country
    assert order.shipping_address.postal_code == dto.postal_code
    assert order.total.value == cart.total.value
    assert order.discount.value == sum([discount.value for discount in cart.discounts])


def test_create_order_service_cart_not_found_exception(service):
    dto = OrderCreateDTO(cart_id="dfdfdf")
    with pytest.raises(InvalidOrderException) as error:
        service.create_order(dto)

    assert error.value.message == f"Cart with id {dto.cart_id} does not exists"
