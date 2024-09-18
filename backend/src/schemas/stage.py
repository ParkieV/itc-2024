from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class StageResponse(BaseModel):
    id: str | None = Field(default=uuid4())
    title: str
    description: str
    event_id: str
    plan_start_date: datetime
    start_date: datetime
    plan_finish_date: datetime
    finish_date: datetime
