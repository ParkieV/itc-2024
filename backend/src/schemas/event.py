from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from src.schemas.stage import StageResponse


class BaseEvent(BaseModel):
    id: str | None = Field(default=uuid4())
    title: str
    road_chunk_id: str
    user_id: str
    plan_start_date: datetime
    start_date: datetime
    plan_finish_date: datetime
    finish_date: datetime


class GetEventResponse(BaseEvent):
    stages: list[StageResponse]

class AddEventRequest(BaseModel):
    id: str | None = Field(default=uuid4())
    title: str
    road_chunk_id: str | None
    user_id: str | None
    plan_start_date: datetime
    start_date: datetime
    plan_finish_date: datetime
    finish_date: datetime