import os
from pinecone import Pinecone, ServerlessSpec

API_KEY = os.getenv("PINECONE_API_KEY")
ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp")  # or your region
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "my-index")  # set your index name

def init_pinecone():
    # Create Pinecone client instance
    pc = Pinecone(api_key=API_KEY)

    # Check if index exists
    existing_indexes = pc.list_indexes().names()
    if INDEX_NAME not in existing_indexes:
        pc.create_index(
            name=INDEX_NAME,
            dimension=1024,  # Change this to your vector dimension
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",       # or 'gcp' based on your env
                region=ENVIRONMENT # match your Pinecone env
            )
        )
        print(f"Created index {INDEX_NAME}")

    index = pc.Index(INDEX_NAME)
    return index

def upsert_to_pinecone(index, vectors):
    # vectors should be list of tuples (id, vector, metadata)
    index.upsert(vectors=vectors)
