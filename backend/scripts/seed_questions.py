"""
Seed the Questions table with initial practice questions.

This script creates sample practice questions across all topics,
with source references to the Livret du citoyen.

Run this script after seeding topics.

Usage:
    python scripts/seed_questions.py
"""

import sys
import os
import uuid

# Add parent directory to path to import models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.question import Question, QuestionSourceReference, AnswerOption
from src.repositories.question_repository import QuestionRepository
from src.shared.constants import Category, Difficulty, QuestionType, GeneratedBy
from datetime import datetime


def create_questions():
    """Define sample practice questions with source references."""
    questions = []
    timestamp = datetime.utcnow().isoformat() + 'Z'

    # French History Questions
    questions.extend([
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
            topic_id="hist-002",
            category=Category.FRENCH_HISTORY,
            question_text="Quelle est la République française actuelle?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer="c",
            explanation="La France vit sous la Cinquième République depuis 1958, fondée par Charles de Gaulle.",
            difficulty=Difficulty.EASY,
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=12,
                section="La Cinquième République"
            ),
            generated_by=GeneratedBy.MANUAL,
            validated=True,
            created_at=timestamp,
            answer_options=[
                AnswerOption(id="a", text="Troisième République"),
                AnswerOption(id="b", text="Quatrième République"),
                AnswerOption(id="c", text="Cinquième République"),
                AnswerOption(id="d", text="Sixième République"),
            ]
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="hist-003",
            category=Category.FRENCH_HISTORY,
            question_text="Qui était le chef de la France libre pendant la Seconde Guerre mondiale?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer="b",
            explanation="Le général Charles de Gaulle a dirigé la France libre depuis Londres et a organisé la Résistance française.",
            difficulty=Difficulty.EASY,
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=11,
                section="La Résistance et la Libération"
            ),
            generated_by=GeneratedBy.MANUAL,
            validated=True,
            created_at=timestamp,
            answer_options=[
                AnswerOption(id="a", text="Philippe Pétain"),
                AnswerOption(id="b", text="Charles de Gaulle"),
                AnswerOption(id="c", text="Georges Clemenceau"),
                AnswerOption(id="d", text="François Mitterrand"),
            ]
        ),
    ])

    # Politics Questions
    questions.extend([
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
            topic_id="pol-002",
            category=Category.FRENCH_POLITICS,
            question_text="Quelle est la durée du mandat du Président de la République?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer="b",
            explanation="Depuis 2000, le mandat présidentiel est de 5 ans (quinquennat), renouvelable une fois.",
            difficulty=Difficulty.EASY,
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=18,
                section="Le Président de la République"
            ),
            generated_by=GeneratedBy.MANUAL,
            validated=True,
            created_at=timestamp,
            answer_options=[
                AnswerOption(id="a", text="4 ans"),
                AnswerOption(id="b", text="5 ans"),
                AnswerOption(id="c", text="6 ans"),
                AnswerOption(id="d", text="7 ans"),
            ]
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-003",
            category=Category.FRENCH_POLITICS,
            question_text="De quelles deux chambres est composé le Parlement français?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer="b",
            explanation="Le Parlement français est composé de l'Assemblée nationale (577 députés) et du Sénat (348 sénateurs).",
            difficulty=Difficulty.EASY,
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=20,
                section="Le Parlement"
            ),
            generated_by=GeneratedBy.MANUAL,
            validated=True,
            created_at=timestamp,
            answer_options=[
                AnswerOption(id="a", text="Le Sénat et la Chambre des députés"),
                AnswerOption(id="b", text="L'Assemblée nationale et le Sénat"),
                AnswerOption(id="c", text="Le Congrès et le Parlement"),
                AnswerOption(id="d", text="La Chambre haute et la Chambre basse"),
            ]
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-004",
            category=Category.FRENCH_POLITICS,
            question_text="Qui dirige une commune?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer="b",
            explanation="Le maire est élu par le conseil municipal et dirige la commune.",
            difficulty=Difficulty.EASY,
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=25,
                section="La commune"
            ),
            generated_by=GeneratedBy.MANUAL,
            validated=True,
            created_at=timestamp,
            answer_options=[
                AnswerOption(id="a", text="Le préfet"),
                AnswerOption(id="b", text="Le maire"),
                AnswerOption(id="c", text="Le député"),
                AnswerOption(id="d", text="Le président du conseil général"),
            ]
        ),
    ])

    # Geography Questions
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="geo-001",
            category=Category.FRENCH_GEOGRAPHY,
            question_text="Combien de régions compte la France métropolitaine depuis 2016?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer="a",
            explanation="Depuis la réforme territoriale de 2016, la France métropolitaine compte 13 régions (plus 5 régions d'outre-mer).",
            difficulty=Difficulty.MEDIUM,
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=30,
                section="Les régions françaises"
            ),
            generated_by=GeneratedBy.MANUAL,
            validated=True,
            created_at=timestamp,
            answer_options=[
                AnswerOption(id="a", text="13"),
                AnswerOption(id="b", text="22"),
                AnswerOption(id="c", text="27"),
                AnswerOption(id="d", text="18"),
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
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="geo-003",
            category=Category.FRENCH_GEOGRAPHY,
            question_text="La France est-elle membre de l'Union européenne?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer="a",
            explanation="La France est l'un des six membres fondateurs de la Communauté européenne (devenue l'UE) en 1957.",
            difficulty=Difficulty.EASY,
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=35,
                section="L'Union européenne"
            ),
            generated_by=GeneratedBy.MANUAL,
            validated=True,
            created_at=timestamp,
            answer_options=[
                AnswerOption(id="a", text="Oui, depuis sa création"),
                AnswerOption(id="b", text="Oui, depuis 1995"),
                AnswerOption(id="c", text="Non"),
                AnswerOption(id="d", text="Non, elle a quitté l'UE"),
            ]
        ),
    ])

    # Culture Questions
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-001",
            category=Category.FRENCH_CULTURE,
            question_text="Qu'est-ce que la laïcité?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer="b",
            explanation="La laïcité est le principe de séparation de l'Église et de l'État, garantissant la liberté de conscience et de culte.",
            difficulty=Difficulty.MEDIUM,
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=40,
                section="La laïcité"
            ),
            generated_by=GeneratedBy.MANUAL,
            validated=True,
            created_at=timestamp,
            answer_options=[
                AnswerOption(id="a", text="L'interdiction de toute religion"),
                AnswerOption(id="b", text="La séparation de l'Église et de l'État"),
                AnswerOption(id="c", text="L'obligation d'être athée"),
                AnswerOption(id="d", text="La religion catholique comme religion d'État"),
            ]
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-002",
            category=Category.FRENCH_CULTURE,
            question_text="Quelles sont les trois couleurs du drapeau français?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer="b",
            explanation="Le drapeau tricolore français est composé de trois bandes verticales: bleu, blanc, rouge.",
            difficulty=Difficulty.EASY,
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=44,
                section="Le drapeau tricolore"
            ),
            generated_by=GeneratedBy.MANUAL,
            validated=True,
            created_at=timestamp,
            answer_options=[
                AnswerOption(id="a", text="Rouge, blanc, noir"),
                AnswerOption(id="b", text="Bleu, blanc, rouge"),
                AnswerOption(id="c", text="Bleu, jaune, rouge"),
                AnswerOption(id="d", text="Vert, blanc, rouge"),
            ]
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-003",
            category=Category.FRENCH_CULTURE,
            question_text="À partir de quel âge peut-on voter en France?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer="b",
            explanation="Le droit de vote est accordé à tous les citoyens français à partir de 18 ans.",
            difficulty=Difficulty.EASY,
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=50,
                section="Le droit de vote"
            ),
            generated_by=GeneratedBy.MANUAL,
            validated=True,
            created_at=timestamp,
            answer_options=[
                AnswerOption(id="a", text="16 ans"),
                AnswerOption(id="b", text="18 ans"),
                AnswerOption(id="c", text="21 ans"),
                AnswerOption(id="d", text="25 ans"),
            ]
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-004",
            category=Category.FRENCH_CULTURE,
            question_text="Quelle est la langue officielle de la République française?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer="b",
            explanation="Le français est la seule langue officielle de la République française, inscrit dans la Constitution.",
            difficulty=Difficulty.MEDIUM,
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=55,
                section="La langue française"
            ),
            generated_by=GeneratedBy.MANUAL,
            validated=True,
            created_at=timestamp,
            answer_options=[
                AnswerOption(id="a", text="Le français et l'anglais"),
                AnswerOption(id="b", text="Le français uniquement"),
                AnswerOption(id="c", text="Le français et les langues régionales"),
                AnswerOption(id="d", text="Il n'y a pas de langue officielle"),
            ]
        ),
    ])

    return questions


def seed_questions():
    """Seed the questions into DynamoDB."""
    print("=== French Civics Test - Question Seeding ===\n")

    # Initialize repository
    repo = QuestionRepository()

    # Create questions
    questions = create_questions()

    print(f"Preparing to seed {len(questions)} questions...\n")

    # Group by topic for display
    topics_count = {}
    for q in questions:
        topics_count[q.topic_id] = topics_count.get(q.topic_id, 0) + 1

    print("📊 Questions by topic:")
    for topic_id, count in sorted(topics_count.items()):
        print(f"   - {topic_id}: {count} questions")

    # Difficulty breakdown
    difficulty_count = {}
    for q in questions:
        difficulty_count[q.difficulty] = difficulty_count.get(q.difficulty, 0) + 1

    print("\n📊 Questions by difficulty:")
    for difficulty, count in sorted(difficulty_count.items(), key=lambda x: x[0].value):
        print(f"   - {difficulty.name}: {count} questions")

    # Confirm before proceeding
    response = input("\n\nProceed with seeding? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("❌ Seeding cancelled.")
        return

    # Batch create questions
    print("\n🚀 Seeding questions...")
    repo.batch_create(questions)

    print(f"\n✅ Successfully seeded {len(questions)} questions!")
    print("\n✨ Question seeding complete!")
    print("\n💡 You can now test the API endpoints with authenticated requests.")


if __name__ == "__main__":
    try:
        seed_questions()
    except KeyboardInterrupt:
        print("\n\n❌ Seeding interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during seeding: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
