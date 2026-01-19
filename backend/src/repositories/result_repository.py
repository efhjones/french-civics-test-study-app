"""
Repository for UserQuestionResults table operations.
"""

import os
from datetime import datetime, timedelta
from typing import List, Optional
from boto3.dynamodb.conditions import Key
from repositories.base_repository import BaseRepository
from models.result import UserQuestionResult


class ResultRepository(BaseRepository):
    """
    Repository for managing user question results.
    """

    def __init__(self):
        table_name = os.getenv('RESULTS_TABLE', 'FrenchCivics-UserQuestionResults')
        super().__init__(table_name)

    def create(self, result: UserQuestionResult) -> None:
        """
        Create a new result record.

        Args:
            result: UserQuestionResult instance to create
        """
        self.put_item(result.to_dynamo())

    def get_user_history(
        self,
        user_id: str,
        limit: Optional[int] = 50,
        newest_first: bool = True
    ) -> List[UserQuestionResult]:
        """
        Get user's answer history.

        Args:
            user_id: User's Cognito sub
            limit: Maximum number of results (default: 50)
            newest_first: Sort order (default: True for descending)

        Returns:
            List of UserQuestionResult instances
        """
        items = self.query(
            key_condition_expression=Key('user_id').eq(user_id),
            expression_attribute_values={},
            scan_index_forward=not newest_first,
            limit=limit
        )
        return [UserQuestionResult.from_dynamo(item) for item in items]

    def get_recent_results(
        self,
        user_id: str,
        days: int = 7
    ) -> List[UserQuestionResult]:
        """
        Get user's results from the last N days.

        Args:
            user_id: User's Cognito sub
            days: Number of days to look back (default: 7)

        Returns:
            List of UserQuestionResult instances
        """
        since_date = datetime.utcnow() - timedelta(days=days)
        since_timestamp = since_date.isoformat() + 'Z'

        items = self.query(
            key_condition_expression=Key('user_id').eq(user_id) & Key('result_id').gte(since_timestamp),
            expression_attribute_values={},
            scan_index_forward=False  # Newest first
        )
        return [UserQuestionResult.from_dynamo(item) for item in items]

    def get_results_by_topic(
        self,
        user_id: str,
        topic_id: str,
        limit: Optional[int] = None
    ) -> List[UserQuestionResult]:
        """
        Get user's results for a specific topic.

        Note: This requires scanning through results since we don't have
        a direct GSI on user_id#topic_id. For production, consider adding GSI.

        Args:
            user_id: User's Cognito sub
            topic_id: Topic ID
            limit: Optional result limit

        Returns:
            List of UserQuestionResult instances
        """
        all_results = self.get_user_history(user_id, limit=None)
        filtered_results = [r for r in all_results if r.topic_id == topic_id]

        if limit:
            filtered_results = filtered_results[:limit]

        return filtered_results

    def count_user_results(self, user_id: str) -> int:
        """
        Count total number of questions answered by user.

        Args:
            user_id: User's Cognito sub

        Returns:
            Count of results
        """
        items = self.query(
            key_condition_expression=Key('user_id').eq(user_id),
            expression_attribute_values={}
        )
        return len(items)

    def get_accuracy_for_topic(
        self,
        user_id: str,
        topic_id: str
    ) -> tuple[int, int, float]:
        """
        Calculate accuracy for a specific topic.

        Args:
            user_id: User's Cognito sub
            topic_id: Topic ID

        Returns:
            Tuple of (correct_count, total_count, accuracy_percentage)
        """
        results = self.get_results_by_topic(user_id, topic_id)

        if not results:
            return 0, 0, 0.0

        total = len(results)
        correct = sum(1 for r in results if r.correct)
        accuracy = (correct / total) * 100 if total > 0 else 0.0

        return correct, total, accuracy
