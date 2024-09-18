from collections.abc import Sequence
from pprint import pprint
from typing import TypeVar

from attrs import define
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel




_MongoCollectionT = TypeVar("_MongoCollectionT", bound=AsyncIOMotorCollection)

@define(repr=False, kw_only=True)
class RoadCRUD:

    _out_schema = TypeVar("_out_schema", bound=BaseModel)
    collection: _MongoCollectionT

    async def add_road(self, road: BaseModel) -> None:
        try:
            await self.collection.insert_one(road.model_dump())
        except Exception as e:
            pprint(e)
            raise HTTPException(400, "Не получилось добавить объект")

    async def add_roads(self, documents: Sequence[BaseModel]) -> None:
        for document in documents:
            await self.add_road(document)

    async def get_road_geometries(self, *, out_schema: _out_schema) -> Sequence[_out_schema]:
        cursor = self.collection.find()
        docs = await cursor.to_list(1)
        lt_geos = []
        while docs:
            lt_geos.append(docs[0])
            docs = await cursor.to_list(1)
        return [out_schema.model_validate(doc) for doc in lt_geos]

    async def get_road_by_id(self, id: str, out_schema: _out_schema) -> _out_schema:
        try:
            doc = await self.collection.find_one({'id': id})

            return out_schema.model_validate(doc)
        except Exception as e:
            pprint(e)
            raise HTTPException(400, "Не получилось взять объект из БД")

