from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import numpy as np
from transformers import pipeline

class VectorDB:
    def __init__(self, collection_name="text_vectors", dimension=768):
        # Initialize Qdrant client and connect to the Qdrant service
        self.client = QdrantClient(host="qdrant", port=6333)
        self.collection_name = collection_name

        # Try to create the collection if it doesn't exist
        try:
            self.client.get_collection(collection_name)
            print(f"Collection {collection_name} already exists.")
        except Exception:
            print(f"Collection {collection_name} does not exist. Creating...")
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=dimension, distance=Distance.COSINE)
            )
            print(f"Collection {collection_name} created successfully.")

    def clear_collection(self):
        # Drop the collection to clear all points and recreate it
        try:
            self.client.delete_collection(self.collection_name)
            print(f"Collection {self.collection_name} has been deleted.")
        except Exception as e:
            print(f"Error deleting collection {self.collection_name}: {str(e)}")

        # Recreate the collection
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )
        print(f"Collection {self.collection_name} has been recreated.")

    def ingest_vectors(self, vectors, payloads):
        # Clear the collection before inserting new data
        self.clear_collection()

        # Convert vectors to list for Qdrant and generate unique IDs
        vectors = np.array(vectors).tolist()  # Convert vectors to list for Qdrant
        ids = list(range(1, len(vectors) + 1))  # Generate unique IDs for each point

        points = [
            PointStruct(id=idx, vector=vector, payload={"text": payload})
            for idx, vector, payload in zip(ids, vectors, payloads)
        ]

        # Upsert the points into the collection
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def query(self, query_vector, top_k=3):
        # Perform similarity search in Qdrant
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector.tolist(),
            limit=top_k
        )

        # Return the matching texts with distances
        results = [{"text": result.payload["text"], "score": result.score} for result in search_result]
        return results

    def generate_answer(self, query_vector, user_request, top_k=3):
        # Step 1: Query Qdrant for relevant context
        context = self.query(query_vector, top_k=top_k)
        context_texts = " ".join([c["text"] for c in context])

        # Step 2: Combine the user's request and retrieved context into a prompt
        prompt = f"Answer the following question based on the context below.\n\nContext: {context_texts}\n\nQuestion: {user_request}\nAnswer:"

        # Step 3: Use Hugging Face Transformers to generate the answer
        # Load a pipeline for text generation
        generator = pipeline('text-generation', model='gpt2')  # device=-1 ensures it runs on CPU
        response = generator(prompt, max_new_tokens=50, num_return_sequences=1)

        # Step 4: Return the generated answer
        #return response[0]['generated_text']
        generated_answer = response[0]['generated_text'].replace(prompt, "").strip()

        # Step 5: Return a JSON object containing the prompt and the result
        return {
            "prompt": prompt,
            "result": generated_answer
        }
