# Data Model and DynamoDB Schema Design

## Overview

This document defines the complete data model for the French Civics Test Preparation App, including DynamoDB table schemas, access patterns, and sample queries.

## Design Principles

1. **Single-table per entity**: Each entity gets its own table for clarity and maintainability
2. **Query-first design**: Tables and indexes optimized for known access patterns
3. **Denormalization**: Some data duplication to avoid expensive joins
4. **Caching**: UserStats table caches computed metrics to avoid expensive aggregations
5. **Source traceability**: Every question links to a specific Livret page/section

---

## Tables

### 1. Users Table

**Purpose**: Store user profile and authentication metadata

**Table Name**: `FrenchCivics-Users`

**Primary Key**:
- **Partition Key (PK)**: `user_id` (String) - Cognito sub claim

**Attributes**:
```typescript
{
  user_id: string;           // Cognito sub (UUID)
  email: string;             // From Cognito
  name?: string;             // Optional display name
  created_at: string;        // ISO 8601 timestamp
  last_login: string;        // ISO 8601 timestamp
  cognito_username: string;  // Cognito username
}
```

**Indexes**: None (always query by user_id)

**Access Patterns**:
1. Get user by user_id (from JWT)
2. Update last_login timestamp on each login

**Sample Item**:
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "email": "marie.dupont@example.com",
  "name": "Marie Dupont",
  "cognito_username": "marie.dupont",
  "created_at": "2026-01-15T10:30:00Z",
  "last_login": "2026-01-17T14:22:33Z"
}
```

**Sample Queries**:
```python
# Get user profile
response = users_table.get_item(
    Key={'user_id': user_id}
)

# Update last login
users_table.update_item(
    Key={'user_id': user_id},
    UpdateExpression='SET last_login = :timestamp',
    ExpressionAttributeValues={':timestamp': datetime.utcnow().isoformat()}
)
```

---

### 2. Topics Table

**Purpose**: Define learning domains and subtopics

**Table Name**: `FrenchCivics-Topics`

**Primary Key**:
- **Partition Key (PK)**: `topic_id` (String)

**Attributes**:
```typescript
{
  topic_id: string;              // e.g., "french_history_revolution"
  category: string;              // "French History" | "French Politics" | "French Geography" | "French Culture"
  name: string;                  // Display name: "French Revolution"
  description: string;           // Brief description
  source_reference: {            // Where in Livret this topic is covered
    pages: number[];             // e.g., [4, 5, 14]
    sections: string[];          // e.g., ["Les principes de la République"]
  };
  created_at: string;
  display_order: number;         // For UI ordering
}
```

**Global Secondary Index (GSI1)**:
- **Partition Key**: `category`
- **Sort Key**: `display_order`
- **Purpose**: List all topics in a category, sorted by display order

**Access Patterns**:
1. Get topic by topic_id
2. List all topics in a category (GSI1)
3. List all topics across all categories

**Sample Item**:
```json
{
  "topic_id": "french_history_revolution",
  "category": "French History",
  "name": "French Revolution",
  "description": "The Revolution of 1789, Declaration of Rights, Republican symbols",
  "source_reference": {
    "pages": [4, 14],
    "sections": ["Les principes de la République", "La Révolution française"]
  },
  "display_order": 3,
  "created_at": "2026-01-10T00:00:00Z"
}
```

**Sample Queries**:
```python
# Get specific topic
response = topics_table.get_item(
    Key={'topic_id': 'french_history_revolution'}
)

# List all topics in "French History" category, sorted
response = topics_table.query(
    IndexName='GSI1-category-displayOrder',
    KeyConditionExpression='category = :cat',
    ExpressionAttributeValues={':cat': 'French History'}
)

# Scan all topics (use sparingly)
response = topics_table.scan()
```

---

### 3. Questions Table

**Purpose**: Store practice questions with answer validation and source references

**Table Name**: `FrenchCivics-Questions`

**Primary Key**:
- **Partition Key (PK)**: `question_id` (String - UUID)

**Attributes**:
```typescript
{
  question_id: string;           // UUID
  topic_id: string;              // Foreign key to Topics
  category: string;              // Denormalized for filtering
  question_text: string;         // The question
  question_type: string;         // "multiple_choice" | "true_false" | "short_answer"
  answer_options?: Array<{       // For multiple choice
    id: string;                  // "a", "b", "c", "d"
    text: string;
  }>;
  correct_answer: string;        // Option ID or exact text
  explanation: string;           // Why this is the correct answer
  difficulty: number;            // 1 (easy), 2 (medium), 3 (hard)
  source_reference: {
    document: string;            // "Livret du citoyen"
    page: number;                // Page number in PDF
    section: string;             // Section heading
    text_excerpt?: string;       // Exact quote from Livret (for AI validation)
  };
  generated_by: string;          // "manual" | "ai"
  validated: boolean;            // Has this been human-reviewed?
  created_at: string;
  updated_at?: string;
  tags?: string[];               // Additional categorization
}
```

**Global Secondary Index (GSI1)**:
- **Partition Key**: `topic_id`
- **Sort Key**: `difficulty`
- **Purpose**: Get all questions for a topic, optionally filtered by difficulty

**Global Secondary Index (GSI2)**:
- **Partition Key**: `category`
- **Sort Key**: `created_at`
- **Purpose**: Get all questions in a category, sorted by creation date

**Access Patterns**:
1. Get question by question_id (answer submission)
2. Get all questions for a topic (GSI1)
3. Get random question from topic with specific difficulty (GSI1 + random selection)
4. Get all questions in a category (GSI2)
5. Filter questions by multiple criteria (Scan with filters - used sparingly)

**Sample Item**:
```json
{
  "question_id": "q1234567-89ab-cdef-0123-456789abcdef",
  "topic_id": "french_history_revolution",
  "category": "French History",
  "question_text": "Quelle est la devise de la République française ?",
  "question_type": "multiple_choice",
  "answer_options": [
    {"id": "a", "text": "Liberté, Égalité, Fraternité"},
    {"id": "b", "text": "Travail, Famille, Patrie"},
    {"id": "c", "text": "Honneur et Patrie"},
    {"id": "d", "text": "Unité, Indivisibilité"}
  ],
  "correct_answer": "a",
  "explanation": "La devise 'Liberté, Égalité, Fraternité' représente les trois valeurs fondamentales de la République française depuis la Révolution de 1789.",
  "difficulty": 1,
  "source_reference": {
    "document": "Livret du citoyen",
    "page": 4,
    "section": "Les principes de la République",
    "text_excerpt": "La République garantit le respect des principes de liberté, d'égalité et de fraternité. Ces trois mots constituent sa devise."
  },
  "generated_by": "manual",
  "validated": true,
  "created_at": "2026-01-15T10:00:00Z",
  "tags": ["republican_values", "symbols"]
}
```

**Sample Queries**:
```python
# Get specific question (for answer validation)
response = questions_table.get_item(
    Key={'question_id': question_id}
)

# Get all questions for a topic
response = questions_table.query(
    IndexName='GSI1-topic-difficulty',
    KeyConditionExpression='topic_id = :topic',
    ExpressionAttributeValues={':topic': 'french_history_revolution'}
)

# Get easy questions for a topic
response = questions_table.query(
    IndexName='GSI1-topic-difficulty',
    KeyConditionExpression='topic_id = :topic AND difficulty = :diff',
    ExpressionAttributeValues={
        ':topic': 'french_history_revolution',
        ':diff': 1
    }
)

# Get all questions in French History category
response = questions_table.query(
    IndexName='GSI2-category-created',
    KeyConditionExpression='category = :cat',
    ExpressionAttributeValues={':cat': 'French History'}
)
```

---

### 4. UserQuestionResults Table

**Purpose**: Record every answer submitted by every user

**Table Name**: `FrenchCivics-UserQuestionResults`

**Primary Key**:
- **Partition Key (PK)**: `user_id` (String)
- **Sort Key (SK)**: `result_id` (String - composite: `timestamp#question_id`)

**Attributes**:
```typescript
{
  user_id: string;               // Cognito sub
  result_id: string;             // "2026-01-17T14:30:00.123Z#q1234567-89ab-cdef-0123-456789abcdef"
  question_id: string;           // Denormalized
  topic_id: string;              // Denormalized for analytics
  category: string;              // Denormalized for analytics
  answered_at: string;           // ISO 8601 timestamp
  correct: boolean;              // Was the answer correct?
  user_answer: string;           // What the user selected
  response_time_ms: number;      // Time taken to answer (milliseconds)
  difficulty: number;            // Denormalized question difficulty
}
```

**Global Secondary Index (GSI1)**:
- **Partition Key**: `user_id#topic_id` (composite)
- **Sort Key**: `answered_at`
- **Purpose**: Get all results for a user within a specific topic, sorted by time

**Access Patterns**:
1. Record new answer result (PutItem)
2. Get user's answer history (Query by user_id, sorted by timestamp DESC)
3. Get user's answers for a specific topic (GSI1)
4. Get recent answers (last N days) for adaptive algorithm

**Why Composite Sort Key?**
- The `result_id` combines timestamp + question_id
- Ensures uniqueness (user can answer same question multiple times)
- Allows efficient time-based queries
- Format: `YYYY-MM-DDTHH:MM:SS.sssZ#question_id`

**Sample Item**:
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "result_id": "2026-01-17T14:30:22.456Z#q1234567-89ab-cdef-0123-456789abcdef",
  "question_id": "q1234567-89ab-cdef-0123-456789abcdef",
  "topic_id": "french_history_revolution",
  "category": "French History",
  "answered_at": "2026-01-17T14:30:22.456Z",
  "correct": true,
  "user_answer": "a",
  "response_time_ms": 8500,
  "difficulty": 1
}
```

**Sample Queries**:
```python
# Record a new answer
results_table.put_item(
    Item={
        'user_id': user_id,
        'result_id': f"{timestamp}#{question_id}",
        'question_id': question_id,
        'topic_id': topic_id,
        'category': category,
        'answered_at': timestamp,
        'correct': is_correct,
        'user_answer': user_answer,
        'response_time_ms': response_time,
        'difficulty': difficulty
    }
)

# Get user's last 50 answers
response = results_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': user_id},
    ScanIndexForward=False,  # Descending order (newest first)
    Limit=50
)

# Get answers from last 7 days (for adaptive algorithm)
from datetime import datetime, timedelta
seven_days_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()

response = results_table.query(
    KeyConditionExpression='user_id = :uid AND result_id >= :since',
    ExpressionAttributeValues={
        ':uid': user_id,
        ':since': seven_days_ago
    },
    ScanIndexForward=False
)

# Get all answers for a specific topic
composite_key = f"{user_id}#{topic_id}"
response = results_table.query(
    IndexName='GSI1-userTopic-answeredAt',
    KeyConditionExpression='user_id_topic_id = :key',
    ExpressionAttributeValues={':key': composite_key}
)
```

---

### 5. UserStats Table

**Purpose**: Cache computed statistics to avoid expensive aggregations

**Table Name**: `FrenchCivics-UserStats`

**Primary Key**:
- **Partition Key (PK)**: `user_id` (String)

**Attributes**:
```typescript
{
  user_id: string;
  last_updated: string;          // ISO 8601 timestamp

  // Overall stats
  total_questions_answered: number;
  overall_accuracy: number;      // 0-100 percentage

  // Category-level stats
  accuracy_by_category: {
    [category: string]: {
      total: number;
      correct: number;
      accuracy: number;          // 0-100 percentage
      last_answered: string;     // ISO 8601
    }
  };

  // Topic-level stats (more granular)
  accuracy_by_topic: {
    [topic_id: string]: {
      total: number;
      correct: number;
      accuracy: number;          // 0-100 percentage
      recent_accuracy: number;   // Weighted for last 7 days
      last_answered: string;     // ISO 8601
    }
  };

  // Adaptive learning data
  weakest_topics: Array<{
    topic_id: string;
    topic_name: string;
    accuracy: number;
  }>;

  strongest_topics: Array<{
    topic_id: string;
    topic_name: string;
    accuracy: number;
  }>;

  // Streak tracking
  current_streak_days: number;
  longest_streak_days: number;
  last_activity_date: string;    // YYYY-MM-DD
}
```

**Indexes**: None (always access by user_id)

**Update Strategy**:
- Updated incrementally after each answer submission
- No need to scan all UserQuestionResults
- Maintains running averages

**Access Patterns**:
1. Get user stats for dashboard
2. Update stats after answer submission
3. Get weak topics for adaptive question selection

**Sample Item**:
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "last_updated": "2026-01-17T14:30:22.456Z",
  "total_questions_answered": 127,
  "overall_accuracy": 78.5,
  "accuracy_by_category": {
    "French History": {
      "total": 45,
      "correct": 38,
      "accuracy": 84.4,
      "last_answered": "2026-01-17T14:30:22.456Z"
    },
    "French Politics": {
      "total": 38,
      "correct": 28,
      "accuracy": 73.7,
      "last_answered": "2026-01-17T12:15:00.000Z"
    },
    "French Geography": {
      "total": 24,
      "correct": 16,
      "accuracy": 66.7,
      "last_answered": "2026-01-16T09:20:00.000Z"
    },
    "French Culture": {
      "total": 20,
      "correct": 17,
      "accuracy": 85.0,
      "last_answered": "2026-01-15T16:45:00.000Z"
    }
  },
  "accuracy_by_topic": {
    "french_history_revolution": {
      "total": 15,
      "correct": 13,
      "accuracy": 86.7,
      "recent_accuracy": 92.3,
      "last_answered": "2026-01-17T14:30:22.456Z"
    },
    "french_politics_institutions": {
      "total": 18,
      "correct": 12,
      "accuracy": 66.7,
      "recent_accuracy": 60.0,
      "last_answered": "2026-01-17T12:15:00.000Z"
    }
  },
  "weakest_topics": [
    {
      "topic_id": "french_geography_overseas",
      "topic_name": "Overseas Territories",
      "accuracy": 50.0
    },
    {
      "topic_id": "french_politics_institutions",
      "topic_name": "Political Institutions",
      "accuracy": 66.7
    },
    {
      "topic_id": "french_history_modern",
      "topic_name": "Modern Era (17th-18th Century)",
      "accuracy": 70.0
    }
  ],
  "strongest_topics": [
    {
      "topic_id": "french_culture_symbols",
      "topic_name": "National Symbols",
      "accuracy": 95.0
    },
    {
      "topic_id": "french_history_revolution",
      "topic_name": "French Revolution",
      "accuracy": 86.7
    }
  ],
  "current_streak_days": 5,
  "longest_streak_days": 12,
  "last_activity_date": "2026-01-17"
}
```

**Sample Queries**:
```python
# Get user stats
response = stats_table.get_item(
    Key={'user_id': user_id}
)

# Update stats after answer (increment pattern)
stats_table.update_item(
    Key={'user_id': user_id},
    UpdateExpression='''
        SET total_questions_answered = total_questions_answered + :inc,
            accuracy_by_category.#cat.total = accuracy_by_category.#cat.total + :inc,
            accuracy_by_category.#cat.correct = accuracy_by_category.#cat.correct + :correct_inc,
            accuracy_by_topic.#topic.total = accuracy_by_topic.#topic.total + :inc,
            accuracy_by_topic.#topic.correct = accuracy_by_topic.#topic.correct + :correct_inc,
            last_updated = :timestamp
    ''',
    ExpressionAttributeNames={
        '#cat': category,
        '#topic': topic_id
    },
    ExpressionAttributeValues={
        ':inc': 1,
        ':correct_inc': 1 if is_correct else 0,
        ':timestamp': timestamp
    }
)
```

---

## S3 Bucket Structure

**Bucket Name**: `french-civics-livret-content-dev`

**Objects**:
```
s3://french-civics-livret-content-dev/
├── source/
│   └── Livret_du_citoyen_V2fev2022_accessible.pdf
│
├── embeddings/
│   ├── livret-embeddings.json              # Vector embeddings for RAG
│   └── livret-chunks.json                  # Text chunks without embeddings
│
└── preprocessing/
    └── chunking-metadata.json              # Chunking configuration used
```

**livret-embeddings.json Structure**:
```json
[
  {
    "chunk_id": "chunk_001",
    "text": "La République est un régime politique dans lequel les dirigeants élus gouvernent au nom du peuple...",
    "embedding": [0.123, -0.456, 0.789, ...],  // 1536-dimension vector
    "page": 4,
    "section": "Les principes de la République",
    "category": "French Politics",
    "word_count": 87
  },
  // ... ~150 chunks total
]
```

---

## Access Pattern Summary

| Access Pattern | Table | Key/Index | Notes |
|---------------|-------|-----------|-------|
| Get user profile | Users | PK: user_id | Direct access |
| List topics by category | Topics | GSI1: category | Sorted by display_order |
| Get question by ID | Questions | PK: question_id | For answer validation |
| Get questions for topic | Questions | GSI1: topic_id | Filter by difficulty |
| Record answer | UserQuestionResults | PutItem | Composite sort key |
| Get user history | UserQuestionResults | PK: user_id | Sort by timestamp DESC |
| Get recent answers (7d) | UserQuestionResults | PK + SK range | For adaptive algorithm |
| Get user stats | UserStats | PK: user_id | Cached metrics |
| Update stats | UserStats | UpdateItem | Incremental updates |

---

## Capacity Planning

### Initial Recommendation: **On-Demand Pricing**

**Rationale**:
- Unpredictable traffic patterns during development
- No capacity planning needed
- Pay only for actual reads/writes
- Auto-scales instantly

**When to Switch to Provisioned**:
- Once you have predictable traffic patterns
- When monthly costs exceed provisioned equivalent
- Typically happens at >100K requests/month per table

### Cost Estimates (On-Demand)

**Assumptions**:
- 100 active users/month
- Each user answers 50 questions/month
- Dashboard viewed 5 times/month per user

**Reads**:
- Questions: 5,000 reads × $0.25/million = $0.00125
- Topics: 500 reads × $0.25/million = $0.000125
- UserStats: 500 reads × $0.25/million = $0.000125
- UserQuestionResults: 1,000 reads × $0.25/million = $0.00025

**Writes**:
- UserQuestionResults: 5,000 writes × $1.25/million = $0.00625
- UserStats: 5,000 updates × $1.25/million = $0.00625
- Questions: 100 writes × $1.25/million = $0.000125

**Total DynamoDB**: ~$0.02/month (negligible)

**Storage**: 5 tables × 10KB avg × 10,000 items = 500MB = $0.125/month

**Grand Total**: ~$0.15/month

---

## Data Validation Rules

### Users Table
- `user_id`: Must be valid UUID from Cognito
- `email`: Must be valid email format
- `created_at`, `last_login`: ISO 8601 timestamps

### Topics Table
- `topic_id`: Snake_case, lowercase
- `category`: Must be one of 4 valid categories
- `display_order`: Positive integer

### Questions Table
- `question_id`: UUID v4
- `topic_id`: Must exist in Topics table (foreign key)
- `difficulty`: Must be 1, 2, or 3
- `answer_options`: Required for multiple_choice, 2-6 options
- `source_reference.page`: Must be valid page number (1-28)

### UserQuestionResults Table
- `result_id`: Format `{ISO-timestamp}#{question_id}`
- `response_time_ms`: Positive integer, reasonable range (100-300000ms)

### UserStats Table
- All accuracy values: 0-100
- `total_questions_answered`: Non-negative integer
- `last_updated`: Must be recent (within last 30 days for active users)

---

## Migration Strategy

### Phase 1: Initial Deployment
1. Deploy empty tables via CDK
2. Seed Topics table (manual data)
3. Seed Questions table (40-60 manual questions)
4. Users table auto-populates on first login

### Phase 2: AI Question Generation
1. Generate embeddings for Livret (preprocessing script)
2. Upload embeddings to S3
3. Deploy RAG Lambda function
4. Generate additional questions (with validation)

### Phase 3: Analytics Enhancement
1. Add derived metrics to UserStats
2. Implement streak tracking
3. Add time-series data for progress charts

---

## Next Steps

With this data model defined, we can now:
1. ✅ Implement CDK stack definitions for all tables
2. ✅ Create Python dataclasses for type safety
3. ✅ Build repository layer (CRUD operations)
4. ✅ Seed initial data (topics and questions)
5. ✅ Implement adaptive learning algorithm

**Ready to proceed with implementation?**
