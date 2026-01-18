"""
Input validation utilities.
"""

import re
from typing import Any, Dict, List, Optional
from datetime import datetime
from ..shared.constants import ValidationLimits, QuestionType


def validate_question_id(question_id: str) -> bool:
    """
    Validate question_id format (UUID).

    Args:
        question_id: Question ID to validate

    Returns:
        True if valid, False otherwise
    """
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(uuid_pattern, question_id, re.IGNORECASE))


def validate_topic_id(topic_id: str) -> bool:
    """
    Validate topic_id format (snake_case).

    Args:
        topic_id: Topic ID to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-z][a-z0-9_]*$'
    return bool(re.match(pattern, topic_id))


def validate_response_time(response_time_ms: int) -> tuple[bool, Optional[str]]:
    """
    Validate response time is within reasonable bounds.

    Args:
        response_time_ms: Response time in milliseconds

    Returns:
        Tuple of (is_valid, error_message)
    """
    if response_time_ms < ValidationLimits.MIN_RESPONSE_TIME_MS:
        return False, f'Response time too short (min: {ValidationLimits.MIN_RESPONSE_TIME_MS}ms)'

    if response_time_ms > ValidationLimits.MAX_RESPONSE_TIME_MS:
        return False, f'Response time too long (max: {ValidationLimits.MAX_RESPONSE_TIME_MS}ms)'

    return True, None


def validate_answer_submission(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate answer submission payload.

    Args:
        data: Answer submission data

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['question_id', 'user_answer']

    # Check required fields
    for field in required_fields:
        if field not in data:
            return False, f'Missing required field: {field}'

    # Validate question_id format
    if not validate_question_id(data['question_id']):
        return False, 'Invalid question_id format'

    # Validate user_answer is not empty
    if not data['user_answer'] or not isinstance(data['user_answer'], str):
        return False, 'user_answer must be a non-empty string'

    # Validate response_time_ms if provided
    if 'response_time_ms' in data:
        if not isinstance(data['response_time_ms'], int):
            return False, 'response_time_ms must be an integer'

        is_valid, error_msg = validate_response_time(data['response_time_ms'])
        if not is_valid:
            return False, error_msg

    return True, None


def validate_question_data(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate question data for creation/update.

    Args:
        data: Question data

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = [
        'topic_id',
        'category',
        'question_text',
        'question_type',
        'correct_answer',
        'explanation',
        'difficulty',
        'source_reference'
    ]

    # Check required fields
    for field in required_fields:
        if field not in data:
            return False, f'Missing required field: {field}'

    # Validate question_type
    if data['question_type'] not in [qt.value for qt in QuestionType]:
        return False, f'Invalid question_type. Must be one of: {[qt.value for qt in QuestionType]}'

    # Validate difficulty
    if data['difficulty'] not in [1, 2, 3]:
        return False, 'Difficulty must be 1, 2, or 3'

    # Validate question_text length
    if len(data['question_text']) > ValidationLimits.MAX_QUESTION_LENGTH:
        return False, f'question_text too long (max: {ValidationLimits.MAX_QUESTION_LENGTH} chars)'

    # Validate explanation length
    if len(data['explanation']) > ValidationLimits.MAX_EXPLANATION_LENGTH:
        return False, f'explanation too long (max: {ValidationLimits.MAX_EXPLANATION_LENGTH} chars)'

    # Validate answer_options for multiple_choice
    if data['question_type'] == QuestionType.MULTIPLE_CHOICE.value:
        if 'answer_options' not in data:
            return False, 'answer_options required for multiple_choice questions'

        options = data['answer_options']
        if not isinstance(options, list):
            return False, 'answer_options must be a list'

        if len(options) < ValidationLimits.MIN_ANSWER_OPTIONS:
            return False, f'Minimum {ValidationLimits.MIN_ANSWER_OPTIONS} answer options required'

        if len(options) > ValidationLimits.MAX_ANSWER_OPTIONS:
            return False, f'Maximum {ValidationLimits.MAX_ANSWER_OPTIONS} answer options allowed'

        # Check each option has 'id' and 'text'
        for opt in options:
            if not isinstance(opt, dict) or 'id' not in opt or 'text' not in opt:
                return False, 'Each answer option must have "id" and "text" fields'

    # Validate source_reference
    source_ref = data['source_reference']
    if not isinstance(source_ref, dict):
        return False, 'source_reference must be a dictionary'

    if 'document' not in source_ref or 'page' not in source_ref or 'section' not in source_ref:
        return False, 'source_reference must include document, page, and section'

    return True, None


def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize string input by stripping whitespace and optionally truncating.

    Args:
        value: String to sanitize
        max_length: Optional maximum length

    Returns:
        Sanitized string
    """
    sanitized = value.strip()

    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    return sanitized
