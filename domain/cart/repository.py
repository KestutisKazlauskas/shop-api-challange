from abc import ABC, abstractmethod

from .entities import Cart


class CartRepository(ABC):
    @abstractmethod
    def generate_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def find_by(self, _id: str) -> Cart:
        raise NotImplementedError

    @abstractmethod
    def delete_by(self, _id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_from(self, cart: Cart) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_from(self, cart: Cart) -> None:
        raise NotImplementedError

