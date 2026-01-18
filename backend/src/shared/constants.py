"""
Shared constants for the French Civics Test application.
"""

from enum import Enum
from typing import Final

# Learning Categories
class Category(str, Enum):
    """Four main learning domains for French civics."""
    FRENCH_HISTORY = "French History"
    FRENCH_POLITICS = "French Politics and Institutions"
    FRENCH_GEOGRAPHY = "French Geography"
    FRENCH_CULTURE = "French Culture"


# Question Types
class QuestionType(str, Enum):
    """Supported question formats."""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"


# Question Difficulty Levels
class Difficulty(int, Enum):
    """Difficulty ratings for questions."""
    EASY = 1
    MEDIUM = 2
    HARD = 3


# Question Generation Sources
class GeneratedBy(str, Enum):
    """Source of question creation."""
    MANUAL = "manual"
    AI = "ai"


# Adaptive Learning Weights
class AdaptiveLearningWeights:
    """Distribution of questions by performance level."""
    WEAK_TOPICS_WEIGHT: Final[float] = 0.60    # 60% weak topics
    MEDIUM_TOPICS_WEIGHT: Final[float] = 0.30  # 30% medium topics
    STRONG_TOPICS_WEIGHT: Final[float] = 0.10  # 10% strong topics

    # Performance thresholds
    WEAK_THRESHOLD: Final[float] = 60.0        # < 60% accuracy = weak
    STRONG_THRESHOLD: Final[float] = 80.0      # > 80% accuracy = strong

    # Recent answer weighting
    RECENT_DAYS: Final[int] = 7                # Last 7 days weighted more heavily
    RECENT_WEIGHT: Final[float] = 0.70         # 70% weight on recent answers
    HISTORICAL_WEIGHT: Final[float] = 0.30     # 30% weight on older answers


# DynamoDB Table Names (populated from environment)
class TableNames:
    """DynamoDB table name constants."""
    USERS: Final[str] = "FrenchCivics-Users"
    TOPICS: Final[str] = "FrenchCivics-Topics"
    QUESTIONS: Final[str] = "FrenchCivics-Questions"
    RESULTS: Final[str] = "FrenchCivics-UserQuestionResults"
    STATS: Final[str] = "FrenchCivics-UserStats"


# S3 Configuration
class S3Config:
    """S3 bucket and object key constants."""
    BUCKET_NAME: Final[str] = "french-civics-livret-content-dev"

    # Object keys
    SOURCE_PDF: Final[str] = "source/Livret_du_citoyen_V2fev2022_accessible.pdf"
    EMBEDDINGS: Final[str] = "embeddings/livret-embeddings.json"
    CHUNKS: Final[str] = "embeddings/livret-chunks.json"


# Livret du Citoyen Metadata
class LivretMetadata:
    """Information about the source document."""
    DOCUMENT_NAME: Final[str] = "Livret du citoyen"
    TOTAL_PAGES: Final[int] = 28
    VERSION: Final[str] = "Février 2022"
    PUBLISHER: Final[str] = "Ministère de l'Intérieur"


# API Response Codes
class ResponseCode(str, Enum):
    """Standard API response status codes."""
    SUCCESS = "success"
    ERROR = "error"
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    INSUFFICIENT_INFORMATION = "insufficient_information"  # For AI RAG


# Validation Constants
class ValidationLimits:
    """Input validation boundaries."""
    MIN_RESPONSE_TIME_MS: Final[int] = 100          # Minimum plausible response time
    MAX_RESPONSE_TIME_MS: Final[int] = 300_000      # 5 minutes max

    MAX_QUESTION_LENGTH: Final[int] = 500           # Characters
    MAX_ANSWER_LENGTH: Final[int] = 200             # Characters
    MAX_EXPLANATION_LENGTH: Final[int] = 1000       # Characters

    MIN_ANSWER_OPTIONS: Final[int] = 2
    MAX_ANSWER_OPTIONS: Final[int] = 6

    MIN_QUESTIONS_PER_TOPIC: Final[int] = 5         # Minimum for adaptive learning


# Statistics Display
class StatsConfig:
    """Configuration for statistics calculation and display."""
    WEAK_TOPICS_DISPLAY_COUNT: Final[int] = 3       # Show top 3 weakest topics
    STRONG_TOPICS_DISPLAY_COUNT: Final[int] = 3     # Show top 3 strongest topics

    HISTORY_DEFAULT_LIMIT: Final[int] = 50          # Default results to return
    HISTORY_MAX_LIMIT: Final[int] = 500             # Maximum results per request

    STREAK_GRACE_PERIOD_HOURS: Final[int] = 36     # Allow 1.5 days between activity
