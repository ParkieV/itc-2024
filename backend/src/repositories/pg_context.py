from typing import TypeVar, Generator

from attrs import define
from sqlalchemy import Engine
from mypyc.ir.ops import Generic
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from src.repositories.cruds import BaseCRUD
from src.shared.config import db_config

T = TypeVar("T", bound=BaseCRUD)


@define(repr=False, kw_only=True)
class PostgresDatabaseContext(Generic[T]):
    """Класс для работы с базой данных PostgreSQL"""

    # Движок базы данных
    engine: Engine | AsyncEngine = create_async_engine(db_config.db_url)

    #: CRUD для взаимодействия с таблицей
    crud: T = BaseCRUD()

    # Сессия соединения с базой данных
    _session: Session | AsyncSession = async_sessionmaker(engine)

    @classmethod
    def get_session(cls) -> Generator[Session | AsyncSession, None, None]:
        """Получить сессию с базой данных"""
        with cls._session() as session:
            try:
                yield session
            except BaseException:
                session.rollback()
                raise
            else:
                session.commit()
