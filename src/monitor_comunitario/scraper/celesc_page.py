from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import Page, async_playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from monitor_comunitario.scraper.parser import clean_page_text


@dataclass(frozen=True)
class CelescScrapeResult:
    """Result produced by a Celesc outage page capture."""

    url: str
    fetched_at: datetime
    html: str
    text: str
    html_snapshot_path: Path
    text_snapshot_path: Path


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(UTC)


def build_snapshot_stem(fetched_at: datetime) -> str:
    """Build a filesystem-safe snapshot name."""
    return f"celesc-outages-{fetched_at.strftime('%Y%m%dT%H%M%SZ')}"


async def accept_cookie_banner(page: Page) -> None:
    """Try to accept Celesc's cookie banner without failing the scrape.

    The banner can appear more than once in the rendered page. This function
    is intentionally defensive: a failed click should not break the capture.
    """
    candidates = [
        page.get_by_role("button", name="Estou ciente"),
        page.get_by_text("Estou ciente", exact=True),
    ]

    for candidate in candidates:
        try:
            if await candidate.count() > 0:
                await candidate.first.click(timeout=2_000)
                return
        except PlaywrightTimeoutError:
            continue


async def fetch_celesc_page(
    url: str,
    snapshot_dir: str,
    headless: bool = True,
    timeout_ms: int = 30_000,
) -> CelescScrapeResult:
    """Fetch the Celesc outage page and persist HTML/TXT snapshots.

    The scraper captures both raw HTML and visible body text. The text snapshot
    gives us a stable debugging artifact even when the page layout changes.
    """
    fetched_at = utc_now()
    snapshot_path = Path(snapshot_dir)
    snapshot_path.mkdir(parents=True, exist_ok=True)

    stem = build_snapshot_stem(fetched_at)

    html_snapshot_path = snapshot_path / f"{stem}.html"
    text_snapshot_path = snapshot_path / f"{stem}.txt"

    latest_html_path = snapshot_path / "latest-celesc-outages.html"
    latest_text_path = snapshot_path / "latest-celesc-outages.txt"

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=headless)
        page = await browser.new_page()
        page.set_default_timeout(timeout_ms)

        await page.goto(url, wait_until="networkidle")
        await accept_cookie_banner(page)
        await page.wait_for_load_state("networkidle")

        html = await page.content()
        raw_text = await page.locator("body").inner_text(timeout=timeout_ms)
        text = clean_page_text(raw_text)

        await browser.close()

    html_snapshot_path.write_text(html, encoding="utf-8")
    text_snapshot_path.write_text(text, encoding="utf-8")

    latest_html_path.write_text(html, encoding="utf-8")
    latest_text_path.write_text(text, encoding="utf-8")

    return CelescScrapeResult(
        url=url,
        fetched_at=fetched_at,
        html=html,
        text=text,
        html_snapshot_path=html_snapshot_path,
        text_snapshot_path=text_snapshot_path,
    )


async def fetch_celesc_page_html(
    url: str,
    snapshot_dir: str,
    headless: bool = True,
    timeout_ms: int = 30_000,
) -> str:
    """Backward-compatible helper that returns only HTML."""
    result = await fetch_celesc_page(
        url=url,
        snapshot_dir=snapshot_dir,
        headless=headless,
        timeout_ms=timeout_ms,
    )
    return result.html
