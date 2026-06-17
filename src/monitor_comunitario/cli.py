from pathlib import Path
from zoneinfo import ZoneInfo

from alembic import command as alembic_command  # type: ignore
from alembic.config import Config as AlembicConfig  # type: ignore
from rich.console import Console
import typer

from monitor_comunitario.core.config import get_settings
from monitor_comunitario.db.init_db import init_db
from monitor_comunitario.db.management import export_data, import_data, seed_demo
from monitor_comunitario.db.session import SessionLocal
from monitor_comunitario.scraper.celesc_page import (
    fetch_celesc_municipality_pages,
    fetch_celesc_page,
)
from monitor_comunitario.scraper.parser import extract_relevant_outage_section
from monitor_comunitario.services.matching import run_matching_cycle
from monitor_comunitario.services.monitoring import run_monitoring_cycle

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
    import asyncio

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


@app.command("scrape-municipalities")
def scrape_municipalities(
    limit: int = typer.Option(
        0,
        "--limit",
        help="Maximum number of municipalities to capture. Use 0 for all.",
    ),
) -> None:
    """Select active municipalities and capture one snapshot per option."""
    import asyncio

    settings = get_settings()
    max_options = limit if limit > 0 else None

    result = asyncio.run(
        fetch_celesc_municipality_pages(
            url=settings.celesc_outages_url,
            snapshot_dir=settings.snapshot_dir,
            headless=settings.scraper_headless,
            timeout_ms=settings.scraper_timeout_ms,
            max_options=max_options,
        )
    )

    console.print("[bold green]Celesc municipality scrape completed[/bold green]")
    console.print(f"URL: {result.url}")
    console.print(f"Fetched at: {result.fetched_at.isoformat()}")
    console.print(f"Active options found: {len(result.options)}")
    console.print(f"Municipalities captured: {len(result.captures)}")
    console.print(f"Index: {result.index_path}")

    if result.options:
        console.print("")
        console.print("[bold]Options preview[/bold]")

        for option in result.options[:10]:
            console.print(f"- {option.label} ({option.value})")


@app.command()
def run_once(
    limit: int = typer.Option(
        0,
        "--limit",
        help="Maximum number of municipalities to process. Use 0 for all.",
    ),
) -> None:
    """Run one monitoring cycle, persist notices and create notifications."""
    init_db()
    max_options = limit if limit > 0 else None
    result = run_monitoring_cycle(limit=max_options)
    run = result.run

    console.print("[bold green]Monitoring run completed[/bold green]")
    console.print(f"Run ID: {run.id}")
    console.print(f"Status: {run.status}")
    console.print(f"Municipality options found: {run.municipalities_found}")
    console.print(f"Municipalities captured: {run.municipalities_captured}")
    console.print(f"Parsed notices: {run.notices_found}")
    console.print(f"Persisted notices: {run.notices_persisted}")
    console.print(f"New notices: {run.notices_created}")
    console.print(f"Users checked: {run.users_checked}")
    console.print(f"Matches created: {run.matches_created}")
    console.print(f"Notifications created: {run.notifications_created}")
    console.print(f"Index: {run.raw_snapshot_path}")

    if run.error_message:
        console.print(f"[red]Error: {run.error_message}[/red]")


@app.command("match-notices")
def match_notices() -> None:
    """Match existing users against persisted notices and create notifications."""
    init_db()

    with SessionLocal() as session:
        summary = run_matching_cycle(session)

    console.print("[bold green]Matching completed[/bold green]")
    console.print(f"Users checked: {summary.users_checked}")
    console.print(f"Notices checked: {summary.notices_checked}")
    console.print(f"Matches created: {summary.matches_created}")
    console.print(f"Notifications created: {summary.notifications_created}")


@app.command()
def worker() -> None:
    """Start the scheduled monitoring worker."""
    from apscheduler.schedulers.blocking import (
        BlockingScheduler,
    )  # type: ignore[import-untyped]
    from apscheduler.triggers.cron import CronTrigger  # type: ignore[import-untyped]

    settings = get_settings()
    timezone = ZoneInfo(settings.app_timezone)

    scheduler = BlockingScheduler(timezone=timezone)
    trigger = CronTrigger(
        hour=settings.scheduler_hour,
        minute=settings.scheduler_minute,
        timezone=timezone,
    )

    scheduler.add_job(
        lambda: run_monitoring_cycle(limit=None),
        trigger=trigger,
        id="daily-celesc-monitor",
        replace_existing=True,
    )

    console.print("[bold green]Worker started[/bold green]")
    time_str = f"{settings.scheduler_hour:02d}:{settings.scheduler_minute:02d}"
    console.print(f"Scheduled daily at {time_str} {settings.app_timezone}")

    scheduler.start()


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


# Database management commands


@app.command("db-upgrade")
def cli_db_upgrade(
    revision: str = typer.Argument("head"),
) -> None:
    """Apply Alembic migrations up to the specified revision (default: head)."""
    cfg = AlembicConfig("alembic.ini")
    alembic_command.upgrade(cfg, revision)
    console.print(f"[green]Migrations applied up to {revision}[/green]")


@app.command("db-downgrade")
def cli_db_downgrade(
    revision: str = typer.Argument("base"),
) -> None:
    """Downgrade Alembic migrations down to the specified revision (default: base)."""
    cfg = AlembicConfig("alembic.ini")
    alembic_command.downgrade(cfg, revision)
    console.print(f"[green]Migrations downgraded to {revision}[/green]")


@app.command("db-current")
def cli_db_current() -> None:
    """Show the current Alembic revision."""
    cfg = AlembicConfig("alembic.ini")
    alembic_command.current(cfg)


@app.command("db-history")
def cli_db_history() -> None:
    """Show the Alembic revision history."""
    cfg = AlembicConfig("alembic.ini")
    alembic_command.history(cfg)


@app.command("db-revision")
def cli_db_revision(
    message: str = typer.Option(
        ..., "--message", "-m", help="Migration message"
    ),
    autogenerate: bool = typer.Option(
        False, "--autogenerate", help="Autogenerate migration from models"
    ),
) -> None:
    """Create a new Alembic migration."""
    cfg = AlembicConfig("alembic.ini")
    alembic_command.revision(cfg, message=message, autogenerate=autogenerate)
    console.print(f"[green]New migration created: {message}[/green]")


@app.command("db-stamp")
def cli_db_stamp(
    revision: str = typer.Argument("head"),
) -> None:
    """Mark the database with the given revision without running migrations."""
    cfg = AlembicConfig("alembic.ini")
    alembic_command.stamp(cfg, revision)
    console.print(f"[green]Database stamped at {revision}[/green]")


@app.command("db-export")
def cli_db_export(
    output: Path = typer.Option(..., "--output", "-o", help="Output JSON file"),
) -> None:
    """Export database tables to a JSON file."""
    export_data(str(output))
    console.print(f"[green]Data exported to {output}[/green]")


@app.command("db-import")
def cli_db_import(
    input: Path = typer.Option(..., "--input", "-i", help="Input JSON file"),
) -> None:
    """Import data from a JSON file into the database."""
    import_data(str(input))
    console.print(f"[green]Data imported from {input}[/green]")


@app.command("db-seed-demo")
def cli_db_seed_demo() -> None:
    """Seed the database with fake data for demonstrations."""
    # Ensure tables exist only for SQLite development
    settings = get_settings()
    if settings.database_url.startswith("sqlite"):
        init_db()
    seed_demo()
    console.print("[green]Demo data seeded successfully[/green]")


if __name__ == "__main__":
    app()
