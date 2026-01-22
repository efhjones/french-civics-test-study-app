#!/usr/bin/env python3
"""
Migrate UserStats table from old field names to new field names.

Old schema:
- accuracy_by_category (with stored 'accuracy' field)
- accuracy_by_topic (with stored 'accuracy' field)

New schema:
- stats_by_category (without 'accuracy' field - calculated via @property)
- stats_by_topic (without 'accuracy' field - calculated via @property)

Usage:
    python scripts/migrate_stats_fields.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import boto3
from decimal import Decimal

def migrate_stats():
    """Migrate all user stats from old to new field names."""

    table_name = os.getenv('STATS_TABLE', 'FrenchCivics-UserStats')
    region = os.getenv('AWS_REGION', 'us-east-1')

    print(f"🔄 Migrating stats in table: {table_name} (region: {region})\n")

    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

    # Scan all items
    print("📥 Scanning table...")
    response = table.scan()
    items = response['Items']

    if not items:
        print("ℹ️  No stats records found")
        return

    print(f"Found {len(items)} stats records\n")

    migrated = 0
    skipped = 0
    errors = 0

    for item in items:
        user_id = item['user_id']

        # Check if already migrated
        if 'stats_by_category' in item:
            print(f"⏭️  {user_id}: Already migrated")
            skipped += 1
            continue

        print(f"🔄 {user_id}: Migrating...")

        try:
            # Get old data
            old_cat_data = item.get('accuracy_by_category', {})
            old_topic_data = item.get('accuracy_by_topic', {})

            # Clean up the data (remove 'accuracy' field)
            new_cat_data = {}
            for category, stats in old_cat_data.items():
                new_cat_data[category] = {
                    'total': stats['total'],
                    'correct': stats['correct'],
                    'last_answered': stats['last_answered']
                }

            new_topic_data = {}
            for topic_id, stats in old_topic_data.items():
                new_topic_data[topic_id] = {
                    'total': stats['total'],
                    'correct': stats['correct'],
                    'recent_accuracy': stats.get('recent_accuracy', Decimal('0')),
                    'last_answered': stats['last_answered']
                }

            # Update item with new field names
            update_expr = "SET stats_by_category = :cat, stats_by_topic = :topic REMOVE accuracy_by_category, accuracy_by_topic"

            table.update_item(
                Key={'user_id': user_id},
                UpdateExpression=update_expr,
                ExpressionAttributeValues={
                    ':cat': new_cat_data,
                    ':topic': new_topic_data
                }
            )

            print(f"   ✅ Migrated successfully")
            migrated += 1

        except Exception as e:
            print(f"   ❌ Error: {e}")
            errors += 1

    print(f"\n{'='*60}")
    print(f"📊 Migration Summary:")
    print(f"   ✅ Migrated: {migrated}")
    print(f"   ⏭️  Skipped:  {skipped}")
    print(f"   ❌ Errors:   {errors}")
    print(f"{'='*60}")

    if errors == 0:
        print("\n✨ Migration complete!")
    else:
        print(f"\n⚠️  Migration completed with {errors} errors")
        sys.exit(1)


if __name__ == "__main__":
    try:
        migrate_stats()
    except KeyboardInterrupt:
        print("\n\n❌ Migration interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
