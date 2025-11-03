from datetime import datetime, timezone
from idtool.domain.entities import IdRecord
from idtool.domain.ports import IdProvider, IdRepository
from idtool.domain.errors import RepositoryError

def generate_ids(provider: IdProvider, repo: IdRepository, count: int) -> list[IdRecord]:
    records = []
    for _ in range(count):
        new_id = provider.generate_id()
        ts = datetime.now(timezone.utc)
        try:
            repo.save(new_id, provider.name, ts)
        except RepositoryError:
            raise
        records.append(IdRecord(id=new_id, provider=provider.name, timestamp=ts))
    return records
