from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OutageNoticeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    source_url: str
    municipality: str
    neighborhood: str
    street: str
    description: str
    raw_text: str
    content_hash: str
    created_at: datetime
