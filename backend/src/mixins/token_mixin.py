from abc import ABC, abstractmethod
from email.base64mime import decode
from typing import Mapping, Any, Literal

import jwt
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing_extensions import TypeVar, Generic

from src.schemas.auth import TokenBaseInfo
from src.shared.config import auth_config, server_config


class AbstractTokenMixin(ABC):
    """Миксин для работы с авторизационными токенами"""


    @property
    @abstractmethod
    def Config(self) -> BaseSettings:
        """Основные настройки для кодирования-декодирования"""


    @abstractmethod
    def generate_token(self, info):
        """
        Генерирует токен

        :param info: Полезная информация
        :return: Сгенерированный токен
        """

    @abstractmethod
    def extract_payload(self, token):
        """
        Извлекает полезную информацию из токена

        :param token: Токен для извлечения
        :return: Извлеченная полезная информация
        """


class JWTTokenMixin(AbstractTokenMixin):
    """Миксин для работы с JSON Web Token"""
    #: Конфигурация для кодировщика
    @property
    def Config(self) -> BaseSettings:
        """Основные настройки для кодирования-декодирования"""
        return auth_config

    def generate_token(self, info: Mapping[str, Any]) -> str:
        """
        Генерирует токен

        :param info: Полезная информация
        :return: Сгенерированный JSON Web Token
        """
        return jwt.encode(**info,
                   key=auth_config.secret_key,
                   algorithm=auth_config.algorithm)

    def extract_payload(self, token: str) -> TokenBaseInfo:
        """
        Извлекает полезную информацию из токена

        :param token: JSON Web Token
        :return: Извлеченная полезная информация
        """
        payload = jwt.decode(jwt=token,
                          key=auth_config.secret_key,
                          algorithms=[auth_config.algorithm])

        return TokenBaseInfo.model_validate(payload)