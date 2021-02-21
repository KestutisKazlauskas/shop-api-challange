import pytest
from domain.product.entities import Product, ProductType
from domain.product.value_objects import Currency
from domain.product.exceptions import InvalidProductException


@pytest.fixture
def product_type():
    return ProductType(id="123", name="fsdfdf")


@pytest.fixture
def product(product_type):
    return Product(name="Long", type=product_type, quantity=12)


def test_product_without_name_invalid_product_exception():
    with pytest.raises(InvalidProductException) as error:
        Product(name=None)

    assert error.value.message == "Product name  is required."


def test_product_name_is_too_long():
    with pytest.raises(InvalidProductException, ) as error:
        Product(name="Long"*244)

    assert error.value.message == "Product name is to long."


def test_product_type_not_set():
    with pytest.raises(InvalidProductException, ) as error:
        Product(name="Long", type=None)

    assert error.value.message == "Product type is required."


def test_product_quantity_not_valid(product_type):
    with pytest.raises(InvalidProductException, ) as error:
        Product(name="Long", type=product_type, quantity=-1)

    assert error.value.message == "Quantity can not be less than 0"


def test_add_image(product):
    product.add_image("Image", "test_url")

    assert product.images[0].name == "Image"
    assert product.images[0].url == "test_url"


def test_set_price(product):
    product.set_product_price(12.90, "USD")

    assert product.price.value == 12.90
    assert product.price.currency == "USD"


def test_invalid_product_price(product):
    with pytest.raises(InvalidProductException, ) as error:
        product.set_product_price(12.90, "KKK")

    assert error.value.message == f"currency not matches {str(Currency.value_list())}"


def test_invalid_product_price_value(product):
    with pytest.raises(InvalidProductException, ) as error:
        product.set_product_price(-12.90, "USD")

    assert error.value.message == f"Price could not be negative."
