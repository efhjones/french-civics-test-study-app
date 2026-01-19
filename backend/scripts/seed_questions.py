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

from src.models.question import Question, QuestionSourceReference
from src.repositories.question_repository import QuestionRepository
from src.shared.constants import Category, Difficulty


def create_questions():
    """Define sample practice questions with source references."""
    questions = []

    # French History Questions
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="hist-001",
            category=Category.FRENCH_HISTORY,
            question_text="En quelle année a débuté la Révolution française?",
            options={"a": "1789", "b": "1792", "c": "1799", "d": "1804"},
            correct_answer="a",
            explanation="La Révolution française a commencé en 1789 avec la prise de la Bastille le 14 juillet.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=8,
                section="Les grandes dates de l'histoire de France"
            ),
            difficulty=Difficulty.EASY
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="hist-002",
            category=Category.FRENCH_HISTORY,
            question_text="Quelle est la République française actuelle?",
            options={"a": "Troisième République", "b": "Quatrième République", "c": "Cinquième République", "d": "Sixième République"},
            correct_answer="c",
            explanation="La France vit sous la Cinquième République depuis 1958, fondée par Charles de Gaulle.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=12,
                section="La Cinquième République"
            ),
            difficulty=Difficulty.EASY
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="hist-003",
            category=Category.FRENCH_HISTORY,
            question_text="Qui était le chef de la France libre pendant la Seconde Guerre mondiale?",
            options={"a": "Philippe Pétain", "b": "Charles de Gaulle", "c": "Georges Clemenceau", "d": "François Mitterrand"},
            correct_answer="b",
            explanation="Le général Charles de Gaulle a dirigé la France libre depuis Londres et a organisé la Résistance française.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=11,
                section="La Résistance et la Libération"
            ),
            difficulty=Difficulty.EASY
        ),
    ])

    # Politics Questions
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-001",
            category=Category.FRENCH_POLITICS,
            question_text="Quelle est la devise de la République française?",
            options={"a": "Honneur et Patrie", "b": "Liberté, Égalité, Fraternité", "c": "Un pour tous, tous pour un", "d": "Travail, Famille, Patrie"},
            correct_answer="b",
            explanation="La devise de la République française est 'Liberté, Égalité, Fraternité', inscrite dans la Constitution.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=15,
                section="Les principes de la République"
            ),
            difficulty=Difficulty.EASY
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-002",
            category=Category.FRENCH_POLITICS,
            question_text="Quelle est la durée du mandat du Président de la République?",
            options={"a": "4 ans", "b": "5 ans", "c": "6 ans", "d": "7 ans"},
            correct_answer="b",
            explanation="Depuis 2000, le mandat présidentiel est de 5 ans (quinquennat), renouvelable une fois.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=18,
                section="Le Président de la République"
            ),
            difficulty=Difficulty.EASY
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-003",
            category=Category.FRENCH_POLITICS,
            question_text="De quelles deux chambres est composé le Parlement français?",
            options={"a": "Le Sénat et la Chambre des députés", "b": "L'Assemblée nationale et le Sénat", "c": "Le Congrès et le Parlement", "d": "La Chambre haute et la Chambre basse"},
            correct_answer="b",
            explanation="Le Parlement français est composé de l'Assemblée nationale (577 députés) et du Sénat (348 sénateurs).",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=20,
                section="Le Parlement"
            ),
            difficulty=Difficulty.EASY
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-004",
            category=Category.FRENCH_POLITICS,
            question_text="Qui dirige une commune?",
            options={"a": "Le préfet", "b": "Le maire", "c": "Le député", "d": "Le président du conseil général"},
            correct_answer="b",
            explanation="Le maire est élu par le conseil municipal et dirige la commune.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=25,
                section="La commune"
            ),
            difficulty=Difficulty.EASY
        ),
    ])

    # Geography Questions
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="geo-001",
            category=Category.FRENCH_GEOGRAPHY,
            question_text="Combien de régions compte la France métropolitaine depuis 2016?",
            options={"a": "13", "b": "22", "c": "27", "d": "18"},
            correct_answer="a",
            explanation="Depuis la réforme territoriale de 2016, la France métropolitaine compte 13 régions (plus 5 régions d'outre-mer).",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=30,
                section="Les régions françaises"
            ),
            difficulty=Difficulty.MEDIUM
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="geo-002",
            category=Category.FRENCH_GEOGRAPHY,
            question_text="Quelle est la capitale de la France?",
            options={"a": "Lyon", "b": "Marseille", "c": "Paris", "d": "Bordeaux"},
            correct_answer="c",
            explanation="Paris est la capitale de la France et sa plus grande ville.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=32,
                section="Les grandes villes"
            ),
            difficulty=Difficulty.EASY
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="geo-003",
            category=Category.FRENCH_GEOGRAPHY,
            question_text="La France est-elle membre de l'Union européenne?",
            options={"a": "Oui, depuis sa création", "b": "Oui, depuis 1995", "c": "Non", "d": "Non, elle a quitté l'UE"},
            correct_answer="a",
            explanation="La France est l'un des six membres fondateurs de la Communauté européenne (devenue l'UE) en 1957.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=35,
                section="L'Union européenne"
            ),
            difficulty=Difficulty.EASY
        ),
    ])

    # Culture Questions
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-001",
            category=Category.FRENCH_CULTURE,
            question_text="Qu'est-ce que la laïcité?",
            options={"a": "L'interdiction de toute religion", "b": "La séparation de l'Église et de l'État", "c": "L'obligation d'être athée", "d": "La religion catholique comme religion d'État"},
            correct_answer="b",
            explanation="La laïcité est le principe de séparation de l'Église et de l'État, garantissant la liberté de conscience et de culte.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=40,
                section="La laïcité"
            ),
            difficulty=Difficulty.MEDIUM
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-002",
            category=Category.FRENCH_CULTURE,
            question_text="Quelles sont les trois couleurs du drapeau français?",
            options={"a": "Rouge, blanc, noir", "b": "Bleu, blanc, rouge", "c": "Bleu, jaune, rouge", "d": "Vert, blanc, rouge"},
            correct_answer="b",
            explanation="Le drapeau tricolore français est composé de trois bandes verticales: bleu, blanc, rouge.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=44,
                section="Le drapeau tricolore"
            ),
            difficulty=Difficulty.EASY
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-003",
            category=Category.FRENCH_CULTURE,
            question_text="À partir de quel âge peut-on voter en France?",
            options={"a": "16 ans", "b": "18 ans", "c": "21 ans", "d": "25 ans"},
            correct_answer="b",
            explanation="Le droit de vote est accordé à tous les citoyens français à partir de 18 ans.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=50,
                section="Le droit de vote"
            ),
            difficulty=Difficulty.EASY
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-004",
            category=Category.FRENCH_CULTURE,
            question_text="Quelle est la langue officielle de la République française?",
            options={"a": "Le français et l'anglais", "b": "Le français uniquement", "c": "Le français et les langues régionales", "d": "Il n'y a pas de langue officielle"},
            correct_answer="b",
            explanation="Le français est la seule langue officielle de la République française, inscrit dans la Constitution.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=55,
                section="La langue française"
            ),
            difficulty=Difficulty.MEDIUM
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
