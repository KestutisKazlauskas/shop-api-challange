from typing import List
from uuid import uuid4
from infrastructure.flask_app import db
from domain.product.repository import ProductRepository as Repository
from domain.product.entities import Product, ProductType
from infrastructure.models import Product as ProductModel, ProductType as ProductTypeModel


class ProductRepository(Repository):
    def generate_id(self) -> str:
        return str(uuid4())

    def find_all(self) -> List[Product]:
        pass

    def find_by(self, _id: str) -> Product:
        pass

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

    def update_from(self, product: Product) -> None:
        pass
