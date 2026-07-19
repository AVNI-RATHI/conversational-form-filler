"""Logging configuration for the application."""

import logging
import sys
from config import settings

def setup_logging() -> None:
    """Configure application-wide logging."""
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.log_level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

setup_logging()
