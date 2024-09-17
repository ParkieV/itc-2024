from datetime import timedelta
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, model_validator, ValidationError

from src.shared.config import auth_config


class TokenBaseInfo(BaseModel):
    iss: str
    sub: int | UUID
    aud: str
    exp: int
    nbf: int
    iat: int
    jti: UUID = UUID().hex
    token_type: Literal['access', 'refresh']

    @model_validator(mode="after")
    def check_timedelta(self):
        if self.nbf != self.iat:
            raise ValidationError("'nbf' и 'iat' должны иметь одинаковое значение")
        elif self.token_type == 'access' and timedelta(seconds=(self.exp - self.nbf)) > timedelta(minutes=auth_config.access_token_expired_minutes):
            raise ValidationError("Некорректно указано значение в 'exp' или 'nbf'")
        elif self.token_type == 'refresh' and timedelta(seconds=(self.exp - self.nbf)) > timedelta(days=auth_config.refresh_token_expired_days):
            raise ValidationError("Некорректно указано значение в 'exp' или 'nbf'")
