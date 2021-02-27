from typing import List
from application.common.dtos import BaseDTO
from dataclasses import dataclass


@dataclass
class OrderItemDTO(BaseDTO):
    name: str
    quantity: int
    price: float


@dataclass
class OrderCreateDTO(BaseDTO):
    # Cart id is required for creating order
    cart_id: str = None
    name: str = None
    surname: str = None
    street: str = None
    city: str = None
    country: str = None
    postal_code: str = None


# Can not get field from OrderCreateDTO
# Because the field is not passed other the inheritance
@dataclass
class OrderDTO(BaseDTO):
    # Only for returning items after order is created
    # This field do not used in order create request
    id: str = None
    items: List[OrderItemDTO] = None
    total: float = None
    currency: str = None
    discount: float = None
    status: str = None
    cart_id: str = None
    name: str = None
    surname: str = None
    street: str = None
    city: str = None
    country: str = None
    postal_code: str = None
