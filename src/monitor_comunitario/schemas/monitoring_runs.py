from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MonitoringRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    started_at: datetime
    finished_at: datetime | None
    status: str
    municipalities_found: int
    municipalities_captured: int
    notices_found: int
    notices_persisted: int
    notices_created: int
    users_checked: int
    matches_created: int
    notifications_created: int
    error_message: str
    raw_snapshot_path: str
