from typing import Any, Literal
from uuid import UUID

import orjson
import structlog

from .settings import EnvEnum

type LogLevelType = Literal["notset", "debug", "info", "warning", "error", "critical"]


def structlog_configure(
    service_instance_id: UUID,
    service_name: str,
    service_version: str,
    service_namespace: str,
    environment: EnvEnum,
    log_level: LogLevelType,
):
    def environment_processor(
        logger: Any, method_name: LogLevelType, event_dict: structlog.typing.EventDict
    ) -> structlog.typing.EventDict:
        event_dict["service.instance.id"] = service_instance_id
        event_dict["service.name"] = service_name
        event_dict["service.namespace"] = service_namespace
        event_dict["service.version"] = service_version
        event_dict["deployment.environment.name"] = str(environment)
        return event_dict

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        environment_processor,
    ]
    if environment == EnvEnum.LOC:
        structlog.configure(
            processors=[
                *shared_processors,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(log_level),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=False,
        )
    else:
        structlog.configure(
            processors=[
                *shared_processors,
                structlog.processors.format_exc_info,
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                structlog.processors.JSONRenderer(serializer=orjson.dumps),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(log_level),
            logger_factory=structlog.BytesLoggerFactory(),
            cache_logger_on_first_use=True,
        )
