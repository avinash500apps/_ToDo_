from fastapi import FastAPI, File, UploadFile
import boto3
from botocore.config import Config
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Fetch credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_REGION = os.getenv("S3_REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# S3 Client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=S3_REGION,
    config=Config(signature_version="s3v4")
)
