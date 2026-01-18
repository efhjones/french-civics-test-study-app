"""
Repository for Questions table operations.
"""

import os
from typing import List, Optional
from boto3.dynamodb.conditions import Key
from .base_repository import BaseRepository
from ..models.question import Question


class QuestionRepository(BaseRepository):
    """
    Repository for managing question data.
    """

    def __init__(self):
        table_name = os.getenv('QUESTIONS_TABLE', 'FrenchCivics-Questions')
        super().__init__(table_name)

    def get_by_id(self, question_id: str) -> Optional[Question]:
        """
        Get question by ID.

        Args:
            question_id: Question ID

        Returns:
            Question instance if found, None otherwise
        """
        item = self.get_item({'question_id': question_id})
        return Question.from_dynamo(item) if item else None

    def create(self, question: Question) -> None:
        """
        Create a new question.

        Args:
            question: Question instance to create
        """
        self.put_item(question.to_dynamo())

    def list_by_topic(
        self,
        topic_id: str,
        difficulty: Optional[int] = None
    ) -> List[Question]:
        """
        List questions for a specific topic, optionally filtered by difficulty.

        Args:
            topic_id: Topic ID
            difficulty: Optional difficulty level (1, 2, or 3)

        Returns:
            List of Question instances
        """
        if difficulty:
            items = self.query(
                key_condition_expression=Key('topic_id').eq(topic_id) & Key('difficulty').eq(difficulty),
                expression_attribute_values={},  # Handled by Key()
                index_name='GSI1-topic-difficulty'
            )
        else:
            items = self.query(
                key_condition_expression=Key('topic_id').eq(topic_id),
                expression_attribute_values={},
                index_name='GSI1-topic-difficulty'
            )

        return [Question.from_dynamo(item) for item in items]

    def list_by_category(
        self,
        category: str,
        limit: Optional[int] = None
    ) -> List[Question]:
        """
        List questions in a specific category.

        Args:
            category: Category name
            limit: Optional result limit

        Returns:
            List of Question instances
        """
        items = self.query(
            key_condition_expression=Key('category').eq(category),
            expression_attribute_values={},
            index_name='GSI2-category-created',
            scan_index_forward=False,  # Newest first
            limit=limit
        )
        return [Question.from_dynamo(item) for item in items]

    def batch_create(self, questions: List[Question]) -> None:
        """
        Batch create multiple questions.

        Args:
            questions: List of Question instances
        """
        items = [question.to_dynamo() for question in questions]
        self.batch_write_items(items)

    def question_exists(self, question_id: str) -> bool:
        """
        Check if question exists.

        Args:
            question_id: Question ID

        Returns:
            True if question exists, False otherwise
        """
        return self.get_by_id(question_id) is not None

    def count_by_topic(self, topic_id: str) -> int:
        """
        Count questions for a specific topic.

        Args:
            topic_id: Topic ID

        Returns:
            Number of questions
        """
        items = self.list_by_topic(topic_id)
        return len(items)
