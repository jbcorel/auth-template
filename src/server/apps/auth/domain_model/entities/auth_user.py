from uuid import UUID

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship, foreign
from server.core.entities import BaseEntity
from server.apps.dim.domain_model.entities import Department
from .association_tables import departments_users


class User(BaseEntity):
    __tablename__ = "auth_users"
    __table_args__ = {
        "comment": "Таблица авторизации пользователей", 
        "schema": "app"
    }

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        comment="Уникальный идентификатор пользователя"
    )
    type: Mapped[str] = mapped_column(comment="Тип пользователя")
    name: Mapped[str] = mapped_column(comment="Имя пользователя")
    email: Mapped[str] = mapped_column(
        CheckConstraint("email = lower(email)", name="is_lowercase_email"), 
        comment="Электронная почта", 
        unique=True
    )
    hashed_password: Mapped[str] = mapped_column(comment="Хэш пароля")
    is_deleted: Mapped[bool] = mapped_column(comment="Пометка на удаление пользователя", server_default='false')
    is_superuser: Mapped[bool] = mapped_column(comment="является ли пользователь администратором")
    departments: Mapped[list[Department]] = relationship(secondary=departments_users)