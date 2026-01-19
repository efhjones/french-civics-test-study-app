"""
Data access repositories for DynamoDB tables.
"""

from repositories.base_repository import BaseRepository
from repositories.user_repository import UserRepository
from repositories.topic_repository import TopicRepository
from repositories.question_repository import QuestionRepository
from repositories.result_repository import ResultRepository
from repositories.stats_repository import StatsRepository

__all__ = [
    'BaseRepository',
    'UserRepository',
    'TopicRepository',
    'QuestionRepository',
    'ResultRepository',
    'StatsRepository',
]
