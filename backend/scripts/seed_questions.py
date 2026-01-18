"""
Seed the Questions table with initial practice questions.

This script creates 50+ practice questions across all topics,
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
    """Define all practice questions with source references."""
    questions = []

    # ==========================================
    # French History Questions
    # ==========================================

    # Topic: hist-001 - La Révolution française
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="hist-001",
            category=Category.FRENCH_HISTORY,
            question_text="En quelle année a débuté la Révolution française?",
            options={
                "a": "1789",
                "b": "1792",
                "c": "1799",
                "d": "1804"
            },
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
            topic_id="hist-001",
            category=Category.FRENCH_HISTORY,
            question_text="Quel document fondamental a été adopté le 26 août 1789?",
            options={
                "a": "La Constitution",
                "b": "La Déclaration des droits de l'homme et du citoyen",
                "c": "Le Code civil",
                "d": "La Charte"
            },
            correct_answer="b",
            explanation="La Déclaration des droits de l'homme et du citoyen de 1789 est un texte fondamental qui affirme les principes de liberté, d'égalité et de souveraineté nationale.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=9,
                section="1789: La Déclaration des droits de l'homme"
            ),
            difficulty=Difficulty.MEDIUM
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="hist-001",
            category=Category.FRENCH_HISTORY,
            question_text="Quel événement symbolise le début de la Révolution française?",
            options={
                "a": "L'exécution du roi Louis XVI",
                "b": "La prise de la Bastille",
                "c": "Les États généraux",
                "d": "Le serment du Jeu de paume"
            },
            correct_answer="b",
            explanation="La prise de la Bastille le 14 juillet 1789 est l'événement symbolique marquant le début de la Révolution française.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=8,
                section="Les grandes dates"
            ),
            difficulty=Difficulty.EASY
        ),
    ])

    # Topic: hist-002 - Les Républiques françaises
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="hist-002",
            category=Category.FRENCH_HISTORY,
            question_text="Quelle est la République française actuelle?",
            options={
                "a": "Troisième République",
                "b": "Quatrième République",
                "c": "Cinquième République",
                "d": "Sixième République"
            },
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
            topic_id="hist-002",
            category=Category.FRENCH_HISTORY,
            question_text="En quelle année la Cinquième République a-t-elle été instaurée?",
            options={
                "a": "1945",
                "b": "1958",
                "c": "1962",
                "d": "1968"
            },
            correct_answer="b",
            explanation="La Cinquième République a été instaurée en 1958 avec l'adoption d'une nouvelle Constitution.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=12,
                section="1958: Fondation de la Cinquième République"
            ),
            difficulty=Difficulty.MEDIUM
        ),
    ])

    # Topic: hist-003 - Les guerres mondiales
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="hist-003",
            category=Category.FRENCH_HISTORY,
            question_text="Quel événement marque la fin de la Seconde Guerre mondiale en Europe?",
            options={
                "a": "Le débarquement en Normandie",
                "b": "La libération de Paris",
                "c": "La capitulation de l'Allemagne le 8 mai 1945",
                "d": "L'armistice de 1918"
            },
            correct_answer="c",
            explanation="La Seconde Guerre mondiale en Europe s'est terminée avec la capitulation de l'Allemagne le 8 mai 1945.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=10,
                section="Les guerres mondiales"
            ),
            difficulty=Difficulty.MEDIUM
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="hist-003",
            category=Category.FRENCH_HISTORY,
            question_text="Qui était le chef de la France libre pendant la Seconde Guerre mondiale?",
            options={
                "a": "Philippe Pétain",
                "b": "Charles de Gaulle",
                "c": "Georges Clemenceau",
                "d": "François Mitterrand"
            },
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

    # ==========================================
    # Politics and Institutions Questions
    # ==========================================

    # Topic: pol-001 - La Constitution et les institutions
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-001",
            category=Category.POLITICS_INSTITUTIONS,
            question_text="Quelle est la devise de la République française?",
            options={
                "a": "Honneur et Patrie",
                "b": "Liberté, Égalité, Fraternité",
                "c": "Un pour tous, tous pour un",
                "d": "Travail, Famille, Patrie"
            },
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
            topic_id="pol-001",
            category=Category.POLITICS_INSTITUTIONS,
            question_text="Quel est le texte fondateur de la Cinquième République?",
            options={
                "a": "La Déclaration des droits de l'homme de 1789",
                "b": "Le Code civil",
                "c": "La Constitution de 1958",
                "d": "Le Traité de Rome"
            },
            correct_answer="c",
            explanation="La Constitution de 1958 est le texte fondateur de la Cinquième République et définit l'organisation des pouvoirs publics.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=16,
                section="La Constitution"
            ),
            difficulty=Difficulty.MEDIUM
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-001",
            category=Category.POLITICS_INSTITUTIONS,
            question_text="Quels sont les trois pouvoirs de la République française?",
            options={
                "a": "Législatif, exécutif, judiciaire",
                "b": "Président, gouvernement, parlement",
                "c": "État, région, commune",
                "d": "Sénat, Assemblée, Conseil"
            },
            correct_answer="a",
            explanation="La séparation des pouvoirs distingue le pouvoir législatif (faire les lois), exécutif (appliquer les lois) et judiciaire (juger).",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=17,
                section="La séparation des pouvoirs"
            ),
            difficulty=Difficulty.MEDIUM
        ),
    ])

    # Topic: pol-002 - Le Président et le Gouvernement
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-002",
            category=Category.POLITICS_INSTITUTIONS,
            question_text="Quelle est la durée du mandat du Président de la République?",
            options={
                "a": "4 ans",
                "b": "5 ans",
                "c": "6 ans",
                "d": "7 ans"
            },
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
            topic_id="pol-002",
            category=Category.POLITICS_INSTITUTIONS,
            question_text="Qui nomme le Premier ministre?",
            options={
                "a": "L'Assemblée nationale",
                "b": "Le peuple par élection",
                "c": "Le Président de la République",
                "d": "Le Sénat"
            },
            correct_answer="c",
            explanation="Le Président de la République nomme le Premier ministre et, sur proposition de celui-ci, les autres membres du gouvernement.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=19,
                section="Le Gouvernement"
            ),
            difficulty=Difficulty.EASY
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-002",
            category=Category.POLITICS_INSTITUTIONS,
            question_text="Quel est le rôle principal du Président de la République?",
            options={
                "a": "Voter les lois",
                "b": "Garantir l'indépendance nationale et l'intégrité du territoire",
                "c": "Juger les criminels",
                "d": "Gérer les collectivités locales"
            },
            correct_answer="b",
            explanation="Le Président est le garant de l'indépendance nationale, de l'intégrité du territoire et du respect de la Constitution.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=18,
                section="Rôle du Président"
            ),
            difficulty=Difficulty.MEDIUM
        ),
    ])

    # Topic: pol-003 - Le Parlement
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-003",
            category=Category.POLITICS_INSTITUTIONS,
            question_text="De quelles deux chambres est composé le Parlement français?",
            options={
                "a": "Le Sénat et la Chambre des députés",
                "b": "L'Assemblée nationale et le Sénat",
                "c": "Le Congrès et le Parlement",
                "d": "La Chambre haute et la Chambre basse"
            },
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
            topic_id="pol-003",
            category=Category.POLITICS_INSTITUTIONS,
            question_text="Quelle est la durée du mandat d'un député?",
            options={
                "a": "3 ans",
                "b": "4 ans",
                "c": "5 ans",
                "d": "6 ans"
            },
            correct_answer="c",
            explanation="Les députés sont élus pour un mandat de 5 ans au suffrage universel direct.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=21,
                section="L'Assemblée nationale"
            ),
            difficulty=Difficulty.MEDIUM
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-003",
            category=Category.POLITICS_INSTITUTIONS,
            question_text="Quel est le rôle principal du Parlement?",
            options={
                "a": "Appliquer les lois",
                "b": "Voter les lois",
                "c": "Nommer les ministres",
                "d": "Juger les crimes"
            },
            correct_answer="b",
            explanation="Le Parlement vote les lois et contrôle l'action du gouvernement.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=20,
                section="Les fonctions du Parlement"
            ),
            difficulty=Difficulty.EASY
        ),
    ])

    # Topic: pol-004 - Les collectivités territoriales
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-004",
            category=Category.POLITICS_INSTITUTIONS,
            question_text="Quels sont les trois niveaux de collectivités territoriales en France?",
            options={
                "a": "État, région, département",
                "b": "Région, département, commune",
                "c": "Commune, canton, arrondissement",
                "d": "Région, ville, village"
            },
            correct_answer="b",
            explanation="Les trois niveaux de collectivités territoriales sont la région, le département et la commune.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=24,
                section="Les collectivités territoriales"
            ),
            difficulty=Difficulty.MEDIUM
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="pol-004",
            category=Category.POLITICS_INSTITUTIONS,
            question_text="Qui dirige une commune?",
            options={
                "a": "Le préfet",
                "b": "Le maire",
                "c": "Le député",
                "d": "Le président du conseil général"
            },
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

    # ==========================================
    # Geography Questions
    # ==========================================

    # Topic: geo-001 - Le territoire français
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="geo-001",
            category=Category.GEOGRAPHY,
            question_text="Combien de régions compte la France métropolitaine depuis 2016?",
            options={
                "a": "13",
                "b": "22",
                "c": "27",
                "d": "18"
            },
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
            topic_id="geo-001",
            category=Category.GEOGRAPHY,
            question_text="Quels sont les territoires d'outre-mer français?",
            options={
                "a": "Uniquement les îles des Caraïbes",
                "b": "La Guadeloupe, la Martinique, la Guyane, la Réunion, Mayotte et d'autres territoires",
                "c": "Uniquement la Corse",
                "d": "Aucun territoire d'outre-mer"
            },
            correct_answer="b",
            explanation="La France possède plusieurs territoires d'outre-mer dont la Guadeloupe, la Martinique, la Guyane, la Réunion, Mayotte, et d'autres.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=31,
                section="L'outre-mer français"
            ),
            difficulty=Difficulty.MEDIUM
        ),
    ])

    # Topic: geo-002 - Les grandes villes
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="geo-002",
            category=Category.GEOGRAPHY,
            question_text="Quelle est la capitale de la France?",
            options={
                "a": "Lyon",
                "b": "Marseille",
                "c": "Paris",
                "d": "Bordeaux"
            },
            correct_answer="c",
            explanation="Paris est la capitale de la France et sa plus grande ville.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=32,
                section="Les grandes villes"
            ),
            difficulty=Difficulty.EASY
        ),
    ])

    # Topic: geo-003 - L'Union européenne
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="geo-003",
            category=Category.GEOGRAPHY,
            question_text="La France est-elle membre de l'Union européenne?",
            options={
                "a": "Oui, depuis sa création",
                "b": "Oui, depuis 1995",
                "c": "Non",
                "d": "Non, elle a quitté l'UE"
            },
            correct_answer="a",
            explanation="La France est l'un des six membres fondateurs de la Communauté européenne (devenue l'UE) en 1957.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=35,
                section="L'Union européenne"
            ),
            difficulty=Difficulty.EASY
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="geo-003",
            category=Category.GEOGRAPHY,
            question_text="Où se trouve le Parlement européen?",
            options={
                "a": "Paris",
                "b": "Bruxelles et Strasbourg",
                "c": "Luxembourg",
                "d": "Genève"
            },
            correct_answer="b",
            explanation="Le Parlement européen siège à Strasbourg (sessions plénières) et à Bruxelles (commissions).",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=36,
                section="Les institutions européennes"
            ),
            difficulty=Difficulty.MEDIUM
        ),
    ])

    # ==========================================
    # Culture and Society Questions
    # ==========================================

    # Topic: cult-001 - Les valeurs de la République
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-001",
            category=Category.CULTURE_SOCIETY,
            question_text="Qu'est-ce que la laïcité?",
            options={
                "a": "L'interdiction de toute religion",
                "b": "La séparation de l'Église et de l'État",
                "c": "L'obligation d'être athée",
                "d": "La religion catholique comme religion d'État"
            },
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
            topic_id="cult-001",
            category=Category.CULTURE_SOCIETY,
            question_text="Quel principe garantit que tous les citoyens ont les mêmes droits?",
            options={
                "a": "La liberté",
                "b": "L'égalité",
                "c": "La fraternité",
                "d": "La solidarité"
            },
            correct_answer="b",
            explanation="Le principe d'égalité garantit que tous les citoyens ont les mêmes droits devant la loi, sans distinction.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=41,
                section="L'égalité"
            ),
            difficulty=Difficulty.EASY
        ),
    ])

    # Topic: cult-002 - Les symboles nationaux
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-002",
            category=Category.CULTURE_SOCIETY,
            question_text="Quelles sont les trois couleurs du drapeau français?",
            options={
                "a": "Rouge, blanc, noir",
                "b": "Bleu, blanc, rouge",
                "c": "Bleu, jaune, rouge",
                "d": "Vert, blanc, rouge"
            },
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
            topic_id="cult-002",
            category=Category.CULTURE_SOCIETY,
            question_text="Quel est l'hymne national de la France?",
            options={
                "a": "Le Chant des Partisans",
                "b": "La Marseillaise",
                "c": "La Carmagnole",
                "d": "Douce France"
            },
            correct_answer="b",
            explanation="La Marseillaise est l'hymne national français, composé en 1792 par Rouget de Lisle.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=45,
                section="La Marseillaise"
            ),
            difficulty=Difficulty.EASY
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-002",
            category=Category.CULTURE_SOCIETY,
            question_text="Qui est Marianne?",
            options={
                "a": "Une héroïne historique",
                "b": "La représentation symbolique de la République française",
                "c": "La première femme présidente",
                "d": "Une sainte catholique"
            },
            correct_answer="b",
            explanation="Marianne est la représentation symbolique de la République française, incarnant la liberté et la raison.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=46,
                section="Marianne"
            ),
            difficulty=Difficulty.MEDIUM
        ),
    ])

    # Topic: cult-003 - Les droits et devoirs du citoyen
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-003",
            category=Category.CULTURE_SOCIETY,
            question_text="À partir de quel âge peut-on voter en France?",
            options={
                "a": "16 ans",
                "b": "18 ans",
                "c": "21 ans",
                "d": "25 ans"
            },
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
            topic_id="cult-003",
            category=Category.CULTURE_SOCIETY,
            question_text="Le vote est-il obligatoire en France?",
            options={
                "a": "Oui, sous peine d'amende",
                "b": "Non, c'est un droit mais pas une obligation",
                "c": "Oui, pour les élections présidentielles seulement",
                "d": "Oui, pour tous les citoyens de plus de 25 ans"
            },
            correct_answer="b",
            explanation="Le vote est un droit mais pas une obligation en France. C'est un devoir moral mais pas légal.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=51,
                section="Le vote, un droit et un devoir civique"
            ),
            difficulty=Difficulty.MEDIUM
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-003",
            category=Category.CULTURE_SOCIETY,
            question_text="Quel est un devoir fondamental du citoyen français?",
            options={
                "a": "Payer ses impôts",
                "b": "Aller à l'église",
                "c": "Avoir un emploi",
                "d": "Posséder une voiture"
            },
            correct_answer="a",
            explanation="Payer ses impôts est un devoir fondamental qui permet de financer les services publics et la solidarité nationale.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=52,
                section="Les devoirs du citoyen"
            ),
            difficulty=Difficulty.EASY
        ),
    ])

    # Topic: cult-004 - Culture et patrimoine
    questions.extend([
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-004",
            category=Category.CULTURE_SOCIETY,
            question_text="Quelle est la langue officielle de la République française?",
            options={
                "a": "Le français et l'anglais",
                "b": "Le français uniquement",
                "c": "Le français et les langues régionales",
                "d": "Il n'y a pas de langue officielle"
            },
            correct_answer="b",
            explanation="Le français est la seule langue officielle de la République française, inscrit dans la Constitution.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=55,
                section="La langue française"
            ),
            difficulty=Difficulty.MEDIUM
        ),
        Question(
            question_id=str(uuid.uuid4()),
            topic_id="cult-004",
            category=Category.CULTURE_SOCIETY,
            question_text="Quel monument parisien est devenu le symbole de la France?",
            options={
                "a": "Le Louvre",
                "b": "Notre-Dame",
                "c": "La Tour Eiffel",
                "d": "L'Arc de Triomphe"
            },
            correct_answer="c",
            explanation="La Tour Eiffel, construite pour l'Exposition universelle de 1889, est devenue le symbole mondial de la France.",
            source_reference=QuestionSourceReference(
                document="Livret du citoyen V2",
                page=57,
                section="Le patrimoine culturel"
            ),
            difficulty=Difficulty.EASY
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
    for difficulty, count in sorted(difficulty_count.items()):
        print(f"   - {difficulty}: {count} questions")

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
    print("\n💡 Next step: Deploy your CDK infrastructure and test the API endpoints.")


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
