"""
Lambda handler for getting a specific topic by ID.

GET /topics/{topicId}
"""

import json
from typing import Any, Dict
from ...repositories.topic_repository import TopicRepository
from ...utils import (
    success_response,
    error_response,
    not_found_response,
    internal_server_error_response,
    extract_user_id_from_event,
    validate_topic_id,
    get_logger,
    log_api_request,
)


logger = get_logger(__name__)
topic_repo = TopicRepository()


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Get a specific topic by ID.

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

        # Get topic_id from path parameters
        path_params = event.get('pathParameters') or {}
        topic_id = path_params.get('topicId')

        if not topic_id:
            return error_response(
                message="Missing topic_id in path",
                status_code=400
            )

        # Validate topic_id format
        if not validate_topic_id(topic_id):
            return error_response(
                message="Invalid topic_id format",
                status_code=400
            )

        # Fetch topic
        logger.info(f"Fetching topic: {topic_id}")
        topic = topic_repo.get_by_id(topic_id)

        if not topic:
            return not_found_response(message=f"Topic {topic_id} not found")

        # Convert to API response format
        topic_data = topic.to_api_response()

        return success_response(data={'topic': topic_data})

    except ValueError as e:
        # User ID extraction failed (should not happen with authorizer)
        logger.error(f"Authorization error: {str(e)}")
        return error_response(
            message="Unauthorized",
            status_code=401
        )

    except Exception as e:
        logger.error(f"Error fetching topic: {str(e)}", exc_info=True)
        return internal_server_error_response(
            message="Failed to fetch topic",
            include_details=False
        )
