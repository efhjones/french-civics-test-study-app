"""
User data model.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """
    Represents a user in the system.

    Attributes are mapped to DynamoDB Users table attributes.
    """

    user_id: str                    # Cognito sub (UUID)
    email: str                      # From Cognito
    cognito_username: str           # Cognito username
    created_at: str                 # ISO 8601 timestamp
    last_login: str                 # ISO 8601 timestamp
    name: Optional[str] = None      # Optional display name

    @classmethod
    def from_dynamo(cls, item: dict) -> 'User':
        """
        Create User instance from DynamoDB item.

        Args:
            item: DynamoDB item dict

        Returns:
            User instance
        """
        return cls(
            user_id=item['user_id'],
            email=item['email'],
            cognito_username=item['cognito_username'],
            created_at=item['created_at'],
            last_login=item['last_login'],
            name=item.get('name')
        )

    def to_dynamo(self) -> dict:
        """
        Convert User to DynamoDB item format.

        Returns:
            Dict suitable for DynamoDB PutItem/UpdateItem
        """
        item = {
            'user_id': self.user_id,
            'email': self.email,
            'cognito_username': self.cognito_username,
            'created_at': self.created_at,
            'last_login': self.last_login
        }

        if self.name:
            item['name'] = self.name

        return item

    def to_api_response(self) -> dict:
        """
        Convert User to API response format.

        Returns:
            Dict for JSON serialization
        """
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name or self.email.split('@')[0],
            'created_at': self.created_at,
            'last_login': self.last_login
        }
