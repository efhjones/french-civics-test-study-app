"""
Structured logging configuration for Lambda functions.
"""

import logging
import json
import os
from typing import Any, Dict, Optional
from datetime import datetime


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)

    # Set level from environment or default to INFO
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Avoid duplicate handlers in Lambda warm starts
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(StructuredFormatter())
        logger.addHandler(handler)

    return logger


class StructuredFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.

        Args:
            record: Log record

        Returns:
            JSON string
        """
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id

        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id

        return json.dumps(log_data)


def log_api_request(
    logger: logging.Logger,
    event: Dict[str, Any],
    user_id: Optional[str] = None
) -> None:
    """
    Log incoming API request details.

    Args:
        logger: Logger instance
        event: API Gateway event
        user_id: Optional user ID
    """
    http_method = event.get('httpMethod', 'UNKNOWN')
    path = event.get('path', 'UNKNOWN')
    request_id = event.get('requestContext', {}).get('requestId', 'UNKNOWN')

    logger.info(
        f"{http_method} {path}",
        extra={
            'user_id': user_id,
            'request_id': request_id,
            'http_method': http_method,
            'path': path
        }
    )


def log_api_response(
    logger: logging.Logger,
    status_code: int,
    execution_time_ms: Optional[float] = None
) -> None:
    """
    Log API response details.

    Args:
        logger: Logger instance
        status_code: HTTP status code
        execution_time_ms: Optional execution time
    """
    log_msg = f"Response {status_code}"
    if execution_time_ms:
        log_msg += f" ({execution_time_ms:.2f}ms)"

    logger.info(log_msg, extra={'status_code': status_code})
