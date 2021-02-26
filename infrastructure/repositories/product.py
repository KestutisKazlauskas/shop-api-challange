from typing import List

from domain.product.entities import Product, ProductType
from domain.product.repository import ProductRepository as Repository
from infrastructure.flask_app import db
from infrastructure.models import Product as ProductModel, ProductType as ProductTypeModel
from . import RepositoryIdGeneratorMixin


class ProductRepository(Repository, RepositoryIdGeneratorMixin):
    @staticmethod
    def _convert_product_model_to_product(product_model: ProductModel) -> Product:
        _type = ProductType(
            id=product_model.product_type.id,
            name=product_model.product_type.name
        )
        product = Product(
            id=product_model.id,
            name=product_model.name,
            type=_type,
            quantity=product_model.quantity
        )
        product.set_product_price(product_model.price_value, product_model.price_currency)
        for image in product_model.images:
            product.add_image(image.get("name"), image.get("url"))

        return product

    def generate_id(self) -> str:
        return self.generate_id()

    def find_all(self) -> List[Product]:
        products = []
        product_models = ProductModel.query.filter_by(is_deleted=False)
        for product_model in product_models:
            products.append(self._convert_product_model_to_product(product_model))

        return products

    def find_by(self, _id: str) -> Product:
        product_model = ProductModel.query.filter_by(id=_id, is_deleted=False).first()

        if product_model:
            return self._convert_product_model_to_product(product_model)

    def find_product_type_by(self, _id: str) -> ProductType:
        return db.session.query(ProductTypeModel).get({"id": _id})

    def create_from(self, product: Product) -> None:
        images = [{"name": image.name, "url": image.url} for image in product.images]
        product_type_model = db.session.query(ProductTypeModel).get({"id": product.type.id})

        if not product_type_model:
            product_type_model = ProductTypeModel(id=product.type.id, name=product.type.name)
            db.session.add(product_type_model)

        product_model = ProductModel(
            id=product.id,
            product_type_id=product_type_model.id,
            name=product.name,
            quantity=product.quantity,
            price_value=product.price.value,
            price_currency=product.price.currency,
            images=images
        )
        db.session.add(product_model)
        db.session.commit()

    def delete_by(self, _id: str) -> None:
        product = ProductModel.query.filter_by(id=_id).first()
        if product:
            product.is_deleted = True
        db.session.commit()
