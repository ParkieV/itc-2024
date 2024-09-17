from typing import Generic, TypeVar

import motor
from attrs import define
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.shared.config import db_config

T = TypeVar("T")


@define(repr=False, kw_only=True)
class MongoDatabaseContext(Generic[T]):
    """Класс для работы с базой данных MongoDB"""

    #: Клиент базы данных
    client: AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(
        db_config.db_url
    )
    print(db_config.db_url)

    #: База данных
    db: AsyncIOMotorDatabase = client[db_config.database_name]

    #: CRUD для взаимодействия с таблицей
    crud: T = None
