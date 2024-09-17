from attrs import define

from src.repositories.cruds.base_crud import BaseCRUD
from src.repositories.models.user import User


@define(repr=False)
class UserCRUD(BaseCRUD[User]):
    """CRUD для работы с таблицей пользователей"""

    #: Модель таблицы базы данных
    _model = User
