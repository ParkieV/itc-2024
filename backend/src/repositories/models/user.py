from uuid import UUID

from sqlalchemy.orm import Mapped

from src.repositories.models import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID]
