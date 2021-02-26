from domain.cart.repository import CartRepository
from domain.cart.entities import Cart
from . import RepositoryIdGeneratorMixin


class Repository(CartRepository, RepositoryIdGeneratorMixin):
    def generate_id(self) -> str:
        return self.generate_id()

    def find_by(self, _id: str) -> Cart:
        pass

    def delete_by(self, _id: str) -> None:
        pass

    def create_from(self, cart: Cart) -> None:
        pass

    def update_from(self, cart: Cart) -> None:
        pass
