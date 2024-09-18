from collections.abc import Sequence
from pprint import pprint
from typing import TypeVar

from attrs import define
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel


_MongoCollectionT = TypeVar("_MongoCollectionT", bound=AsyncIOMotorCollection)

@define(repr=False, kw_only=True)
class EventCRUD:

    _out_schema = TypeVar("_out_schema", bound=BaseModel)
    collection: _MongoCollectionT

    async def add_event(self, event: BaseModel):
        try:
            await self.collection.insert_one(event.model_dump())
        except Exception as e:
            pprint(e)
            raise HTTPException(400, "Не получилось добавить объект")

    async def get_event_by_id(self, id: str, out_schema: _out_schema) -> _out_schema:
        try:
            event = await self.collection.find_one({'id': id})

            return out_schema.model_validate(event)
        except Exception as e:
            pprint(e)
            raise HTTPException(400, "Не получилось взять объект из БД")

    async def get_events(self, out_schema: _out_schema) -> Sequence[_out_schema]:
        try:
            events = self.collection.find()

            return [out_schema.model_validate(event) async for event in events]
        except Exception as e:
            pprint(e)
            raise HTTPException(400, "Не получилось взять объект из БД")
