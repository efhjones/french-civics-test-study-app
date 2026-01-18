"""
User question result data model.
"""

from dataclasses import dataclass


@dataclass
class UserQuestionResult:
    """
    Represents a single answer submission by a user.

    Attributes are mapped to DynamoDB UserQuestionResults table attributes.
    """

    user_id: str
    result_id: str              # Composite: "{timestamp}#{question_id}"
    question_id: str
    topic_id: str
    category: str
    answered_at: str            # ISO 8601 timestamp
    correct: bool
    user_answer: str
    response_time_ms: int
    difficulty: int

    @classmethod
    def from_dynamo(cls, item: dict) -> 'UserQuestionResult':
        """
        Create UserQuestionResult instance from DynamoDB item.

        Args:
            item: DynamoDB item dict

        Returns:
            UserQuestionResult instance
        """
        return cls(
            user_id=item['user_id'],
            result_id=item['result_id'],
            question_id=item['question_id'],
            topic_id=item['topic_id'],
            category=item['category'],
            answered_at=item['answered_at'],
            correct=item['correct'],
            user_answer=item['user_answer'],
            response_time_ms=item['response_time_ms'],
            difficulty=item['difficulty']
        )

    def to_dynamo(self) -> dict:
        """
        Convert UserQuestionResult to DynamoDB item format.

        Returns:
            Dict suitable for DynamoDB PutItem
        """
        return {
            'user_id': self.user_id,
            'result_id': self.result_id,
            'question_id': self.question_id,
            'topic_id': self.topic_id,
            'category': self.category,
            'answered_at': self.answered_at,
            'correct': self.correct,
            'user_answer': self.user_answer,
            'response_time_ms': self.response_time_ms,
            'difficulty': self.difficulty
        }

    def to_api_response(self) -> dict:
        """
        Convert UserQuestionResult to API response format.

        Returns:
            Dict for JSON serialization
        """
        return {
            'question_id': self.question_id,
            'topic_id': self.topic_id,
            'category': self.category,
            'answered_at': self.answered_at,
            'correct': self.correct,
            'user_answer': self.user_answer,
            'response_time_ms': self.response_time_ms,
            'difficulty': self.difficulty
        }

    @staticmethod
    def create_result_id(timestamp: str, question_id: str) -> str:
        """
        Create composite result_id for sort key.

        Args:
            timestamp: ISO 8601 timestamp
            question_id: Question UUID

        Returns:
            Composite ID string
        """
        return f"{timestamp}#{question_id}"

    @staticmethod
    def parse_result_id(result_id: str) -> tuple[str, str]:
        """
        Parse composite result_id into timestamp and question_id.

        Args:
            result_id: Composite ID string

        Returns:
            Tuple of (timestamp, question_id)
        """
        parts = result_id.split('#', 1)
        return parts[0], parts[1]
