import boto3
import os
from dotenv import load_dotenv

load_dotenv()
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

aws_bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1", aws_access_key_id =aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


