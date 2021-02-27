from uuid import uuid4


class RepositoryIdGenerator:
    @staticmethod
    def generate_id() -> str:
        return str(uuid4())
