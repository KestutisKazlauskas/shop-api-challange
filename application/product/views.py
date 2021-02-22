from flask import jsonify, request
from flask.views import MethodView

from domain.product.exceptions import InvalidProductException
from infrastructure.repositories.product import ProductRepository
from infrastructure.utils import does_image_exists
from . import product_blueprint
from .requests import ProductRequestConverter
from .responses import ProductResponseConverter
from .services import ProductService


class ProductApiView(MethodView):
    """
    Request body example for POST api/products/:
        {
            "name": "Test product",
            "product_type_id": "4585a664-9aef-44da-ba0c-9aa4ea787ce5",
            "product_type_name": "Not Sport",
            "quantity": 4,
            "price": 12.39,
            "currency": "USD",
            "images": [
                {"name": "This is a name", "url": "https://via.placeholder.com/300/09f/fff.png"}
            ]
        }
    """
    def __init__(self):
        super().__init__()
        self.repository = ProductRepository()
        self.request_converter = ProductRequestConverter()
        self.response_converter = ProductResponseConverter()
        self.service = ProductService(self.repository, does_image_exists)

    def get(self, product_id):
        if product_id:
            product = self.repository.find_by(product_id)
            if not product:
                return jsonify({"message": "Product not found"}), 404

            return jsonify(self.response_converter.convert_product_to_response(product))

        products = self.repository.find_all()

        return jsonify([self.convert_product_to_response(product) for product in products])

    def post(self):
        product_dto = self.request_converter.convert_create_request_to_dto(request.data)
        try:
            # Product application service will take care of the product presisting to db
            # Will return valid domain Product
            product = self.service.create_product(product_dto)
        except InvalidProductException as e:
            response, code = self.response_converter.convert_exception_to_response(e)
            return jsonify(response), code

        return jsonify(self.response_converter.convert_product_to_response(product))

    def delete(self, product_id):
        try:
            self.service.archive_product(product_id)
        except InvalidProductException as e:
            response, code = self.response_converter.convert_exception_to_response(e)
            return jsonify(response), code

        return None, 204


product_view = ProductApiView.as_view("product_api")
product_blueprint.add_url_rule("/products/", defaults={"product_id": None}, view_func=product_view, methods=["GET"])
product_blueprint.add_url_rule("/products/", view_func=product_view, methods=["POST"])
product_blueprint.add_url_rule("/products/<int:product_id>", view_func=product_view, methods=["GET", "DELETE"])
