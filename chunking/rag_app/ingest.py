# rag_app/ingest.py
import uuid
from dotenv import load_dotenv
import os

from vector_store_pinecone import init_pinecone, upsert_to_pinecone
from utils import read_file, chunk_text, load_embed_model

load_dotenv()  # Load env vars from .env

def ingest_file(file_path):
    text = read_file(file_path)
    chunks = chunk_text(text)
    embed_model = load_embed_model()
    index = init_pinecone()

    vectors = []
    for chunk in chunks:
        emb = embed_model.encode(chunk).tolist()
        id = str(uuid.uuid4())
        metadata = {"text": chunk}
        vectors.append((id, emb, metadata))

    upsert_to_pinecone(index, vectors)
    print(f"Upserted {len(vectors)} chunks into Pinecone.")

if __name__ == "__main__":
    file_path = os.path.join("data", "scraped_data.txt")
    ingest_file(file_path)
