from dataclasses import dataclass
from typing import List

from application.common.dtos import BaseDTO


@dataclass
class ProductDTO(BaseDTO):
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
