from datetime import datetime
from idtool.domain.entities import IdRecord
from idtool.domain.ports import IdRepository
from idtool.domain.errors import RepositoryError


def list_ids(repo: IdRepository, limit: int | None = None) -> list[IdRecord]:
    try:
        raw_records = repo.list(limit)
    except RepositoryError:
        # przekazujemy wyżej, CLI to obsłuży ładnym komunikatem
        raise

    records: list[IdRecord] = []

    for rec in raw_records:
        try:
            ts = datetime.fromisoformat(rec.get("timestamp", ""))
        except Exception:
            # jeśli timestamp nieczytelny – pomijamy ten wpis
            continue

        record = IdRecord(
            id=rec.get("id", ""),
            provider=rec.get("provider", ""),
            timestamp=ts,
        )
        records.append(record)

    # sortowanie: od najnowszego do najstarszego
    records.sort(key=lambda r: r.timestamp, reverse=True)

    # ograniczenie, jeśli repo nie zrobiło tego samo
    if limit:
        records = records[:limit]

    return records