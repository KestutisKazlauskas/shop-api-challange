from abc import ABC, abstractmethod
from typing import List

from .entities import Product, ProductType


class ProductRepository(ABC):
    @abstractmethod
    def generate_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Product]:
        raise NotImplementedError

    @abstractmethod
    def find_by(self, _id: str) -> Product:
        raise NotImplementedError

    @abstractmethod
    def find_product_type_by(self, _id: str) -> ProductType:
        raise NotImplementedError

    @abstractmethod
    def create_from(self, product: Product) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_by(self, product_id: str) -> None:
        raise NotImplementedError

