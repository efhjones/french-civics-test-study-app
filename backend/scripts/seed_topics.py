"""
Seed the Topics table with initial topics across 4 categories.

This script creates 15 topics across the 4 main categories:
- French History
- French Politics and Institutions
- French Geography
- French Culture and Society

Run this script after deploying the CDK infrastructure.

Usage:
    python scripts/seed_topics.py
"""

import sys
import os
from datetime import datetime

# Add parent directory to path to import models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.topic import Topic
from src.repositories.topic_repository import TopicRepository
from src.shared.constants import Category


def create_topics():
    """Define all topics with metadata."""
    topics = [
        # ==========================================
        # Category 1: French History (4 topics)
        # ==========================================
        Topic(
            topic_id="hist-001",
            title="La Révolution française",
            category=Category.FRENCH_HISTORY,
            description="La période révolutionnaire de 1789 à 1799, incluant les principaux événements, figures et impacts.",
            display_order=1,
            icon="calendar",
            color="#e74c3c",
            estimated_questions=12
        ),
        Topic(
            topic_id="hist-002",
            title="Les Républiques françaises",
            category=Category.FRENCH_HISTORY,
            description="L'évolution des cinq républiques, de la Première République (1792) à la Cinquième République (1958).",
            display_order=2,
            icon="landmark",
            color="#e67e22",
            estimated_questions=10
        ),
        Topic(
            topic_id="hist-003",
            title="Les guerres mondiales",
            category=Category.FRENCH_HISTORY,
            description="La participation de la France aux deux guerres mondiales, la Résistance, et la Libération.",
            display_order=3,
            icon="shield",
            color="#c0392b",
            estimated_questions=8
        ),
        Topic(
            topic_id="hist-004",
            title="Grands personnages historiques",
            category=Category.FRENCH_HISTORY,
            description="Les figures marquantes de l'histoire de France: rois, présidents, héros et intellectuels.",
            display_order=4,
            icon="user",
            color="#8e44ad",
            estimated_questions=10
        ),

        # ==========================================
        # Category 2: Politics and Institutions (4 topics)
        # ==========================================
        Topic(
            topic_id="pol-001",
            title="La Constitution et les institutions",
            category=Category.POLITICS_INSTITUTIONS,
            description="La Constitution de 1958, la séparation des pouvoirs, et les institutions de la République.",
            display_order=1,
            icon="book-open",
            color="#3498db",
            estimated_questions=15
        ),
        Topic(
            topic_id="pol-002",
            title="Le Président et le Gouvernement",
            category=Category.POLITICS_INSTITUTIONS,
            description="Le rôle du Président de la République, du Premier ministre et du Conseil des ministres.",
            display_order=2,
            icon="briefcase",
            color="#2980b9",
            estimated_questions=12
        ),
        Topic(
            topic_id="pol-003",
            title="Le Parlement",
            category=Category.POLITICS_INSTITUTIONS,
            description="L'Assemblée nationale et le Sénat: rôles, élections, et processus législatif.",
            display_order=3,
            icon="building",
            color="#1abc9c",
            estimated_questions=10
        ),
        Topic(
            topic_id="pol-004",
            title="Les collectivités territoriales",
            category=Category.POLITICS_INSTITUTIONS,
            description="Les régions, départements, communes et leurs compétences respectives.",
            display_order=4,
            icon="map",
            color="#16a085",
            estimated_questions=8
        ),

        # ==========================================
        # Category 3: French Geography (3 topics)
        # ==========================================
        Topic(
            topic_id="geo-001",
            title="Le territoire français",
            category=Category.GEOGRAPHY,
            description="La France métropolitaine et d'outre-mer: superficie, frontières, régions et départements.",
            display_order=1,
            icon="globe",
            color="#27ae60",
            estimated_questions=10
        ),
        Topic(
            topic_id="geo-002",
            title="Les grandes villes et régions",
            category=Category.GEOGRAPHY,
            description="Les principales villes françaises, leurs caractéristiques et leur importance.",
            display_order=2,
            icon="city",
            color="#2ecc71",
            estimated_questions=8
        ),
        Topic(
            topic_id="geo-003",
            title="L'Union européenne",
            category=Category.GEOGRAPHY,
            description="La place de la France dans l'Union européenne, institutions européennes et coopération.",
            display_order=3,
            icon="flag",
            color="#229954",
            estimated_questions=10
        ),

        # ==========================================
        # Category 4: Culture and Society (4 topics)
        # ==========================================
        Topic(
            topic_id="cult-001",
            title="Les valeurs de la République",
            category=Category.CULTURE_SOCIETY,
            description="Liberté, Égalité, Fraternité, Laïcité et les principes fondamentaux de la République française.",
            display_order=1,
            icon="heart",
            color="#f39c12",
            estimated_questions=12
        ),
        Topic(
            topic_id="cult-002",
            title="Les symboles nationaux",
            category=Category.CULTURE_SOCIETY,
            description="Le drapeau tricolore, La Marseillaise, Marianne, et autres symboles de la France.",
            display_order=2,
            icon="star",
            color="#f1c40f",
            estimated_questions=8
        ),
        Topic(
            topic_id="cult-003",
            title="Les droits et devoirs du citoyen",
            category=Category.CULTURE_SOCIETY,
            description="Les droits fondamentaux, le vote, le service civique, et les responsabilités civiques.",
            display_order=3,
            icon="scale",
            color="#e67e22",
            estimated_questions=10
        ),
        Topic(
            topic_id="cult-004",
            title="Culture et patrimoine français",
            category=Category.CULTURE_SOCIETY,
            description="La langue française, la littérature, les arts, et le patrimoine culturel.",
            display_order=4,
            icon="palette",
            color="#d35400",
            estimated_questions=10
        ),
    ]

    return topics


def seed_topics():
    """Seed the topics into DynamoDB."""
    print("=== French Civics Test - Topic Seeding ===\n")

    # Initialize repository
    repo = TopicRepository()

    # Create topics
    topics = create_topics()

    print(f"Preparing to seed {len(topics)} topics...\n")

    # Check which topics already exist
    existing_count = 0
    new_count = 0

    for topic in topics:
        if repo.topic_exists(topic.topic_id):
            print(f"  ⏭️  Topic already exists: {topic.topic_id} - {topic.title}")
            existing_count += 1
        else:
            print(f"  ✅ Creating topic: {topic.topic_id} - {topic.title}")
            new_count += 1

    if new_count == 0:
        print("\n✨ All topics already exist. No action needed.")
        return

    # Confirm before proceeding
    print(f"\n📊 Summary:")
    print(f"   - Existing topics: {existing_count}")
    print(f"   - New topics to create: {new_count}")
    print(f"   - Total topics: {len(topics)}")

    response = input("\nProceed with seeding? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("❌ Seeding cancelled.")
        return

    # Batch create topics
    print("\n🚀 Seeding topics...")
    new_topics = [t for t in topics if not repo.topic_exists(t.topic_id)]

    if new_topics:
        repo.batch_create(new_topics)
        print(f"\n✅ Successfully seeded {len(new_topics)} topics!")

    # Display summary by category
    print("\n📋 Topics by category:")
    for category in [Category.FRENCH_HISTORY, Category.POLITICS_INSTITUTIONS,
                     Category.GEOGRAPHY, Category.CULTURE_SOCIETY]:
        category_topics = [t for t in topics if t.category == category]
        print(f"\n   {category}:")
        for topic in category_topics:
            print(f"      - {topic.topic_id}: {topic.title}")

    print("\n✨ Topic seeding complete!")
    print("\n💡 Next step: Run 'python scripts/seed_questions.py' to add practice questions.")


if __name__ == "__main__":
    try:
        seed_topics()
    except KeyboardInterrupt:
        print("\n\n❌ Seeding interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during seeding: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
