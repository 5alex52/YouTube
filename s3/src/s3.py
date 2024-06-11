import boto3
from botocore.client import Config
from src.settings import settings


s3 = boto3.client(
    "s3",
    endpoint_url=settings.S3_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    region_name=settings.AWS_REGION,
)