"""
Lambda handler for getting user profile.

GET /users/me
"""

import json
from datetime import datetime
from typing import Any, Dict
from repositories.user_repository import UserRepository
from models.user import User
from utils import (
    success_response,
    error_response,
    internal_server_error_response,
    extract_user_id_from_event,
    extract_user_email_from_event,
    get_all_claims,
    get_logger,
    log_api_request,
)


logger = get_logger(__name__)
user_repo = UserRepository()


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Get or create user profile.

    If the user doesn't exist in our database yet, create a profile
    from the Cognito JWT claims. Update last_login timestamp.

    Args:
        event: API Gateway Lambda proxy event
        context: Lambda context

    Returns:
        API Gateway Lambda proxy response
    """
    try:
        # Extract user info from JWT
        user_id = extract_user_id_from_event(event)
        email = extract_user_email_from_event(event)
        claims = get_all_claims(event)

        log_api_request(logger, event, user_id)

        # Check if user exists
        user = user_repo.get_by_id(user_id)

        if user:
            # User exists - update last login
            logger.info(f"Existing user found: {user_id}")
            user_repo.update_last_login(user_id)
            user.last_login = datetime.utcnow().isoformat() + 'Z'
        else:
            # New user - create profile from JWT claims
            logger.info(f"New user detected: {user_id}, creating profile")

            timestamp = datetime.utcnow().isoformat() + 'Z'
            cognito_username = claims.get('cognito:username', email)
            name = claims.get('name') or claims.get('given_name')

            user = User(
                user_id=user_id,
                email=email,
                cognito_username=cognito_username,
                created_at=timestamp,
                last_login=timestamp,
                name=name
            )

            user_repo.create(user)
            logger.info(f"User profile created: {user_id}")

        # Convert to API response format
        user_data = user.to_api_response()

        return success_response(
            data={'user': user_data},
            message="User profile retrieved successfully"
        )

    except ValueError as e:
        logger.error(f"Authorization error: {str(e)}")
        return error_response(message="Unauthorized", status_code=401)

    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}", exc_info=True)
        return internal_server_error_response(
            message="Failed to get user profile",
            include_details=False
        )
