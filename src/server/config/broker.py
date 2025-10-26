import structlog
from faststream.kafka.fastapi import KafkaRouter

from .settings import get_settings

logger = structlog.get_logger()
settings = get_settings()
broker_router = KafkaRouter(
    settings.kafka.bootstrap_servers,
    acks="all",
    logger=logger,
    schema_url="/api/asyncapi",
    include_in_schema=True,
    compression_type="lz4",
)
