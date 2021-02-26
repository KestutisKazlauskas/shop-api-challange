from application.common.requests import RequestConverter
from .dtos import ProductDTO


class ProductRequestConverter(RequestConverter):
    def convert_create_request_to_dto(self, request_data: bytes) -> ProductDTO:
        data = self.convert_byte_to_dict(request_data)
        if not data:
            return ProductDTO()

        look_for_fields = self.data_class_field_names(ProductDTO)
        return ProductDTO(**{key: data.get(key) for key in look_for_fields})
