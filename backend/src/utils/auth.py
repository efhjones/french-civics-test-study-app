"""
Authentication utilities for extracting user information from JWT tokens.
"""

from typing import Optional, Dict, Any


def extract_user_id_from_event(event: Dict[str, Any]) -> str:
    """
    Extract user_id (Cognito sub) from API Gateway event.

    CRITICAL SECURITY: This is the ONLY way to get user_id.
    NEVER accept user_id from request body or query parameters.

    Args:
        event: API Gateway Lambda proxy event

    Returns:
        User ID (Cognito sub claim)

    Raises:
        ValueError: If user_id cannot be extracted (unauthorized request)
    """
    try:
        # Extract from Cognito authorizer claims
        authorizer = event.get('requestContext', {}).get('authorizer', {})
        claims = authorizer.get('claims', {})

        user_id = claims.get('sub')

        if not user_id:
            raise ValueError('Missing user_id in JWT claims')

        return user_id

    except (KeyError, AttributeError) as e:
        raise ValueError(f'Failed to extract user_id from event: {str(e)}')


def extract_user_email_from_event(event: Dict[str, Any]) -> Optional[str]:
    """
    Extract user email from API Gateway event.

    Args:
        event: API Gateway Lambda proxy event

    Returns:
        User email if available, None otherwise
    """
    try:
        authorizer = event.get('requestContext', {}).get('authorizer', {})
        claims = authorizer.get('claims', {})
        return claims.get('email')
    except (KeyError, AttributeError):
        return None


def extract_cognito_username_from_event(event: Dict[str, Any]) -> Optional[str]:
    """
    Extract Cognito username from API Gateway event.

    Args:
        event: API Gateway Lambda proxy event

    Returns:
        Cognito username if available, None otherwise
    """
    try:
        authorizer = event.get('requestContext', {}).get('authorizer', {})
        claims = authorizer.get('claims', {})
        return claims.get('cognito:username')
    except (KeyError, AttributeError):
        return None


def get_all_claims(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get all JWT claims from the event.

    Useful for debugging or extracting custom claims.

    Args:
        event: API Gateway Lambda proxy event

    Returns:
        Dictionary of all claims
    """
    try:
        authorizer = event.get('requestContext', {}).get('authorizer', {})
        return authorizer.get('claims', {})
    except (KeyError, AttributeError):
        return {}
