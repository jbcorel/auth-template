from datetime import timedelta
from enum import StrEnum
from functools import lru_cache
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel, EmailStr, HttpUrl, PlainValidator, PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from ..utils import get_path


class EnvEnum(StrEnum):
    LOC = "loc"
    DEV = "dev"
    PROD = "prod"


class Kafka(BaseModel):
    bootstrap_servers: list[str]
    input_topic: str
    output_topic: str


class Minio(BaseModel):
    """
    Minio.

    :cvar endpoint: Абсолютный URL адрес Minio API.
    :cvar access_key: Логин.
    :cvar secret_key: Пароль.
    :cvar secure: Используется ли защищенный режим.
    :cvar bucket_name: Имя корзины.
    """

    endpoint: str
    access_key: str
    secret_key: str
    secure: bool
    bucket_name: str


class SMTP(BaseModel):
    host: str
    port: int
    username: str
    password: SecretStr
    starttls: bool
    from_email: EmailStr


class Settings(BaseSettings):
    env: EnvEnum
    debug: bool = False
    service_instance_id: UUID
    service_name: str = "server"
    service_namespace: str = "Example Namespace"
    service_version: str = "0.1.0"
    database_url: PostgresDsn
    # TODO подумать над миграцией на чистый HttpUrl с учетом нюанса: https://github.com/pydantic/pydantic/issues/7186
    project_url: Annotated[str, PlainValidator(lambda v: HttpUrl(v)), AfterValidator(lambda x: str(x).rstrip("/"))]
    secret_key: str
    redis_url: RedisDsn
    token_lifetime: timedelta = timedelta(days=5)
    kafka: Kafka
    # minio: Minio
    smtp: SMTP

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=get_path("../../../.env"),
        env_nested_delimiter="__",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
