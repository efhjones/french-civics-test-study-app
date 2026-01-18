"""
Lambda handler for listing topics.

GET /topics
Optional query parameters:
  - category: Filter by category name
"""

import json
from typing import Any, Dict
from ...repositories.topic_repository import TopicRepository
from ...utils import (
    success_response,
    error_response,
    internal_server_error_response,
    extract_user_id_from_event,
    get_logger,
    log_api_request,
)


logger = get_logger(__name__)
topic_repo = TopicRepository()


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    List all topics, optionally filtered by category.

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

        # Get query parameters
        query_params = event.get('queryStringParameters') or {}
        category = query_params.get('category')

        # Fetch topics
        if category:
            logger.info(f"Listing topics for category: {category}")
            topics = topic_repo.list_by_category(category)
        else:
            logger.info("Listing all topics")
            topics = topic_repo.list_all()

        # Convert to API response format
        topics_data = [topic.to_api_response() for topic in topics]

        return success_response(
            data={
                'topics': topics_data,
                'count': len(topics_data)
            }
        )

    except ValueError as e:
        # User ID extraction failed (should not happen with authorizer)
        logger.error(f"Authorization error: {str(e)}")
        return error_response(
            message="Unauthorized",
            status_code=401
        )

    except Exception as e:
        logger.error(f"Error listing topics: {str(e)}", exc_info=True)
        return internal_server_error_response(
            message="Failed to list topics",
            include_details=False  # Set to True in development
        )
