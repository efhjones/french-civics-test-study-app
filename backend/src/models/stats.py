"""
User statistics data model.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class CategoryStats:
    """Statistics for a single category."""
    total: int
    correct: int
    accuracy: float
    last_answered: str


@dataclass
class TopicStats:
    """Statistics for a single topic."""
    total: int
    correct: int
    accuracy: float
    recent_accuracy: float
    last_answered: str


@dataclass
class TopicRanking:
    """Ranking entry for weakest/strongest topics."""
    topic_id: str
    topic_name: str
    accuracy: float


@dataclass
class UserStats:
    """
    Represents cached user performance statistics.

    Attributes are mapped to DynamoDB UserStats table attributes.
    """

    user_id: str
    last_updated: str
    total_questions_answered: int
    overall_accuracy: float
    accuracy_by_category: Dict[str, CategoryStats]
    accuracy_by_topic: Dict[str, TopicStats]
    weakest_topics: list[TopicRanking]
    strongest_topics: list[TopicRanking]
    current_streak_days: int
    longest_streak_days: int
    last_activity_date: str

    @classmethod
    def from_dynamo(cls, item: dict) -> 'UserStats':
        """
        Create UserStats instance from DynamoDB item.

        Args:
            item: DynamoDB item dict

        Returns:
            UserStats instance
        """
        # Parse category stats
        accuracy_by_category = {}
        for category, stats_data in item.get('accuracy_by_category', {}).items():
            accuracy_by_category[category] = CategoryStats(
                total=int(stats_data['total']),
                correct=int(stats_data['correct']),
                accuracy=float(stats_data['accuracy']),
                last_answered=stats_data['last_answered']
            )

        # Parse topic stats
        accuracy_by_topic = {}
        for topic_id, stats_data in item.get('accuracy_by_topic', {}).items():
            accuracy_by_topic[topic_id] = TopicStats(
                total=int(stats_data['total']),
                correct=int(stats_data['correct']),
                accuracy=float(stats_data['accuracy']),
                recent_accuracy=float(stats_data['recent_accuracy']),
                last_answered=stats_data['last_answered']
            )

        # Parse weakest topics
        weakest_topics = [
            TopicRanking(
                topic_id=t['topic_id'],
                topic_name=t['topic_name'],
                accuracy=float(t['accuracy'])
            )
            for t in item.get('weakest_topics', [])
        ]

        # Parse strongest topics
        strongest_topics = [
            TopicRanking(
                topic_id=t['topic_id'],
                topic_name=t['topic_name'],
                accuracy=float(t['accuracy'])
            )
            for t in item.get('strongest_topics', [])
        ]

        return cls(
            user_id=item['user_id'],
            last_updated=item['last_updated'],
            total_questions_answered=int(item['total_questions_answered']),
            overall_accuracy=float(item['overall_accuracy']),
            accuracy_by_category=accuracy_by_category,
            accuracy_by_topic=accuracy_by_topic,
            weakest_topics=weakest_topics,
            strongest_topics=strongest_topics,
            current_streak_days=int(item.get('current_streak_days', 0)),
            longest_streak_days=int(item.get('longest_streak_days', 0)),
            last_activity_date=item.get('last_activity_date', '')
        )

    def to_dynamo(self) -> dict:
        """
        Convert UserStats to DynamoDB item format.

        Returns:
            Dict suitable for DynamoDB PutItem
        """
        # Convert category stats
        accuracy_by_category = {}
        for category, stats in self.accuracy_by_category.items():
            accuracy_by_category[category] = {
                'total': stats.total,
                'correct': stats.correct,
                'accuracy': stats.accuracy,
                'last_answered': stats.last_answered
            }

        # Convert topic stats
        accuracy_by_topic = {}
        for topic_id, stats in self.accuracy_by_topic.items():
            accuracy_by_topic[topic_id] = {
                'total': stats.total,
                'correct': stats.correct,
                'accuracy': stats.accuracy,
                'recent_accuracy': stats.recent_accuracy,
                'last_answered': stats.last_answered
            }

        # Convert weakest topics
        weakest_topics = [
            {
                'topic_id': t.topic_id,
                'topic_name': t.topic_name,
                'accuracy': t.accuracy
            }
            for t in self.weakest_topics
        ]

        # Convert strongest topics
        strongest_topics = [
            {
                'topic_id': t.topic_id,
                'topic_name': t.topic_name,
                'accuracy': t.accuracy
            }
            for t in self.strongest_topics
        ]

        return {
            'user_id': self.user_id,
            'last_updated': self.last_updated,
            'total_questions_answered': self.total_questions_answered,
            'overall_accuracy': self.overall_accuracy,
            'accuracy_by_category': accuracy_by_category,
            'accuracy_by_topic': accuracy_by_topic,
            'weakest_topics': weakest_topics,
            'strongest_topics': strongest_topics,
            'current_streak_days': self.current_streak_days,
            'longest_streak_days': self.longest_streak_days,
            'last_activity_date': self.last_activity_date
        }

    def to_api_response(self) -> dict:
        """
        Convert UserStats to API response format.

        Returns:
            Dict for JSON serialization
        """
        return {
            'total_questions_answered': self.total_questions_answered,
            'overall_accuracy': round(self.overall_accuracy, 1),
            'accuracy_by_category': {
                category: {
                    'total': stats.total,
                    'correct': stats.correct,
                    'accuracy': round(stats.accuracy, 1)
                }
                for category, stats in self.accuracy_by_category.items()
            },
            'weakest_topics': [
                {
                    'topic_id': t.topic_id,
                    'topic_name': t.topic_name,
                    'accuracy': round(t.accuracy, 1)
                }
                for t in self.weakest_topics
            ],
            'strongest_topics': [
                {
                    'topic_id': t.topic_id,
                    'topic_name': t.topic_name,
                    'accuracy': round(t.accuracy, 1)
                }
                for t in self.strongest_topics
            ],
            'current_streak_days': self.current_streak_days,
            'longest_streak_days': self.longest_streak_days,
            'last_activity_date': self.last_activity_date,
            'last_updated': self.last_updated
        }

    @staticmethod
    def create_empty(user_id: str, timestamp: str) -> 'UserStats':
        """
        Create an empty UserStats instance for a new user.

        Args:
            user_id: User's Cognito sub
            timestamp: Current timestamp

        Returns:
            Empty UserStats instance
        """
        return UserStats(
            user_id=user_id,
            last_updated=timestamp,
            total_questions_answered=0,
            overall_accuracy=0.0,
            accuracy_by_category={},
            accuracy_by_topic={},
            weakest_topics=[],
            strongest_topics=[],
            current_streak_days=0,
            longest_streak_days=0,
            last_activity_date=''
        )
