#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import * as dotenv from 'dotenv';
import * as path from 'path';
import { CognitoStack } from '../lib/cognito-stack';
import { DynamoDBStack } from '../lib/dynamodb-stack';
import { S3Stack } from '../lib/s3-stack';
import { LambdaStack } from '../lib/lambda-stack';
import { ApiGatewayStack } from '../lib/api-gateway-stack';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

const app = new cdk.App();

// Get environment variables
const account = process.env.AWS_ACCOUNT_ID || process.env.CDK_DEFAULT_ACCOUNT;
const region = process.env.AWS_REGION || process.env.CDK_DEFAULT_REGION || 'us-east-1';
const environment = process.env.ENVIRONMENT || 'development';

if (!account) {
  throw new Error('AWS_ACCOUNT_ID must be set in .env file or CDK_DEFAULT_ACCOUNT must be available');
}

const env = {
  account,
  region,
};

// Stack naming prefix
const stackPrefix = `FrenchCivics-${environment}`;

// 1. Cognito Stack - Authentication
const cognitoStack = new CognitoStack(app, `${stackPrefix}-Cognito`, {
  env,
  description: 'Cognito User Pool for French Civics Test App',
});

// 2. DynamoDB Stack - Data persistence
const dynamoDBStack = new DynamoDBStack(app, `${stackPrefix}-DynamoDB`, {
  env,
  description: 'DynamoDB tables for French Civics Test App',
});

// 3. S3 Stack - Static content and embeddings
const s3Stack = new S3Stack(app, `${stackPrefix}-S3`, {
  env,
  description: 'S3 bucket for Livret du citoyen content and embeddings',
});

// 4. Lambda Stack - Business logic
const lambdaStack = new LambdaStack(app, `${stackPrefix}-Lambda`, {
  env,
  description: 'Lambda functions for French Civics Test App',
  userPool: cognitoStack.userPool,
  tables: dynamoDBStack.tables,
  livretBucket: s3Stack.livretBucket,
});

// 5. API Gateway Stack - REST API
const apiGatewayStack = new ApiGatewayStack(app, `${stackPrefix}-ApiGateway`, {
  env,
  description: 'API Gateway for French Civics Test App',
  userPool: cognitoStack.userPool,
  lambdaFunctions: lambdaStack.functions,
});

// Add tags to all stacks
const tags = {
  Project: 'FrenchCivicsTest',
  Environment: environment,
  ManagedBy: 'CDK',
};

Object.entries(tags).forEach(([key, value]) => {
  cdk.Tags.of(app).add(key, value);
});

// Outputs
new cdk.CfnOutput(cognitoStack, 'CognitoUserPoolId', {
  value: cognitoStack.userPool.userPoolId,
  description: 'Cognito User Pool ID',
  exportName: `${stackPrefix}-UserPoolId`,
});

new cdk.CfnOutput(cognitoStack, 'CognitoClientId', {
  value: cognitoStack.userPoolClient.userPoolClientId,
  description: 'Cognito User Pool Client ID',
  exportName: `${stackPrefix}-ClientId`,
});

new cdk.CfnOutput(apiGatewayStack, 'ApiGatewayUrl', {
  value: apiGatewayStack.api.url,
  description: 'API Gateway URL',
  exportName: `${stackPrefix}-ApiUrl`,
});

new cdk.CfnOutput(s3Stack, 'LivretBucketName', {
  value: s3Stack.livretBucket.bucketName,
  description: 'S3 Bucket for Livret content',
  exportName: `${stackPrefix}-BucketName`,
});
