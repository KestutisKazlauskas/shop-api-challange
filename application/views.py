from flask import jsonify
from flask.views import MethodView
from . import product_blueprint


class ProductApiView(MethodView):

    def get(self, product_id):
        print("veikia")
        if product_id is None:
            # return a list of users
            pass
        else:
            # expose a single user
            pass
        return jsonify({"welcome": "hello"})

    def post(self):
        # create a new user
        pass

    def delete(self, product_id):
        # delete a single user
        pass

    def put(self, product_id):
        # update a single user
        pass


product_view = ProductApiView.as_view("product_api")
product_blueprint.add_url_rule("/products/", defaults={"product_id": None}, view_func=product_view, methods=["GET"])
product_blueprint.add_url_rule("/products/", view_func=product_view, methods=["POST"])
product_blueprint.add_url_rule("/products/<int:product_id>", view_func=product_view, methods=["GET", "PUT", "DELETE"])
