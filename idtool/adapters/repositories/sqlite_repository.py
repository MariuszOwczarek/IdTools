from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy import text, create_engine
from idtool.domain.errors import RepositoryError
from idtool.config.config import SQLITE_PATH

class SQLiteIdRepository:
    def __init__(self, path: Path | None = None):
        self.path = path or SQLITE_PATH
        self.engine = create_engine(f'sqlite:///{self.path}', future=True)
        self._ensure_schema()
    
    def _ensure_schema(self):
        create_sql="""
        CREATE TABLE IF NOT EXISTS ids(
            id TEXT PRIMARY KEY,
            provider TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );
        """

        with self.engine.begin() as conn:
            conn.execute(text(create_sql))
    
    def save(self, value: str, provider: str, timestamp: datetime) -> None:
        try:
            insert_sql = """
            INSERT INTO ids(id, provider,timestamp)
            VALUES(:id, :provider, :timestamp);
            """

            with self.engine.begin() as conn:
                conn.execute(text(insert_sql),
                {'id': value, 'provider':provider, 'timestamp':timestamp.isoformat()}
                )
        except OSError as e:
            raise RepositoryError from e

    def list(self, limit: int | None = None) -> list[dict[str, str]]:
        query_sql = "SELECT id, provider, timestamp FROM ids ORDER BY timestamp"
        params = {}

        if limit:
            query_sql += " LIMIT :limit"
            params["limit"] = limit

        with self.engine.begin() as conn:
            result = conn.execute(text(query_sql), params)
            return [dict(row._mapping) for row in result]