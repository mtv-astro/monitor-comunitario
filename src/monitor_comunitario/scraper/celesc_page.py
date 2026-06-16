from pathlib import Path

from playwright.async_api import async_playwright


async def fetch_celesc_page_html(
    url: str,
    snapshot_dir: str,
    headless: bool = True,
    timeout_ms: int = 30_000,
) -> str:
    """Fetch the Celesc outage page and persist a raw HTML snapshot.

    The parser will be developed separately. Keeping fetch and parse apart
    makes it easier to debug layout changes on the Celesc website.
    """
    snapshot_path = Path(snapshot_dir)
    snapshot_path.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()
        page.set_default_timeout(timeout_ms)

        await page.goto(url, wait_until="networkidle")
        html = await page.content()

        (snapshot_path / "latest-celesc-outages.html").write_text(html, encoding="utf-8")

        await browser.close()

    return html
