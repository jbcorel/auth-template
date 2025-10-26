from fastapi import Response
from ..repositories import AuthTokenRepository


async def handle(
    repository: AuthTokenRepository, 
    token: str
) -> None:
    await repository.delete(token=token)