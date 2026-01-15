"""Enhanced logging configuration for JC Agent.

Provides structured logging with context tracking and log aggregation support.
"""
from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Any

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False


def setup_logging(
    log_level: str = "INFO",
    log_file: Path | None = None,
    json_format: bool = False,
) -> logging.Logger:
    """Configure application logging with structured output.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        json_format: If True, output logs in JSON format for aggregation
    
    Returns:
        Configured logger instance
    
    Example:
        >>> logger = setup_logging("INFO", Path("jc_agent.log"))
        >>> logger.info("Application started", version="2.0.0")
    """
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    logger = logging.getLogger("jc_agent")
    logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    if json_format and STRUCTLOG_AVAILABLE:
        console_formatter = structlog.stdlib.ProcessorFormatter(
            processor=structlog.dev.ConsoleRenderer(),
        )
    else:
        console_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(console_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """Get a logger instance for a specific module.
    
    Args:
        name: Logger name, typically __name__
    
    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"jc_agent.{name}")
    return logging.getLogger("jc_agent")


class LogContext:
    """Context manager for adding structured context to logs.
    
    Example:
        >>> logger = get_logger(__name__)
        >>> with LogContext(request_id="abc-123", user="john"):
        ...     logger.info("Processing request")
    """
    
    def __init__(self, **kwargs: Any):
        self.context = kwargs
        self.previous_context: dict[str, Any] = {}
    
    def __enter__(self):
        if STRUCTLOG_AVAILABLE:
            for key, value in self.context.items():
                structlog.contextvars.bind_contextvars(**{key: value})
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if STRUCTLOG_AVAILABLE:
            structlog.contextvars.clear_contextvars()
