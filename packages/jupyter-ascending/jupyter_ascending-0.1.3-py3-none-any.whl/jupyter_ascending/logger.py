import sys

from loguru import logger

__all__ = ["J_LOGGER"]

config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{time} - {message}"},
        {"sink": "/tmp/jupyter_ascending/log.log", "serialize": False},
    ],
}

logger.configure(**config)  # type: ignore

# Just give a global constant to import for now
J_LOGGER = logger
