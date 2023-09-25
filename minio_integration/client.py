from django.conf import settings
import json
import boto3
import minio
policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": "*"},
            "Action": [
                "s3:GetBucketLocation",
                "s3:ListBucket",
                "s3:ListBucketMultipartUploads",
            ],
            "Resource": "arn:aws:s3:::my-bucket",
        },
        {
            "Effect": "Allow",
            "Principal": {"AWS": "*"},
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListMultipartUploadParts",
                "s3:AbortMultipartUpload",
            ],
            "Resource": "arn:aws:s3:::my-bucket/images/*",
        },
    ],
}


def get_minio_client():
    return minio.Minio(
        endpoint=settings.MINIO_S3_ENDPOINT,
        access_key=settings.MINIO_S3_ACCESS_KEY_ID,
        secret_key=settings.MINIO_S3_SECRET_ACCESS_KEY,
        region=settings.MINIO_S3_REGION_NAME,
    )


def create_busket(client, bucket_name):
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name, location=settings.MINIO_S3_REGION_NAME, object_lock=False)


def s3_generate_presigned_post(file_path: str, file_type: str):
    s3_client = get_minio_client()
    s3_client.set_bucket_policy(settings.MINIO_STORAGE_BUCKET_NAME, json.dumps(policy))
    create_busket(s3_client, settings.MINIO_STORAGE_BUCKET_NAME)

    acl = settings.MINIO_DEFAULT_ACL
    expires_in = settings.MINIO_PRESIGNED_EXPIRY

    presigned_data = s3_client.presigned_put_object(
        settings.MINIO_STORAGE_BUCKET_NAME,
        file_path,
        expires=expires_in,
    )

    return presigned_data
