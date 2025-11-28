from django.conf import settings

from project.project.custom_s3 import get_s3_client

def upload_to_s3(file, filename):
    s3 = get_s3_client()
    key = f"media/{filename}"

    s3.upload_fileobj(
        file,
        settings.AWS_STORAGE_BUCKET_NAME,
        key
    )

    return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{key}"
