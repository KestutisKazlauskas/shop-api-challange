from dataclasses import dataclass
from domain.product.exceptions import InvalidProductException


@dataclass(frozen=True)
class Image:
    name: str = None
    url: str = None

    def __post_init__(self):
        if not self.name:
            raise InvalidProductException("Product image name is required.")

        if not self.url:
            raise InvalidProductException("Product image url is required.")

