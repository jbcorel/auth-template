from logging import getLogger
import sqlalchemy as sa

from ..entities import User
from server.core.repository import BaseRepository, UuidRepositoryMixin


logger = getLogger(__name__)


class AbstractAuthUserRepository[AuthUserType](UuidRepositoryMixin[AuthUserType], BaseRepository[AuthUserType]):
    async def get_by_email(self, email: str) -> AuthUserType | None:
        instance = await self.session.scalar(sa.select(self.model).where(self.model.email == email.lower()))
        return instance

    async def get_list(self, search: str | None = None) -> sa.ScalarResult[AuthUserType]:
        stmt = sa.select(self.model).order_by(self.model.name)
        if search is not None:
            stmt = stmt.where(
                sa.or_(
                    self.model.name.ilike(f"%{search}%"),
                    self.model.email.ilike(f"%{search}%"),
                )
            )
        return await self.session.scalars(stmt)
    

class UserRepository(AbstractAuthUserRepository[User]):
    model = User