"""
Data models for the French Civics Test application.

This package contains dataclasses that map to DynamoDB table schemas
and provide serialization/deserialization methods.
"""

from .user import User
from .topic import Topic, SourceReference
from .question import Question, AnswerOption, QuestionSourceReference
from .result import UserQuestionResult
from .stats import (
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
