from typing import Protocol
from datetime import datetime

#==================
#PORTS
#==================

class IdProvider(Protocol):
    name: str
    def generate_id(self) -> str:
        ...


class IdRepository(Protocol):
    def save(self, value: str, provider: str, timestamp: datetime) -> None:
        ...

    def list(self, limit: int | None = None) -> list[dict[str, str]]:
        ...
