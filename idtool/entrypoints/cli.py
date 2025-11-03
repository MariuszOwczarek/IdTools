import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime, timezone
from idtool.domain.types import ProviderType, RepositoryType
from idtool.application.services import make_provider, make_repository
from idtool.application.use_cases.generate_ids import generate_ids
from idtool.application.use_cases.list_ids import list_ids

app = typer.Typer(help="Simple UUID generator that saves to a JSONL file.")

@app.command("gen")
def generate_ids_cmd(
    count: int = typer.Option(1, "--count", "-n", help="How many IDs to generate"),
    provider: ProviderType = typer.Option(ProviderType.UUID4, "--provider"),
    repo: RepositoryType = typer.Option(RepositoryType.JSONL, "--repo"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable color output")
):
    provider = make_provider(provider)
    repo = make_repository(repo)
    console = Console(no_color=no_color)
    records = generate_ids(provider, repo, count)

    for rec in records:
        console.print(
            Panel.fit(
                f"Provider: [cyan]{rec.provider}[/cyan]\n"
                f"ID: [green]{rec.id}[/green]\n"
                f"Timestamp: [dim]{rec.timestamp.isoformat()}[/dim]",
                title="Generated ID",
                border_style="cyan",
                box=box.DOUBLE_EDGE,
            )
        )
    console.print(f"[green]Saved {len(records)} record(s) to[/green] [bold]{repo.path}[/bold]")

@app.command("list")
def list_ids_cmd(
    limit: int = typer.Option(10, "--limit", "-l", help="How many last IDs to show"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable color output"),
    repo: RepositoryType = typer.Option(RepositoryType.JSONL, "--repo")
):
    """List last generated IDs."""
    from idtool.application.use_cases.list_ids import list_ids

    console = Console(no_color=no_color)
    repo = make_repository(repo)
    records = list_ids(repo, limit)

    if not records:
        console.print(
            Panel.fit(
                "[yellow]No records found.[/yellow]\n"
                "Tip: generate some first with [bold]idtool gen[/bold].",
                title="Nothing to Show",
                border_style="yellow",
                box=box.ROUNDED,
            )
        )
        raise typer.Exit(code=0)

    table = Table(title=None, show_lines=False, box=box.SIMPLE_HEAVY)
    table.add_column("Timestamp", style="dim", no_wrap=True)
    table.add_column("Provider", style="cyan", no_wrap=True)
    table.add_column("ID", style="bold", overflow="fold")

    for rec in records:
        table.add_row(
            rec.timestamp.isoformat(),
            rec.provider,
            rec.id
        )

    console.print(
        Panel.fit(
            f"Showing [bold]{len(records)}[/bold] record(s)\n"
            f"Source: [bold]{getattr(repo, 'path', 'n/a')}[/bold]",
            title="ID List",
            border_style="cyan",
            box=box.DOUBLE_EDGE,
        )
    )

    console.print(table)


def main():
    app()

if __name__ == "__main__":
    main()