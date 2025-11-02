import uuid
import ksuid
import ulid
import os, hashlib
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Protocol
import typer
from rich.console import Console
from rich.table import Table



#ERRORS
class RepositoryError(Exception):
    ...

#PORTS
class IdProvider(Protocol):
    name: str
    def generate_id(self) -> str:
        ...


class IdRepository(Protocol):
    def save(self, value: str, provider: str, timestamp: datetime) -> None:
        ...

    def list(self, limit: int | None = None) -> list[dict[str, str]]:
        ...

#ADAPTERS IDPROVIDER
class UUIDIdProvider:
    name = "uuid4"

    def generate_id(self) -> str:
        return str(uuid.uuid4())

class KSUIDIdProvider:
    name = "ksuid"

    def generate_id(self) -> str:
        return str(ksuid.ksuid())

class SHA256IdProvider:
    name = "sha256"
    def generate_id(self) -> str:
        return hashlib.sha256(os.urandom(32)).hexdigest()

class ULIDIdProvider:
    name = "ulid"
    def generate_id(self) -> str:
        return str(ulid.ulid())

#ADAPTERS IDREPOSITORY
class JsonlIdRepository:
    def __init__(self, path: Path | None = None):
        self.path = path or Path("providers.jsonl")
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


# APP TYPER
app = typer.Typer(help="Simple UUID generator that saves to a JSONL file.")


@app.command("gen")
def generate_ids(
    count: int = typer.Option(1, "--count", "-n", help="How many IDs to generate"),
    uuid4: bool = typer.Option(False, "--uuid4", help="Use UUIDv4 provider"),
    ksuid: bool = typer.Option(False, "--ksuid", help="Use KSUID provider"),
    sha256: bool = typer.Option(False, "--sha256", help="Use SHA256 provider"),
    ulid: bool = typer.Option(False, "--ulid", help="Use ULID provider"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable color output"),
):
    """Generate one or more IDs and save them to uuid.jsonl"""
    # pick provider based on the chosen flag
    if sum([uuid4, ksuid, sha256, ulid]) > 1:
        typer.echo("Error: please specify only one provider flag (--uuid4 / --ksuid / --sha256 / --ulid).")
        raise typer.Exit(code=1)

    if uuid4:
        provider = UUIDIdProvider()
    elif ksuid:
        provider = KSUIDIdProvider()
    elif sha256:
        provider = SHA256IdProvider()
    elif ulid:
        provider = ULIDIdProvider()
    else:
        provider = UUIDIdProvider() 
    
    repo = JsonlIdRepository()
    console = Console(no_color=no_color)

    for _ in range(count):
        new_id = provider.generate_id()
        ts = datetime.now(timezone.utc)
        repo.save(new_id, provider.name, ts)
        console.print(f"[dim]{ts.isoformat()}[/dim] [cyan]{new_id}[/cyan]")

    console.print(f"[green]Saved {count} record(s) to[/green] [bold]{repo.path}[/bold]")


@app.command("list")
def list_ids(
    limit: int = typer.Option(10, "--limit", "-l", help="How many last IDs to show"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable color output"),
):
    
    console = Console(no_color=no_color)

    """List last generated IDs from the JSONL file."""
    repo = JsonlIdRepository()
    console = Console(no_color=no_color)
    records = repo.list(limit)

    if not records:
        console.print("[yellow]No records found.[/yellow]")
        raise typer.Exit(code=0)

    table = Table(title=f"Last {min(limit, len(records))} IDs")
    table.add_column("timestamp", style="dim")
    table.add_column("provider", style="cyan")
    table.add_column("id", style="bold")

    for rec in records:
        table.add_row(rec.get("timestamp",""), rec.get("provider",""), rec.get("id",""))

    console.print(table)

if __name__ == "__main__":
    app()