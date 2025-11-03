from idtool.domain.errors import RepositoryError
from datetime import datetime
import json
from pathlib import Path
from idtool.config.config import JSONL_PATH


class JsonlIdRepository:
    def __init__(self, path: Path | None = None):
        self.path = path or JSONL_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, value: str, provider: str, timestamp: datetime) -> None:
        try:
            record = {
                "timestamp": timestamp.isoformat(),
                "id": value,
                "provider": provider,
            }
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except OSError as e:
            raise RepositoryError from e
        

    def list(self, limit: int | None = None) -> list[dict[str, str]]:
        """Read entries from the JSONL file."""
        if not self.path.exists():
            return []
        records = []
        with self.path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    records.append(record)
                except json.JSONDecodeError:
                    continue  # skip invalid lines gracefully
        if limit:
            return records[-limit:]
        return records
