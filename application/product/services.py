from typing import Callable

from domain.product.entities import Product, ProductType
from domain.product.exceptions import InvalidProductException
from domain.product.repository import ProductRepository
from .dtos import ProductDTO


class ProductService:
    def __init__(self, repository: ProductRepository, image_validator: Callable[[str], bool]):
        self.repository = repository
        self.image_validator = image_validator

    def find_or_create_product_type(self, _id: str, name: str) -> ProductType:
        if _id:
            product_type = self.repository.find_product_type_by(_id)
            if not product_type:
                raise InvalidProductException(f"{_id} product type does not exist")

        else:
            product_type = ProductType(
                id=self.repository.generate_id(),
                name=name
            )

        return product_type

    def create_product(self, product_dto: ProductDTO) -> Product:
        _id = self.repository.generate_id()
        product_type = self.find_or_create_product_type(
            product_dto.product_type_id, product_dto.product_type_name
        )
        product = Product(
            id=_id,
            name=product_dto.name,
            quantity=product_dto.quantity,
            type=product_type,
        )
        images = product_dto.images or []
        for image in images:
            if not self.image_validator(image.get("url")):
                raise InvalidProductException("Image with provided url does not exist.")
            product.add_image(name=image.get("name"), url=image.get("url"))

        product.set_product_price(product_dto.price, product_dto.currency)

        self.repository.create_from(product)

        return product

    def archive_product(self, product_id: str):
        product = self.repository.find_by(_id=product_id)
        # TODO maybe do not do this action and only delete from  repository???
        product.archive_product()
        self.repository.update_from(product)



