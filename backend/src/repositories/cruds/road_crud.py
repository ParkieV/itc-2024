from collections.abc import Sequence
from pprint import pprint

from attrs import define
from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel

from typing_extensions import TypeVar


_MongoCollectionT = TypeVar("T", bound=AsyncIOMotorCollection)


@define(repr=False, kw_only=True)
class RoadCRUD:

    _out_schema = TypeVar("_out_schema", bound=BaseModel)
    collection: _MongoCollectionT

    async def add_object(self, document: BaseModel) -> None:
        try:
            await self.collection.insert_one(document.model_dump())
        except Exception as e:
            pprint(e)
            raise HTTPException(400, "Не получилось добавить объект")

    async def add_objects(self, documents: Sequence[BaseModel]) -> None:
        for document in documents:
            await self.add_object(document)

    async def get_geometries(self, *, out_schema: _out_schema) -> Sequence[_out_schema]:
        cursor = self.collection.find()
        docs = await cursor.to_list(1)
        lt_geos = []
        while docs:
            lt_geos.append(docs[0])
            docs = await cursor.to_list(1)
        return [out_schema.model_validate(doc) for doc in lt_geos]
