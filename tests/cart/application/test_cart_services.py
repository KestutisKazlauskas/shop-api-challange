import pytest

from application.cart.dtos import CartCreateDTO, ItemCreateDTO
from application.cart.services import CartService
from domain.cart.exceptions import InvalidCartException
from tests.common.mock_repositories import ProductMockRepository, CartMockRepository
from tests.common.mock_product import create_product
from tests.common.mock_cart import create_cart, create_cart_item


@pytest.fixture
def product_repository():
    return ProductMockRepository()


@pytest.fixture()
def cart_repository():
    return CartMockRepository()


@pytest.fixture
def service(cart_repository, product_repository):
    return CartService(cart_repository, product_repository)


def test_create_cart_service_return_cart(service):
    cart_create_dto = CartCreateDTO(items=[ItemCreateDTO(product_id="exists", quantity=1)])
    product = create_product()
    cart = service.create_cart(cart_create_dto)

    assert len(cart.items) == 1
    assert cart.items[0].product_id == product.id


def test_create_cart_service_product_does_not_exists(service):
    cart_dto = CartCreateDTO(items=[ItemCreateDTO(product_id="not", quantity=1)])
    with pytest.raises(InvalidCartException) as error:
        service.create_cart(cart_dto)

    assert error.value.message == f"Product with id {cart_dto.items[0].product_id} does not exists"


def test_ad_to_cart_service_working_correctly(service):
    item_dto = ItemCreateDTO(product_id="exists", quantity=1)
    cart = create_cart(items=[create_cart_item()])
    cart, item = service.add_to_cart(cart, item_dto)

    assert len(cart.items) == 2


def test_ad_to_cart_service_product_does_not_exists(service):
    item_dto = ItemCreateDTO(product_id="no", quantity=1)
    cart = create_cart(items=[create_cart_item()])
    with pytest.raises(InvalidCartException) as error:
        service.add_to_cart(cart, item_dto)

    assert error.value.message == f"Product with id {item_dto.product_id} does not exists"
