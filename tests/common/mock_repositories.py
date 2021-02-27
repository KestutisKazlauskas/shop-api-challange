import datetime
from domain.product.entities import Product, ProductType
from domain.product.repository import ProductRepository
from domain.cart.repository import CartRepository
from domain.order.repository import OrderRepository
from .mock_product import create_product
from .mock_cart import create_cart, create_cart_item


class ProductMockRepository(ProductRepository):
    def generate_id(self) -> str:
        return str(datetime.datetime.now())

    def find_all(self):
        raise []

    def find_by(self, _id: str) -> Product:
        if _id == "exists":
            return create_product()

    def find_product_type_by(self, _id: str) -> ProductType:
        return ProductType(id=_id, name="Tests")

    def create_product_type(self, product_type: ProductType) -> None:
        pass

    def create_from(self, product: Product) -> None:
        pass

    def delete_by(self, _id: str) -> None:
        pass


class CartMockRepository(CartRepository):
    def generate_id(self) -> str:
        return str(datetime.datetime.now())

    def find_by(self, _id: str):
        if _id == "exists":
            return create_cart(items=[create_cart_item()])

    def delete_by(self, _id: str) -> None:
        pass

    def create_from(self, cart) -> None:
        pass

    def update_from(self, cart) -> None:
        pass


class OrderMockRepository(OrderRepository):
    def generate_id(self) -> str:
        return str(datetime.datetime.now())

    def create_from(self, order) -> None:
        pass

    def find_by(self, _id: str):
        pass
