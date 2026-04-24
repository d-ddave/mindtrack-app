import boto3
from botocore.config import Config

from app.core.config import settings

_s3_client = boto3.client(
    "s3",
    endpoint_url=settings.CLOUDFLARE_R2_ENDPOINT,
    aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY,
    aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_KEY,
    config=Config(
        signature_version="s3v4",
        region_name="auto",
    ),
)


def upload_file(
    file_bytes: bytes,
    key: str,
    content_type: str = "application/octet-stream",
) -> str:
    _s3_client.put_object(
        Bucket=settings.CLOUDFLARE_R2_BUCKET,
        Key=key,
        Body=file_bytes,
        ContentType=content_type,
    )
    return key


def get_presigned_url(key: str, expires_in: int = 3600) -> str:
    url = _s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.CLOUDFLARE_R2_BUCKET,
            "Key": key,
        },
        ExpiresIn=expires_in,
    )
    return url


def delete_file(key: str) -> None:
    _s3_client.delete_object(
        Bucket=settings.CLOUDFLARE_R2_BUCKET,
        Key=key,
    )


def list_files(prefix: str = "") -> list[str]:
    response = _s3_client.list_objects_v2(
        Bucket=settings.CLOUDFLARE_R2_BUCKET,
        Prefix=prefix,
    )
    contents = response.get("Contents", [])
    return [obj["Key"] for obj in contents]
