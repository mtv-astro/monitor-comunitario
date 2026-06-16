import asyncio
from pathlib import Path

import typer
from rich.console import Console

from monitor_comunitario.core.config import get_settings
from monitor_comunitario.scraper.celesc_page import fetch_celesc_page
from monitor_comunitario.scraper.parser import extract_relevant_outage_section

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
def scrape() -> None:
    """Capture the Celesc scheduled outage page with Playwright."""
    settings = get_settings()

    result = asyncio.run(
        fetch_celesc_page(
            url=settings.celesc_outages_url,
            snapshot_dir=settings.snapshot_dir,
            headless=settings.scraper_headless,
            timeout_ms=settings.scraper_timeout_ms,
        )
    )

    relevant_text = extract_relevant_outage_section(result.text)
    preview = relevant_text[:1_000] if relevant_text else result.text[:1_000]

    console.print("[bold green]Celesc scrape completed[/bold green]")
    console.print(f"URL: {result.url}")
    console.print(f"Fetched at: {result.fetched_at.isoformat()}")
    console.print(f"HTML snapshot: {result.html_snapshot_path}")
    console.print(f"Text snapshot: {result.text_snapshot_path}")
    console.print(f"HTML bytes: {len(result.html.encode('utf-8'))}")
    console.print(f"Text chars: {len(result.text)}")

    if preview:
        console.print("")
        console.print("[bold]Text preview[/bold]")
        console.print(preview)


@app.command()
def run_once() -> None:
    """Run one monitoring cycle.

    This command is intentionally a placeholder in the bootstrap package.
    The implementation will call the monitoring service after parser,
    database matching and notification providers are implemented.
    """
    console.print("[yellow]run-once ainda será implementado na fase de worker.[/yellow]")


@app.command()
def worker() -> None:
    """Start the scheduled worker.

    This command is intentionally a placeholder in the bootstrap package.
    """
    console.print("[yellow]worker ainda será implementado na fase de scheduler.[/yellow]")


@app.command()
def snapshots() -> None:
    """List saved scraper snapshots."""
    settings = get_settings()
    snapshot_dir = Path(settings.snapshot_dir)

    if not snapshot_dir.exists():
        console.print("[yellow]No snapshot directory found.[/yellow]")
        return

    for file in sorted(snapshot_dir.iterdir(), reverse=True):
        if file.is_file():
            console.print(str(file))


if __name__ == "__main__":
    app()
