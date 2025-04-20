
from .storage import Storage
from io import BytesIO
from src.core.config import settings
import boto3
import asyncio


class S3Storage(Storage):
    def __init__(self, bucket_name: str, region_name: str = 'us-east-1', access_key: str = None, secret_key: str = None):
        self.bucket_name = bucket_name
        self.region_name = region_name
        self.s3_client = boto3.client(
            's3',
            region_name=self.region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    async def upload(self, file: BytesIO, file_name: str) -> str:
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._upload_file, file, file_name)
            return f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{file_name}"
        except Exception as e:
            raise

    def _upload_file(self, file: BytesIO, file_name: str):
        try:
            self.s3_client.upload_fileobj(file, self.bucket_name, file_name)
        except Exception as e:
            raise


s3_storage = S3Storage(
    bucket_name=settings.s3_bucket_name,
    region_name=settings.s3_region_name,
    access_key=settings.s3_access_key,
    secret_key=settings.s3_secret_key
)