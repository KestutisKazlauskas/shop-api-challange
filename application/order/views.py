from flask import jsonify, request
from flask.views import MethodView

from domain.order.exceptions import InvalidOrderException
from infrastructure.repositories.cart import CartRepository
from infrastructure.repositories.order import OrderRepository
from . import order_blueprint
from .requests import OrderRequestConverter
from .responses import OrderResponseConverter
from .services import OrderService


class OrderView(MethodView):
    def __init__(self):
        super().__init__()
        self.cart_repository = CartRepository()
        self.order_repository = OrderRepository()
        self.request_converter = OrderRequestConverter()
        self.response_converter = OrderResponseConverter()
        self.service = OrderService(self.order_repository, self.cart_repository)

    def post(self):
        order_create_dto = self.request_converter.convert_create_request_to_dto(request.data)
        try:
            order = self.service.create_order(order_create_dto)
        except InvalidOrderException as error:
            response, code = self.response_converter.convert_exception_to_response(error)
            return response, code

        return jsonify(self.response_converter.convert_order_to_response(order)), 201

    def get(self, order_id):
        order = self.order_repository.find_by(order_id)
        if not order:
            return jsonify({"message": "Cart not found"}), 404

        return jsonify(self.response_converter.convert_order_to_response(order))


order_view = OrderView.as_view("order_api")
order_blueprint.add_url_rule("/orders/", view_func=order_view, methods=["POST"])
order_blueprint.add_url_rule("/orders/<order_id>", view_func=order_view, methods=["GET"])
