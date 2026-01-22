"""
Lambda handler for getting the next question from user's question pool.

GET /questions/next

Query parameters:
  - debug: Set to 'true' to include debug information
"""

import json
from typing import Any, Dict
from repositories.question_repository import QuestionRepository, Question
from repositories.stats_repository import StatsRepository
from utils import (
    success_response,
    error_response,
    internal_server_error_response,
    extract_user_id_from_event,
    get_logger,
    log_api_request,
)


logger = get_logger(__name__)
question_repo = QuestionRepository()
stats_repo = StatsRepository()


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Get the next question from user's question pool.

    The logic:
    1. Get user's stats (contains unanswered_questions pool)
    2. If no stats exist, initialize with all questions
    3. If unanswered_questions is empty, reset pool (move answered back)
    4. Pick first question from unanswered_questions
    5. Return question details

    Args:
        event: API Gateway Lambda proxy event
        context: Lambda context

    Returns:
        API Gateway Lambda proxy response with question (without correct answer)
    """
    try:
        # Extract user_id from JWT
        user_id = extract_user_id_from_event(event)
        log_api_request(logger, event, user_id)

        # Check if debug mode is enabled
        query_params = event.get('queryStringParameters') or {}
        debug_mode = query_params.get('debug', '').lower() == 'true'

        # Get user stats (contains question pools)
        logger.info(f"Fetching stats for user {user_id}")
        stats = stats_repo.get_by_user_id(user_id)

        # Initialize if doesn't exist
        if not stats:
            logger.info(f"No stats found for user {user_id}, initializing...")
            stats = stats_repo.initialize_for_user(user_id)
            logger.info(f"Initialized stats with {len(stats.unanswered_questions)} questions")

        # Check if we need to reset (all questions answered)
        if not stats.unanswered_questions:
            logger.info(f"User {user_id} completed all questions, resetting pool...")
            import random
            from datetime import datetime

            def myFunc(question: Question):
                return question.question_id

            # Move all answered back to unanswered
            stats.unanswered_questions = list(map(myFunc, question_repo.list_all()))
            stats.answered_questions = []

            # Shuffle for variety
            random.shuffle(stats.unanswered_questions)

            # Update timestamp
            stats.last_updated = datetime.utcnow().isoformat() + 'Z'

            # Save the reset
            stats_repo.create_or_update(stats)
            logger.info(f"Reset complete, {len(stats.unanswered_questions)} questions available")

        # Pick next question from unanswered pool (first one)
        next_question_id = stats.unanswered_questions[0]
        logger.info(f"Selected question {next_question_id} from pool of {len(stats.unanswered_questions)} unanswered")

        # Fetch full question details
        selected_question = question_repo.get_by_id(next_question_id)

        if not selected_question:
            logger.error(f"Question {next_question_id} not found in database")
            return error_response(
                message="Question not found in database",
                status_code=500
            )

        # Convert to API response format (hides correct answer)
        question_data = selected_question.to_api_response(include_answer=False)

        # Prepare response
        response_data = {'question': question_data}

        # Include debug info if requested
        if debug_mode:
            response_data['debug'] = {
                'unanswered_remaining': len(stats.unanswered_questions),
                'answered_count': len(stats.answered_questions),
                'total_questions': len(stats.unanswered_questions) + len(stats.answered_questions)
            }

        return success_response(
            data=response_data,
            message="Next question selected from pool"
        )

    except ValueError as e:
        logger.error(f"Authorization error: {str(e)}")
        return error_response(message="Unauthorized", status_code=401)

    except Exception as e:
        logger.error(f"Error getting next question: {str(e)}", exc_info=True)
        return internal_server_error_response(
            message="Failed to get next question",
            include_details=False
        )
