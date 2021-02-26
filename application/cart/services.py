from domain.cart.entities import Cart, Item
from domain.product.entities import Product
from domain.cart.exceptions import InvalidCartException
from infrastructure.repositories.cart import Repository as CartRepository
from infrastructure.repositories.product import Repository as ProductRepository
from .dtos import CartCreateDTO, ItemCreateDTO


class CartService:
    def __init__(self, cart_repository: CartRepository, product_repository: ProductRepository):
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    def _retrieve_cart_item_product(self, product_id: str):
        product = self.product_repository.find_by(product_id)
        if not product:
            raise InvalidCartException(f"Product with id {product_id} does not exists")

        return product

    def _create_item(self, item_dto: ItemCreateDTO, product: Product) -> Item:
        return Item(
            id=self.cart_repository.generate_id(),
            product_id=product.id,
            product_type_id=product.type.id,
            product_name=product.name,
            unit_price=product.price,
            quantity=item_dto.quantity
        )

    def create_cart(self, cart_dto: CartCreateDTO) -> Cart:
        items = []
        for item_dto in cart_dto.items:
            product = self._retrieve_cart_item_product(item_dto.product_id)
            items.append(self._create_item(item_dto, product))

        cart = Cart(id=self.cart_repository.generate_id(), items=items)
        self.cart_repository.create_from(cart)

        return cart

    def add_to_cart(self, cart: Cart, item_dto: ItemCreateDTO) -> (Cart, Item):
        product = self._retrieve_cart_item_product(item_dto.product_id)
        item = self._create_item(item_dto, product)
        cart.add_item(item)

        self.cart_repository.update_from(cart)

        return cart, item
