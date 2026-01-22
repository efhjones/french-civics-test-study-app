"""
Topic data model.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class SourceReference:
    """Reference to where a topic appears in the Livret du citoyen."""
    pages: List[int]
    sections: List[str]


@dataclass
class Topic:
    """
    Represents a learning topic/subtopic.

    Attributes are mapped to DynamoDB Topics table attributes.
    """

    topic_id: str
    category: str
    name: str
    description: str
    source_reference: SourceReference
    display_order: int
    created_at: str

    @classmethod
    def from_dynamo(cls, item: dict) -> 'Topic':
        """
        Create Topic instance from DynamoDB item.

        Args:
            item: DynamoDB item dict

        Returns:
            Topic instance
        """
        source_ref_data = item['source_reference']
        source_ref = SourceReference(
            pages=[int(p) for p in source_ref_data['pages']],
            sections=source_ref_data['sections']
        )

        return cls(
            topic_id=item['topic_id'],
            category=item['category'],
            name=item['name'],
            description=item['description'],
            source_reference=source_ref,
            display_order=int(item['display_order']),
            created_at=item['created_at']
        )

    def to_dynamo(self) -> dict:
        """
        Convert Topic to DynamoDB item format.

        Returns:
            Dict suitable for DynamoDB PutItem
        """
        return {
            'topic_id': self.topic_id,
            'category': self.category,
            'name': self.name,
            'description': self.description,
            'source_reference': {
                'pages': self.source_reference.pages,
                'sections': self.source_reference.sections
            },
            'display_order': self.display_order,
            'created_at': self.created_at
        }

    def to_api_response(self) -> dict:
        """
        Convert Topic to API response format.

        Returns:
            Dict for JSON serialization
        """
        return {
            'topic_id': self.topic_id,
            'category': self.category,
            'name': self.name,
            'description': self.description,
            'source_pages': self.source_reference.pages,
            'display_order': self.display_order
        }
