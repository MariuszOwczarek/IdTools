from idtool.adapters.id_providers.uuid4_provider import UUIDIdProvider
from idtool.adapters.id_providers.ksuid_provider import KSUIDIdProvider
from idtool.adapters.id_providers.sha256_provider import SHA256IdProvider
from idtool.adapters.id_providers.ulid_provider import ULIDIdProvider
from idtool.adapters.repositories.jsonl_repository import JsonlIdRepository
from idtool.adapters.repositories.sqlite_repository import SQLiteIdRepository
from idtool.domain.types import ProviderType, RepositoryType

def make_provider(provider_type: ProviderType):
    provider_map = {
    ProviderType.UUID4: UUIDIdProvider,
    ProviderType.KSUID: KSUIDIdProvider,
    ProviderType.SHA256: SHA256IdProvider,
    ProviderType.ULID: ULIDIdProvider}
    return provider_map[provider_type]()

def make_repository(repo_type: RepositoryType):
    repo_map = {
    RepositoryType.JSONL: JsonlIdRepository,
    RepositoryType.SQLITE: SQLiteIdRepository}
    return repo_map[repo_type]()