import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from streaming import StreamingDataset
from api.model import RegressionModel
from api.minio_client import get_minio_client
from config.constants import MINIO_BUCKET_NAME, MINIO_SHARDS_DIR, BATCH_SIZE, EPOCHS, TRAINED_MODEL_PATH, TFIDF_VECTOR_PATH
import joblib

def remove_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

# Function to download the TF-IDF vectorizer from MinIO
def download_tfidf_vectorizer(minio_client):
    remove_file_if_exists(TFIDF_VECTOR_PATH)
    os.makedirs(os.path.dirname(TFIDF_VECTOR_PATH), exist_ok=True)
    data = minio_client.download_object(MINIO_BUCKET_NAME, TFIDF_VECTOR_PATH)
    with open(TFIDF_VECTOR_PATH, 'wb') as f:
        f.write(data)
    return joblib.load(TFIDF_VECTOR_PATH)
    
# Function to upload model to MinIO
def upload_model_to_minio(minio_client, model_path):    
    minio_client.delete_object(MINIO_BUCKET_NAME, model_path)
    print(f"Existing model {model_path} deleted from MinIO.")
    
    # Upload the new model
    with open(model_path, 'rb') as model_file:
        file_size = os.path.getsize(model_path)
        minio_client.upload_object(MINIO_BUCKET_NAME, model_path, model_file.read(), file_size)
        print(f"New model {model_path} uploaded to MinIO.")



# Function to load dataset from MinIO shards
def load_dataset(folder_name):
    # Print out paths for debugging
    local_path = f'/tmp/{folder_name}'
    remote_path = f's3://{MINIO_BUCKET_NAME}/{MINIO_SHARDS_DIR}/{folder_name}'
    print(f"Local path: {local_path}")
    print(f"Remote path: {remote_path}")
    
    # Create StreamingDataset with local and remote paths for training or validation data
    dataset = StreamingDataset(
        local=local_path,  # Local cache directory
        remote=remote_path,  # Remote location in MinIO
        shuffle=True,
        batch_size=BATCH_SIZE,  # Pass batch_size to StreamingDataset
        predownload=8 * BATCH_SIZE,  # Explicitly set predownload
        num_canonical_nodes=1,  # Set num_canonical_nodes (depends on your setup)
        shuffle_block_size=262144  # Set shuffle_block_size
    )
    return DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False)


def train_logic():
    minio_client = get_minio_client()
    
    # Download the TF-IDF vectorizer from MinIO
    tfidf = download_tfidf_vectorizer(minio_client)
    input_dim = len(tfidf.get_feature_names_out())  # Actual TF-IDF input dimension

    # Initialize the model, loss function, and optimizer
    model = RegressionModel(input_dim)
    criterion = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

    # Load the training and validation datasets
    train_loader = load_dataset('train')
    val_loader = load_dataset('test')

    # Training loop
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        for batch in train_loader:
            # If batch['inputs'] and batch['targets'] are tensors, use clone().detach()
            inputs = batch['inputs'].clone().detach().float()  # Ensure it's copied properly as a tensor
            targets = batch['targets'].clone().detach().float().unsqueeze(1)  # Ensure it's copied properly as a tensor

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        print(f'Epoch {epoch+1}/{EPOCHS}, Loss: {running_loss/len(train_loader)}')

        # Validation loop
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for batch in val_loader:
                inputs = batch['inputs'].clone().detach().float()  # Ensure it's copied properly as a tensor
                targets = batch['targets'].clone().detach().float().unsqueeze(1)  # Ensure it's copied properly as a tensor

                outputs = model(inputs)
                loss = criterion(outputs, targets)
                val_loss += loss.item()

        print(f'Epoch {epoch+1}/{EPOCHS}, Validation Loss: {val_loss/len(val_loader)}')

    # Save the trained model
    torch.save(model.state_dict(), TRAINED_MODEL_PATH)
    print("Model training completed successfully.")
    
     # Upload the model to MinIO
    upload_model_to_minio(minio_client, TRAINED_MODEL_PATH)
    print("Model uploaded to s3.")

