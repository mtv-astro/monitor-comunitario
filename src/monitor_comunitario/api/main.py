from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from monitor_comunitario.api.routes_admin import router as admin_router
from monitor_comunitario.api.routes_notifications import router as notifications_router
from monitor_comunitario.api.routes_outage_notices import router as outage_notices_router
from monitor_comunitario.api.routes_users import router as users_router
from monitor_comunitario.core.config import get_settings
from monitor_comunitario.db.init_db import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize local database structures when the API starts."""
    init_db()
    yield


app = FastAPI(
    title="Monitor Comunitário Celesc",
    description="Monitor público de desligamentos programados da Celesc com alertas por endereço.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(users_router)
app.include_router(outage_notices_router)
app.include_router(notifications_router)
app.include_router(admin_router)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    """Return a minimal healthcheck for local development and deploy probes."""
    return {
        "status": "ok",
        "environment": settings.app_env,
        "timezone": settings.app_timezone,
    }
