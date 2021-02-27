from domain.order.repository import OrderRepository
from domain.order.entities import Order
from . import RepositoryIdGeneratorMixin


class Repository(OrderRepository, RepositoryIdGeneratorMixin):
    def generate_id(self) -> str:
        return self.generate_id()

    def create_from(self, order: Order) -> None:
        pass

    def find_by(self, _id: str) -> Order:
        pass
