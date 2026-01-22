"""
Lambda handler for getting user answer history.

GET /users/me/history

Query parameters:
  - limit: Number of results to return (default: 50, max: 200)
  - topic_id: Filter by specific topic
  - days: Only return results from last N days (default: all)
"""

import json
from typing import Any, Dict
from repositories.result_repository import ResultRepository
from utils import (
    success_response,
    error_response,
    validation_error_response,
    internal_server_error_response,
    extract_user_id_from_event,
    get_logger,
    log_api_request,
)


logger = get_logger(__name__)
result_repo = ResultRepository()


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Get user answer history with optional filtering.

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

        # Parse query parameters
        query_params = event.get('queryStringParameters') or {}

        # Limit parameter (default: 50, max: 200)
        try:
            limit = int(query_params.get('limit', '50'))
            if limit < 1 or limit > 200:
                return validation_error_response(
                    message="Limit must be between 1 and 200"
                )
        except ValueError:
            return validation_error_response(message="Invalid limit parameter")

        # Days parameter (filter by recency)
        days = None
        if 'days' in query_params:
            try:
                days = int(query_params['days'])
                if days < 1:
                    return validation_error_response(
                        message="Days must be positive"
                    )
            except ValueError:
                return validation_error_response(message="Invalid days parameter")

        # Topic filter
        topic_id = query_params.get('topic_id')

        # Fetch results based on filters
        if topic_id:
            logger.info(f"Fetching history for user {user_id}, topic {topic_id}, limit {limit}")
            results = result_repo.get_results_by_topic(
                user_id=user_id,
                topic_id=topic_id,
                limit=limit
            )
        elif days:
            logger.info(f"Fetching history for user {user_id}, last {days} days, limit {limit}")
            results = result_repo.get_recent_results(
                user_id=user_id,
                days=days
            )
            # Apply limit manually for recent results
            results = results[:limit]
        else:
            logger.info(f"Fetching history for user {user_id}, limit {limit}")
            results = result_repo.get_user_history(
                user_id=user_id,
                limit=limit
            )

        # Convert to API response format
        results_data = [result.to_api_response() for result in results]

        # Calculate summary stats from this result set
        total = len(results_data)
        correct_count = sum(1 for r in results_data if r['correct'])
        accuracy = (correct_count / total * 100) if total > 0 else 0

        return success_response(
            data={
                'results': results_data,
                'summary': {
                    'total': total,
                    'correct': correct_count,
                    'incorrect': total - correct_count,
                    'accuracy': round(accuracy, 1)
                }
            },
            message="Answer history retrieved successfully"
        )

    except ValueError as e:
        logger.error(f"Authorization error: {str(e)}")
        return error_response(message="Unauthorized", status_code=401)

    except Exception as e:
        logger.error(f"Error getting user history: {str(e)}", exc_info=True)
        return internal_server_error_response(
            message="Failed to get answer history",
            include_details=False
        )
