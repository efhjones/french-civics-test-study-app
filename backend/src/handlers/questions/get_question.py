"""
Lambda handler for getting a specific question by ID.

GET /questions/{questionId}
"""

import json
from typing import Any, Dict
from ...repositories.question_repository import QuestionRepository
from ...utils import (
    success_response,
    error_response,
    not_found_response,
    internal_server_error_response,
    extract_user_id_from_event,
    validate_question_id,
    get_logger,
    log_api_request,
)


logger = get_logger(__name__)
question_repo = QuestionRepository()


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Get a specific question by ID.

    Returns the question WITHOUT the correct answer (for practice mode).
    To include the answer, pass ?include_answer=true (for review mode).

    Args:
        event: API Gateway Lambda proxy event
        context: Lambda context

    Returns:
        API Gateway Lambda proxy response
    """
    try:
        # Extract user_id for logging
        user_id = extract_user_id_from_event(event)
        log_api_request(logger, event, user_id)

        # Get question_id from path parameters
        path_params = event.get('pathParameters') or {}
        question_id = path_params.get('questionId')

        if not question_id:
            return error_response(
                message="Missing question_id in path",
                status_code=400
            )

        # Validate question_id format
        if not validate_question_id(question_id):
            return error_response(
                message="Invalid question_id format",
                status_code=400
            )

        # Check if answer should be included (for review mode)
        query_params = event.get('queryStringParameters') or {}
        include_answer = query_params.get('include_answer', '').lower() == 'true'

        # Fetch question
        logger.info(f"Fetching question: {question_id}, include_answer: {include_answer}")
        question = question_repo.get_by_id(question_id)

        if not question:
            return not_found_response(message=f"Question {question_id} not found")

        # Convert to API response format (hides correct answer by default)
        question_data = question.to_api_response(include_answer=include_answer)

        return success_response(data={'question': question_data})

    except ValueError as e:
        # User ID extraction failed (should not happen with authorizer)
        logger.error(f"Authorization error: {str(e)}")
        return error_response(
            message="Unauthorized",
            status_code=401
        )

    except Exception as e:
        logger.error(f"Error fetching question: {str(e)}", exc_info=True)
        return internal_server_error_response(
            message="Failed to fetch question",
            include_details=False
        )
