"""
Adaptive learning algorithm for selecting the next question.

This module implements the core adaptive learning logic:
- Analyzes user performance across topics
- Classifies topics as weak/medium/strong
- Weights recent performance more heavily
- Selects next question using 60/30/10 distribution
"""

import random
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional, Tuple
from models.question import Question
from models.result import UserQuestionResult
from shared.constants import AdaptiveLearningWeights


class TopicPerformance:
    """Represents user performance for a single topic."""

    def __init__(self, topic_id: str, category: str):
        self.topic_id = topic_id
        self.category = category
        self.total_attempts = 0
        self.correct_attempts = 0
        self.recent_attempts = 0  # Last 7 days
        self.recent_correct = 0
        self.last_attempted: Optional[str] = None  # ISO timestamp
        self.accuracy = 0.0
        self.weighted_accuracy = 0.0  # Weighted by recency

    def calculate_accuracy(self):
        """Calculate overall and weighted accuracy."""
        # Overall accuracy
        if self.total_attempts > 0:
            self.accuracy = (self.correct_attempts / self.total_attempts) * 100
        else:
            self.accuracy = 0.0

        # Weighted accuracy (70% recent, 30% overall)
        if self.recent_attempts > 0:
            recent_accuracy = (self.recent_correct / self.recent_attempts) * 100
            # If we have both recent and historical data, weight recent more
            if self.total_attempts > self.recent_attempts:
                self.weighted_accuracy = (recent_accuracy * 0.7) + (self.accuracy * 0.3)
            else:
                # Only have recent data
                self.weighted_accuracy = recent_accuracy
        else:
            # No recent data, use overall
            self.weighted_accuracy = self.accuracy

    def classify_strength(self) -> str:
        """
        Classify topic as weak, medium, or strong.

        Returns:
            'weak', 'medium', or 'strong'
        """
        if self.weighted_accuracy < AdaptiveLearningWeights.WEAK_THRESHOLD:
            return 'weak'
        elif self.weighted_accuracy < AdaptiveLearningWeights.STRONG_THRESHOLD:
            return 'medium'
        else:
            return 'strong'


class AdaptiveLearningService:
    """Service for selecting the next question based on user performance."""

    def __init__(self):
        self.recent_days = 7  # Look back 7 days for recency weighting

    def analyze_performance(
        self,
        results: List[UserQuestionResult],
        available_topics: List[str]
    ) -> Dict[str, TopicPerformance]:
        """
        Analyze user performance across topics.

        Args:
            results: User's question results
            available_topics: List of topic IDs that have questions

        Returns:
            Dictionary mapping topic_id to TopicPerformance
        """
        # Initialize performance tracking for all available topics
        topic_performance: Dict[str, TopicPerformance] = {}

        # Calculate cutoff for "recent" (last 7 days)
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=self.recent_days)

        # Process all results
        for result in results:
            topic_id = result.topic_id

            # Initialize if not seen yet
            if topic_id not in topic_performance:
                topic_performance[topic_id] = TopicPerformance(
                    topic_id=topic_id,
                    category=result.category
                )

            perf = topic_performance[topic_id]

            # Update total counts
            perf.total_attempts += 1
            if result.correct:
                perf.correct_attempts += 1

            # Check if this is a recent result
            # Handle both correct format (Z suffix) and malformed old data (+00:00+00:00)
            try:
                # First, clean up any malformed timestamps from old data
                clean_timestamp = result.answered_at.replace('+00:00+00:00', '+00:00').replace('Z', '+00:00')
                result_date = datetime.fromisoformat(clean_timestamp)
            except (ValueError, AttributeError):
                # If parsing fails, skip this result
                continue

            if result_date >= cutoff_date:
                perf.recent_attempts += 1
                if result.correct:
                    perf.recent_correct += 1

            # Update last attempted timestamp
            if perf.last_attempted is None or result.answered_at > perf.last_attempted:
                perf.last_attempted = result.answered_at

        # Add topics that haven't been attempted yet (they're automatically "weak")
        for topic_id in available_topics:
            if topic_id not in topic_performance:
                # Use empty string for category (will be filled from topic data)
                topic_performance[topic_id] = TopicPerformance(
                    topic_id=topic_id,
                    category=""
                )

        # Calculate accuracies
        for perf in topic_performance.values():
            perf.calculate_accuracy()

        return topic_performance

    def select_topic(
        self,
        topic_performance: Dict[str, TopicPerformance]
    ) -> Optional[str]:
        """
        Select a topic using 60/30/10 distribution (weak/medium/strong).

        Args:
            topic_performance: Dictionary of topic performances

        Returns:
            Selected topic_id or None if no topics available
        """
        if not topic_performance:
            return None

        # Group topics by strength
        weak_topics = []
        medium_topics = []
        strong_topics = []

        for topic_id, perf in topic_performance.items():
            strength = perf.classify_strength()
            if strength == 'weak':
                weak_topics.append(topic_id)
            elif strength == 'medium':
                medium_topics.append(topic_id)
            else:
                strong_topics.append(topic_id)

        # Shuffle each list to ensure randomness when weights are equal
        random.shuffle(weak_topics)
        random.shuffle(medium_topics)
        random.shuffle(strong_topics)

        # If no topics in a category, redistribute weight
        # For example, if no medium topics, give that 30% to weak topics

        # Build weighted pool
        pool = []

        # Add weak topics (60% probability)
        if weak_topics:
            weight_per_weak = AdaptiveLearningWeights.WEAK_TOPICS_WEIGHT / len(weak_topics)
            pool.extend([(topic_id, weight_per_weak) for topic_id in weak_topics])

        # Add medium topics (30% probability)
        if medium_topics:
            weight_per_medium = AdaptiveLearningWeights.MEDIUM_TOPICS_WEIGHT / len(medium_topics)
            pool.extend([(topic_id, weight_per_medium) for topic_id in medium_topics])

        # Add strong topics (10% probability)
        if strong_topics:
            weight_per_strong = AdaptiveLearningWeights.STRONG_TOPICS_WEIGHT / len(strong_topics)
            pool.extend([(topic_id, weight_per_strong) for topic_id in strong_topics])

        if not pool:
            return None

        # Shuffle the pool to ensure randomness
        random.shuffle(pool)

        # Weighted random selection
        topics, weights = zip(*pool)
        selected_topic = random.choices(topics, weights=weights, k=1)[0]

        return selected_topic

    def select_question(
        self,
        questions: List[Question],
        all_results: List[UserQuestionResult],
        topic_id: Optional[str] = None
    ) -> Optional[Question]:
        """
        Select a question from the given list.

        Prioritizes:
        1. Questions from the selected topic (if specified)
        2. Questions never answered before
        3. Questions answered longest ago
        4. Random selection within those constraints

        Args:
            questions: Available questions
            all_results: All user results (for determining what's been answered)
            topic_id: Optional topic to filter by

        Returns:
            Selected Question or None
        """
        if not questions:
            return None

        # Filter by topic if specified
        if topic_id:
            questions = [q for q in questions if q.topic_id == topic_id]

        if not questions:
            return None

        # Build a map of question_id -> most recent answer timestamp
        answered_map = {}
        for result in all_results:
            if result.question_id not in answered_map:
                answered_map[result.question_id] = result.answered_at
            else:
                # Keep the most recent timestamp
                if result.answered_at > answered_map[result.question_id]:
                    answered_map[result.question_id] = result.answered_at

        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Built answered_map with {len(answered_map)} unique questions from {len(all_results)} results")

        # Separate into never-answered and previously-answered
        never_answered = []
        previously_answered = []

        for question in questions:
            if question.question_id not in answered_map:
                never_answered.append(question)
            else:
                previously_answered.append((question, answered_map[question.question_id]))

        # Priority 1: Never answered questions (shuffle for true randomness)
        if never_answered:
            logger.info(f"Found {len(never_answered)} never-answered questions out of {len(questions)} total")
            random.shuffle(never_answered)
            selected = never_answered[0]
            logger.info(f"Selected never-answered question: {selected.question_id}")
            return selected

        # Priority 2: Questions answered longest ago
        if previously_answered:
            logger.info(f"All {len(previously_answered)} questions have been answered - selecting oldest")
            # Sort by timestamp (oldest first)
            previously_answered.sort(key=lambda x: x[1])
            # Return the question answered longest ago
            selected = previously_answered[0][0]
            oldest_timestamp = previously_answered[0][1]
            logger.info(f"Selected oldest answered question: {selected.question_id}, last answered: {oldest_timestamp}")
            return selected

        # Should never reach here, but just in case
        return random.choice(questions) if questions else None

    def get_next_question(
        self,
        all_results: List[UserQuestionResult],
        recent_results: List[UserQuestionResult],
        all_questions: List[Question],
        available_topics: List[str]
    ) -> Tuple[Optional[Question], Dict[str, any]]:
        """
        Main entry point for adaptive question selection.

        Args:
            all_results: All user results (for performance analysis and question filtering)
            recent_results: Recent results (last 7 days, for performance weighting)
            all_questions: All available questions
            available_topics: List of topic IDs that have questions

        Returns:
            Tuple of (selected Question or None, debug_info dict)
        """
        debug_info = {}

        # Analyze performance
        topic_performance = self.analyze_performance(all_results, available_topics)
        debug_info['topic_performance'] = {
            tid: {
                'accuracy': perf.weighted_accuracy,
                'strength': perf.classify_strength(),
                'attempts': perf.total_attempts
            }
            for tid, perf in topic_performance.items()
        }

        # Select topic
        selected_topic_id = self.select_topic(topic_performance)
        debug_info['selected_topic'] = selected_topic_id

        if not selected_topic_id:
            return None, debug_info

        # Select question from that topic (using all_results to avoid repeats)
        question = self.select_question(
            questions=all_questions,
            all_results=all_results,
            topic_id=selected_topic_id
        )
        debug_info['selected_question_id'] = question.question_id if question else None

        return question, debug_info
