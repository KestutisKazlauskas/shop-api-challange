from flask import jsonify, request
from flask.views import MethodView

from domain.cart.exceptions import InvalidCartException
from infrastructure.repositories.cart import CartRepository
from infrastructure.repositories.product import ProductRepository
from . import cart_blueprint
from .requests import CartRequestConverter
from .responses import CartResponseConverter
from .services import CartService


class CartView(MethodView):

    def __init__(self):
        super().__init__()
        self.cart_repository = CartRepository()
        self.product_repository = ProductRepository()
        self.request_converter = CartRequestConverter()
        self.response_converter = CartResponseConverter()
        self.service = CartService(self.cart_repository, self.product_repository)

    def get(self, cart_id):
        cart = self.cart_repository.find_by(cart_id)
        if not cart:
            return jsonify({"message": "Cart not found"}), 404

        return jsonify(self.response_converter.convert_cart_to_response(cart)), 200

    def post(self):
        cart_create_dto = self.request_converter.convert_create_request_to_dto(request.data)
        try:
            cart = self.service.create_cart(cart_create_dto)
        except InvalidCartException as error:
            response, code = self.response_converter.convert_exception_to_response(error)
            return jsonify(response), code

        return jsonify(self.response_converter.convert_cart_to_response(cart)), 201

    def delete(self, cart_id):
        self.cart_repository.delete_by(cart_id)

        return jsonify(None), 204


class CartItemView(MethodView):
    def __init__(self):
        super().__init__()
        self.cart_repository = CartRepository()
        self.product_repository = ProductRepository()
        self.request_converter = CartRequestConverter()
        self.response_converter = CartResponseConverter()
        self.service = CartService(self.cart_repository, self.product_repository)

    def post(self, cart_id):
        cart = self.cart_repository.find_by(cart_id)
        if not cart:
            return jsonify({"message": "Cart not found"}), 404

        item_create_dto = self.request_converter.convert_create_item_request_to_dto(request.data)
        try:
            _, item = self.service.add_to_cart(cart, item_create_dto)
        except InvalidCartException as error:
            response, code = self.response_converter.convert_exception_to_response(error)
            return jsonify(response), code

        # TODO maybe here could return whole cart response because cart state has been changed
        return jsonify(self.response_converter.convert_cart_item_to_response(item)), 201

    def delete(self, cart_id, item_id):
        cart = self.cart_repository.find_by(cart_id)
        if not cart:
            return jsonify({"message": "Cart not found"}), 404

        try:
            cart.remove_item(item_id)
            self.cart_repository.update_from(cart)
        except InvalidCartException as error:
            response, code = self.response_converter.convert_exception_to_response(error)
            return jsonify(response), code

        # TODO maybe here could return whole cart response because cart state has been changed
        return jsonify(None), 204


cart_view = CartView.as_view("cart_api")
cart_item_view = CartItemView.as_view("cart_item_api")
cart_blueprint.add_url_rule("/carts/", view_func=cart_view, methods=["POST"])
cart_blueprint.add_url_rule("/carts/<cart_id>/", view_func=cart_view, methods=["GET", "DELETE"])
cart_blueprint.add_url_rule("/carts/<cart_id>/items/", view_func=cart_item_view, methods=["POST"])
cart_blueprint.add_url_rule("/carts/<cart_id>/items/<item_id>/", view_func=cart_item_view, methods=["DELETE"])
