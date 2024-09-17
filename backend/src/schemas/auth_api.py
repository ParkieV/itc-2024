from pydantic import BaseModel, EmailStr


class RegisterUserInfo(BaseModel):
    nickname: str
    email: EmailStr
    password: str

class AuthRequestInfo(BaseModel):
    login: str | EmailStr
    password: str

class AuthResponseInfo(BaseModel):
    access_token: str
    refresh_token: str

class RefreshResponseInfo(AuthResponseInfo):
    pass
