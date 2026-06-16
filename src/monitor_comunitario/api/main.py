from fastapi import FastAPI

from monitor_comunitario.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Monitor Comunitário Celesc",
    description="Monitor público de desligamentos programados da Celesc com alertas por endereço.",
    version="0.1.0",
)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    """Return a minimal healthcheck for local development and deploy probes."""
    return {
        "status": "ok",
        "environment": settings.app_env,
        "timezone": settings.app_timezone,
    }
