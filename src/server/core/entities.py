import enum
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy import DateTime, func, MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects import postgresql as psql
from typing import Any
from uuid import UUID, uuid4


class BaseEntity(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        },
        schema="app",
    )
    type_annotation_map = {
        datetime: DateTime(timezone=True),
        dict[str, Any]: psql.JSONB,
        enum.Enum: sa.Enum(enum.Enum, values_callable=lambda obj: [e.value for e in obj]),
    }

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), comment="Создан")
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now(), server_default=func.now(), comment="Обновлен")

    def __repr__(self):
        attributes = {k: getattr(self, k) for k in self.__mapper__.columns.keys()}
        return "{class_name}({attributes})".format(
            class_name=self.__class__.__name__,
            attributes=", ".join("{}={!r}".format(k, v) for k, v in attributes.items()),
        )


class UUIDPKMixin:
    """Миксин для добавления идентификатора - первичного ключа. Используется не везде, поэтому вынесен отдельно от BaseEntity"""

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
        default=uuid4,
        comment="Уникальный идентификатор записи",
    )
