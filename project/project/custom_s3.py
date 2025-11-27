import boto3
from django.core.files.storage import Storage
from django.conf import settings


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )


class Boto3StaticStorage(Storage):
    folder = "static"  # folder inside bucket

    def _open(self, name, mode="rb"):
        s3 = get_s3_client()
        obj = s3.get_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"{self.folder}/{name}"
        )
        return obj['Body']

    def _save(self, name, content):
        s3 = get_s3_client()
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"{self.folder}/{name}",
            Body=content.read(),
            ACL="public-read",
            ContentType="application/octet-stream",
        )
        return name

    def url(self, name):
        return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{self.folder}/{name}"


class Boto3MediaStorage(Storage):
    folder = "media"  # for user uploads

    def _open(self, name, mode="rb"):
        s3 = get_s3_client()
        obj = s3.get_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"{self.folder}/{name}"
        )
        return obj['Body']

    def _save(self, name, content):
        s3 = get_s3_client()
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"{self.folder}/{name}",
            Body=content.read(),
            ACL="public-read",
        )
        return name

    def url(self, name):
        return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{self.folder}/{name}"
