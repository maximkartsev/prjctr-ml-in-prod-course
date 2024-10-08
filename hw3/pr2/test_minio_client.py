import pytest
from minio_client import get_minio_client

@pytest.fixture(scope="function")
def minio_client():
    client = get_minio_client()
    bucket_name = "testbucket"
    client.create_bucket(bucket_name)
    yield client
    client.delete_bucket(bucket_name)


def test_upload_and_download_object(minio_client):
    object_name = "test.txt"
    content = b"Hello, MinIO!"
    minio_client.upload_object("testbucket", object_name, content, len(content))

    downloaded_content = minio_client.download_object("testbucket", object_name)
    assert downloaded_content == content


def test_list_objects(minio_client):
    object_name = "test_list.txt"
    content = b"List me!"
    minio_client.upload_object("testbucket", object_name, content, len(content))

    objects = minio_client.list_objects("testbucket")
    assert object_name in objects


def test_delete_object(minio_client):
    object_name = "test_delete.txt"
    content = b"Delete me!"
    minio_client.upload_object("testbucket", object_name, content, len(content))

    minio_client.delete_object("testbucket", object_name)

    objects = minio_client.list_objects("testbucket")
    assert object_name not in objects


def test_create_existing_bucket(minio_client):
    with pytest.raises(Exception):
        minio_client.create_bucket("testbucket")
