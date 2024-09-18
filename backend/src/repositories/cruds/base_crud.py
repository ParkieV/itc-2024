from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Generic

from attrs import define
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from typing_extensions import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, DeclarativeBase


class AbstractCRUD(ABC):

    #: Модель таблицы базы данных
    _model: DeclarativeBase

    @abstractmethod
    def get_object(self, object_info, out_schema, session):
        """
        Получение информации об объекте из базы данных

        :param object_info: Информация для поиска объекта
        :param session: Сессия БД
        """

    @abstractmethod
    def get_objects(self, objects_info: Sequence, session): ...

    @abstractmethod
    def add_object(self, object_info, session): ...

    @abstractmethod
    def add_objects(self, objects_info: Sequence, session):
        """
        До
        :param objects_info:
        :param session:
        :return:
        """

    @abstractmethod
    def update_object(self, object_info, session): ...

    @abstractmethod
    def update_objects(self, objects_info: Sequence, session): ...

    @abstractmethod
    def remove_object(self, object_info, session): ...

    @abstractmethod
    def remove_objects(self, objects_info: Sequence, session): ...


# Тип для SQLAlchemy моделей
DBModelType = TypeVar("DBModelType", bound=DeclarativeBase)


@define(repr=False)
class BaseCRUD(AbstractCRUD, Generic[DBModelType]):
    """Базовый класс-реализация CRUD операций"""

    _model = type(DBModelType)
    _out_schema = TypeVar("_out_schema", bound=BaseModel)

    async def get_object(
        self,
        object_info: BaseModel,
        *,
        out_schema: _out_schema,
        session: AsyncSession | Session,
    ) -> _out_schema:
        """
        Получение информации об объекте из базы данных

        :param object_info: Информация для поиска объекта
        :param out_schema: Тип возвращаемой Pydantic модели
        :param session: Сессия БД

        :return: Искомый объект

        :raise ValueError: Объект не был найден
        """
        # Перевод из Alembic модели в SQLAlchemy модель
        object_model: DBModelType = self._model(**object_info.model_dump())

        query = select(object_model)

        if (
            result_object := (await session.execute(query)).scalar_one_or_none()
        ) is None:
            raise ValueError("Объект не найден")

        return out_schema.model_validate(result_object)

    async def add_object(
        self, object_model: BaseModel, session: AsyncSession | Session
    ) -> None:
        """
        Добавление объекта в базу данных

        :param object_model: Модель объекта
        :param session: сессия БД
        """
        # Перевод из Alembic модели в SQLAlchemy модель
        object_model: DBModelType = self._model(**object_model.model_dump())

        query = insert(object_model)

        await session.execute(query)

    # async def add_objects(self, objects_info: Sequence[BaseModel], session: AsyncSession | Session) -> list[DBModelType]:
    #
    #     object_model_list: list[DBModelType] = [self._model(**object_info.model_dump()) for object_info in objects_info]

    async def remove_object(
        self, object_info: BaseModel, session: AsyncSession | Session
    ) -> None:
        """"""
