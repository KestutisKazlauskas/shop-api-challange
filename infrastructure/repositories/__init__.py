from uuid import uuid4


class RepositoryIdGeneratorMixin:
    @staticmethod
    def generate_id() -> str:
        return str(uuid4())
