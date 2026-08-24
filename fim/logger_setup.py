"""
logger_setup.py
----------------
Configures Python's built-in `logging` module so that every alert
and scan result is written both to the console (for immediate
visibility) and to a persistent log file (for later audit / evidence).
"""

import logging
from fim.config import LOG_FILE


def get_logger(name: str = "fim") -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        # Logger already configured (avoids duplicate handlers on repeated calls)
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
