from sqlalchemy import Table, Column, ForeignKey
from server.core.entities import BaseEntity


departments_users = Table(
    "association_department_user",
    BaseEntity.metadata,
    Column(
        "user_id",
        ForeignKey("app.users.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="Идентификатор пользователя ДНС"
    ),
    Column(
        "department_id",
        ForeignKey("dim.departments.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="Идентификатор филиала ДНС"
    ),
    comment="Таблица ассоциаций Пользователь ДНС - Филиал ДНС",
    schema="app"
)
