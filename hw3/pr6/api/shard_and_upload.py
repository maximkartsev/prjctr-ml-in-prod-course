import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from streaming import MDSWriter
from sklearn.model_selection import train_test_split
import joblib
from api.minio_client import get_minio_client
from config.constants import MINIO_SHARDS_DIR, MINIO_BUCKET_NAME, NUM_SHARDS, TFIDF_VECTOR_PATH

# Function to remove the target bucket and all its contents
def remove_bucket_if_exists(minio_client, bucket_name):
    if minio_client.client.bucket_exists(bucket_name):
        objects = minio_client.list_objects(bucket_name, recursive=True)
        for obj in objects:
            minio_client.delete_object(bucket_name, obj)
        minio_client.delete_bucket(bucket_name)

def remove_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def shard_and_upload_logic(csv_file_path: str, test_size=0.2):
    # Initialize Minio client
    minio_client = get_minio_client()

    # Remove the bucket and its contents if it already exists
    remove_bucket_if_exists(minio_client, MINIO_BUCKET_NAME)

    # Remove the TFIDF_VECTOR_PATH file if it exists
    remove_file_if_exists(TFIDF_VECTOR_PATH)

    # Create a new bucket
    minio_client.create_bucket(MINIO_BUCKET_NAME)

    # Load CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Split the data into training and testing sets
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=42)

    # Create and fit the TF-IDF vectorizer on the entire dataset (train and test)
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf.fit(df['excerpt'])

    # Save the TF-IDF vectorizer to MinIO
    os.makedirs(os.path.dirname(TFIDF_VECTOR_PATH), exist_ok=True)
    joblib.dump(tfidf, TFIDF_VECTOR_PATH)
    with open(TFIDF_VECTOR_PATH, 'rb') as f:
        minio_client.upload_object(MINIO_BUCKET_NAME, TFIDF_VECTOR_PATH, f.read(), os.path.getsize(TFIDF_VECTOR_PATH))

    # Helper function to shard and upload data
    def shard_and_upload(df_part, folder_name):
        # Transform the text data into TF-IDF vectors
        X = tfidf.transform(df_part['excerpt']).toarray()
        y = df_part['target'].values.astype(float)

        # Define columns for MDSWriter
        columns = {
            'inputs': 'ndarray',
            'targets': 'float32'
        }

        # Create the path for shards in MinIO
        shard_path = f's3://{MINIO_BUCKET_NAME}/{MINIO_SHARDS_DIR}/{folder_name}'

        compression = 'zstd'

        # Write shard data to the local folder
        with MDSWriter(out=shard_path, columns=columns, keep_local=False, compression=compression, size_limit="67mb") as writer:
            for i in range(len(X)):
                writer.write({
                    'inputs': X[i],
                    'targets': y[i]
                })

        print(f"Sharded and uploaded {folder_name} dataset successfully.")

    # Shard and upload training and testing datasets
    shard_and_upload(train_df, 'train')
    shard_and_upload(test_df, 'test')

    print("Sharding, uploading, and saving TF-IDF vectorizer completed successfully.")
