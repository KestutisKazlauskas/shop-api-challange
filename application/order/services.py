from .dtos import OrderCreateDTO
from domain.order.entities import Order, Item, Price
from domain.order.exceptions import InvalidOrderException
from infrastructure.repositories.order import Repository as OrderRepository
from infrastructure.repositories.cart import Repository as CartRepository


class OrderService:
    def __init__(self, order_repository: OrderRepository, cart_repository: CartRepository):
        self.order_repository = order_repository
        self.cart_repository = cart_repository

    @staticmethod
    def convert_cart_items_to_order(cart_item) -> Item:
        return Item(name=cart_item.product_name, quantity=cart_item.quantity, price=cart_item.unit_price)

    def create_order(self, order_dto: OrderCreateDTO) -> Order:
        cart = self.cart_repository.find_by(order_dto.cart_id)
        if not cart:
            raise InvalidOrderException(f"Cart with id {order_dto.cart_id} does not exists")

        order = Order(
            id=self.order_repository.generate_id(),
            cart_id=cart.id,
            items=[self.convert_cart_items_to_order(item) for item in cart.items],
            discount=Price(sum([discount.value for discount in cart.discounts])),
            total=cart.total
        )
        if order_dto.name or order_dto.surname:
            order.set_customer_information(order_dto.name, order_dto.surname)

        if any([order_dto.street, order_dto.city, order_dto.country, order_dto.postal_code]):
            order.set_shipping_information(order_dto.street, order_dto.city, order_dto.country, order_dto.postal_code)

        self.order_repository.create_from(order)

        return order
