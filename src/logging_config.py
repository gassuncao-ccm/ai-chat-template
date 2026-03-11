#pylint: disable=invalid-name
#pylint: disable=global-statement
from typing import Optional

import logging
import os
import sys
from pythonjsonlogger.json import JsonFormatter

_configured = False

def configure_logging(level: Optional[str] = None):
    global _configured
    if _configured:
        return

    env = (os.getenv("ENV") or "development").lower()
    default_level = "INFO" if env == "development" else "INFO"
    log_level = (level or os.getenv("LOG_LEVEL") or default_level).upper()
    formatter = os.getenv("LOG_FORMAT", "plain")
    handlers = []

    if formatter == "json":
        try:
            json_fmt = JsonFormatter(
                "%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)d"
            )
            stream = logging.StreamHandler(sys.stdout)
            stream.setFormatter(json_fmt)
            handlers.append(stream)
        except ImportError:
            pass

    if not handlers:
        stream = logging.StreamHandler(sys.stdout)
        stream.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(name)s - %(message)s"))
        handlers.append(stream)

    logging.basicConfig(level=log_level, handlers=handlers, force=True)
    _configured = True

def get_logger(name: str):
    if not _configured:
        configure_logging()
    return logging.getLogger(name)
