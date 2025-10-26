from typing import Annotated
from ipaddress import IPv4Address

from fastapi import APIRouter, Depends, status, Body

from server.config.settings import get_settings, Settings
from server.core.deps import Mailer, get_mailer
from .deps import (
    get_user_by_credentials,
    User,
    AuthTokenRepository,
    get_auth_token_repository,
    get_user_by_token,
    get_session_token,
    get_client_ip,
    get_client_user_agent
)
from .domain_model.use_cases import (
    create_session_token,
    logout,
    hash_password
)


router = APIRouter()


@router.post("/hash-password")
async def hash_password_route(payload: Annotated[hash_password.PasswordDTO, Body()]) -> hash_password.HashedPasswordDTO:
    return hash_password.handle(payload)


@router.post(
    "/token/",
    responses={401: {"description": "Not authenticated"}},
    description="Получение токена по логину и паролю",
)
async def create_session_token_route(
    user: Annotated[User, Depends(get_user_by_credentials)],
    repository: Annotated[AuthTokenRepository, Depends(get_auth_token_repository)],
    mailer: Annotated[Mailer, Depends(get_mailer)],
    settings: Annotated[Settings, Depends(get_settings)],
    client_ip: Annotated[IPv4Address, Depends(get_client_ip)],
    user_agent: Annotated[str, Depends(get_client_user_agent)]
) -> create_session_token.DTO:
    return await create_session_token.handle(
        user=user, 
        repository=repository,
        mailer=mailer,
        settings=settings,
        client_ip=client_ip,
        user_agent=user_agent
    )


@router.get(
    "/me/"
)
async def get_me(
    user: Annotated[User, Depends(get_user_by_token)]
):
    """Пока используется для дебага, в будущем понадобится.""" 
    return user #TODO сделать схему, пока закомментить


@router.post(
    "/logout",
    responses={401: {"description": "Not authenticated"}},
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout_user(
    token_repository: Annotated[str, Depends(get_auth_token_repository)],
    session_token: Annotated[str, Depends(get_session_token)],
):
    return await logout.handle(
        repository=token_repository,
        token=session_token
    )