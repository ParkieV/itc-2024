import json
from typing import Any

from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.shared.constants import _ENV_PATH


class ServerSettings(BaseSettings):
    host: str
    port: int
    origins: list[str] = Field(validation_alias='allow_origins')
    credentials: bool = Field(validation_alias='allow_credentials')
    methods: list[str] = Field(validation_alias='allow_methods')
    headers: list[str] = Field(validation_alias='allow_headers')
    public_url: str = Field(validation_alias='public_url')

    model_config = SettingsConfigDict(extra='allow', env_prefix='backend_', env_file=_ENV_PATH)

    @field_validator('origins', 'methods', 'headers', mode='before')
    def parse_json_list(v: Any) -> list[str]:
        if isinstance(v, str):
            return json.loads(v)
        else:
            raise ValidationError()
        return v

class DBSettings(BaseSettings):
    driver: str = Field(validation_alias='driver')
    username: str = Field(validation_alias='user_name')
    password: str = Field(validation_alias='password')
    host: str = Field(validation_alias='host')
    port: int | None = Field(None, validation_alias='port')
    database_name: str = Field(validation_alias='name')

    @property
    def db_url(self) -> str:
        return f"{self.driver}://{self.host}{f':{self.port}' if self.port is not None else ''}/{self.database_name}"

    model_config = SettingsConfigDict(extra='allow', env_prefix='db_', env_file=_ENV_PATH)

class AuthSettings(BaseSettings):
    secret_key: str = Field(validation_alias='secret_key')
    algorithm: str = Field(validation_alias='algorithm')
    access_token_expired_minutes: int = Field(validation_alias='access_token_expired_minutes')
    refresh_token_expired_days: int = Field(validation_alias='refresh_token_expired_days')

    model_config = SettingsConfigDict(extra='allow', env_prefix='auth_', env_file=_ENV_PATH)


server_config = ServerSettings() #type: ignore
db_config = DBSettings() #type: ignore
auth_config = AuthSettings() #type: ignore