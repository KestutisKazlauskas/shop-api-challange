from application.product.dtos import ProductDTO
from domain.product.entities import Product
from domain.product.exceptions import InvalidProductException


class ProductResponseConverter:

    @staticmethod
    def convert_product_to_response(product: Product) -> dict:
        product_dto = ProductDTO(
            id=product.id,
            name=product.name,
            price=product.price.value,
            quantity=product.quantity,
            currency=product.price.currency,
            product_type_id=product.type.id,
            product_type_name=product.type.name,
            images=[
                {"url": image.url, "name": image.name} for image in product.images
            ]
        )

        return product_dto.to_dict()

    @staticmethod
    def convert_exception_to_response(exception: InvalidProductException) -> (dict, int):
        return {"message": exception.message}, 400
