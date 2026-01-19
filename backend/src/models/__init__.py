"""
Data models for the French Civics Test application.

This package contains dataclasses that map to DynamoDB table schemas
and provide serialization/deserialization methods.
"""

from models.user import User
from models.topic import Topic, SourceReference
from models.question import Question, AnswerOption, QuestionSourceReference
from models.result import UserQuestionResult
from models.stats import (
    UserStats,
    CategoryStats,
    TopicStats,
    TopicRanking
)

__all__ = [
    # User models
    'User',

    # Topic models
    'Topic',
    'SourceReference',

    # Question models
    'Question',
    'AnswerOption',
    'QuestionSourceReference',

    # Result models
    'UserQuestionResult',

    # Stats models
    'UserStats',
    'CategoryStats',
    'TopicStats',
    'TopicRanking',
]
