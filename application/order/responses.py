from application.common.responses import ResponseConverter
from domain.order.entities import Order, Item
from .dtos import OrderDTO, OrderItemDTO


class OrderResponseConverter(ResponseConverter):

    @staticmethod
    def _convert_item(order_item: Item) -> OrderItemDTO:
        return OrderItemDTO(
            name=order_item.name,
            price=order_item.price.value,
            quantity=order_item.quantity
        )

    @staticmethod
    def _convert_customer(customer) -> dict:
        if customer:
            return {
                "name": customer.name,
                "surname": customer.surname,
            }
        return {}

    @staticmethod
    def _convert_shipping_address(address) -> dict:
        if address:
            return {
                "street": address.street,
                "city": address.city,
                "country": address.country,
                "postal_code": address.postal_code,
            }
        return {}

    def convert_order_to_response(self, order: Order) -> dict:
        return OrderDTO(
            id=order.id,
            cart_id=order.cart_id,
            total=order.total.value,
            currency=order.total.currency,
            discount=order.discount.value,
            status=order.status.value,
            items=[self._convert_item(item) for item in order.items],
            **self._convert_customer(order.customer),
            **self._convert_shipping_address(order.shipping_address),
        ).to_dict()
