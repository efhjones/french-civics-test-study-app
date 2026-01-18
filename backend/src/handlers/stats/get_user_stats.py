"""
Lambda handler for getting user statistics.

GET /users/me/stats
"""

import json
from typing import Any, Dict
from ...repositories.stats_repository import StatsRepository
from ...utils import (
    success_response,
    error_response,
    internal_server_error_response,
    extract_user_id_from_event,
    get_logger,
    log_api_request,
)


logger = get_logger(__name__)
stats_repo = StatsRepository()


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Get user statistics.

    Returns cached statistics including:
    - Overall performance
    - Category breakdowns
    - Topic breakdowns
    - Current streak

    If stats don't exist yet, initialize them.

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

        # Get stats
        logger.info(f"Fetching stats for user: {user_id}")
        stats = stats_repo.get_by_user_id(user_id)

        if not stats:
            # Initialize stats if they don't exist
            logger.info(f"Stats not found for user {user_id}, initializing")
            stats = stats_repo.initialize_for_user(user_id)

        # Convert to API response format
        stats_data = stats.to_api_response()

        return success_response(
            data={'stats': stats_data},
            message="User statistics retrieved successfully"
        )

    except ValueError as e:
        logger.error(f"Authorization error: {str(e)}")
        return error_response(message="Unauthorized", status_code=401)

    except Exception as e:
        logger.error(f"Error getting user stats: {str(e)}", exc_info=True)
        return internal_server_error_response(
            message="Failed to get user statistics",
            include_details=False
        )
