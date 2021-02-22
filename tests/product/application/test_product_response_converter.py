import pytest
from application.product.responses import ProductResponseConverter
from domain.product.exceptions import InvalidProductException
# TODO make product fixtures in separate
from domain.product.entities import Product, ProductType, Image, Price

from unittest import TestCase
unittest_assertions = TestCase()


@pytest.fixture
def response_converter():
    return ProductResponseConverter()


@pytest.fixture
def product():
    return Product(
        id="Test",
        name="Test",
        quantity=12,
        type=ProductType(id="test", name="Test"),
        images=[Image(name="test", url="test_url")],
        price=Price(12.34, "USD"),
    )


def test_convert_product_response(response_converter, product):
    data = response_converter.convert_product_to_response(product)
    correct_images = [{"url": image.url, "name": image.name} for image in product.images]
    assert data.get("id") == product.id
    assert data.get("name") == product.name
    assert data.get("quantity") == product.quantity
    assert data.get("price") == product.price.value
    assert data.get("currency") == product.price.currency
    assert data.get("product_type_id") == product.type.id
    assert data.get("product_type_name") == product.type.name
    for key, image in enumerate(correct_images):
        unittest_assertions.assertDictEqual(data.get("images")[key], image)


def test_convert_exception_to_response(response_converter):
    error = InvalidProductException(message="This is error")
    response, code = response_converter.convert_exception_to_response(error)
    assert response == {"message": error.message}
    assert code == 400

