import boto3
import botocore.config
import json
from datetime import datetime
from botocore.exceptions import ClientError


def generate_code_using_bedrock(message:str,language:str) ->str:

    # Create a Bedrock Runtime client in the AWS Region of your choice.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Set the model ID, e.g., Claude 3 Haiku.
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"

    prompt = f"""
Human: Write {language} code for the following instructions: {message}.
    Assistant:
    """

    # Format the request payload using the model's native structure.
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.5,
        "messages": [
            {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)
    print(f'actual request to send to bedrock model {request}')
    print("MODEL ID:", model_id)
    print("REGION:", boto3.session.Session().region_name)

    try:
        #bedrock = boto3.client("bedrock-runtime",region_name="us-east-1",config = botocore.config.Config(read_timeout=300, retries = {'max_attempts':3}))
        response = client.invoke_model(modelId=model_id, body=request)
        print(f"Response from bedrock {response}")
        response_content = response["body"].read().decode("utf-8")
        response_data = json.loads(response_content)
        print(f'actual response_data {response_data}')
        response_data = json.loads(response_content)
        code = response_data["content"][0]["text"].strip()
        return code

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

def save_code_to_s3_bucket(code, s3_bucket, s3_key):

    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body = code)
        print("Code saved to s3")

    except Exception as e:
        print("Error when saving the code to s3")

def lambda_handler(event, context):

    if 'body' in event and event['body']:
        body = json.loads(event['body'])
        message = body['message']
        language = body['key']

    elif 'queryStringParameters' in event:
        params = event['queryStringParameters']
        message = params['message']
        language = params['key']

    else:
        return {
            "statusCode": 400,
            "body": "Invalid request"
        }

    print(message, language)

    generated_code = generate_code_using_bedrock(message, language)

    if generated_code:
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f'code-output/{current_time}.py'
        s3_bucket = 'bedrock-gen-code-bucket'

        save_code_to_s3_bucket(generated_code,s3_bucket,s3_key)

    else:
        print("No code was generated")

    return {
        'statusCode':200,
        'body':json.dumps('Code generation ')

    }