import os
import sys

from loguru import Logger, logger


def get_logger() -> Logger:
    logger.remove(0)
    logger.add(
        sys.stdout,
        format="{message}",
        level=os.getenv("BZS_LOG_LEVEL", "INFO"),
        serialize=True,
    )
    return logger
