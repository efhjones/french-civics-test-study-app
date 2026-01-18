"""
Repository for Topics table operations.
"""

import os
from typing import List, Optional
from boto3.dynamodb.conditions import Key
from .base_repository import BaseRepository
from ..models.topic import Topic


class TopicRepository(BaseRepository):
    """
    Repository for managing topic data.
    """

    def __init__(self):
        table_name = os.getenv('TOPICS_TABLE', 'FrenchCivics-Topics')
        super().__init__(table_name)

    def get_by_id(self, topic_id: str) -> Optional[Topic]:
        """
        Get topic by ID.

        Args:
            topic_id: Topic ID

        Returns:
            Topic instance if found, None otherwise
        """
        item = self.get_item({'topic_id': topic_id})
        return Topic.from_dynamo(item) if item else None

    def create(self, topic: Topic) -> None:
        """
        Create a new topic.

        Args:
            topic: Topic instance to create
        """
        self.put_item(topic.to_dynamo())

    def list_all(self) -> List[Topic]:
        """
        List all topics.

        Returns:
            List of Topic instances
        """
        items = self.scan()
        return [Topic.from_dynamo(item) for item in items]

    def list_by_category(self, category: str) -> List[Topic]:
        """
        List topics in a specific category, sorted by display_order.

        Args:
            category: Category name

        Returns:
            List of Topic instances sorted by display_order
        """
        items = self.query(
            key_condition_expression=Key('category').eq(category),
            expression_attribute_values={},  # Handled by Key()
            index_name='GSI1-category-displayOrder',
            scan_index_forward=True  # Ascending order
        )
        return [Topic.from_dynamo(item) for item in items]

    def batch_create(self, topics: List[Topic]) -> None:
        """
        Batch create multiple topics.

        Args:
            topics: List of Topic instances
        """
        items = [topic.to_dynamo() for topic in topics]
        self.batch_write_items(items)

    def topic_exists(self, topic_id: str) -> bool:
        """
        Check if topic exists.

        Args:
            topic_id: Topic ID

        Returns:
            True if topic exists, False otherwise
        """
        return self.get_by_id(topic_id) is not None
