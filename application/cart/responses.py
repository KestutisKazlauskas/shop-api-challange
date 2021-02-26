from application.common.responses import ResponseConverter
from domain.cart.entities import Cart, Item
from .dtos import CartDTO, CartItemDTO


class CartResponseConverter(ResponseConverter):

    @staticmethod
    def _convert_cart_item_to_dto(cart_item: Item):
        return CartItemDTO(
            id=cart_item.id,
            product_id=cart_item.product_id,
            name=cart_item.product_name,
            quantity=cart_item.quantity,
            price=cart_item.unit_price.value,
        )

    def convert_cart_item_to_response(self, cart_item: Item) -> dict:
        return self._convert_cart_item_to_dto(cart_item).to_dict()

    def convert_cart_to_response(self, cart: Cart) -> dict:
        items = []
        for cart_item in cart.items:
            items.append(self._convert_cart_item_to_dto(cart_item))

        return CartDTO(
            id=cart.id,
            currency=cart.total.currency,
            total=cart.total.value,
            discount=sum([discount.value for discount in cart.discounts]),
            items=items
        ).to_dict()
