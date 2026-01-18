"""
Repository for Users table operations.
"""

import os
from datetime import datetime
from typing import Optional
from .base_repository import BaseRepository
from ..models.user import User


class UserRepository(BaseRepository):
    """
    Repository for managing user data.
    """

    def __init__(self):
        table_name = os.getenv('USERS_TABLE', 'FrenchCivics-Users')
        super().__init__(table_name)

    def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User's Cognito sub

        Returns:
            User instance if found, None otherwise
        """
        item = self.get_item({'user_id': user_id})
        return User.from_dynamo(item) if item else None

    def create(self, user: User) -> None:
        """
        Create a new user.

        Args:
            user: User instance to create
        """
        self.put_item(user.to_dynamo())

    def update_last_login(self, user_id: str) -> User:
        """
        Update user's last login timestamp.

        Args:
            user_id: User's Cognito sub

        Returns:
            Updated User instance
        """
        updated_item = self.update_item(
            key={'user_id': user_id},
            update_expression='SET last_login = :timestamp',
            expression_attribute_values={
                ':timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        )
        return User.from_dynamo(updated_item)

    def update_profile(self, user_id: str, name: Optional[str] = None) -> User:
        """
        Update user profile information.

        Args:
            user_id: User's Cognito sub
            name: Optional display name

        Returns:
            Updated User instance
        """
        update_parts = []
        attribute_values = {}

        if name is not None:
            update_parts.append('name = :name')
            attribute_values[':name'] = name

        if not update_parts:
            # No updates to make
            return self.get_by_id(user_id)

        update_expression = 'SET ' + ', '.join(update_parts)

        updated_item = self.update_item(
            key={'user_id': user_id},
            update_expression=update_expression,
            expression_attribute_values=attribute_values
        )
        return User.from_dynamo(updated_item)

    def user_exists(self, user_id: str) -> bool:
        """
        Check if user exists.

        Args:
            user_id: User's Cognito sub

        Returns:
            True if user exists, False otherwise
        """
        return self.get_by_id(user_id) is not None
