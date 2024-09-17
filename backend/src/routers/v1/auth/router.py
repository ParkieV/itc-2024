from fastapi import APIRouter, HTTPException, status

from src.schemas.auth_api import (AuthRequestInfo, AuthResponseInfo,
                                  RefreshResponseInfo, RegisterUserInfo)
from src.schemas.user import UserInfoModel, UserLoginModel
from src.services.auth.handler import OAuth2AuthHandler, AbstractAuthHandler

router = APIRouter(prefix='/auth')

#: Обработчик авторизации
auth_handler: OAuth2AuthHandler = OAuth2AuthHandler[UserInfoModel]

@router.post('/signin')
async def signin(user_info: RegisterUserInfo) -> None:
    """
    Эндпоинт для регистрации пользователя в системе

    :param user_info: Пользовательские данные для регистрации в системе
    """
    auth_user_model: UserInfoModel = UserInfoModel.model_obj(user_info)

    auth_handler.register_user(auth_user_model)

@router.post('/login')
async def login(user_info: AuthRequestInfo) -> AuthResponseInfo:
    """
    Эндпоинт для авторизации пользователя в системе

    :param user_info: Пользовательские данные для авторизации в системе

    :return AuthResponseInfo: Данные для доступа к ресурсам при успешной авторизации в системе

    :raise HTTPException(status_code=404): Пользователь не был найден
    """
    auth_user_model: UserLoginModel = UserLoginModel.model_obj(user_info)

    auth_handler.login_user(auth_user_model)



# Предполагается делать обновление через хедеры
@router.post('/refresh')
async def refresh() -> RefreshResponseInfo:
    """
    Эндпоинт для обновления доступа в систему

    :return AuthResponseInfo: Данные для доступа к ресурсам при успешной авторизации в системе

    :raise HTTPException(status_code=404): Пользователь не был найден
    """
    ...

# Предполагается делать обновление через хедеры
@router.get('/logout')
async def logout() -> None:
    """Эндпоинт для выхода из системы"""
    auth_handler.logout_user(user)