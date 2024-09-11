# MinIO-Client
MINIO_ENDPOINT="minio:9000"
MINIO_ACCESS_KEY="minioadmin"
MINIO_SECRET_KEY="minioadmin"
MINIO_USE_SSL="0"

# MinIO-related constants
MINIO_BUCKET_NAME = "dataset-bucket"
MINIO_SHARDS_DIR = "shards"

# Model-related constants
TFIDF_MAX_FEATURES = 10000
MODEL_HIDDEN_LAYER_1_UNITS = 128
MODEL_HIDDEN_LAYER_2_UNITS = 64
MODEL_OUTPUT_UNITS = 1

# File paths
TRAINED_MODEL_PATH = "model/trained_model.pth"
TFIDF_VECTOR_PATH = "model/tfidf_vectorizer.pkl"

# Other constants
NUM_SHARDS = 10
BATCH_SIZE = 32
EPOCHS = 10