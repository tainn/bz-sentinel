import os
import sys
from dataclasses import dataclass

from loguru import Logger, logger


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


def init_logger() -> Logger:
    logger.remove(0)
    logger.add(
        sys.stdout,
        format="{message}",
        level=os.getenv("BZS_LOG_LEVEL", "INFO"),
        serialize=True,
    )
    return logger
