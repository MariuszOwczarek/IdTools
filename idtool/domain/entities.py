from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class IdRecord:
    id: str
    provider: str
    timestamp: datetime
    