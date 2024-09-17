from collections.abc import Sequence
from pprint import pprint

from attrs import define
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
            print('b')
            await self.collection.insert_one(document.model_dump())
            print('c')
        except Exception as e:
            pprint(e)
            raise HTTPException(400, "Не получилось добавить объект")

    async def add_objects(self, documents: Sequence[BaseModel]) -> None:
        for document in documents:
            await self.add_object(document)
