"""
Question data model.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AnswerOption:
    """Represents a single answer option for multiple choice questions."""
    id: str      # "a", "b", "c", "d"
    text: str


@dataclass
class QuestionSourceReference:
    """Reference to where question content appears in the Livret."""
    document: str           # "Livret du citoyen"
    page: int              # Page number
    section: str           # Section heading
    text_excerpt: Optional[str] = None  # Exact quote for validation


@dataclass
class Question:
    """
    Represents a practice question.

    Attributes are mapped to DynamoDB Questions table attributes.
    """

    question_id: str
    topic_id: str
    category: str
    question_text: str
    question_type: str              # "multiple_choice", "true_false", "short_answer"
    correct_answer: str
    explanation: str
    difficulty: int                 # 1, 2, or 3
    source_reference: QuestionSourceReference
    generated_by: str               # "manual" or "ai"
    validated: bool
    created_at: str
    answer_options: Optional[List[AnswerOption]] = None
    updated_at: Optional[str] = None
    tags: Optional[List[str]] = None

    @classmethod
    def from_dynamo(cls, item: dict) -> 'Question':
        """
        Create Question instance from DynamoDB item.

        Args:
            item: DynamoDB item dict

        Returns:
            Question instance
        """
        # Parse source reference
        source_ref_data = item['source_reference']
        source_ref = QuestionSourceReference(
            document=source_ref_data['document'],
            page=int(source_ref_data['page']),
            section=source_ref_data['section'],
            text_excerpt=source_ref_data.get('text_excerpt')
        )

        # Parse answer options if present
        answer_options = None
        if 'answer_options' in item:
            answer_options = [
                AnswerOption(id=opt['id'], text=opt['text'])
                for opt in item['answer_options']
            ]

        return cls(
            question_id=item['question_id'],
            topic_id=item['topic_id'],
            category=item['category'],
            question_text=item['question_text'],
            question_type=item['question_type'],
            correct_answer=item['correct_answer'],
            explanation=item['explanation'],
            difficulty=int(item['difficulty']),
            source_reference=source_ref,
            generated_by=item['generated_by'],
            validated=item['validated'],
            created_at=item['created_at'],
            answer_options=answer_options,
            updated_at=item.get('updated_at'),
            tags=item.get('tags', [])
        )

    def to_dynamo(self) -> dict:
        """
        Convert Question to DynamoDB item format.

        Returns:
            Dict suitable for DynamoDB PutItem
        """
        item = {
            'question_id': self.question_id,
            'topic_id': self.topic_id,
            'category': self.category,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'difficulty': self.difficulty,
            'source_reference': {
                'document': self.source_reference.document,
                'page': self.source_reference.page,
                'section': self.source_reference.section
            },
            'generated_by': self.generated_by,
            'validated': self.validated,
            'created_at': self.created_at
        }

        if self.source_reference.text_excerpt:
            item['source_reference']['text_excerpt'] = self.source_reference.text_excerpt

        if self.answer_options:
            item['answer_options'] = [
                {'id': opt.id, 'text': opt.text}
                for opt in self.answer_options
            ]

        if self.updated_at:
            item['updated_at'] = self.updated_at

        if self.tags:
            item['tags'] = self.tags

        return item

    def to_api_response(self, include_answer: bool = False) -> dict:
        """
        Convert Question to API response format.

        Args:
            include_answer: If True, include correct_answer (for review/feedback).
                          If False, omit it (for practice mode).

        Returns:
            Dict for JSON serialization
        """
        response = {
            'question_id': self.question_id,
            'topic_id': self.topic_id,
            'category': self.category,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'difficulty': self.difficulty,
            'source_reference': {
                'document': self.source_reference.document,
                'page': self.source_reference.page,
                'section': self.source_reference.section
            }
        }

        if self.answer_options:
            response['answer_options'] = [
                {'id': opt.id, 'text': opt.text}
                for opt in self.answer_options
            ]

        if include_answer:
            response['correct_answer'] = self.correct_answer
            response['explanation'] = self.explanation

        return response
