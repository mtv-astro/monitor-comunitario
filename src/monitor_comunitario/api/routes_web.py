from pathlib import Path
from typing import Any

from fastapi import APIRouter
from fastapi.responses import FileResponse

from monitor_comunitario.core.config import get_settings

STATIC_DIR = Path(__file__).resolve().parents[1] / "web" / "static"

router = APIRouter(tags=["web"])


@router.get("/", include_in_schema=False)
def home() -> FileResponse:
    """Serve the public user registration page."""
    return FileResponse(STATIC_DIR / "index.html")


@router.get("/admin", include_in_schema=False)
def admin_dashboard() -> FileResponse:
    """Serve the internal admin diagnostics dashboard page."""
    return FileResponse(STATIC_DIR / "admin.html")


@router.get("/admin/", include_in_schema=False)
def admin_dashboard_with_trailing_slash() -> FileResponse:
    """Serve the internal admin diagnostics dashboard page."""
    return FileResponse(STATIC_DIR / "admin.html")


@router.get("/privacidade", include_in_schema=False)
def privacy_policy() -> FileResponse:
    """Serve the privacy policy page."""
    return FileResponse(STATIC_DIR / "privacy.html")


@router.get("/termos", include_in_schema=False)
def terms_of_use() -> FileResponse:
    """Serve the terms of use page."""
    return FileResponse(STATIC_DIR / "terms.html")


@router.get("/cookies", include_in_schema=False)
def cookie_policy() -> FileResponse:
    """Serve the cookie and local storage policy page."""
    return FileResponse(STATIC_DIR / "cookies.html")


@router.get("/public/config", include_in_schema=False)
def public_config() -> dict[str, Any]:
    """Return non-secret browser configuration flags."""
    settings = get_settings()

    return {
        "ads_enabled": settings.ads_enabled,
        "ads_provider": settings.ads_provider,
        "adsense_client_id": settings.adsense_client_id if settings.ads_enabled else "",
        "adsense_default_slot": settings.adsense_default_slot if settings.ads_enabled else "",
        "analytics_enabled": settings.analytics_enabled,
        "analytics_provider": settings.analytics_provider,
        "google_analytics_id": (
            settings.google_analytics_id if settings.analytics_enabled else ""
        ),
        "consent_required": settings.consent_required,
        "consent_version": settings.consent_version,
    }
