"""
Base repository with common DynamoDB operations.
"""

import os
import boto3
from typing import Any, Dict, Optional, List
from botocore.exceptions import ClientError


class BaseRepository:
    """
    Base repository class providing common DynamoDB operations.
    """

    def __init__(self, table_name: str):
        """
        Initialize repository with table name.

        Args:
            table_name: DynamoDB table name
        """
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
        self.table_name = table_name

    def get_item(self, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get a single item by primary key.

        Args:
            key: Primary key dict (e.g., {'user_id': '123'})

        Returns:
            Item dict if found, None otherwise
        """
        try:
            response = self.table.get_item(Key=key)
            return response.get('Item')
        except ClientError as e:
            raise Exception(f"Error getting item from {self.table_name}: {e}")

    def put_item(self, item: Dict[str, Any]) -> None:
        """
        Put (create or replace) an item.

        Args:
            item: Item to put

        Raises:
            Exception: If put operation fails
        """
        try:
            self.table.put_item(Item=item)
        except ClientError as e:
            raise Exception(f"Error putting item to {self.table_name}: {e}")

    def update_item(
        self,
        key: Dict[str, Any],
        update_expression: str,
        expression_attribute_values: Dict[str, Any],
        expression_attribute_names: Optional[Dict[str, str]] = None,
        return_values: str = 'ALL_NEW'
    ) -> Optional[Dict[str, Any]]:
        """
        Update an item.

        Args:
            key: Primary key
            update_expression: DynamoDB update expression
            expression_attribute_values: Values for the expression
            expression_attribute_names: Optional attribute name mappings
            return_values: What to return (default: ALL_NEW)

        Returns:
            Updated item if return_values is set, None otherwise
        """
        try:
            update_kwargs = {
                'Key': key,
                'UpdateExpression': update_expression,
                'ExpressionAttributeValues': expression_attribute_values,
                'ReturnValues': return_values
            }

            if expression_attribute_names:
                update_kwargs['ExpressionAttributeNames'] = expression_attribute_names

            response = self.table.update_item(**update_kwargs)
            return response.get('Attributes')
        except ClientError as e:
            raise Exception(f"Error updating item in {self.table_name}: {e}")

    def delete_item(self, key: Dict[str, Any]) -> None:
        """
        Delete an item.

        Args:
            key: Primary key

        Raises:
            Exception: If delete operation fails
        """
        try:
            self.table.delete_item(Key=key)
        except ClientError as e:
            raise Exception(f"Error deleting item from {self.table_name}: {e}")

    def query(
        self,
        key_condition_expression: Any,
        expression_attribute_values: Dict[str, Any],
        index_name: Optional[str] = None,
        scan_index_forward: bool = True,
        limit: Optional[int] = None,
        filter_expression: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Query items with automatic pagination handling.

        Args:
            key_condition_expression: Key condition expression
            expression_attribute_values: Values for the expression
            index_name: Optional GSI name
            scan_index_forward: Sort order (True=ascending, False=descending)
            limit: Optional result limit (total items to return across all pages)
            filter_expression: Optional filter expression

        Returns:
            List of items (handles pagination automatically)
        """
        try:
            query_kwargs = {
                'KeyConditionExpression': key_condition_expression,
                'ExpressionAttributeValues': expression_attribute_values,
                'ScanIndexForward': scan_index_forward
            }

            if index_name:
                query_kwargs['IndexName'] = index_name

            if filter_expression:
                query_kwargs['FilterExpression'] = filter_expression

            # Handle pagination
            items = []
            last_evaluated_key = None

            while True:
                # Add pagination key if we're continuing from a previous page
                if last_evaluated_key:
                    query_kwargs['ExclusiveStartKey'] = last_evaluated_key

                # If limit is set, only request remaining items
                if limit:
                    remaining = limit - len(items)
                    if remaining <= 0:
                        break
                    query_kwargs['Limit'] = remaining

                response = self.table.query(**query_kwargs)
                page_items = response.get('Items', [])
                items.extend(page_items)

                # Check if there are more pages
                last_evaluated_key = response.get('LastEvaluatedKey')
                if not last_evaluated_key:
                    break

                # If we've hit our limit, stop
                if limit and len(items) >= limit:
                    break

            return items
        except ClientError as e:
            raise Exception(f"Error querying {self.table_name}: {e}")

    def scan(
        self,
        filter_expression: Optional[Any] = None,
        expression_attribute_values: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Scan table (use sparingly - expensive operation).

        Args:
            filter_expression: Optional filter expression
            expression_attribute_values: Values for the expression
            limit: Optional result limit

        Returns:
            List of items
        """
        try:
            scan_kwargs = {}

            if filter_expression:
                scan_kwargs['FilterExpression'] = filter_expression

            if expression_attribute_values:
                scan_kwargs['ExpressionAttributeValues'] = expression_attribute_values

            if limit:
                scan_kwargs['Limit'] = limit

            response = self.table.scan(**scan_kwargs)
            return response.get('Items', [])
        except ClientError as e:
            raise Exception(f"Error scanning {self.table_name}: {e}")

    def batch_get_items(self, keys: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Batch get multiple items.

        Args:
            keys: List of primary keys

        Returns:
            List of items
        """
        try:
            response = self.dynamodb.batch_get_item(
                RequestItems={
                    self.table_name: {
                        'Keys': keys
                    }
                }
            )
            return response.get('Responses', {}).get(self.table_name, [])
        except ClientError as e:
            raise Exception(f"Error batch getting items from {self.table_name}: {e}")

    def batch_write_items(self, items: List[Dict[str, Any]]) -> None:
        """
        Batch write multiple items.

        Args:
            items: List of items to write

        Raises:
            Exception: If batch write fails
        """
        try:
            with self.table.batch_writer() as batch:
                for item in items:
                    batch.put_item(Item=item)
        except ClientError as e:
            raise Exception(f"Error batch writing items to {self.table_name}: {e}")
