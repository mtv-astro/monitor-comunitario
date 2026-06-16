import typer
from rich.console import Console

from monitor_comunitario.core.config import get_settings

app = typer.Typer(help="Monitor Comunitário Celesc development CLI.")
console = Console()


@app.command()
def doctor() -> None:
    """Print basic environment information."""
    settings = get_settings()
    console.print("[bold green]Monitor Comunitário[/bold green]")
    console.print(f"Environment: {settings.app_env}")
    console.print(f"Timezone: {settings.app_timezone}")
    console.print(f"Celesc URL: {settings.celesc_outages_url}")
    console.print(f"Notification provider: {settings.notification_provider}")


@app.command()
def run_once() -> None:
    """Run one monitoring cycle.

    This command is intentionally a placeholder in the bootstrap package.
    The implementation will call the monitoring service after scraper,
    parser, database and notification providers are implemented.
    """
    console.print("[yellow]run-once ainda será implementado na fase de scraper/worker.[/yellow]")


@app.command()
def worker() -> None:
    """Start the scheduled worker.

    This command is intentionally a placeholder in the bootstrap package.
    """
    console.print("[yellow]worker ainda será implementado na fase de scheduler.[/yellow]")


if __name__ == "__main__":
    app()
