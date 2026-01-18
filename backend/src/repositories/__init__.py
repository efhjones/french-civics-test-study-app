"""
Data access repositories for DynamoDB tables.
"""

from .base_repository import BaseRepository
from .user_repository import UserRepository
from .topic_repository import TopicRepository
from .question_repository import QuestionRepository
from .result_repository import ResultRepository
from .stats_repository import StatsRepository

__all__ = [
    'BaseRepository',
    'UserRepository',
    'TopicRepository',
    'QuestionRepository',
    'ResultRepository',
    'StatsRepository',
]
