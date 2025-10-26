from datetime import datetime, timezone
from ipaddress import IPv4Address
from typing import Self
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import INET
from server.core.entities import BaseEntity
from .auth_user import User
from ...utils import hash_secret

class AuthTokenInfo(BaseEntity):
    __tablename__ = "auth_tokens"
    __table_args__ = {"comment": "Таблица с токенами авторизации", "schema": "app"}

    token: Mapped[str] = mapped_column(comment="Токен авторизации", primary_key=True)
    client_ip: Mapped[IPv4Address] = mapped_column(INET, comment="IP-Адрес владельца токена")
    user_agent: Mapped[str] = mapped_column(comment="User-agent пользователя")
    user_id: Mapped[User] = mapped_column(
        ForeignKey(User.id, ondelete="CASCADE", onupdate="CASCADE"),
        comment="Идентификатор владельца токена",
    )
    expires: Mapped[datetime] = mapped_column(comment="Дата истечения токена")
    
    def is_valid(self):
        return self.expires > datetime.now(timezone.utc)
    
    @classmethod
    def create(
        cls,
        token: str,
        client_ip: IPv4Address,
        user_agent: str,
        user_id: UUID,
        expires: datetime
    ) -> Self:
        return AuthTokenInfo(
            token=hash_secret(token),
            client_ip=client_ip,
            user_agent=user_agent,
            user_id=user_id,
            expires=expires
        )