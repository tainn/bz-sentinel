import logging
import os
from dataclasses import dataclass
from logging import Logger, getLogger
from typing import Any

logger: Logger = getLogger(__name__)


@dataclass
class Struct:
    author_name: str = None
    author_url: str = None
    last_post_url: str = None
    last_post_id: str = None
    forum_name: str = None
    forum_url: str = None
    thread_name: str = None
    thread_url: str = None


def conf_logs() -> None:
    level: dict[str, Any] = {
        "NOTSET": logging.NOTSET,
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    logging.basicConfig(
        level=level.get(os.getenv("BZS_LOG_LEVEL", "INFO")),
        format=(
            "{"
            '"time": "%(asctime)s", '
            '"level": "%(levelname)s", '
            '"name": "%(name)s", '
            '"message": "%(message)s"'
            "}"
        ),
    )

    logger.info("Logging configured")
