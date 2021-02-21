from dataclasses import dataclass
from typing import List


@dataclass
class ProductDTO:
    id: str = None
    name: str = None
    quantity: int = None
    price: float = None
    currency: str = None
    # Product_id or Product_type_name is required.
    # For product creation
    product_type_id: str = None
    product_type_name: str = None
    images: List[dict] = None

    def to_dict(self):
        keys = self.__annotations__
        return {key: getattr(self, key) for key in keys}
