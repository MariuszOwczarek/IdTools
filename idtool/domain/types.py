
from enum import Enum

#==================
#ENUMS
#==================

class ProviderType(str, Enum):
    UUID4 = 'uuid4'
    KSUID = 'ksuid'
    SHA256 = 'sha256'
    ULID = 'ulid'

    def __str__(self) -> str:
        return self.value


class RepositoryType(str, Enum):
    JSONL ='jsonl'
    SQLITE = 'sqlite'

    def __str__(self) -> str:
        return self.value
