from domain.order.repository import OrderRepository as Repository
from domain.order.entities import Order
from . import RepositoryIdGenerator


class OrderRepository(Repository):
    def __init__(self, uuid_generator=None):
        self.uuid_generator = uuid_generator or RepositoryIdGenerator()

    def generate_id(self) -> str:
        return self.uuid_generator.generate_id()

    def create_from(self, order: Order) -> None:
        pass

    def find_by(self, _id: str) -> Order:
        pass
