from application.common.requests import RequestConverter
from .dtos import CartCreateDTO, ItemCreateDTO


class CartRequestConverter(RequestConverter):

    def _convert_item_to_dto(self, item_data: dict) -> ItemCreateDTO:
        item_data_keys = self.data_class_field_names(ItemCreateDTO)
        return ItemCreateDTO(**{key: item_data.get(key) for key in item_data_keys})

    def convert_create_request_to_dto(self, request_data: bytes) -> CartCreateDTO:
        data = self.convert_byte_to_dict(request_data)
        if not data:
            return CartCreateDTO()

        items = data.get("items", [])
        item_objs = []
        for item_request in items:
            item_objs.append(self._convert_item_to_dto(item_request))

        return CartCreateDTO(items=item_objs)

    def convert_create_item_request_to_dto(self, request_data: bytes) -> ItemCreateDTO:
        data = self.convert_byte_to_dict(request_data)
        if not data:
            return ItemCreateDTO("")

        return self._convert_item_to_dto(data)
