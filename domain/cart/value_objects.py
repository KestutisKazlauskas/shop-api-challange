from dataclasses import dataclass
from domain.common.value_objects import Price


@dataclass(frozen=True)
class Discount(Price):
    name: str = None

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value and self.currency == other.currency
