import asyncio
import os
from functools import partial
from minio import Minio

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "avatars")
MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() == "true"

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE,
)


async def ensure_bucket():
    loop = asyncio.get_running_loop()
    exists = await loop.run_in_executor(None, client.bucket_exists, MINIO_BUCKET)
    if not exists:
        await loop.run_in_executor(None, client.make_bucket, MINIO_BUCKET)


async def upload_file(object_name: str, data, length: int, content_type: str) -> str:
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        None,
        partial(client.put_object, MINIO_BUCKET, object_name, data, length, content_type=content_type),
    )
    scheme = "https" if MINIO_SECURE else "http"
    return f"{scheme}://{MINIO_ENDPOINT}/{MINIO_BUCKET}/{object_name}"


async def check_connection() -> bool:
    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, client.bucket_exists, MINIO_BUCKET)
        return True
    except Exception:
        return False
