from logging import getLogger
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import NotFound


logger = getLogger(__name__)

class BaseRepository[ModelType]:
    model: ModelType

    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, instance: ModelType):
        """
        Добавление сущности в список отслеживания хранилищем

        :param instance: Сущность
        """

        self.session.add(instance)

    async def flush(self):
        """
        Отправка отслеживаемых сущностей в хранилище без фиксации изменений
        """
        await self.session.flush()

    async def refresh(self, instance: ModelType):
        """
        Обновляет аттрибуты сущности данными из хранилища

        :param instance: Сущность
        """
        await self.session.refresh(instance)


class UuidRepositoryMixin[ModelType]: 
    async def get_by_id(self, instance_id: UUID) -> ModelType | None:
        """
        Получение сущности из хранилища по идентификатору

        :param instance_id: Идентификатор сущности
        :return: Сущность | None
        """
        instance = await self.session.scalar(sa.select(self.model).where(self.model.id == instance_id))
        return instance

    async def delete(self, instance_id: UUID):
        """
        Удаление сущности из хранилища

        :param instance_id: Идентификатор сущности
        """
        await self.session.execute(sa.delete(self.model).where(self.model.id == instance_id))