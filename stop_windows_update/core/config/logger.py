import logging
import os
from pathlib import Path

P_DATA_DIR = Path(os.environ.get("ALLUSERSPROFILE") or r"C:\ProgramData")
LOGGING_LEVEL = logging.INFO
LOGGER_NAME = "stop_windows_update"


def get_logging_config() -> dict:
    log_file = P_DATA_DIR / "stop_windows_updates.log"
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s | %(levelname)s: [%(name)s:%(funcName)s:%(lineno)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "level": LOGGING_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
            "file": {
                "level": LOGGING_LEVEL,
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "standard",
                "filename": str(log_file.as_posix()),
                "when": "D",
                "interval": 15,
                "backupCount": 8,
                "encoding": "utf-8",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": LOGGING_LEVEL,
        },
        "loggers": {
            LOGGER_NAME: {
                "handlers": ["console", "file"],
                "propagate": False,
                "level": LOGGING_LEVEL,
            },
        },
    }
