import json
from typing import List, Type
from dataclasses import dataclass


class RequestConverter:

    @staticmethod
    def data_class_field_names(data_class_type: Type[dataclass]) -> List[str]:
        annotations = data_class_type.__annotations__
        return [key for key in annotations]

    @staticmethod
    def convert_byte_to_dict(data: bytes) -> dict:
        try:
            data = json.loads(data)
        except ValueError:
            return {}

        return data
