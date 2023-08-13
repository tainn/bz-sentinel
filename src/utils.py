import logging
import os
from dataclasses import dataclass
from typing import Any


@dataclass
class Struct:
    author_name: str = ""
    author_url: str = ""
    last_post_url: str = ""
    last_post_id: str = ""
    forum_name: str = ""
    forum_url: str = ""
    thread_name: str = ""
    thread_url: str = ""


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
        format='{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}',
        force=True,
    )
