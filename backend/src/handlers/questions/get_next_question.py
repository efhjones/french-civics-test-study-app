"""
Lambda handler for getting the next question using adaptive learning.

GET /questions/next

Query parameters:
  - debug: Set to 'true' to include debug information about topic selection
"""

import json
from typing import Any, Dict
from repositories.question_repository import QuestionRepository
from repositories.result_repository import ResultRepository
from repositories.topic_repository import TopicRepository
from services.adaptive_learning import AdaptiveLearningService
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
result_repo = ResultRepository()
topic_repo = TopicRepository()
adaptive_service = AdaptiveLearningService()


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Get the next question using adaptive learning algorithm.

    The algorithm:
    1. Analyzes user performance across all topics
    2. Classifies topics as weak (<60%), medium (60-80%), or strong (>80%)
    3. Weights recent performance (last 7 days) more heavily
    4. Selects a topic using 60/30/10 distribution (weak/medium/strong)
    5. Selects a question from that topic (avoiding recently answered ones)

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

        # Get all user results for performance analysis
        logger.info(f"Fetching all results for user {user_id}")
        all_results = result_repo.get_user_history(user_id, limit=1000)

        # Get recent results (last 7 days) for filtering out recently answered questions
        recent_results = result_repo.get_recent_results(user_id, days=7)

        # Get all available questions
        logger.info("Fetching all available questions")
        all_questions = question_repo.list_all()

        if not all_questions:
            return error_response(
                message="No questions available in the database. Please seed questions first.",
                status_code=503
            )

        # Get list of topics that have questions
        available_topics = list(set(q.topic_id for q in all_questions))
        logger.info(f"Found {len(all_questions)} questions across {len(available_topics)} topics")

        # Use adaptive learning service to select next question
        selected_question, debug_info = adaptive_service.get_next_question(
            all_results=all_results,
            recent_results=recent_results,
            all_questions=all_questions,
            available_topics=available_topics
        )

        if not selected_question:
            return error_response(
                message="Unable to select a question. This is unusual.",
                status_code=500
            )

        logger.info(f"Selected question {selected_question.question_id} from topic {selected_question.topic_id}")

        # Convert to API response format (hides correct answer)
        question_data = selected_question.to_api_response(include_answer=False)

        # Prepare response
        response_data = {'question': question_data}

        # Include debug info if requested
        if debug_mode:
            response_data['debug'] = debug_info

        return success_response(
            data=response_data,
            message="Next question selected using adaptive learning"
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
