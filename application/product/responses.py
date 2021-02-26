from application.common.responses import ResponseConverter
from application.product.dtos import ProductDTO
from domain.product.entities import Product


class ProductResponseConverter(ResponseConverter):

    @staticmethod
    def convert_product_to_response(product: Product) -> dict:
        images = product.images or []
        product_dto = ProductDTO(
            id=product.id,
            name=product.name,
            price=product.price.value,
            quantity=product.quantity,
            currency=product.price.currency,
            product_type_id=product.type.id,
            product_type_name=product.type.name,
            images=[
                {"url": image.url, "name": image.name} for image in images
            ]
        )

        return product_dto.to_dict()
