from datetime import datetime, timezone
from typing import Annotated
from ipaddress import IPv4Address

from fastapi import Depends, Form, Header, Request
from fastapi.security import OAuth2PasswordBearer

from server.core.exceptions import NotAuthenticated, DomainError
from server.core.deps import (
    AsyncSession,
    get_async_session
)

from .domain_model.entities import User
from .domain_model.repositories import AuthTokenRepository, UserRepository
from .utils import verify_password, hash_secret


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token/")

def get_user_repository(session: Annotated[AsyncSession, Depends(get_async_session)]) -> UserRepository:
    return UserRepository(session)
 

def get_auth_token_repository(session: Annotated[AsyncSession, Depends(get_async_session)]) -> AuthTokenRepository:
    return AuthTokenRepository(session)


def get_session_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    """
    Возвращает токен сессии как он хранится в БД
    """
    return hash_secret(token)


async def get_client_ip(req: Request) -> IPv4Address:
    if not req.client:
        raise DomainError(detail="Missing client ip address")
    return IPv4Address(req.client.host)


async def get_client_user_agent(user_agent: Annotated[str, Header()] = None):
    if not user_agent:
        raise DomainError("Missing User-agent header")
    return user_agent


async def get_user_by_credentials(
    email: Annotated[str, Form(alias="username")],
    password: Annotated[str, Form()],
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    user = await repository.get_by_email(email.lower())
    
    if user is None or not verify_password(password, user.hashed_password):
        raise NotAuthenticated(detail="Неверный логин и/или пароль")

    if user.is_deleted:
        raise NotAuthenticated(detail="Вам закрыт доступ к порталу АСЦ")

    return user


async def get_user_by_token(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    token_repository: Annotated[AuthTokenRepository, Depends(get_auth_token_repository)],
    session: Annotated[str, Depends(get_session_token)]
) -> User:
    auth_token = await token_repository.get_by_token_str(session)

    if not auth_token:
        raise NotAuthenticated("Неверный токен авторизации")

    if auth_token.expires < datetime.now(timezone.utc):
        await token_repository.delete(auth_token.token)
        raise NotAuthenticated("Истёк токен авторизации")

    user = await user_repository.get_by_id(auth_token.user_id)

    if not user or user.is_deleted:
        raise NotAuthenticated("Вам закрыт доступ")
    
    return user