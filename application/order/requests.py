from application.common.requests import RequestConverter
from .dtos import OrderCreateDTO


class OrderRequestConverter(RequestConverter):

    def convert_create_request_to_dto(self, request_data: bytes) -> OrderCreateDTO:
        data = self.convert_byte_to_dict(request_data)
        if not data:
            return OrderCreateDTO()

        look_for_fields = self.data_class_field_names(OrderCreateDTO)
        return OrderCreateDTO(**{key: data.get(key) for key in look_for_fields})
