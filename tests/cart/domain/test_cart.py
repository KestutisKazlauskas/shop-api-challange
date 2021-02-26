import pytest

from domain.cart.entities import Cart
from domain.cart.exceptions import InvalidCartException
from tests.common.mock_cart import create_cart_item, create_cart


@pytest.fixture
def cart_item():
    return create_cart_item()


@pytest.fixture
def cart(cart_item):
    return create_cart([cart_item])


def test_cart_total_is_correct(cart, cart_item):
    correct_total = cart_item.unit_price * cart_item.quantity

    assert cart.total.value == correct_total.value
    assert cart.total.currency == correct_total.currency


def test_can_add_item_when_total_limit_exceed_100_usd(cart):
    item = create_cart_item(100.0)
    can_add_product = cart.can_add_item(item)

    assert can_add_product == False


def test_can_add_when_limit_not_exceed(cart):
    item = create_cart_item(10.0)
    can_add_product = cart.can_add_item(item)

    assert can_add_product == True


def test_add_item_appends_item_and_changes_total(cart):
    total_items = len(cart.items)
    total_value = cart.total.value

    item = create_cart_item(5.0)
    cart.add_item(item)

    correct_total_value = total_value + item.unit_price.value * item.quantity

    assert len(cart.items) == total_items + 1
    assert cart.total.value == correct_total_value


def test_item_already_added_exception(cart, cart_item):
    with pytest.raises(InvalidCartException):
        cart.add_item(cart_item)


def test_every_fifth_same_type_product_item_free(cart):
    # add 9 more products
    # first product already exists
    for _ in range(9):
        cart.add_item(create_cart_item())

    fifth_item = cart.items[4]
    tenth_item = cart.items[9]
    assert fifth_item.unit_price.value == 0
    assert tenth_item.unit_price.value == 0


def test_every_fifth_same_type_product_item_free_rollback(cart, cart_item):
    # Test the case:
    #   Added 5 items of the same product type
    #   Removed not the last free item which was added
    #   The added item should become not free anymore because it is not a fifth item.
    for _ in range(4):
        cart.add_item(create_cart_item())
    fifth_item = cart.items[4]

    cart.remove_item(cart_item.id)

    free_item = cart.items[3]
    assert free_item.unit_price.value != 0
    assert free_item.unit_price.value == fifth_item.unit_price.value


def test_1_dollar_discount_on_20_dollar_total_applied(cart):
    item = create_cart_item(10.0)
    cart.add_item(item)

    assert cart.total.value == 19.0


def test_1_dollar_discount_on_20_dollar_total_unapplied(cart, cart_item):
    item = create_cart_item(10.0)
    cart.add_item(item)
    cart.remove_item(item.id)

    assert len(cart.items) == 1
    assert cart.total.value == (cart_item.unit_price * cart_item.quantity).value
