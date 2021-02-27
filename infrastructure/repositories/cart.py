from domain.cart.entities import Cart, Item, Price
from domain.cart.repository import CartRepository as Repository
from infrastructure.flask_app import db
from infrastructure.models import Cart as CartModel, CartItem, Discount
from . import RepositoryIdGenerator


class CartRepository(Repository):

    def __init__(self, uuid_generator=None):
        self.uuid_generator = uuid_generator or RepositoryIdGenerator()

    @staticmethod
    def _model_item_to_cart_item(model_item) -> Item:
        free_unit_price = None
        if model_item.free_unit_price:
            free_unit_price = Price(model_item.free_unit_price, model_item.currency)

        return Item(
            id=str(model_item.id),
            product_id=str(model_item.product_id),
            product_type_id=str(model_item.product_type_id),
            product_name=model_item.product_name,
            quantity=model_item.quantity,
            unit_price=Price(model_item.unit_price, model_item.currency),
            free_unit_price=free_unit_price
        )

    @staticmethod
    def _create_items(cart_id, items):
        for item in items:
            db.session.add(CartItem(
                id=item.id,
                cart_id=cart_id,
                product_id=item.product_id,
                product_name=item.product_name,
                product_type_id=item.product_type_id,
                quantity=item.quantity,
                unit_price=item.unit_price.value,
                currency=item.unit_price.currency,
                free_unit_price=item.free_unit_price.value if item.free_unit_price else None,
            ))

    @staticmethod
    def _create_discounts(cart_id, discounts):
        for discount in discounts:
            db.session.add(Discount(
                cart_id=cart_id,
                name=discount.name,
                price=discount.value,
                currency=discount.currency
            ))

    def generate_id(self) -> str:
        return self.uuid_generator.generate_id()

    def find_by(self, _id: str) -> Cart:
        cart_model = CartModel.query.filter_by(id=_id, is_deleted=False).first()
        if cart_model:
            cart = Cart(
                id=str(cart_model.id),
                items=[self._model_item_to_cart_item(item) for item in cart_model.items]
            )

            return cart

    def delete_by(self, _id: str) -> None:
        cart_model = CartModel.query.filter_by(id=_id).first()
        cart_model.is_deleted = True
        db.session.commit()

    def create_from(self, cart: Cart) -> None:
        cart_model = CartModel(
            id=cart.id,
            total=cart.total.value,
            currency=cart.total.currency,
        )
        db.session.add(cart_model)
        self._create_items(cart.id, cart.items)
        self._create_discounts(cart.id, cart.discounts)
        db.session.commit()

    def update_from(self, cart: Cart) -> None:
        Discount.query.filter_by(cart_id=cart.id).delete()
        CartItem.query.filter_by(cart_id=cart.id).delete()

        # Update cart object
        cart_model = CartModel.query.filter_by(id=cart.id).first()
        cart_model.total = cart.total.value
        cart_model.currency = cart.total.currency

        # Update items and discounts
        self._create_items(cart.id, cart.items)
        self._create_discounts(cart.id, cart.discounts)
        db.session.commit()
