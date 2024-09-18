from collections.abc import Sequence
from pprint import pprint
from typing import TypeVar

from attrs import define
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel

from src.schemas.stage import StageResponse

_MongoCollectionT = TypeVar("_MongoCollectionT", bound=AsyncIOMotorCollection)

@define(repr=False, kw_only=True)
class StageCRUD:

    _out_schema = TypeVar("_out_schema", bound=BaseModel)
    collection: _MongoCollectionT

    async def add_stage(self, stage: StageResponse):
        try:
            await self.collection.insert_one(stage.model_dump())
        except Exception as e:
            pprint(e)
            raise HTTPException(400, "Не получилось добавить объект")

    async def get_stages_by_event_id(self, event_id: str, out_schema: _out_schema) -> Sequence[_out_schema]:
        try:
            stages = self.collection.find({'event_id': event_id})

            return [out_schema.model_validate(stage) async for stage in stages]
        except Exception as e:
            pprint(e)
            raise HTTPException(400, "Не получилось взять объект из БД")
