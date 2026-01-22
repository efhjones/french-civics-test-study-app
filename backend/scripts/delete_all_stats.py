#!/usr/bin/env python3
"""
Delete all user stats from UserStats table.

This is useful when you want to start fresh with a new schema.
All users will get fresh stats on their next answer submission.

Usage:
    python scripts/delete_all_stats.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import boto3


def delete_all_stats():
    """Delete all stats records from the table."""

    table_name = os.getenv('STATS_TABLE', 'FrenchCivics-UserStats')
    region = os.getenv('AWS_REGION', 'us-east-1')

    print(f"🗑️  Deleting all stats from: {table_name} (region: {region})\n")

    # Confirm with user
    response = input("⚠️  This will DELETE ALL user statistics. Are you sure? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("❌ Deletion cancelled")
        return

    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

    # Scan all items
    print("\n📥 Scanning table...")
    response = table.scan()
    items = response['Items']

    if not items:
        print("ℹ️  No stats records found")
        return

    print(f"Found {len(items)} stats records to delete\n")

    deleted = 0
    errors = 0

    for item in items:
        user_id = item['user_id']

        try:
            print(f"🗑️  Deleting stats for: {user_id}")
            table.delete_item(Key={'user_id': user_id})
            deleted += 1
        except Exception as e:
            print(f"   ❌ Error: {e}")
            errors += 1

    print(f"\n{'='*60}")
    print(f"📊 Deletion Summary:")
    print(f"   🗑️  Deleted: {deleted}")
    print(f"   ❌ Errors:  {errors}")
    print(f"{'='*60}")

    if errors == 0:
        print("\n✅ All stats deleted successfully!")
        print("ℹ️  Users will get fresh stats on next answer submission.")
    else:
        print(f"\n⚠️  Deletion completed with {errors} errors")
        sys.exit(1)


if __name__ == "__main__":
    try:
        delete_all_stats()
    except KeyboardInterrupt:
        print("\n\n❌ Deletion interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Deletion failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
