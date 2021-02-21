import json
from typing import List, Type
from dataclasses import dataclass
from .dtos import ProductDTO


class ProductRequestConverter:

    @staticmethod
    def _data_class_field_names(data_class_type: Type[dataclass]) -> List[str]:
        annotations = data_class_type.__annotations__
        return [key for key in annotations]

    def convert_create_request_to_dto(self, request_data: bytes) -> ProductDTO:
        try:
            data = json.loads(request_data)
        except ValueError:
            return ProductDTO()

        look_for_fields = self._data_class_field_names(ProductDTO)

        return ProductDTO(**{key: data.get(key) for key in look_for_fields})
