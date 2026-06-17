from pydantic import BaseModel

from monitor_comunitario.schemas.monitoring_runs import MonitoringRunRead


class ReadinessRead(BaseModel):
    """Public readiness response."""

    status: str
    database: str


class DatabaseDiagnostics(BaseModel):
    """Database diagnostic status."""

    status: str


class SchedulerDiagnostics(BaseModel):
    """Scheduler configuration exposed to the admin diagnostics endpoint."""

    enabled: bool
    hour: int
    minute: int


class NotificationDiagnostics(BaseModel):
    """Notification configuration exposed to the admin diagnostics endpoint."""

    provider: str
    evolution_enabled: bool


class DiagnosticsRead(BaseModel):
    """Admin operational diagnostics response."""

    status: str
    environment: str
    timezone: str
    database: DatabaseDiagnostics
    scheduler: SchedulerDiagnostics
    notifications: NotificationDiagnostics
    latest_run: MonitoringRunRead | None = None
