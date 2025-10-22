"""Logging configuration and utilities."""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger


_logger_configured = False


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    rotation: str = "10 MB",
    retention: str = "1 month",
    format_string: Optional[str] = None,
) -> None:
    """
    Configure application-wide logging.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        rotation: When to rotate log files
        retention: How long to keep old log files
        format_string: Custom format string for logs
    """
    global _logger_configured

    if _logger_configured:
        return

    # Remove default handler
    logger.remove()

    # Default format if not provided
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )

    # Add console handler with colors
    logger.add(
        sys.stderr,
        format=format_string,
        level=level,
        colorize=True,
    )

    # Add file handler if specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_file,
            format=format_string,
            level=level,
            rotation=rotation,
            retention=retention,
            compression="zip",
        )

    _logger_configured = True
    logger.info(f"Logging configured at {level} level")


def get_logger(name: str):
    """
    Get a logger instance with the given name.

    Args:
        name: Logger name (typically __name__ of the module)

    Returns:
        Logger instance
    """
    return logger.bind(name=name)


# Convenience function for quick logging setup from config
def setup_logging_from_config(config) -> None:
    """
    Setup logging using Settings configuration.

    Args:
        config: Settings instance
    """
    level = config.get('logging.level', 'INFO')
    log_to_file = config.get('logging.log_to_file', True)
    format_string = config.get('logging.format')
    rotation = config.get('logging.rotation', '10 MB')
    retention = config.get('logging.retention', '1 month')

    log_file = None
    if log_to_file:
        logs_dir = config.get_path('paths.logs')
        log_file = logs_dir / 'ag_dedicated.log'

    setup_logging(
        level=level,
        log_file=log_file,
        rotation=rotation,
        retention=retention,
        format_string=format_string,
    )
