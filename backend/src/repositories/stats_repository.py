"""
Repository for UserStats table operations.
"""

import os
from datetime import datetime
from typing import Optional
from repositories.base_repository import BaseRepository
from models.stats import UserStats


class StatsRepository(BaseRepository):
    """
    Repository for managing user statistics.
    """

    def __init__(self):
        table_name = os.getenv('STATS_TABLE', 'FrenchCivics-UserStats')
        super().__init__(table_name)

    def get_by_user_id(self, user_id: str) -> Optional[UserStats]:
        """
        Get user statistics.

        Args:
            user_id: User's Cognito sub

        Returns:
            UserStats instance if found, None otherwise
        """
        item = self.get_item({'user_id': user_id})
        return UserStats.from_dynamo(item) if item else None

    def create_or_update(self, stats: UserStats) -> None:
        """
        Create or update user statistics.

        Args:
            stats: UserStats instance
        """
        self.put_item(stats.to_dynamo())

    def initialize_for_user(self, user_id: str) -> UserStats:
        """
        Initialize empty stats for a new user.

        Args:
            user_id: User's Cognito sub

        Returns:
            Initialized UserStats instance
        """
        timestamp = datetime.utcnow().isoformat() + 'Z'
        stats = UserStats.create_empty(user_id, timestamp)
        self.create_or_update(stats)
        return stats

    def increment_category_stats(
        self,
        user_id: str,
        category: str,
        is_correct: bool,
        timestamp: str
    ) -> None:
        """
        Increment category-level statistics.

        Args:
            user_id: User's Cognito sub
            category: Category name
            is_correct: Whether answer was correct
            timestamp: Current timestamp
        """
        from decimal import Decimal
        from botocore.exceptions import ClientError

        try:
            # Try to increment (assumes category exists)
            update_expression = """
                ADD total_questions_answered :inc
                SET stats_by_category.#cat.#total = stats_by_category.#cat.#total + :inc,
                    stats_by_category.#cat.#correct = stats_by_category.#cat.#correct + :correct_inc,
                    stats_by_category.#cat.last_answered = :timestamp,
                    last_updated = :timestamp
            """

            self.update_item(
                key={'user_id': user_id},
                update_expression=update_expression,
                expression_attribute_names={
                    '#cat': category,
                    '#total': 'total',
                    '#correct': 'correct'
                },
                expression_attribute_values={
                    ':inc': 1,
                    ':correct_inc': 1 if is_correct else 0,
                    ':timestamp': timestamp
                }
            )
        except Exception as e:
            if 'invalid for update' in str(e).lower() or 'document path' in str(e).lower():
                # Category doesn't exist, create it with initial values
                update_expression = """
                    ADD total_questions_answered :inc
                    SET stats_by_category.#cat = :new_category,
                        last_updated = :timestamp
                """

                self.update_item(
                    key={'user_id': user_id},
                    update_expression=update_expression,
                    expression_attribute_names={
                        '#cat': category
                    },
                    expression_attribute_values={
                        ':inc': 1,
                        ':new_category': {
                            'total': 1,
                            'correct': 1 if is_correct else 0,
                            'last_answered': timestamp
                        },
                        ':timestamp': timestamp
                    }
                )
            else:
                raise

    def increment_topic_stats(
        self,
        user_id: str,
        topic_id: str,
        is_correct: bool,
        timestamp: str
    ) -> None:
        """
        Increment topic-level statistics.

        Args:
            user_id: User's Cognito sub
            topic_id: Topic ID
            is_correct: Whether answer was correct
            timestamp: Current timestamp
        """
        from decimal import Decimal
        from botocore.exceptions import ClientError

        try:
            # Try to increment (assumes topic exists)
            update_expression = """
                SET stats_by_topic.#topic.#total = stats_by_topic.#topic.#total + :inc,
                    stats_by_topic.#topic.#correct = stats_by_topic.#topic.#correct + :correct_inc,
                    stats_by_topic.#topic.last_answered = :timestamp,
                    last_updated = :timestamp
            """

            self.update_item(
                key={'user_id': user_id},
                update_expression=update_expression,
                expression_attribute_names={
                    '#topic': topic_id,
                    '#total': 'total',
                    '#correct': 'correct'
                },
                expression_attribute_values={
                    ':inc': 1,
                    ':correct_inc': 1 if is_correct else 0,
                    ':timestamp': timestamp
                }
            )
        except Exception as e:
            if 'invalid for update' in str(e).lower() or 'document path' in str(e).lower():
                # Topic doesn't exist, create it with initial values
                update_expression = """
                    SET stats_by_topic.#topic = :new_topic,
                        last_updated = :timestamp
                """

                self.update_item(
                    key={'user_id': user_id},
                    update_expression=update_expression,
                    expression_attribute_names={
                        '#topic': topic_id
                    },
                    expression_attribute_values={
                        ':new_topic': {
                            'total': 1,
                            'correct': 1 if is_correct else 0,
                            'recent_accuracy': Decimal('0'),
                            'last_answered': timestamp
                        },
                        ':timestamp': timestamp
                    }
                )
            else:
                raise

    def update_streak(
        self,
        user_id: str,
        current_streak: int,
        longest_streak: int,
        last_activity_date: str
    ) -> None:
        """
        Update user's streak information.

        Args:
            user_id: User's Cognito sub
            current_streak: Current streak days
            longest_streak: Longest streak days
            last_activity_date: Date of last activity (YYYY-MM-DD)
        """
        self.update_item(
            key={'user_id': user_id},
            update_expression="""
                SET current_streak_days = :current,
                    longest_streak_days = :longest,
                    last_activity_date = :date
            """,
            expression_attribute_values={
                ':current': current_streak,
                ':longest': longest_streak,
                ':date': last_activity_date
            }
        )

    def stats_exist(self, user_id: str) -> bool:
        """
        Check if stats exist for user.

        Args:
            user_id: User's Cognito sub

        Returns:
            True if stats exist, False otherwise
        """
        return self.get_by_user_id(user_id) is not None
