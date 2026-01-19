"""
Seed a few sample questions to test the system.
"""

import sys
import os
import uuid
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.question import Question, QuestionSourceReference, AnswerOption
from src.repositories.question_repository import QuestionRepository
from src.shared.constants import Category, Difficulty, QuestionType, GeneratedBy


def create_sample_questions():
    timestamp = datetime.utcnow().isoformat() + 'Z'

    questions = [
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="hist-001",
            category=Category.FRENCH_HISTORY,
            question_text="En quelle année a débuté la Révolution française?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer="a",
            explanation="La Révolution française a commencé en 1789 avec la prise de la Bastille le 14 juillet.",
            difficulty=Difficulty.EASY,
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=8,
                section="Les grandes dates de l'histoire de France"
            ),
            generated_by=GeneratedBy.MANUAL,
            validated=True,
            created_at=timestamp,
            answer_options=[
                AnswerOption(id="a", text="1789"),
                AnswerOption(id="b", text="1792"),
                AnswerOption(id="c", text="1799"),
                AnswerOption(id="d", text="1804"),
            ]
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-001",
            category=Category.FRENCH_POLITICS,
            question_text="Quelle est la devise de la République française?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer="b",
            explanation="La devise de la République française est 'Liberté, Égalité, Fraternité', inscrite dans la Constitution.",
            difficulty=Difficulty.EASY,
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=15,
                section="Les principes de la République"
            ),
            generated_by=GeneratedBy.MANUAL,
            validated=True,
            created_at=timestamp,
            answer_options=[
                AnswerOption(id="a", text="Honneur et Patrie"),
                AnswerOption(id="b", text="Liberté, Égalité, Fraternité"),
                AnswerOption(id="c", text="Un pour tous, tous pour un"),
                AnswerOption(id="d", text="Travail, Famille, Patrie"),
            ]
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="geo-002",
            category=Category.FRENCH_GEOGRAPHY,
            question_text="Quelle est la capitale de la France?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer="c",
            explanation="Paris est la capitale de la France et sa plus grande ville.",
            difficulty=Difficulty.EASY,
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=32,
                section="Les grandes villes"
            ),
            generated_by=GeneratedBy.MANUAL,
            validated=True,
            created_at=timestamp,
            answer_options=[
                AnswerOption(id="a", text="Lyon"),
                AnswerOption(id="b", text="Marseille"),
                AnswerOption(id="c", text="Paris"),
                AnswerOption(id="d", text="Bordeaux"),
            ]
        ),
    ]

    return questions


if __name__ == "__main__":
    print("=== Seeding Sample Questions ===\n")

    repo = QuestionRepository()
    questions = create_sample_questions()

    print(f"Creating {len(questions)} sample questions...")
    repo.batch_create(questions)

    print(f"\n✅ Successfully seeded {len(questions)} questions!")
    print("\n💡 You can now test the /questions/next endpoint to see the adaptive learning in action.")
