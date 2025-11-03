import uuid

class UUIDIdProvider:
    name = "uuid4"

    def generate_id(self) -> str:
        return str(uuid.uuid4())