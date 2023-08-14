import os
import sys

from loguru import logger


def init_logger() -> None:
    logger.remove(0)
    logger.add(
        sys.stdout,
        format="{message}",
        level=os.getenv("BZS_LOG_LEVEL", "INFO"),
        serialize=True,
    )
