from abc import ABC, abstractmethod

from .entities import Order


class OrderRepository(ABC):
    @abstractmethod
    def generate_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_from(self, order: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by(self, _id: str) -> Order:
        raise NotImplementedError
