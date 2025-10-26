from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from server.core.entities import BaseEntity, UUIDPKMixin


class DimMixin(UUIDPKMixin):
    __table_args__ = {"schema": "dim"}

    code: Mapped[str] = mapped_column(unique=True, nullable=False, comment="Код в справочниках 1С")
    name: Mapped[str] = mapped_column(comment="Наименование")
    is_deleted: Mapped[bool] = mapped_column(comment="Пометка на удаление", default=False, server_default="false")


# ------------------------------------------------------------------------------------

class Department(DimMixin, BaseEntity):
    __tablename__ = "departments"