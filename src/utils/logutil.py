import json
import logging.config
import os


def configure() -> None:
    with open(os.getenv("LOGGING_JSON"), "r") as rf:
        logging.config.dictConfig(json.load(rf))
