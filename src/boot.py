from __future__ import annotations

import os
import sys

import loguru
from loguru import logger


def get_logger() -> loguru.Logger:
    logger.remove(0)
    logger.add(
        sys.stdout,
        format="{message}",
        level=os.getenv("BZS_LOG_LEVEL", "INFO"),
        serialize=True,
    )
    return logger
