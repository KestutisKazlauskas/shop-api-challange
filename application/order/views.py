from flask import jsonify, request
from flask.views import MethodView
from . import order_blueprint


class OrderView(MethodView):

    def post(self):
        return jsonify({}), 201

    def get(self, order_id):
        return jsonify({})


order_view = OrderView.as_view("order_api")
order_blueprint.add_url_rule("/orders/", view_func=order_view, methods=["POST"])
order_blueprint.add_url_rule("/orders/<order_id>", view_func=order_view, methods=["GET"])
