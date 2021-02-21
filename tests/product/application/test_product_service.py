import datetime
from typing import List

import pytest

from application.product.dtos import ProductDTO
from application.product.services import ProductService
from domain.product.entities import Product, ProductType
from domain.product.repository import ProductRepository


def image_validator(url: str):
    return True


class Repository(ProductRepository):
    def generate_id(self) -> str:
        return str(datetime.datetime.now())

    def find_all(self) -> List[Product]:
        raise []

    def find_by(self, _id: int) -> Product:
        raise NotImplementedError

    def find_product_type_by(self, _id: str) -> ProductType:
        return ProductType(id=_id, name="Tests")

    def create_product_type(self, product_type: ProductType) -> None:
        raise NotImplementedError

    def create_from(self, product: Product) -> None:
        pass

    def update_from(self, product: Product) -> None:
        pass


@pytest.fixture
def validator():
    return image_validator


@pytest.fixture
def repository():
    return Repository()


@pytest.fixture
def service(repository, validator):
    return ProductService(repository, validator)


@pytest.fixture
def product_dto():
    return ProductDTO(
        name="Test",
        quantity=12,
        price=12.30,
        currency="USD",
        product_type_name="New Type",
        images=[{"url": "test", "name": "Name"}]
    )


def test_find_product_type_by_id_return_existing_product_type(service):
    product_type = service.find_or_create_product_type(_id="test", name=None)
    assert product_type.id == "test"
    assert product_type.name == "Tests"


def test_find_product_type_by_id_return_new_product_type(service):
    product_type = service.find_or_create_product_type(_id=None, name="Another name")
    assert product_type.id != "test"
    assert product_type.name == "Another name"


def test_create_product_product_is_returned(service, product_dto):
    product = service.create_product(product_dto)
    assert product.name == product_dto.name
    assert product.quantity == product_dto.quantity
    assert product.price.value == product_dto.price
    assert product.price.currency == product_dto.currency
    assert product.type.name == product_dto.product_type_name
    assert product.images[0].name == product_dto.images[0].get("name")
    assert product.images[0].url == product_dto.images[0].get("url")




