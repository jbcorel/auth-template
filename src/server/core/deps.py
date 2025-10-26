from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from faststream.kafka import KafkaBroker
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from server.config.broker import broker_router
from server.config.database import async_session_factory
from server.config.settings import Settings, get_settings
from server.services.mailer import Mailer


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        else:
            await session.commit()
        finally:
            await session.close()

def get_broker() -> KafkaBroker:
    return broker_router.broker


def get_mailer(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Mailer:
    return Mailer(
        host=settings.smtp.host,
        port=settings.smtp.port,
        username=settings.smtp.username,
        password=settings.smtp.password,
        starttls=settings.smtp.starttls,
        from_email=settings.smtp.from_email,
    )


def get_redis(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Redis:
    return Redis(
        host=settings.redis_url.host,
        port=settings.redis_url.port,
        password=settings.redis_url.password,
        db=int(settings.redis_url.path.replace("/", "")),
    )
