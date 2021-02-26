from typing import List
from application.common.dtos import BaseDTO
from dataclasses import dataclass


@dataclass
class ItemCreateDTO(BaseDTO):
    product_id: str
    quantity: int = 0


@dataclass
class CartCreateDTO(BaseDTO):
    items: List[ItemCreateDTO] = None


@dataclass
class CartItemDTO(BaseDTO):
    id: str = ""
    product_id: str = ""
    name: str = ""
    quantity: int = 0
    price: float = 0.0


@dataclass
class CartDTO(BaseDTO):
    id: str = ""
    currency: str = ""
    discount: float = 0.0
    total: float = 0.0
    items: List[CartItemDTO] = None
