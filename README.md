## Bedrock Code Generation API using AWS Lambda

This project demonstrates how to build a serverless code generation API using Amazon Bedrock and Claude models. The API accepts a programming request (e.g., "implement binary search in Python"), sends the prompt to a Claude model via Amazon Bedrock, generates code, and saves the generated output to an Amazon S3 bucket.

The entire solution is implemented in a single Python Lambda function and exposed through Amazon API Gateway.

## Architecture

Client (Postman / App)
        │
        ▼
Amazon API Gateway
        │
        ▼
AWS Lambda (Python)
        │
        ▼
Amazon Bedrock (Claude Model)
        │
        ▼
Generated Code
        │
        ▼
Amazon S3 Bucket

## Features

Serverless API for AI-powered code generation

Uses Amazon Bedrock Claude model

Accepts prompt input via API Gateway

Generates code in the requested language

Saves generated code to Amazon S3

Lightweight single-file Lambda implementation

Simple JSON API interface

## Technologies Used

AWS Lambda

Amazon Bedrock

Anthropic Claude Model

Amazon API Gateway

Amazon S3

Python (boto3 SDK)

## Prerequisites

Before deploying this project, ensure the following:

AWS Account with Bedrock access

Bedrock model access enabled for Claude

IAM role with permissions:

bedrock:InvokeModel

s3:PutObject

S3 bucket created to store generated code

Python 3.x runtime enabled for Lambda

## API Request Format

Endpoint example:

POST /code-generation

Request body:

{
  "key": "python",
  "message": "implement binary search"
}

Parameters:

Field	Description
key	Programming language
message	Description of code to generate
Example API Request
{
  "key": "javascript",
  "message": "implement linear search"
}
Example Response
{
  "generated_code": "function linearSearch(arr, target) { ... }"
}
Generated Code Storage

The generated code is automatically saved in the configured S3 bucket.

## Example structure:

s3://code-generation-output/
        ├── python_binary_search.txt
        ├── javascript_linear_search.txt

## Lambda Function Workflow

API Gateway sends request to Lambda

Lambda extracts:

programming language

prompt instruction

Lambda formats prompt for Claude model

Lambda calls Amazon Bedrock invoke_model API

Claude generates code

Lambda parses the response

Generated code is stored in Amazon S3

Code is returned to the API client

Example Claude Prompt Sent to Bedrock
Write python code for the following instructions:
implement binary search.
IAM Permissions Required

Example IAM policy for Lambda execution role:

{
  "Effect": "Allow",
  "Action": [
    "bedrock:InvokeModel",
    "s3:PutObject"
  ],
  "Resource": "*"
}
Configuration

Update the following variables in the Lambda function:

model_id = "anthropic.claude-3-haiku-20240307-v1:0"
s3_bucket = "your-s3-bucket-name"
Deployment Steps

Create an S3 bucket

Create a Lambda function (Python runtime)

Upload the Python code

Attach IAM role with Bedrock and S3 permissions

Increase Lambda timeout to 30 seconds

Create an API Gateway HTTP API

Integrate API Gateway with Lambda

Deploy the API

Testing the API

You can test the API using Postman or curl.

Example:

POST https://<api-id>.execute-api.<region>.amazonaws.com/code-generation

Body:

{
  "key": "python",
  "message": "implement binary search"
}
Possible Enhancements

Add support for multiple Bedrock models

Implement streaming responses

Add prompt templates

Store metadata in DynamoDB

Add authentication using Amazon Cognito

Build a frontend UI for prompt submission

Author

This project demonstrates a simple serverless AI-powered code generation API using Amazon Bedrock and AWS Lambda.