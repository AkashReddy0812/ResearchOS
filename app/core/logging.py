import logging
import sys

from app.core.config import get_settings
from app.core.constants import (
    APP_LOGGER_NAME,
    DEFAULT_DATE_FORMAT,
    DEFAULT_LOG_FORMAT,
)


def configure_logging() -> logging.Logger:
    """
    Configure the application logger.
    """

    settings = get_settings()

    logger = logging.getLogger(APP_LOGGER_NAME)

    logger.setLevel(settings.logging.level)

    logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt=DEFAULT_LOG_FORMAT,
        datefmt=DEFAULT_DATE_FORMAT,
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.propagate = False

    return logger


logger = configure_logging()