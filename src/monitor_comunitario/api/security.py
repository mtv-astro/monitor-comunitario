from secrets import compare_digest
from typing import Annotated

from fastapi import Header, HTTPException, status

from monitor_comunitario.core.config import get_settings


def require_admin_api_key(
    x_admin_api_key: Annotated[str | None, Header(alias="X-Admin-API-Key")] = None,
) -> None:
    """Require a configured admin API key for protected admin endpoints."""
    expected_api_key = get_settings().admin_api_key.strip()

    if not expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin API key is not configured.",
        )

    provided_api_key = (x_admin_api_key or "").strip()

    if not provided_api_key or not compare_digest(provided_api_key, expected_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing admin API key.",
        )
