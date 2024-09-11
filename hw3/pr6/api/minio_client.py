import os
import io
from minio import Minio
from config.constants import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_USE_SSL

class MinioClient:
    def __init__(self, endpoint, access_key, secret_key, secure=True):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)

    def create_bucket(self, bucket_name):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
        else:
            raise Exception(f"Bucket '{bucket_name}' already exists.")

    def upload_object(self, bucket_name, object_name, data, length, content_type='application/octet-stream'):
        self.client.put_object(bucket_name, object_name, io.BytesIO(data), length, content_type=content_type)

    def download_object(self, bucket_name, object_name):
        response = self.client.get_object(bucket_name, object_name)
        return response.read()

    def list_objects(self, bucket_name, prefix=None, recursive=False):
        objects = self.client.list_objects(bucket_name, prefix=prefix, recursive=recursive)
        return [obj.object_name for obj in objects]

    def delete_object(self, bucket_name, object_name):
        self.client.remove_object(bucket_name, object_name)

    def delete_bucket(self, bucket_name):
        if self.client.bucket_exists(bucket_name):
            objects = self.list_objects(bucket_name)
            for obj in objects:
                self.delete_object(bucket_name, obj)
            self.client.remove_bucket(bucket_name)
        else:
            raise Exception(f"Bucket '{bucket_name}' does not exist.")


def get_minio_client():
    endpoint = os.getenv("MINIO_ENDPOINT", MINIO_ENDPOINT)
    access_key = os.getenv("MINIO_ACCESS_KEY", MINIO_ACCESS_KEY)
    secret_key = os.getenv("MINIO_SECRET_KEY", MINIO_SECRET_KEY)
    secure = os.getenv("MINIO_USE_SSL", MINIO_USE_SSL) == "1"
    return MinioClient(endpoint, access_key, secret_key, secure)