# French Civics Test Preparation App

A production-quality learning application for French citizenship test preparation, built with modern serverless architecture on AWS.

## Project Overview

This application helps users prepare for the French naturalization civics test by:

- Providing practice questions across 4 learning domains (History, Politics, Geography, Culture)
- Tracking learning progress and identifying weak areas
- Adaptively selecting questions based on user performance
- Generating AI-powered practice questions using RAG (Retrieval-Augmented Generation)
- Offering detailed progress analytics and insights

## Technology Stack

### Frontend

- **React** with TypeScript
- **Functional components** and hooks
- **AWS Cognito** authentication (Hosted UI)

### Backend

- **Python** on AWS Lambda
- **API Gateway** with Cognito JWT authorizer
- **DynamoDB** for data persistence
- **S3** for source content storage
- **AWS Bedrock** (Claude) or OpenAI for AI question generation

### Infrastructure

- **AWS CDK** (TypeScript) for Infrastructure as Code
- **CloudWatch** for logging and monitoring

## Project Structure

```
french-civics-test-app/
├── backend/
│   ├── infrastructure/          # AWS CDK code
│   │   ├── bin/                 # CDK app entry point
│   │   └── lib/                 # Stack definitions
│   ├── src/
│   │   ├── handlers/            # Lambda function handlers
│   │   │   ├── topics/
│   │   │   ├── questions/
│   │   │   ├── stats/
│   │   │   ├── user/
│   │   │   └── rag/
│   │   ├── services/            # Business logic layer
│   │   ├── repositories/        # Data access layer
│   │   ├── models/              # Data models
│   │   ├── utils/               # Helper functions
│   │   └── shared/              # Shared constants and types
│   ├── tests/                   # Unit and integration tests
│   ├── scripts/                 # Deployment and seeding scripts
│   │   └── Livret_du_citoyen_V2fev2022_accessible.pdf
│   ├── .env                     # Environment variables (not committed)
│   ├── .env.example             # Environment template
│   ├── .gitignore
│   ├── requirements.txt         # Python dependencies
│   └── requirements-dev.txt     # Dev dependencies
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   │   ├── auth/
│   │   │   ├── practice/
│   │   │   ├── dashboard/
│   │   │   └── common/
│   │   ├── pages/               # Top-level route components
│   │   ├── services/            # API integration
│   │   │   ├── api/
│   │   │   └── auth/
│   │   ├── hooks/               # Custom React hooks
│   │   ├── contexts/            # React Context providers
│   │   ├── types/               # TypeScript types
│   │   ├── utils/               # Helper functions
│   │   ├── styles/              # Global styles
│   │   └── config/              # Configuration
│   ├── .env                     # Environment variables (not committed)
│   ├── .env.example             # Environment template
│   ├── .gitignore
│   └── package.json
│
├── .gitignore                   # Root gitignore
└── README.md                    # This file
```

## Learning Domains

All questions must belong to one of four categories:

1. **French History**

   - Prehistory & Antiquity
   - Middle Ages
   - Modern Era (17th-18th century)
   - French Revolution
   - 19th-20th Century
   - World Wars

2. **French Politics and Institutions**

   - Republican principles (Liberté, Égalité, Fraternité)
   - Government structure (President, Parliament, Courts)
   - Rights and duties of citizens
   - Local government (communes, departments, regions)

3. **French Culture**

   - Notable figures (writers, scientists, artists)
   - Language and arts
   - National symbols (flag, anthem, motto)

4. **French Geography**
   - Regions and departments
   - Physical geography (mountains, rivers)
   - Overseas territories

## Data Models

### Core Entities

- **User**: Authentication and profile
- **Topic**: Learning domain categorization
- **Question**: Practice questions with source references
- **UserQuestionResult**: Individual answer records
- **UserStats**: Cached performance metrics

## Setup Instructions

### Prerequisites

1. **AWS Account** with programmatic access configured
2. **Node.js** (v16+) and npm
3. **Python** (3.9+)
4. **AWS CLI** installed and configured
5. **Git** for version control

### Step 1: Configure AWS Credentials

```bash
# Check if AWS CLI is installed
aws --version

# Configure credentials (if not already done)
aws configure

# Verify access
aws sts get-caller-identity
```

### Step 2: Update Environment Variables

#### Backend

1. Get your AWS Account ID:

   ```bash
   aws sts get-caller-identity --query Account --output text
   ```

2. Edit `backend/.env`:
   - Paste your AWS Account ID
   - (Optional) Add OpenAI API key if not using Bedrock

#### Frontend

Environment variables will be populated after backend deployment.

### Step 3: Install Dependencies

#### Backend CDK

```bash
cd backend/infrastructure
npm install
```

#### Backend Python (for local development)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### Frontend

```bash
cd frontend
npm install
```

### Step 4: Bootstrap AWS CDK (One-time)

```bash
cd backend/infrastructure
cdk bootstrap aws://YOUR-ACCOUNT-ID/us-east-1
```

### Step 5: Deploy Infrastructure

```bash
cd backend/infrastructure
cdk deploy --all
```

This will create:

- Cognito User Pool
- DynamoDB tables
- Lambda functions
- API Gateway
- S3 buckets
- IAM roles

**Important**: After deployment, CDK will output:

- `CognitoUserPoolId`
- `CognitoClientId`
- `ApiGatewayUrl`

Copy these values to:

- `backend/.env`
- `frontend/.env`

### Step 6: Seed Initial Questions

```bash
cd backend
python scripts/seed_initial_questions.py
```

### Step 7: Run Frontend Locally

```bash
cd frontend
npm start
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

## Development Workflow

### Running Tests

#### Backend

```bash
cd backend
pytest tests/
```

#### Frontend

```bash
cd frontend
npm test
```

### Code Quality

#### Backend (Python)

```bash
# Type checking
mypy src/

# Linting
flake8 src/

# Formatting
black src/
```

#### Frontend (TypeScript/React)

```bash
# Linting
npm run lint

# Formatting
npm run format
```

### Local Lambda Testing

Use AWS SAM CLI for local testing:

```bash
cd backend
sam local start-api
```

## Architecture Decisions

### Why DynamoDB over RDS?

- **Serverless fit**: No connection pooling issues with Lambda
- **Performance**: Single-digit millisecond latency
- **Cost**: Pay-per-request, no idle database cost
- **Scalability**: Automatic scaling

### Why In-Lambda Vector Search over OpenSearch?

- **Corpus size**: Only ~150 chunks from 28-page Livret
- **Cost**: $0.10/month vs $350/month
- **Performance**: Faster for small datasets (10-20ms)
- **Simplicity**: Fewer services to manage

### Why Manual Question Seeding First?

- Ensures quality baseline (40-60 curated questions)
- Validates data model before AI generation
- Provides examples for AI prompt engineering

## Adaptive Learning Algorithm

The system uses a weighted algorithm to select questions:

- **60%** from weak topics (accuracy < 60%)
- **30%** from medium topics (accuracy 60-80%)
- **10%** from strong topics (accuracy > 80%)

Recent answers (last 7 days) are weighted more heavily than older ones.

## AI Question Generation (RAG Pipeline)

### Hallucination Prevention Strategy

1. **Retrieve**: Find relevant Livret chunks via vector similarity
2. **Constrain**: Provide ONLY retrieved text to LLM
3. **Prompt**: Instruct LLM to return "INSUFFICIENT_INFORMATION" if answer not in text
4. **Validate**: Verify answer exists in source chunks
5. **Store**: Save question with source reference

**Golden Rule**: No question is saved without explicit source validation.

## Security

- **Authentication**: AWS Cognito with JWT tokens
- **Authorization**: API Gateway Cognito Authorizer
- **User ID**: Always extracted from JWT claims, NEVER from request body
- **IAM**: Least-privilege roles for all services
- **Secrets**: Stored in AWS Secrets Manager (API keys)
- **Encryption**: DynamoDB encryption at rest enabled
- **Audit**: CloudTrail logs all API calls

## Next Steps

1. ✅ **Architecture and folder structure** (Done)
2. 🔄 **Data model and DynamoDB schema design** (Next)
3. ⏳ Authentication and backend skeleton
4. ⏳ Flashcard flow and progress tracking
5. ⏳ Adaptive learning algorithm
6. ⏳ AI RAG pipeline and validation
7. ⏳ Frontend integration
8. ⏳ Dashboard and analytics

## Resources

- [Livret du citoyen (PDF)](backend/scripts/Livret_du_citoyen_V2fev2022_accessible.pdf)
- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [React Documentation](https://react.dev/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)

**Author**: Emily Jones
**Last Updated**: 2026-01-17
