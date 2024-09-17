from uuid import UUID

from pydantic import BaseModel, EmailStr, model_validator, ValidationError


class UserBaseModel(BaseModel):
    id: UUID
    first_name: str
    middle_name: str | None
    last_name: str
    nickname: str
    email: EmailStr
    password: str


class UserInfoModel(BaseModel):
    id: UUID | None
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    nickname: str | None
    email: EmailStr | None
    password: str | None

    @model_validator(mode='after')
    def check_unique_strs(self) -> None:
        if self.id is None and self.email is None:
            raise ValidationError("Поле 'id' или 'email' должно быть заполнено")


class UserLoginModel(BaseModel):
    nickname: str | None
    email: EmailStr | None
    password: str

    @model_validator(mode='after')
    def check_unique_strs(self) -> None:
        if self.nickname is None and self.email is None:
            raise ValidationError("Поле 'id' или 'nickname' должно быть заполнено")