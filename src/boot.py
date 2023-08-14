import os
import sys

from loguru import logger as _logger


def init_logger() -> None:
    logger = _logger.opt(raw=True)
    logger.remove(0)
    logger.add(
        sys.stdout,
        format="{message}",
        level=os.getenv("BZS_LOG_LEVEL", "INFO"),
        serialize=True,
    )
