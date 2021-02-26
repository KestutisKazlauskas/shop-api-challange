from domain.product.entities import Product, ProductType, Image, Price


def create_product():
    return Product(
        id="Test",
        name="Test",
        quantity=12,
        type=ProductType(id="test", name="Test"),
        images=[Image(name="test", url="test_url")],
        price=Price(12.34, "USD"),
    )