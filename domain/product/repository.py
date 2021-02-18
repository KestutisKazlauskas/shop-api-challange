from abc import ABC, abstractmethod
from .entities import Product


class ProductRepository(ABC):
    @abstractmethod
    def find_all(self):
        raise NotImplementedError

    @abstractmethod
    def find_by(self, _id: int):
        raise NotImplementedError

    @abstractmethod
    def save(self, product: Product):
        raise NotImplementedError

    @abstractmethod
    def updated(self, product: Product):
        raise NotImplementedError
