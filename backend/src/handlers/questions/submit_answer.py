"""
Lambda handler for submitting an answer.

POST /questions/answer
Request body:
{
  "question_id": "uuid",
  "user_answer": "a",
  "response_time_ms": 8500
}
"""

import json
from datetime import datetime
from typing import Any, Dict
from repositories.question_repository import QuestionRepository
from repositories.result_repository import ResultRepository
from repositories.stats_repository import StatsRepository
from models.result import UserQuestionResult
from utils import (
    success_response,
    error_response,
    not_found_response,
    validation_error_response,
    internal_server_error_response,
    extract_user_id_from_event,
    validate_answer_submission,
    get_logger,
    log_api_request,
)


logger = get_logger(__name__)
question_repo = QuestionRepository()
result_repo = ResultRepository()
stats_repo = StatsRepository()


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Submit an answer and update user statistics.

    Args:
        event: API Gateway Lambda proxy event
        context: Lambda context

    Returns:
        API Gateway Lambda proxy response
    """
    try:
        # Extract user_id from JWT
        user_id = extract_user_id_from_event(event)
        log_api_request(logger, event, user_id)

        # Parse request body
        body = json.loads(event.get('body', '{}'))

        # Validate request
        is_valid, error_msg = validate_answer_submission(body)
        if not is_valid:
            return validation_error_response(message=error_msg)

        question_id = body['question_id']
        user_answer = body['user_answer']
        response_time_ms = body.get('response_time_ms', 0)

        # Get the question
        question = question_repo.get_by_id(question_id)
        if not question:
            return not_found_response(message="Question not found")

        # Check if answer is correct
        is_correct = (user_answer == question.correct_answer)

        # Create timestamp
        timestamp = datetime.utcnow().isoformat() + 'Z'

        # Create result record
        result = UserQuestionResult(
            user_id=user_id,
            result_id=UserQuestionResult.create_result_id(timestamp, question_id),
            question_id=question_id,
            topic_id=question.topic_id,
            category=question.category,
            answered_at=timestamp,
            correct=is_correct,
            user_answer=user_answer,
            response_time_ms=response_time_ms,
            difficulty=question.difficulty
        )

        # Save result
        result_repo.create(result)
        logger.info(f"Result saved for user {user_id}, question {question_id}, correct: {is_correct}")

        # Update user stats (initialize if doesn't exist)
        if not stats_repo.stats_exist(user_id):
            stats_repo.initialize_for_user(user_id)

        # Increment stats
        stats_repo.increment_category_stats(
            user_id=user_id,
            category=question.category,
            is_correct=is_correct,
            timestamp=timestamp
        )

        stats_repo.increment_topic_stats(
            user_id=user_id,
            topic_id=question.topic_id,
            is_correct=is_correct,
            timestamp=timestamp
        )

        logger.info(f"Stats updated for user {user_id}")

        # Prepare response
        response_data = {
            'correct': is_correct,
            'explanation': question.explanation,
            'source_reference': {
                'document': question.source_reference.document,
                'page': question.source_reference.page,
                'section': question.source_reference.section
            }
        }

        # Include correct answer if user was wrong
        if not is_correct:
            response_data['correct_answer'] = question.correct_answer

        return success_response(
            data=response_data,
            message="Answer submitted successfully"
        )

    except ValueError as e:
        logger.error(f"Authorization error: {str(e)}")
        return error_response(message="Unauthorized", status_code=401)

    except json.JSONDecodeError:
        return validation_error_response(message="Invalid JSON in request body")

    except Exception as e:
        logger.error(f"Error submitting answer: {str(e)}", exc_info=True)
        return internal_server_error_response(
            message="Failed to submit answer",
            include_details=False
        )
