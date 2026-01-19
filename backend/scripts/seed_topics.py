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

from src.models.topic import Topic, SourceReference
from src.repositories.topic_repository import TopicRepository
from src.shared.constants import Category


def create_topics():
    """Define all topics with metadata."""
    timestamp = datetime.utcnow().isoformat() + 'Z'

    topics = [
        # ==========================================
        # Category 1: French History (4 topics)
        # ==========================================
        Topic(
            topic_id="hist-001",
            name="La Révolution française",
            category=Category.FRENCH_HISTORY,
            description="La période révolutionnaire de 1789 à 1799, incluant les principaux événements, figures et impacts.",
            source_reference=SourceReference(pages=[8, 9, 10], sections=["La Révolution française", "1789"]),
            display_order=1,
            created_at=timestamp
        ),
        Topic(
            topic_id="hist-002",
            name="Les Républiques françaises",
            category=Category.FRENCH_HISTORY,
            description="L'évolution des cinq républiques, de la Première République (1792) à la Cinquième République (1958).",
            source_reference=SourceReference(pages=[11, 12], sections=["Les Républiques"]),
            display_order=2,
            created_at=timestamp
        ),
        Topic(
            topic_id="hist-003",
            name="Les guerres mondiales",
            category=Category.FRENCH_HISTORY,
            description="La participation de la France aux deux guerres mondiales, la Résistance, et la Libération.",
            source_reference=SourceReference(pages=[10, 11], sections=["Les guerres mondiales"]),
            display_order=3,
            created_at=timestamp
        ),
        Topic(
            topic_id="hist-004",
            name="Grands personnages historiques",
            category=Category.FRENCH_HISTORY,
            description="Les figures marquantes de l'histoire de France: rois, présidents, héros et intellectuels.",
            source_reference=SourceReference(pages=[8, 12], sections=["Personnages historiques"]),
            display_order=4,
            created_at=timestamp
        ),

        # ==========================================
        # Category 2: Politics and Institutions (4 topics)
        # ==========================================
        Topic(
            topic_id="pol-001",
            name="La Constitution et les institutions",
            category=Category.FRENCH_POLITICS,
            description="La Constitution de 1958, la séparation des pouvoirs, et les institutions de la République.",
            source_reference=SourceReference(pages=[15, 16, 17], sections=["La Constitution"]),
            display_order=1,
            created_at=timestamp
        ),
        Topic(
            topic_id="pol-002",
            name="Le Président et le Gouvernement",
            category=Category.FRENCH_POLITICS,
            description="Le rôle du Président de la République, du Premier ministre et du Conseil des ministres.",
            source_reference=SourceReference(pages=[18, 19], sections=["Le Président", "Le Gouvernement"]),
            display_order=2,
            created_at=timestamp
        ),
        Topic(
            topic_id="pol-003",
            name="Le Parlement",
            category=Category.FRENCH_POLITICS,
            description="L'Assemblée nationale et le Sénat: rôles, élections, et processus législatif.",
            source_reference=SourceReference(pages=[20, 21], sections=["Le Parlement"]),
            display_order=3,
            created_at=timestamp
        ),
        Topic(
            topic_id="pol-004",
            name="Les collectivités territoriales",
            category=Category.FRENCH_POLITICS,
            description="Les régions, départements, communes et leurs compétences respectives.",
            source_reference=SourceReference(pages=[24, 25], sections=["Les collectivités"]),
            display_order=4,
            created_at=timestamp
        ),

        # ==========================================
        # Category 3: French Geography (3 topics)
        # ==========================================
        Topic(
            topic_id="geo-001",
            name="Le territoire français",
            category=Category.FRENCH_GEOGRAPHY,
            description="La France métropolitaine et d'outre-mer: superficie, frontières, régions et départements.",
            source_reference=SourceReference(pages=[30, 31], sections=["Le territoire"]),
            display_order=1,
            created_at=timestamp
        ),
        Topic(
            topic_id="geo-002",
            name="Les grandes villes et régions",
            category=Category.FRENCH_GEOGRAPHY,
            description="Les principales villes françaises, leurs caractéristiques et leur importance.",
            source_reference=SourceReference(pages=[32], sections=["Les villes"]),
            display_order=2,
            created_at=timestamp
        ),
        Topic(
            topic_id="geo-003",
            name="L'Union européenne",
            category=Category.FRENCH_GEOGRAPHY,
            description="La place de la France dans l'Union européenne, institutions européennes et coopération.",
            source_reference=SourceReference(pages=[35, 36], sections=["L'Union européenne"]),
            display_order=3,
            created_at=timestamp
        ),

        # ==========================================
        # Category 4: Culture and Society (4 topics)
        # ==========================================
        Topic(
            topic_id="cult-001",
            name="Les valeurs de la République",
            category=Category.FRENCH_CULTURE,
            description="Liberté, Égalité, Fraternité, Laïcité et les principes fondamentaux de la République française.",
            source_reference=SourceReference(pages=[40, 41], sections=["Les valeurs", "La laïcité"]),
            display_order=1,
            created_at=timestamp
        ),
        Topic(
            topic_id="cult-002",
            name="Les symboles nationaux",
            category=Category.FRENCH_CULTURE,
            description="Le drapeau tricolore, La Marseillaise, Marianne, et autres symboles de la France.",
            source_reference=SourceReference(pages=[44, 45, 46], sections=["Les symboles"]),
            display_order=2,
            created_at=timestamp
        ),
        Topic(
            topic_id="cult-003",
            name="Les droits et devoirs du citoyen",
            category=Category.FRENCH_CULTURE,
            description="Les droits fondamentaux, le vote, le service civique, et les responsabilités civiques.",
            source_reference=SourceReference(pages=[50, 51, 52], sections=["Droits et devoirs"]),
            display_order=3,
            created_at=timestamp
        ),
        Topic(
            topic_id="cult-004",
            name="Culture et patrimoine français",
            category=Category.FRENCH_CULTURE,
            description="La langue française, la littérature, les arts, et le patrimoine culturel.",
            source_reference=SourceReference(pages=[55, 57], sections=["Culture et patrimoine"]),
            display_order=4,
            created_at=timestamp
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
            print(f"  ⏭️  Topic already exists: {topic.topic_id} - {topic.name}")
            existing_count += 1
        else:
            print(f"  ✅ Creating topic: {topic.topic_id} - {topic.name}")
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
    for category in [Category.FRENCH_HISTORY, Category.FRENCH_POLITICS,
                     Category.FRENCH_GEOGRAPHY, Category.FRENCH_CULTURE]:
        category_topics = [t for t in topics if t.category == category]
        print(f"\n   {category}:")
        for topic in category_topics:
            print(f"      - {topic.topic_id}: {topic.name}")

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
