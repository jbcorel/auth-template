from uuid import UUID
import sqlalchemy as sa
from server.core.repository import BaseRepository
from ..entities import AuthTokenInfo
from sqlalchemy import ScalarResult

class AuthTokenRepository(BaseRepository[AuthTokenInfo]):
    model = AuthTokenInfo

    async def get_by_token_str(self, token: str) -> AuthTokenInfo | None:
        return await self.session.scalar(sa.select(self.model).where(self.model.token == token))

    async def get_by_user_id(self, user_id: UUID) -> ScalarResult[AuthTokenInfo]:
        return await self.session.scalars(sa.select(self.model).where(self.model.user_id == user_id))

    async def delete(self, token: str) -> None:
        await self.session.execute(sa.delete(self.model).where(self.model.token == token))