"""
Utility functions for the French Civics Test application.
"""

from utils.auth import (
    extract_user_id_from_event,
    extract_user_email_from_event,
    extract_cognito_username_from_event,
    get_all_claims,
)

from utils.responses import (
    success_response,
    error_response,
    not_found_response,
    unauthorized_response,
    validation_error_response,
    internal_server_error_response,
)

from utils.validators import (
    validate_question_id,
    validate_topic_id,
    validate_response_time,
    validate_answer_submission,
    validate_question_data,
    sanitize_string,
)

from utils.logging import (
    get_logger,
    log_api_request,
    log_api_response,
)

__all__ = [
    # Auth utilities
    'extract_user_id_from_event',
    'extract_user_email_from_event',
    'extract_cognito_username_from_event',
    'get_all_claims',

    # Response builders
    'success_response',
    'error_response',
    'not_found_response',
    'unauthorized_response',
    'validation_error_response',
    'internal_server_error_response',

    # Validators
    'validate_question_id',
    'validate_topic_id',
    'validate_response_time',
    'validate_answer_submission',
    'validate_question_data',
    'sanitize_string',

    # Logging
    'get_logger',
    'log_api_request',
    'log_api_response',
]
