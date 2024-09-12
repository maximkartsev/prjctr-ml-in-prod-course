from fastapi import FastAPI
from app.vectorizer import get_bert_embeddings
from app.vectordb import VectorDB
import os

app = FastAPI()

# Initialize Qdrant-based vector database
vector_db = VectorDB()

# Load and ingest data from the dataset
@app.get("/ingest")
def ingest_data():
    data_file = "/app/data/sample_texts.txt"
    
    if not os.path.exists(data_file):
        return {"error": "Dataset file not found"}

    # Read the dataset
    with open(data_file, 'r') as f:
        texts = f.readlines()

    # Convert texts to vectors using BERT
    vectors = get_bert_embeddings(texts)

    # Ingest the vectors into Qdrant
    vector_db.ingest_vectors(vectors, texts)

    return {"message": f"Ingested {len(texts)} texts into Qdrant."}


# Perform similarity search in the VectorDB
@app.get("/query")
def query_vector_db(query_text: str, top_k: int = 3):
    # Convert the query to a vector
    query_vector = get_bert_embeddings([query_text])

    # Perform similarity search in Qdrant
    results = vector_db.query(query_vector[0], top_k=top_k)

    return {"results": results}

@app.get("/generate_answer")
def get_answer(query_text: str, top_k: int = 3):
    # Step 1: Convert the query to a vector
    query_vector = get_bert_embeddings([query_text])[0]

    # Step 2: Generate the answer using context and Hugging Face LLM
    answer = vector_db.generate_answer(query_vector, query_text, top_k=top_k)

    return {"answer": answer}