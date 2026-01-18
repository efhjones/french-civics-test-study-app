"""
Utilities for building standardized API responses.
"""

import json
from typing import Any, Dict, Optional
from http import HTTPStatus


def success_response(
    data: Any,
    status_code: int = HTTPStatus.OK,
    message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Build a successful API response.

    Args:
        data: Response payload
        status_code: HTTP status code (default: 200)
        message: Optional success message

    Returns:
        API Gateway Lambda proxy response dict
    """
    body = {
        'status': 'success',
        'data': data
    }

    if message:
        body['message'] = message

    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',  # Configure properly in production
            'Access-Control-Allow-Credentials': True,
        },
        'body': json.dumps(body)
    }


def error_response(
    message: str,
    status_code: int = HTTPStatus.BAD_REQUEST,
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Build an error API response.

    Args:
        message: Error message
        status_code: HTTP status code (default: 400)
        error_code: Optional error code for client handling
        details: Optional additional error details

    Returns:
        API Gateway Lambda proxy response dict
    """
    body = {
        'status': 'error',
        'message': message
    }

    if error_code:
        body['error_code'] = error_code

    if details:
        body['details'] = details

    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
        'body': json.dumps(body)
    }


def not_found_response(message: str = 'Resource not found') -> Dict[str, Any]:
    """
    Build a 404 Not Found response.

    Args:
        message: Error message

    Returns:
        API Gateway Lambda proxy response dict
    """
    return error_response(
        message=message,
        status_code=HTTPStatus.NOT_FOUND,
        error_code='NOT_FOUND'
    )


def unauthorized_response(message: str = 'Unauthorized') -> Dict[str, Any]:
    """
    Build a 401 Unauthorized response.

    Args:
        message: Error message

    Returns:
        API Gateway Lambda proxy response dict
    """
    return error_response(
        message=message,
        status_code=HTTPStatus.UNAUTHORIZED,
        error_code='UNAUTHORIZED'
    )


def validation_error_response(
    message: str,
    validation_errors: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Build a 422 Unprocessable Entity response for validation errors.

    Args:
        message: Error message
        validation_errors: Dictionary of field-specific validation errors

    Returns:
        API Gateway Lambda proxy response dict
    """
    return error_response(
        message=message,
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        error_code='VALIDATION_ERROR',
        details=validation_errors or {}
    )


def internal_server_error_response(
    message: str = 'Internal server error',
    include_details: bool = False,
    details: Optional[str] = None
) -> Dict[str, Any]:
    """
    Build a 500 Internal Server Error response.

    Args:
        message: Error message
        include_details: Whether to include error details (only for dev/debug)
        details: Error details (e.g., exception message)

    Returns:
        API Gateway Lambda proxy response dict
    """
    error_details = None
    if include_details and details:
        error_details = {'error': details}

    return error_response(
        message=message,
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        error_code='INTERNAL_ERROR',
        details=error_details
    )
