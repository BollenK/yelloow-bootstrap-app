import logging
import logging.config
from typing import Any, Callable, List

import structlog
from structlog.threadlocal import merge_threadlocal

from src.yelloow_app.shared.config import config

shared_processors: List[Callable[[Any, str, Any], Any]] = [
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.UnicodeDecoder(),
]

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "colored": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=True),
                "foreign_pre_chain": shared_processors,
            },
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(sort_keys=True),
                "foreign_pre_chain": shared_processors,
            },
        },
        "handlers": {
            "default": {
                "level": "DEBUG" if config.is_development() else "INFO",
                "class": "logging.StreamHandler",
                "formatter": "colored" if config.is_development() else "json",
            }
        },
        "loggers": {
            "": {"handlers": ["default"], "level": "INFO"},
            "alembic": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "lyv": {
                "handlers": ["default"],
                "level": "DEBUG" if config.is_development() else "INFO",
                "propagate": False,
            },
        },
    }
)

structlog.configure(
    processors=[merge_threadlocal] + shared_processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],  # type: ignore # noqa
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)


def get_logger(name):
    return structlog.get_logger()
