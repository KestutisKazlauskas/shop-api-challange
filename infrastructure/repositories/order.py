from infrastructure.flask_app import db
from domain.order.repository import OrderRepository as Repository
from domain.order.entities import Order, Customer, Address, Item, Price, Status
from infrastructure.models import Order as OrderModel, OrderItem
from . import RepositoryIdGenerator


class OrderRepository(Repository):
    def __init__(self, uuid_generator=None):
        self.uuid_generator = uuid_generator or RepositoryIdGenerator()

    @staticmethod
    def _convert_order_item(item: OrderItem, currency) -> Item:
        return Item(
            name=item.name,
            quantity=item.quantity,
            price=Price(item.price, currency)
        )

    @staticmethod
    def _create_order_item(item: Item, order_id: str):
        db.session.add(OrderItem(order_id=order_id, name=item.name, quantity=item.quantity, price=item.price.value))

    def generate_id(self) -> str:
        return self.uuid_generator.generate_id()

    def create_from(self, order: Order) -> None:
        order_model = OrderModel(
            id=order.id,
            cart_id=order.cart_id,
            total=order.total.value,
            discount=order.discount.value,
            currency=order.total.currency,
            status=order.status.value,
            customer_name=order.customer.name if order.customer else None,
            customer_surname=order.customer.surname if order.customer else None,
            street=order.shipping_address.street if order.shipping_address else None,
            city=order.shipping_address.city if order.shipping_address else None,
            country=order.shipping_address.country if order.shipping_address else None,
            postal_code=order.shipping_address.postal_code if order.shipping_address else None,
        )
        for item in order.items:
            self._create_order_item(item, order.id)

        db.session.add(order_model)
        db.session.commit()

    def find_by(self, _id: str) -> Order:
        order_model = OrderModel.query.filter_by(id=_id).first()
        if order_model:
            customer = None
            if order_model.customer_name:
                customer = Customer(order_model.customer_name, order_model.customer_surname)

            address = None
            if order_model.street:
                address = Address(
                    street=order_model.street,
                    city=order_model.city,
                    country=order_model.country,
                    postal_code=order_model.postal_code
                )
            order = Order(
                id=str(order_model.id),
                cart_id=str(order_model.cart_id),
                items=[self._convert_order_item(item, order_model.currency) for item in order_model.items],
                customer=customer,
                shipping_address=address,
                total=Price(order_model.total, order_model.currency),
                discount=Price(order_model.discount, order_model.currency),
                status=Status(order_model.status)
            )

            return order

