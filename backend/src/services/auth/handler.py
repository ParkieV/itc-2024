from abc import ABC, abstractmethod
from datetime import time, datetime
from os import access
from typing import Generic, TypeVar, Any

from attrs import define
from fastapi import HTTPException, status
from pydantic import BaseModel

from src.mixins.token_mixin import AbstractTokenMixin, JWTTokenMixin
from src.repositories.cruds import UserCRUD
from src.repositories.pg_context import PostgresDatabaseContext
from src.schemas.auth import TokenBaseInfo
from src.schemas.user import UserBaseModel
from src.shared.config import server_config, auth_config


@define(repr=False, kw_only=True)
class AbstractAuthHandler(ABC):
    """Класс-обработчик, управляющий доступом и правами в системе"""

    #: Контекст базы данных
    database_context: Any

    #: Токенизатор
    tokenizator: AbstractTokenMixin

    @abstractmethod
    def check_user(self, user) -> bool:
        """
        Проверяет, есть ли пользователь в системе

        :param user: Информация о пользователе

        :return: Есть ли пользователь в системе
        """


    @abstractmethod
    def register_user(self, user) -> None:
        """
        Добавляет пользователя в систему

        :param user: Информация о пользователе
        """

    @abstractmethod
    def logout_user(self, user) -> None:
        """
        Удаляет пользователя из системы

        :param user: Информация о пользователе
        """

T = TypeVar('T', bound=BaseModel)

@define(repr=False, kw_only=True)
class OAuth2AuthHandler(AbstractAuthHandler, Generic[T]):
    """Обработчик системы получения доступа в систему с помощью протокола OAuth 2.0"""

    #: Контекст базы данных
    _database_context: PostgresDatabaseContext[UserCRUD] = PostgresDatabaseContext(crud=UserCRUD())

    #: Токенизатор
    tokenizator = JWTTokenMixin()

    def check_user(self, user: T) -> bool:
        """
        Проверяет, есть ли пользователь в системе

        :param user: Информация о пользователе

        :return: Есть ли пользователь в системе
        """
        try:
            self._database_context.crud.get_object(user,
                                                   out_schema=UserBaseModel,
                                                   session=next(self._database_context.get_session()))
        except ValueError:
            return False
        else:
            return True

    def register_user(self, user: T) -> None:
        """
        Добавляет пользователя в систему

        :param user: Информация о пользователе
        """
        if self.check_user(user):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Пользователь уже создан')

        self._database_context.crud.add_object(user,
                                               session=next(self._database_context.get_session()))

    def login_user(self, user: BaseModel):
        """
        Проверяет, есть ли у пользователя доступ в систему

        :param user: данные пользователя
        :return: Данные пользователя
        """
        try:
            self.check_user(user)
        except ValueError:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                "Пользователь не найден")
        else:
            time_now = datetime.now().second
            access_info = TokenBaseInfo(iss=server_config.public_url,
                                        sub=server_config.public_url,
                                        exp=time_now + auth_config.access_token_expired_minutes * 60,
                                        nbf=time_now,
                                        iat=time_now,
                                        token_type='access')
            access_token = self.tokenizator.generate_token(access_info.model_dump())
            refresh_info = TokenBaseInfo(iss=server_config.public_url,
                                        sub=server_config.public_url,
                                        exp=time_now + auth_config.access_token_expired_minutes * 60,
                                        nbf=time_now,
                                        iat=time_now,
                                        token_type='refresh')
            refresh_token = self.tokenizator.generate_token(refresh_info.model_dump())
            return access_token, refresh_token

    def logout_user(self, user: T) -> None:
        """
        Удаляет пользователя из системы

        :param user: Информация о пользователе
        """
        self._database_context.crud.remove_object(user,
                                                  session=next(self._database_context.get_session()))

