import orjson

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .settings import get_settings

settings = get_settings()
async_engine = create_async_engine(
    str(settings.database_url),
    json_serializer=lambda o: orjson.dumps(o, default=jsonable_encoder),
    json_deserializer=orjson.loads
)
async_session_factory = async_sessionmaker(async_engine, autoflush=False, autocommit=False, expire_on_commit=False)

# Подключение моделей
from server.core.entities import BaseEntity
from server.apps.auth.domain_model import entities as auth_entities
