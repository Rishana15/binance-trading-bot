"""
logging_config.py — Centralized logging setup.
Logs to both console (INFO+) and a rotating file (DEBUG+).
"""

import logging
import logging.handlers
import os
from datetime import datetime


def setup_logging(log_dir: str = "logs", log_level: str = "DEBUG") -> None:
    """
    Configure root logger with:
      - StreamHandler  → console (INFO and above)
      - RotatingFileHandler → logs/trading_bot_YYYYMMDD.log (DEBUG and above)

    Args:
        log_dir:   Directory to store log files (created if missing)
        log_level: Minimum level for the file handler ("DEBUG", "INFO", etc.)
    """
    os.makedirs(log_dir, exist_ok=True)

    date_str = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f"trading_bot_{date_str}.log")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers on repeated calls (e.g., during tests)
    if root_logger.handlers:
        return

    fmt = logging.Formatter(
        fmt="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --- Console handler ------------------------------------------------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(fmt)
    root_logger.addHandler(console_handler)

    # --- File handler (rotating, max 5 MB, keep 3 backups) --------------
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(getattr(logging, log_level.upper(), logging.DEBUG))
    file_handler.setFormatter(fmt)
    root_logger.addHandler(file_handler)

    logging.getLogger(__name__).info("Logging initialised → %s", log_file)
